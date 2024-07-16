import os

# get the input and convert it to int
github_token = os.environ.get("github_token_for_push")
if github_token:
    print(f'github_token_for_push: {github_token}')
else:
    raise ValueError('ERROR: github_token_for_push not provided')

github_username = os.environ.get("github_username")
if github_username:
    print(f'github_username: {github_username}')
else:
    print('WARNING: github_username not provided')

leetcode_username = os.environ.get("leetcode_username")
if leetcode_username:
    print(f'leetcode_username: {leetcode_username}')
else:
    print('WARNING: leetcode_username not provided')
    
from datetime import datetime
print(f"::set-output name=run_at::{datetime.now().isoformat()}Z")