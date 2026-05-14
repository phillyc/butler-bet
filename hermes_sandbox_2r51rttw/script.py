from hermes_tools import terminal, read_file
from pathlib import Path
import os

repo = Path("/tmp/butler-bet")

# Add all current files (without the submodule)
add_all = terminal("cd /tmp/butler-bet && git add -A && git status --short")
print("Files to be committed:")
print(add_all['output'][:1000])

# Remove the submodule reference completely
rm_submodule = terminal("cd /tmp/butler-bet && git rm -rf --cached andrej-karpathy-skills 2>&1")
print(f"\nRemove submodule: {rm_submodule['output']}")

# Check for other unwanted files
unwanted_files = ['master_index.html.tmp', 'master_last-check.txt.tmp', 'HEAD_index.html', 'actual.html', 'staged.html']
for f in unwanted_files:
    file_path = repo / f
    if file_path.exists():
        os.remove(file_path)
        print(f"Removed {f}")

# Stage the changes
stage_changes = terminal("cd /tmp/butler-bet && git add -A && git status --short")
print(f"\nCurrent status:\n{stage_changes['output'][:500]}")

# Commit
commit_result = terminal("cd /tmp/butler-bet && git commit -m 'Clean up: remove broken submodule and temp files'")
print(f"\nCommit: {commit_result['output'][:500]}")

# Push
push_result = terminal("cd /tmp/butler-bet && git push origin master --force")
print(f"\nPush: {push_result['output'][:300]}")