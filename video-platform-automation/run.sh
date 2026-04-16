#!/bin/bash
#
# video-platform-automation
# Single command entry point for the video pipeline
#
# Usage:
#   ./run.sh [OPTIONS]
#
# Options:
#   --niche <music|storytime|podcast>    Pipeline to run (default: music)
#   --prompt <string>                    Input prompt for the pipeline
#   --channel-id <id>                    Channel identifier (default: default)
#   --build                              Build image before running
#   --rebuild                            Force rebuild image
#   --existing                           Use existing container
#   --stop                               Stop running container
#   --logs                               Show container logs
#   --shell                              Open shell in container
#   --gpu                                Use GPU (default on NVIDIA systems)
#   --cpu                                Use CPU only (no GPU)
#   --help                               Show this help
#

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Default values
NICHE="music"
PROMPT=""
CHANNEL_ID="default"
BUILD=false
REBUILD=false
EXISTING=false
STOP=false
LOGS=false
SHELL=false
GPU=true

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --niche)
            NICHE="$2"
            shift 2
            ;;
        --prompt)
            PROMPT="$2"
            shift 2
            ;;
        --channel-id)
            CHANNEL_ID="$2"
            shift 2
            ;;
        --build)
            BUILD=true
            shift
            ;;
        --rebuild)
            REBUILD=true
            shift
            ;;
        --existing)
            EXISTING=true
            shift
            ;;
        --stop)
            STOP=true
            shift
            ;;
        --logs)
            LOGS=true
            shift
            ;;
        --shell)
            SHELL=true
            shift
            ;;
        --gpu)
            GPU=true
            shift
            ;;
        --cpu)
            GPU=false
            shift
            ;;
        --help)
            echo "Usage: $0 [OPTIONS]"
            echo ""
            echo "Options:"
            echo "  --niche <music|storytime|podcast>    Pipeline to run (default: music)"
            echo "  --prompt <string>                    Input prompt for the pipeline"
            echo "  --channel-id <id>                    Channel identifier (default: default)"
            echo "  --build                              Build image before running"
            echo "  --rebuild                            Force rebuild image"
            echo "  --existing                           Use existing container"
            echo "  --stop                               Stop running container"
            echo "  --logs                               Show container logs"
            echo "  --shell                              Open shell in container"
            echo "  --gpu                                Use GPU (default on NVIDIA systems)"
            echo "  --cpu                                Use CPU only (no GPU)"
            echo "  --help                               Show this help"
            exit 0
            ;;
        *)
            echo -e "${RED}Unknown option: $1${NC}"
            exit 1
            ;;
    esac
done

# Validate niche
if [[ ! "$NICHE" =~ ^(music|storytime|podcast)$ ]]; then
    echo -e "${RED}Invalid niche: $NICHE. Must be music, storytime, or podcast${NC}"
    exit 1
fi

# Check if Docker is running
if ! docker info &> /dev/null; then
    echo -e "${RED}Docker is not running. Please start Docker and try again.${NC}"
    exit 1
fi

# Build command based on GPU support
if $GPU; then
    # Check for NVIDIA runtime
    if ! docker info 2>&1 | grep -q "nvidia"; then
        echo -e "${YELLOW}NVIDIA runtime not detected, using CPU mode${NC}"
        GPU=false
    fi
fi

echo -e "${BLUE}=================================================${NC}"
echo -e "${BLUE}  Video Platform Automation Pipeline${NC}"
echo -e "${BLUE}=================================================${NC}"
echo ""
echo -e "Niche:     ${GREEN}$NICHE${NC}"
echo -e "Channel:   ${GREEN}$CHANNEL_ID${NC}"
if [[ -n "$PROMPT" ]]; then
    echo -e "Prompt:    ${GREEN}$PROMPT${NC}"
else
    echo -e "${YELLOW}Warning: No prompt provided, using default${NC}"
fi
echo ""

# Stop existing container if running
if $STOP; then
    echo -e "${BLUE}Stopping existing container...${NC}"
    docker compose -f docker-compose.yml stop video-pipeline-${CHANNEL_ID} 2>/dev/null || true
    docker compose -f docker-compose.yml rm -f video-pipeline-${CHANNEL_ID} 2>/dev/null || true
    echo -e "${GREEN}Done${NC}"
    exit 0
fi

# Rebuild or build if requested
if $REBUILD || $BUILD; then
    echo -e "${BLUE}Building Docker image...${NC}"
    if $REBUILD; then
        docker compose -f docker-compose.yml build --no-cache
    else
        docker compose -f docker-compose.yml build
    fi
    echo -e "${GREEN}Build complete${NC}"
    echo ""
fi

# Check if running in existing mode
if $EXISTING; then
    echo -e "${BLUE}Using existing container...${NC}"
    if $LOGS; then
        docker compose -f docker-compose.yml logs -f --tail=100 video-pipeline-${CHANNEL_ID}
    elif $SHELL; then
        docker compose -f docker-compose.yml exec video-pipeline-${CHANNEL_ID} /bin/bash
    else
        echo -e "${GREEN}Container running: video-pipeline-${CHANNEL_ID}${NC}"
        echo -e "${YELLOW}Use --logs or --shell for more options${NC}"
    fi
    exit 0
fi

# Show logs if requested
if $LOGS; then
    echo -e "${BLUE}Showing logs...${NC}"
    docker compose -f docker-compose.yml logs -f --tail=100 video-pipeline-${CHANNEL_ID}
    exit 0
fi

# Open shell if requested
if $SHELL; then
    echo -e "${BLUE}Opening shell...${NC}"
    docker compose -f docker-compose.yml exec video-pipeline-${CHANNEL_ID} /bin/bash
    exit 0
fi

# Create config directory and prompt file if not exists
mkdir -p config/${CHANNEL_ID} output/${CHANNEL_ID} logs/${CHANNEL_ID}

# Write prompt to config file
if [[ -n "$PROMPT" ]]; then
    echo "$PROMPT" > config/${CHANNEL_ID}/prompt.txt
fi

# Write niche config
cat > config/${CHANNEL_ID}/config.yaml << EOF
niche: $NICHE
channel_id: $CHANNEL_ID
prompt_file: config/${CHANNEL_ID}/prompt.txt
output_dir: output/${CHANNEL_ID}
EOF

# Run the pipeline
if ! $EXISTING; then
    echo -e "${BLUE}Starting pipeline...${NC}"
    if $GPU; then
        docker compose -f docker-compose.yml up -d video-pipeline-${CHANNEL_ID}
        echo -e "${GREEN}Container started: video-pipeline-${CHANNEL_ID}${NC}"
        echo -e "${YELLOW}Monitor logs with: ./run.sh --channel-id $CHANNEL_ID --logs${NC}"
    else
        # CPU mode - need to override environment variable
        GPU=false docker compose -f docker-compose.yml up video-pipeline-${CHANNEL_ID}
        echo -e "${GREEN}Pipeline completed (CPU mode)${NC}"
    fi
fi

# Show container status
echo ""
echo -e "${BLUE}Container Status:${NC}"
docker compose -f docker-compose.yml ps video-pipeline-${CHANNEL_ID}

echo ""
echo -e "${GREEN}Done!${NC}"
echo -e "Output will be in: output/${CHANNEL_ID}/"
