import july

def generate_heatmap(username, json):
    return july.heatmap(json['data'].keys(), json['data'].values(),
                 title=f"{username}'s with {json['summary']}", cmap="github_transparent",
                 colorbar=True,
                 weekday_width=3,
                 fontfamily="monospace",
                 fontsize=12,
                 facecolor='None')