import axios from 'axios';
import type { StatsResponse } from '../types';
import { standardizeText, getDateTemplate } from '../utils/textUtils';

const GITHUB_BASE_URL = 'https://github.com/users/{username}/contributions';

/**
 * Fetch GitHub contribution data for a user
 * Note: This may require a CORS proxy in browser environments
 */
export async function getGitHubContribution(username: string): Promise<StatsResponse> {
  try {
    const url = GITHUB_BASE_URL.replace('{username}', username);
    
    // Note: In a real browser environment, this will likely be blocked by CORS
    // You may need to use a proxy service like cors-anywhere or implement server-side proxy
    const response = await axios.get(url, {
      headers: {
        'User-Agent': 'DevChart-Vue-Module'
      }
    });

    const data = getDateTemplate();
    
    // Parse the HTML response to extract contribution data
    const parser = new DOMParser();
    const doc = parser.parseFromString(response.data, 'text/html');
    
    // Find the summary text
    const summaryElement = doc.querySelector('h2.f4.text-normal.mb-2');
    const summary = summaryElement 
      ? standardizeText(summaryElement.textContent || '')
      : 'contributions in the last year';
    
    // Find the contribution calendar
    const table = doc.querySelector('table.ContributionCalendar-grid');
    if (table) {
      const days = table.querySelectorAll('td.ContributionCalendar-day');
      days.forEach((day) => {
        const date = day.getAttribute('data-date');
        const level = day.getAttribute('data-level');
        if (date && level) {
          data[date] = parseInt(level, 10);
        }
      });
    }

    return {
      username,
      title: 'Github Contribution',
      summary: `GitHub with ${summary}`,
      data
    };
  } catch (error) {
    console.error('Error fetching GitHub data:', error);
    return {
      username,
      title: 'Github Contribution',
      summary: 'GitHub with 0 contributions in the last year (fetch failed)',
      data: getDateTemplate()
    };
  }
}

/**
 * Alternative method using GitHub API (requires authentication)
 * This is a placeholder for potential future implementation
 */
export async function getGitHubContributionAPI(username: string, token?: string): Promise<StatsResponse> {
  // This would use the GitHub GraphQL API which requires authentication
  // For now, fall back to the scraping method
  return getGitHubContribution(username);
}