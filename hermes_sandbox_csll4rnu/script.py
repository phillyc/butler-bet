from hermes_tools import terminal

# Commit and push the changes
repo = "/tmp/butler-bet"

# Stage changes
stage = terminal(f"cd {repo} && git add -A")
print("Stage output:", stage['output'])

# Commit
commit = terminal(f"cd {repo} && git commit -m 'Butler Bet update: May 14, 2026 - Figure 03 8-hour autonomous demo'")
print("Commit output:", commit['output'])

# Push
push = terminal(f"cd {repo} && git push")
print("Push output:", push['output'])