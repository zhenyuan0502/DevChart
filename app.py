import matplotlib
matplotlib.use('Agg')

from flask import Flask, jsonify, Response, send_file
import libs.stats as stats

import numpy as np; np.random.seed(sum(map(ord, 'calmap')))

import matplotlib.pyplot as plt
import pandas as pd
import calmap
import io
import base64

app = Flask(__name__)
app.json.sort_keys = False

@app.route('/api/<username>/json')
def get_github_stats_json(username):
    json = stats.get_contribution(username)
    return jsonify(json), 200, {'Content-Type': 'application/json'}


from mpl_toolkits.axes_grid1 import make_axes_locatable

@app.route('/api/<username>/svg')
def get_github_stats_svg(username):
    # https://pythonhosted.org/calmap/
    # https://github.com/e-hulten/july
    json = stats.get_contribution(username)
    
    events = pd.Series(json['data'])
    events.index = pd.to_datetime(events.index)
    
    # Create a buffer to save the plot
    buffer = io.BytesIO()

    # Plot the calmap and save it to the buffer
    fig = plt.figure(figsize=(10,4))
    ax = fig.add_subplot(111)
    cax = calmap.yearplot(events, 
                    dayticks=[0, 2, 4, 6], 
                    cmap=u'Greens')
    
    divider = make_axes_locatable(cax)
    lcax = divider.append_axes("right", size="2%", pad=0.5)
    fig.colorbar(cax.get_children()[1], cax=lcax)

    plt.savefig(buffer, format='svg')
    plt.close()

    # Convert the buffer to base64 encoded string
    buffer.seek(0)
    base64.b64encode(buffer.getvalue()).decode()

    # Return the SVG response
    return send_file(buffer, mimetype='image/svg+xml')
  
@app.route('/')
def index():
    return 'Hello, World!'

if __name__ == '__main__':
    app.run(debug=True)