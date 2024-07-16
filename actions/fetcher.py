import os
import argparse
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

RUN_MODE = ['local', 'github_action']
parser = argparse.ArgumentParser(description='Dev Chart Fetcher')
parser.add_argument('--run_mode', action="store", dest='run_mode', default='github_action')
parser.add_argument('--username_github', action="store", dest='username_github', default=None)
parser.add_argument('--username_leetcode', action="store", dest='username_leetcode', default=None)

args = parser.parse_args()
if args.run_mode not in RUN_MODE:
    raise ValueError('Invalid run_mode, accepted: local, github_action')

if args.run_mode == 'github_action':
    USERNAME_GITHUB = os.environ.get("username_github")
    if USERNAME_GITHUB:
        print(f'username_github: {USERNAME_GITHUB}')
    else:
        print('WARNING: username_github not provided')

    USERNAME_LEETCODE = os.environ.get("username_leetcode")
    if USERNAME_LEETCODE:
        print(f'username_leetcode: {USERNAME_LEETCODE}')
    else:
        print('WARNING: username_leetcode not provided')
        
elif args.run_mode == 'local':
    USERNAME_GITHUB = args.username_github
    USERNAME_LEETCODE = args.username_leetcode
    
from datetime import datetime
print(f"::set-output name=run_at::{datetime.now().isoformat()}Z")

import libs.stats as stats
from heatmap_chart import generate_heatmap

import matplotlib.pyplot as plt

STYLES = ['dark_background', 'default']
THEME_MODES = ['dark', 'light']
ASSETS_DIR = 'assets'

if not os.path.exists(ASSETS_DIR):
    os.makedirs(ASSETS_DIR)

def fetch_github():
    if not USERNAME_GITHUB:
        return

    print(f'USERNAME_GITHUB: {USERNAME_GITHUB}')

    json = stats.get_github_contribution(USERNAME_GITHUB)
    
    for i in range(len(STYLES)):
        plt.style.use(STYLES[i])
        generate_heatmap(USERNAME_GITHUB, json)
        plt.savefig(f'{ASSETS_DIR}/github_{THEME_MODES[i]}.svg', format='svg', bbox_inches='tight', transparent=True)
            
    return

def fetch_leetcode():
    if not USERNAME_LEETCODE:
        return

    print(f'USERNAME_LEETCODE: {USERNAME_LEETCODE}')

    json = stats.get_leetcode_submission(USERNAME_LEETCODE)
    
    for i in range(len(STYLES)):
        plt.style.use(STYLES[i])
        generate_heatmap(USERNAME_LEETCODE, json)
        plt.savefig(f'{ASSETS_DIR}/leetcode_{THEME_MODES[i]}.svg', format='svg', bbox_inches='tight', transparent=True)
            
    return


def __main__():
    print('Fetching Github and Leetcode data...')
    fetch_github()
    fetch_leetcode()
    
__main__()

