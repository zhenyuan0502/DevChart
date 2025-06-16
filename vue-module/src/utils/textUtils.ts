/**
 * Remove newlines and extra spacing from text
 */
export function removeNewlinesAndSpacing(text: string): string {
  return text.replace(/\n/g, '').trim();
}

/**
 * Standardize text by removing newlines and normalizing whitespace
 */
export function standardizeText(text: string): string {
  const cleaned = removeNewlinesAndSpacing(text);
  return cleaned.replace(/\s+/g, ' ');
}

/**
 * Convert Unix timestamp to YYYY-MM-DD date string
 */
export function unixTimestampToDate(timestamp: string | number): string {
  const ts = typeof timestamp === 'string' ? parseInt(timestamp) : timestamp;
  return new Date(ts * 1000).toISOString().split('T')[0];
}

/**
 * Get date template for the last 366 days
 */
export function getDateTemplate(): Record<string, number> {
  const today = new Date();
  const last366Days = new Date(today.getTime() - 366 * 24 * 60 * 60 * 1000);
  
  const data: Record<string, number> = {};
  data[today.toISOString().split('T')[0]] = 0;
  data[last366Days.toISOString().split('T')[0]] = 0;
  
  return data;
}

/**
 * Format date as YYYY-MM-DD
 */
export function formatDate(date: Date): string {
  return date.toISOString().split('T')[0];
}