import os
import argparse
import sys
from datetime import datetime
import matplotlib.pyplot as plt
import libs.stats as stats
from heatmap_chart import generate_heatmap

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

RUN_MODES = ['local', 'github_action']
parser = argparse.ArgumentParser(description='Dev Chart Fetcher')
parser.add_argument('--run_mode', action="store", dest='run_mode', default='github_action')
parser.add_argument('--username_github', action="store", dest='username_github', default=None)
parser.add_argument('--username_leetcode', action="store", dest='username_leetcode', default=None)

args = parser.parse_args()
if args.run_mode not in RUN_MODES:
    raise ValueError('Invalid run_mode, accepted: local, github_action')

if args.run_mode == 'github_action':
    GITHUB_USERNAME = os.environ.get("username_github")
    if GITHUB_USERNAME:
        print(f'username_github: {GITHUB_USERNAME}')
    else:
        print('WARNING: username_github not provided')

    LEETCODE_USERNAME = os.environ.get("username_leetcode")
    if LEETCODE_USERNAME:
        print(f'username_leetcode: {LEETCODE_USERNAME}')
    else:
        print('WARNING: username_leetcode not provided')

elif args.run_mode == 'local':
    GITHUB_USERNAME = args.username_github
    LEETCODE_USERNAME = args.username_leetcode

print(f"::set-output name=run_at::{datetime.now().isoformat()}Z")

STYLES = ['dark_background', 'default']
THEME_MODES = ['dark', 'light']
ASSETS_DIR = 'assets'

if not os.path.exists(ASSETS_DIR):
    os.makedirs(ASSETS_DIR)

def fetch_github():
    """
    Fetch GitHub contribution data and generate heatmap SVGs.
    """
    if not GITHUB_USERNAME:
        return

    print(f'GITHUB_USERNAME: {GITHUB_USERNAME}')

    github_data = stats.get_github_contribution(GITHUB_USERNAME)

    for i in range(len(STYLES)):
        plt.style.use(STYLES[i])
        generate_heatmap(GITHUB_USERNAME, github_data)
        plt.savefig(f'{ASSETS_DIR}/github_{THEME_MODES[i]}.svg', format='svg', bbox_inches='tight', transparent=True)

def fetch_leetcode():
    """
    Fetch LeetCode submission data and generate heatmap SVGs.
    """
    if not LEETCODE_USERNAME:
        return

    print(f'LEETCODE_USERNAME: {LEETCODE_USERNAME}')

    leetcode_data = stats.get_leetcode_submission(LEETCODE_USERNAME)

    for i in range(len(STYLES)):
        plt.style.use(STYLES[i])
        generate_heatmap(LEETCODE_USERNAME, leetcode_data)
        plt.savefig(f'{ASSETS_DIR}/leetcode_{THEME_MODES[i]}.svg', format='svg', bbox_inches='tight', transparent=True)

def main():
    """
    Main function to fetch GitHub and LeetCode data.
    """
    print('Fetching GitHub and LeetCode data...')
    fetch_github()
    fetch_leetcode()

if __name__ == "__main__":
    main()
