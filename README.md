# DevChart

DevChart is a Flask-based web application designed to visualize coding activity from platforms like GitHub and LeetCode. It generates statistical charts that represent a user's coding contributions over time, offering both JSON data and SVG visuals. You can use these charts to showcase your coding progress, share your achievements, or analyze your coding habits on your own blog or website.

Inpired by [githubchart-api](https://github.com/2016rshah/githubchart-api) from Ruby, I ported it to Python Flask to support more features and platforms. E.g dark and light mode depending on user preference, and more platforms...

## Snapshot
### Dark mode:
![Dark mode](examples/dark.png)
### Light mode:
![Light mode](examples/light.png)

## Features

- **GitHub Contribution Chart**: Visualize your GitHub contributions in a calendar heatmap.
- **LeetCode Submission Stats**: Get insights into your LeetCode submission statistics.
- Supports output in both JSON and SVG formats for easy integration and sharing.

## Roadmap
- Deploy to user own GitHub Actions for automatic updates. Then you can use the generated SVG link directly.
- Support more platforms like Codeforces, AtCoder, etc.
- Customizable chart styles and colors.

## Getting Started

### Prerequisites

- Developed in Python 3.11.9. For lower please help check compatibility. 
- pip (Python package installer)

### Installation

1. Clone the repository to your local machine:

```
git clone https://github.com/zhenyuan0502/DevChart.git
```

2. Run `init.ps1` to install the required Python packages as well as .env
3. Run `run.ps1` or `F5` to start the local Flask server on `http://localhost:5000`
4. Access:
- `http://localhost:5000/api/github/<username>/svg` to get GitHub contribution chart data in light mode
- `http://localhost:5000/api/github/<username>/svg?theme_mode=dark` to get GitHub contribution chart data with dark theme
- `http://localhost:5000/api/github/<username>/svg?mode=test&theme_mode=dark` to simulate GitHub contribution chart data with dark theme
- `http://localhost:5000/api/github/<username>/json` to get GitHub contribution chart data in JSON format

The same with LeetCode:
- `http://localhost:5000/api/leetcode/<username>/svg` to get LeetCode submission chart data
- `http://localhost:5000/api/leetcode/<username>/json` to get LeetCode submission chart data in JSON format

1. Deploy to your own server or cloud service to share your coding activity with others!

### Used libraries:
- Flask
- July (customized) https://github.com/e-hulten/july
- Calmap https://github.com/MarvinT/calmap/


For you information, this README is mostly written by GitHub Copilot, as well as coding part :)