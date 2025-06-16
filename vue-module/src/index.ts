import { App } from 'vue';
import DevChart from './components/DevChart.vue';

// Export components
export { default as DevChart } from './components/DevChart.vue';

// Export types
export type {
  ChartData,
  StatsResponse,
  ChartOptions,
  ChartOutput,
  Platform,
  GitHubContribution,
  LeetCodeSubmission
} from './types';

// Export services
export { getGitHubContribution } from './services/githubService';
export { getLeetCodeSubmission } from './services/leetcodeService';

// Export utilities
export { generateHeatmap } from './utils/chartGenerator';
export * from './utils/textUtils';

// Vue plugin install function
export function install(app: App) {
  app.component('DevChart', DevChart);
}

// Default export for plugin usage
export default {
  install
};