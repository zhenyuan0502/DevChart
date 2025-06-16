import { createApp } from 'vue'
import DevChart from './components/DevChart.vue'

createApp({
  components: {
    DevChart
  },
  data() {
    return {
      githubUsername: 'zhenyuan0502',
      githubTheme: 'light' as 'light' | 'dark',
      githubOutput: 'svg' as 'svg' | 'json' | 'both',
      
      leetcodeUsername: '',
      leetcodeTheme: 'light' as 'light' | 'dark',
      leetcodeOutput: 'svg' as 'svg' | 'json' | 'both'
    }
  }
}).mount('#app')