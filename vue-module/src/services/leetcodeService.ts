import axios from 'axios';
import type { StatsResponse } from '../types';
import { unixTimestampToDate, getDateTemplate } from '../utils/textUtils';

const LEETCODE_BASE_URL = 'https://leetcode.com/graphql/';

const LEETCODE_QUERY = `
  query userProfileCalendar($username: String!, $year: Int) {
    matchedUser(username: $username) {
      userCalendar(year: $year) {
        activeYears
        streak
        totalActiveDays
        dccBadges {
          timestamp
          badge {
            name
            icon
          }
        }
        submissionCalendar
      }
    }
  }
`;

/**
 * Fetch LeetCode submission data for a user
 */
export async function getLeetCodeSubmission(username: string): Promise<StatsResponse> {
  try {
    const response = await axios.post(LEETCODE_BASE_URL, {
      operationName: 'userProfileCalendar',
      query: LEETCODE_QUERY,
      variables: {
        username,
      }
    }, {
      headers: {
        'Content-Type': 'application/json',
        'User-Agent': 'DevChart-Vue-Module'
      }
    });

    const data = getDateTemplate();
    let sum = 0;

    const responseData = response.data;
    
    if (responseData.errors) {
      return {
        username,
        title: 'LeetCode Submission',
        summary: `LeetCode with ${sum} submissions in past one year`,
        data
      };
    }

    const user = responseData.data?.matchedUser?.userCalendar;
    if (!user) {
      return {
        username,
        title: 'LeetCode Submission',
        summary: `LeetCode with ${sum} submissions in past one year (user not found)`,
        data
      };
    }

    const submissions = JSON.parse(user.submissionCalendar || '{}');
    
    for (const [timestamp, count] of Object.entries(submissions)) {
      const date = unixTimestampToDate(timestamp);
      const submissionCount = typeof count === 'number' ? count : parseInt(count as string, 10) || 0;
      data[date] = submissionCount;
      sum += submissionCount;
    }

    return {
      username,
      title: 'LeetCode Submission',
      summary: `LeetCode with ${sum} submissions in past one year`,
      data
    };
  } catch (error) {
    console.error('Error fetching LeetCode data:', error);
    return {
      username,
      title: 'LeetCode Submission',
      summary: 'LeetCode with 0 submissions in past one year (fetch failed)',
      data: getDateTemplate()
    };
  }
}