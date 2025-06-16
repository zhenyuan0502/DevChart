import * as d3 from 'd3';
import type { ChartData } from '../types';

interface HeatmapOptions {
  width?: number;
  height?: number;
  cellSize?: number;
  monthLabels?: boolean;
  weekdayLabels?: boolean;
  colorScheme?: string;
  theme?: 'light' | 'dark';
  showColorbar?: boolean;
  showTitle?: boolean;
}

/**
 * Generate SVG heatmap chart similar to GitHub contribution chart
 */
export function generateHeatmap(
  data: ChartData, 
  username: string,
  summary: string,
  options: HeatmapOptions = {}
): string {
  const {
    width = 800,
    height = 200,
    cellSize = 12,
    monthLabels = true,
    weekdayLabels = true,
    colorScheme = 'github',
    theme = 'light',
    showColorbar = true,
    showTitle = true
  } = options;

  // Create SVG element
  const svg = d3.create('svg')
    .attr('width', width)
    .attr('height', height)
    .attr('viewBox', `0 0 ${width} ${height}`)
    .style('font-family', 'monospace')
    .style('font-size', '12px');

  // Parse data and get date range
  const dates = Object.keys(data).map(d => new Date(d)).sort((a, b) => a.getTime() - b.getTime());
  const values = Object.values(data);
  const maxValue = Math.max(...values);
  const minValue = Math.min(...values);

  // Color scales based on theme
  const colorScale = getColorScale(colorScheme, theme, minValue, maxValue);

  // Calculate grid dimensions
  const startDate = dates[0];
  const endDate = dates[dates.length - 1];
  const yearStart = new Date(startDate.getFullYear(), 0, 1);
  const yearEnd = new Date(endDate.getFullYear(), 11, 31);
  
  // const weeksInYear = d3.timeWeek.count(yearStart, yearEnd);

  // Calculate margins
  const margin = { top: showTitle ? 60 : 20, right: 20, bottom: 20, left: weekdayLabels ? 40 : 20 };
  
  // Main group for the heatmap
  const g = svg.append('g')
    .attr('transform', `translate(${margin.left}, ${margin.top})`);

  // Add title
  if (showTitle) {
    svg.append('text')
      .attr('x', width / 2)
      .attr('y', 20)
      .attr('text-anchor', 'middle')
      .attr('font-weight', 'bold')
      .attr('font-size', '16px')
      .attr('fill', theme === 'dark' ? '#ffffff' : '#000000')
      .text(`${username}'s ${summary}`);
  }

  // Add weekday labels
  if (weekdayLabels) {
    const weekdays = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'];
    g.selectAll('.weekday-label')
      .data(weekdays)
      .enter()
      .append('text')
      .attr('class', 'weekday-label')
      .attr('x', -10)
      .attr('y', (d, i) => i * (cellSize + 1) + cellSize / 2)
      .attr('text-anchor', 'end')
      .attr('dominant-baseline', 'middle')
      .attr('font-size', '10px')
      .attr('fill', theme === 'dark' ? '#cccccc' : '#666666')
      .text(d => d);
  }

  // Add month labels
  if (monthLabels) {
    const monthFormat = d3.timeFormat('%b');
    const months = d3.timeMonths(yearStart, yearEnd);
    
    g.selectAll('.month-label')
      .data(months)
      .enter()
      .append('text')
      .attr('class', 'month-label')
      .attr('x', d => d3.timeWeek.count(yearStart, d) * (cellSize + 1) + cellSize / 2)
      .attr('y', -5)
      .attr('text-anchor', 'middle')
      .attr('font-size', '10px')
      .attr('fill', theme === 'dark' ? '#cccccc' : '#666666')
      .text(monthFormat);
  }

  // Create cells for each day
  dates.forEach(date => {
    const dateStr = date.toISOString().split('T')[0];
    const value = data[dateStr] || 0;
    const weeksSinceStart = d3.timeWeek.count(yearStart, date);
    const dayOfWeek = date.getDay();
    
    g.append('rect')
      .attr('x', weeksSinceStart * (cellSize + 1))
      .attr('y', dayOfWeek * (cellSize + 1))
      .attr('width', cellSize)
      .attr('height', cellSize)
      .attr('fill', colorScale(value))
      .attr('stroke', theme === 'dark' ? '#2d3748' : '#e2e8f0')
      .attr('stroke-width', 0.5)
      .append('title')
      .text(`${dateStr}: ${value} contributions`);
  });

  // Add colorbar
  if (showColorbar) {
    addColorbar(svg, colorScale, minValue, maxValue, width - 200, height - 40, theme);
  }

  return svg.node()?.outerHTML || '';
}

/**
 * Get color scale based on scheme and theme
 */
function getColorScale(scheme: string, theme: 'light' | 'dark', min: number, max: number) {
  let colors: string[];
  
  if (scheme === 'github') {
    if (theme === 'dark') {
      colors = ['#161b22', '#0e4429', '#006d32', '#26a641', '#39d353'];
    } else {
      colors = ['#ebedf0', '#9be9a8', '#40c463', '#30a14e', '#216e39'];
    }
  } else {
    // Default green scheme
    colors = theme === 'dark' 
      ? ['#1a1a1a', '#003d00', '#006600', '#009900', '#00cc00']
      : ['#f0f0f0', '#c6e48b', '#7bc96f', '#239a3b', '#196127'];
  }

  return d3.scaleQuantile<string>()
    .domain([min, max])
    .range(colors);
}

/**
 * Add colorbar to the SVG
 */
function addColorbar(
  svg: d3.Selection<SVGSVGElement, any, null, undefined>,
  colorScale: d3.ScaleQuantile<string>,
  min: number,
  max: number,
  x: number,
  y: number,
  theme: 'light' | 'dark'
) {
  const legendWidth = 120;
  const legendHeight = 12;
  const legendSteps = 5;
  
  const legend = svg.append('g')
    .attr('transform', `translate(${x}, ${y})`);

  // Add "Less" label
  legend.append('text')
    .attr('x', -30)
    .attr('y', legendHeight / 2)
    .attr('text-anchor', 'end')
    .attr('dominant-baseline', 'middle')
    .attr('font-size', '10px')
    .attr('fill', theme === 'dark' ? '#cccccc' : '#666666')
    .text('Less');

  // Add color squares
  for (let i = 0; i < legendSteps; i++) {
    const value = min + (max - min) * (i / (legendSteps - 1));
    legend.append('rect')
      .attr('x', i * (legendWidth / legendSteps))
      .attr('y', 0)
      .attr('width', legendWidth / legendSteps)
      .attr('height', legendHeight)
      .attr('fill', colorScale(value))
      .attr('stroke', theme === 'dark' ? '#2d3748' : '#e2e8f0')
      .attr('stroke-width', 0.5);
  }

  // Add "More" label
  legend.append('text')
    .attr('x', legendWidth + 10)
    .attr('y', legendHeight / 2)
    .attr('text-anchor', 'start')
    .attr('dominant-baseline', 'middle')
    .attr('font-size', '10px')
    .attr('fill', theme === 'dark' ? '#cccccc' : '#666666')
    .text('More');
}