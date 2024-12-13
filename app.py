import matplotlib
# matplotlib.use('Agg')

from flask import Flask, jsonify, Response, send_file, render_template, url_for, request
import libs.stats as stats

import numpy as np; np.random.seed(sum(map(ord, 'calmap')))

import matplotlib.pyplot as plt
import pandas as pd
import io
import july 
from heatmap_chart import generate_heatmap
app = Flask(__name__)
app.json.sort_keys = False

@app.route('/api/github/<username>/json')
def get_github_stats_json(username):
    """
    Get GitHub contribution stats in JSON format.

    Args:
        username (str): GitHub username.

    Returns:
        Response: JSON response containing GitHub contribution stats.
    """
    json_data = stats.get_github_contribution(username)
    return jsonify(json_data), 200, {'Content-Type': 'application/json'}

def generate_calendar_chart(username, stats_function):
    """
    Generate a calendar chart for the given username using the specified stats function.

    Args:
        username (str): Username for which to generate the chart.
        stats_function (function): Function to fetch stats for the given username.

    Returns:
        Response: SVG response containing the generated calendar chart.
    """
    mode = request.args.get('mode', default='prod')
    theme_mode = request.args.get('theme_mode', default='light')
    
    if mode not in ['prod', 'test']:
        return jsonify({'error': 'Invalid mode, accepted: prod, test'}), 400, {'Content-Type': 'application/json'}
    
    if theme_mode not in ['dark', 'light']:
        return jsonify({'error': 'Invalid theme_mode, accepted: dark, light'}), 400, {'Content-Type': 'application/json'}
    
    json_data = stats_function(username)
    
    background_color = ''
    if theme_mode == 'dark':
        plt.style.use('dark_background')
        background_color = '#1a1a1a'
    elif theme_mode == 'light':
        plt.style.use('default')
        background_color = '#f0f0f0'
        
    # Create a buffer to save the plot
    buffer = io.BytesIO()
        
    generate_heatmap(username, json_data)
  
    plt.savefig(buffer, backend='svg', format='svg', bbox_inches='tight', transparent=True)
    plt.close()
    buffer.seek(0)
    
    if mode == 'test':
        return render_template('index.html', 
                               css_content='body {background-color: '+ background_color + ';}',
                               svg_content=buffer.getvalue().decode('utf-8'))
    
    if mode == 'prod':
        return send_file(buffer, mimetype='image/svg+xml')
    
    return jsonify({'error': 'Invalid'}), 400, {'Content-Type': 'application/json'}


@app.route('/api/github/<username>/svg')
def get_github_stats_svg(username):
    """
    Get GitHub contribution stats in SVG format.

    Args:
        username (str): GitHub username.

    Returns:
        Response: SVG response containing GitHub contribution stats.
    """
    return generate_calendar_chart(username, stats.get_github_contribution)


@app.route('/api/leetcode/<username>/json')
def get_leetcode_stats_json(username):
    """
    Get LeetCode submission stats in JSON format.

    Args:
        username (str): LeetCode username.

    Returns:
        Response: JSON response containing LeetCode submission stats.
    """
    json_data = stats.get_leetcode_submission(username)
    return jsonify(json_data), 200, {'Content-Type': 'application/json'}


@app.route('/api/leetcode/<username>/svg')
def get_leetcode_stats_svg(username):
    """
    Get LeetCode submission stats in SVG format.

    Args:
        username (str): LeetCode username.

    Returns:
        Response: SVG response containing LeetCode submission stats.
    """
    return generate_calendar_chart(username, stats.get_leetcode_submission)

# Load Browser Favorite Icon
@app.route('/favicon.ico')
def favicon():
    """
    Serve the favicon.

    Returns:
        Response: Favicon image.
    """
    return url_for('static', filename='image/favicon.png')

if __name__ == '__main__':
    app.run(debug=True)