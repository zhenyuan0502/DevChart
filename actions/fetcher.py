import os

# get the input and convert it to int
REPOSITORY_TOKEN = os.environ.get("REPOSITORY_TOKEN")
if REPOSITORY_TOKEN:
    print(f'REPOSITORY_TOKEN: {REPOSITORY_TOKEN}')
else:
    raise ValueError('ERROR: REPOSITORY_TOKEN not provided')

username_github = os.environ.get("username_github")
if username_github:
    print(f'username_github: {username_github}')
else:
    print('WARNING: username_github not provided')

username_leetcode = os.environ.get("username_leetcode")
if username_leetcode:
    print(f'username_leetcode: {username_leetcode}')
else:
    print('WARNING: username_leetcode not provided')
    
from datetime import datetime
print(f"::set-output name=run_at::{datetime.now().isoformat()}Z")


