import matplotlib
matplotlib.use('Agg')

from flask import Flask, jsonify, Response, send_file
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
    # https://pythonhosted.org/calmap/
    # https://github.com/e-hulten/july
    json = stats.get_contribution(username)
    
    # Create a buffer to save the plot
    buffer = io.BytesIO()

    # Plot the calmap and save it to the buffer
    july.heatmap(json['data'].keys(), json['data'].values(),
                 title=f"{username}'s Github Activity", cmap="github",
                 colorbar=True,
                 fontfamily="monospace",
                 fontsize=12)
    
    plt.savefig(buffer, format='svg')
    plt.close()

    # Convert the buffer to base64 encoded string
    buffer.seek(0)
    base64.b64encode(buffer.getvalue()).decode()

    # Return the SVG response
    return send_file(buffer, mimetype='image/svg+xml')

if __name__ == '__main__':
    app.run(debug=True)