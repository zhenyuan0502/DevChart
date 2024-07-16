import matplotlib
matplotlib.use('Agg')

from flask import Flask, jsonify, Response, send_file, render_template, url_for, request
import libs.stats as stats

import numpy as np; np.random.seed(sum(map(ord, 'calmap')))

import matplotlib.pyplot as plt
import pandas as pd
import io
import base64
import july 

app = Flask(__name__)
app.json.sort_keys = False

@app.route('/api/<username>/json')
def get_github_stats_json(username):
    json = stats.get_contribution(username)
    return jsonify(json), 200, {'Content-Type': 'application/json'}

@app.route('/api/<username>/svg')
def get_github_stats_svg(username):
    mode = request.args.get('mode', default='prod')
    theme_mode = request.args.get('theme_mode', default='light')
    
    if mode not in ['prod', 'test']:
        return jsonify({'error': 'Invalid mode, accepted: prod, test'}), 400, {'Content-Type': 'application/json'}
    
    if theme_mode not in ['dark', 'light']:
        return jsonify({'error': 'Invalid theme_mode, accepted: dark, light'}), 400, {'Content-Type': 'application/json'}
    
    json = stats.get_contribution(username)
    
    # Create a buffer to save the plot
    buffer = io.BytesIO()
    background_color = ''
    if theme_mode == 'dark':
        plt.style.use('dark_background')
        background_color = '#1a1a1a'
    elif theme_mode == 'light':
        plt.style.use('default')
        background_color = '#f0f0f0'
        
    july.heatmap(json['data'].keys(), json['data'].values(),
                 title=f"{username}'s Github Activity", cmap="github_transparent",
                 colorbar=True,
                 fontfamily="monospace",
                 fontsize=12,
                 facecolor='None')
    
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


# Load Browser Favorite Icon
@app.route('/favicon.ico')
def favicon():
    return url_for('static', filename='image/favicon.png')

if __name__ == '__main__':
    app.run(debug=True)