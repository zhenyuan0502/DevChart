<template>
  <div class="dev-chart" :class="themeClass">
    <div v-if="loading" class="loading">
      Loading {{ platform }} data for {{ username }}...
    </div>
    
    <div v-else-if="error" class="error">
      {{ error }}
    </div>
    
    <div v-else class="chart-container">
      <div v-if="outputFormat === 'svg' || outputFormat === 'both'" 
           class="svg-container" 
           v-html="svgContent">
      </div>
      
      <pre v-if="outputFormat === 'json' || outputFormat === 'both'" 
           class="json-output">{{ JSON.stringify(jsonData, null, 2) }}</pre>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, watch } from 'vue';
import type { Platform, StatsResponse } from '../types';
import { getGitHubContribution } from '../services/githubService';
import { getLeetCodeSubmission } from '../services/leetcodeService';
import { generateHeatmap } from '../utils/chartGenerator';

interface Props {
  username: string;
  platform: Platform;
  theme?: 'light' | 'dark';
  outputFormat?: 'svg' | 'json' | 'both';
  width?: number;
  height?: number;
  colorScheme?: string;
  showColorbar?: boolean;
  showTitle?: boolean;
  showWeekdays?: boolean;
  showMonths?: boolean;
}

const props = withDefaults(defineProps<Props>(), {
  theme: 'light',
  outputFormat: 'svg',
  width: 800,
  height: 200,
  colorScheme: 'github',
  showColorbar: true,
  showTitle: true,
  showWeekdays: true,
  showMonths: true
});

const loading = ref(false);
const error = ref<string | null>(null);
const jsonData = ref<StatsResponse | null>(null);
const svgContent = ref<string>('');

const themeClass = computed(() => `dev-chart--${props.theme}`);

const chartOptions = computed(() => ({
  width: props.width,
  height: props.height,
  colorScheme: props.colorScheme,
  theme: props.theme,
  showColorbar: props.showColorbar,
  showTitle: props.showTitle,
  weekdayLabels: props.showWeekdays,
  monthLabels: props.showMonths
}));

async function fetchData() {
  loading.value = true;
  error.value = null;
  
  try {
    let data: StatsResponse;
    
    if (props.platform === 'github') {
      data = await getGitHubContribution(props.username);
    } else if (props.platform === 'leetcode') {
      data = await getLeetCodeSubmission(props.username);
    } else {
      throw new Error(`Unsupported platform: ${props.platform}`);
    }
    
    jsonData.value = data;
    
    if (props.outputFormat === 'svg' || props.outputFormat === 'both') {
      svgContent.value = generateHeatmap(
        data.data,
        data.username,
        data.summary,
        chartOptions.value
      );
    }
  } catch (err) {
    error.value = err instanceof Error ? err.message : 'An error occurred';
    console.error('Error fetching data:', err);
  } finally {
    loading.value = false;
  }
}

// Watch for prop changes and refetch data
watch(
  () => [props.username, props.platform],
  () => {
    if (props.username) {
      fetchData();
    }
  },
  { immediate: true }
);

// Watch for chart option changes and regenerate SVG
watch(
  () => chartOptions.value,
  () => {
    if (jsonData.value && (props.outputFormat === 'svg' || props.outputFormat === 'both')) {
      svgContent.value = generateHeatmap(
        jsonData.value.data,
        jsonData.value.username,
        jsonData.value.summary,
        chartOptions.value
      );
    }
  },
  { deep: true }
);

// Expose methods for external use
defineExpose({
  fetchData,
  getJsonData: () => jsonData.value,
  getSvgContent: () => svgContent.value
});
</script>

<style scoped>
.dev-chart {
  font-family: monospace;
  font-size: 12px;
}

.dev-chart--light {
  color: #000000;
  background-color: #ffffff;
}

.dev-chart--dark {
  color: #ffffff;
  background-color: #1a1a1a;
}

.loading {
  text-align: center;
  padding: 20px;
  font-style: italic;
}

.error {
  color: #ff6b6b;
  text-align: center;
  padding: 20px;
  background-color: rgba(255, 107, 107, 0.1);
  border: 1px solid rgba(255, 107, 107, 0.3);
  border-radius: 4px;
  margin: 10px 0;
}

.chart-container {
  margin: 10px 0;
}

.svg-container {
  margin-bottom: 20px;
}

.svg-container :deep(svg) {
  max-width: 100%;
  height: auto;
}

.json-output {
  background-color: var(--bg-color, #f8f9fa);
  border: 1px solid var(--border-color, #e9ecef);
  border-radius: 4px;
  padding: 15px;
  overflow-x: auto;
  font-size: 11px;
  line-height: 1.4;
}

.dev-chart--dark .json-output {
  --bg-color: #2d3748;
  --border-color: #4a5568;
}

.dev-chart--light .json-output {
  --bg-color: #f8f9fa;
  --border-color: #e9ecef;
}
</style>