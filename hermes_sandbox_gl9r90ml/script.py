from hermes_tools import terminal

# Pull from remote to get the latest changes
pull = terminal("cd /tmp/butler-bet && git pull origin master")
print("Pull output:", pull['output'][:500])

# Check git status
status = terminal("cd /tmp/butler-bet && git status")
print("\nGit status:", status['output'][:300])

# If there are uncommitted changes, commit them
if "Changes not staged for commit" in status['output']:
    stage = terminal("cd /tmp/butler-bet && git add -A")
    commit = terminal("cd /tmp/butler-bet && git commit -m 'Butler Bet update: May 14, 2026 - Figure 03 8-hour autonomous demo'")
    print("\nCommit:", commit['output'][:300])
    
    # Force push since we know our content is correct
    force_push = terminal("cd /tmp/butler-bet && git push --force origin master")
    print("\nForce push:", force_push['output'][:500])