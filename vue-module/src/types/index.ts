export interface ChartData {
  [date: string]: number;
}

export interface StatsResponse {
  username: string;
  title: string;
  summary: string;
  data: ChartData;
}

export interface ChartOptions {
  username: string;
  theme?: 'light' | 'dark';
  width?: number;
  height?: number;
  colorScheme?: string;
  showColorbar?: boolean;
  showTitle?: boolean;
  showWeekdays?: boolean;
  showMonths?: boolean;
}

export interface ChartOutput {
  svg?: string;
  json?: StatsResponse;
}

export type Platform = 'github' | 'leetcode';

export interface GitHubContribution {
  date: string;
  level: number;
  count?: number;
}

export interface LeetCodeSubmission {
  timestamp: string;
  submissions: number;
}