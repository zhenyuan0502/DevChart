# DevChart Vue Module

A Vue 3 + Vite module for generating developer activity charts from GitHub and LeetCode data. This module provides a standalone implementation of the DevChart functionality as a reusable Vue component.

## Features

- 📊 **GitHub Contribution Charts**: Visualize GitHub contributions in a calendar heatmap
- 🧩 **LeetCode Submission Charts**: Display LeetCode submissions over time  
- 🎨 **Theme Support**: Light and dark themes
- 📱 **Responsive Design**: Charts adapt to different screen sizes
- 🎯 **Multiple Output Formats**: SVG charts and JSON data
- 📦 **Standalone Module**: Can be used as an npm package
- 🔧 **TypeScript Support**: Full TypeScript definitions included
- ⚡ **Vue 3 + Vite**: Modern development stack

## Installation

```bash
npm install devchart-vue
```

## Usage

### Basic Vue Component Usage

```vue
<template>
  <div>
    <!-- GitHub contribution chart -->
    <DevChart 
      username="your-username"
      platform="github"
      theme="light"
      output-format="svg"
    />
    
    <!-- LeetCode submission chart -->
    <DevChart 
      username="your-username"
      platform="leetcode"
      theme="dark"
      output-format="both"
    />
  </div>
</template>

<script setup>
import { DevChart } from 'devchart-vue'
</script>
```

### Vue Plugin Usage

```js
// main.js
import { createApp } from 'vue'
import DevChart from 'devchart-vue'
import App from './App.vue'

const app = createApp(App)
app.use(DevChart)
app.mount('#app')
```

```vue
<!-- Now you can use the component globally -->
<template>
  <dev-chart username="your-username" platform="github" />
</template>
```

### Direct API Usage

```js
import { getGitHubContribution, getLeetCodeSubmission, generateHeatmap } from 'devchart-vue'

// Fetch GitHub data
const githubData = await getGitHubContribution('username')
console.log(githubData.data) // Chart data
console.log(githubData.summary) // Summary text

// Fetch LeetCode data  
const leetcodeData = await getLeetCodeSubmission('username')

// Generate SVG heatmap
const svgChart = generateHeatmap(
  githubData.data,
  'username', 
  githubData.summary,
  { theme: 'dark', width: 900, height: 200 }
)
```

## Component Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `username` | `string` | **required** | GitHub or LeetCode username |
| `platform` | `'github' \| 'leetcode'` | **required** | Data source platform |
| `theme` | `'light' \| 'dark'` | `'light'` | Chart color theme |
| `outputFormat` | `'svg' \| 'json' \| 'both'` | `'svg'` | Output format to display |
| `width` | `number` | `800` | Chart width in pixels |
| `height` | `number` | `200` | Chart height in pixels |
| `colorScheme` | `string` | `'github'` | Color scheme for the heatmap |
| `showColorbar` | `boolean` | `true` | Show/hide the color legend |
| `showTitle` | `boolean` | `true` | Show/hide the chart title |
| `showWeekdays` | `boolean` | `true` | Show/hide weekday labels |
| `showMonths` | `boolean` | `true` | Show/hide month labels |

## API Functions

### `getGitHubContribution(username: string)`

Fetches GitHub contribution data for the specified user.

**Returns:** `Promise<StatsResponse>`

```js
{
  username: "octocat",
  title: "Github Contribution", 
  summary: "GitHub with 1,234 contributions in the last year",
  data: {
    "2023-01-01": 3,
    "2023-01-02": 0,
    // ... more dates
  }
}
```

**Note:** GitHub scraping may be blocked by CORS in browser environments. Consider using a proxy server or implementing server-side data fetching.

### `getLeetCodeSubmission(username: string)`

Fetches LeetCode submission data using the LeetCode GraphQL API.

**Returns:** `Promise<StatsResponse>`

```js
{
  username: "coder123",
  title: "LeetCode Submission",
  summary: "LeetCode with 456 submissions in past one year", 
  data: {
    "2023-01-01": 2,
    "2023-01-02": 1,
    // ... more dates
  }
}
```

### `generateHeatmap(data, username, summary, options)`

Generates an SVG heatmap chart from the provided data.

**Parameters:**
- `data: ChartData` - Date-keyed contribution counts
- `username: string` - Username for the chart title
- `summary: string` - Summary text for the chart title  
- `options: HeatmapOptions` - Chart configuration options

**Returns:** `string` - SVG markup

## Development Setup

1. Clone the repository
2. Install dependencies:
   ```bash
   npm install
   ```

3. Start development server:
   ```bash
   npm run dev
   ```

4. Build the library:
   ```bash
   npm run build-lib
   ```

## CORS Considerations

When using GitHub data fetching in browser environments, you may encounter CORS restrictions. The GitHub contributions page doesn't allow cross-origin requests from browsers.

**Solutions:**
1. **Server-side proxy**: Implement the data fetching on your backend
2. **CORS proxy service**: Use a service like `cors-anywhere` (not recommended for production)
3. **GitHub API**: Use the official GitHub GraphQL API (requires authentication)

LeetCode data fetching should work directly from browsers as their GraphQL API supports CORS.

## Comparison with Python Version

This Vue module provides equivalent functionality to the Python Flask version:

| Feature | Python Version | Vue Module |
|---------|----------------|------------|
| GitHub Data | ✅ Web scraping | ✅ Web scraping (CORS limited) |
| LeetCode Data | ✅ GraphQL API | ✅ GraphQL API |
| Chart Generation | ✅ Matplotlib + July | ✅ D3.js SVG |
| Themes | ✅ Light/Dark | ✅ Light/Dark |
| Output Formats | ✅ SVG/JSON | ✅ SVG/JSON |
| Deployment | ✅ Flask server | ✅ Client-side component |

## License

MIT License - see LICENSE file for details.

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue.

## Related Projects

- [Original Python DevChart](../README.md) - Flask-based server implementation
- [July](https://github.com/e-hulten/july) - Python calendar heatmap library (inspiration)
- [D3.js](https://d3js.org/) - JavaScript data visualization library (used for charts)