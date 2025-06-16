import { describe, it, expect } from 'vitest'
import { getDateTemplate, standardizeText, unixTimestampToDate, formatDate } from '../utils/textUtils'

describe('textUtils', () => {
  it('should standardize text correctly', () => {
    const input = '  Hello   world  \n  with   newlines  ';
    const expected = 'Hello world with newlines';
    expect(standardizeText(input)).toBe(expected);
  });

  it('should convert unix timestamp to date', () => {
    const timestamp = 1640995200; // 2022-01-01 00:00:00 UTC
    const expected = '2022-01-01';
    expect(unixTimestampToDate(timestamp)).toBe(expected);
  });

  it('should format date correctly', () => {
    const date = new Date('2023-06-15T10:30:00Z');
    expect(formatDate(date)).toBe('2023-06-15');
  });

  it('should create date template with current and past dates', () => {
    const template = getDateTemplate();
    expect(typeof template).toBe('object');
    expect(Object.keys(template)).toHaveLength(2);
    
    // Should have today's date
    const today = new Date().toISOString().split('T')[0];
    expect(template).toHaveProperty(today);
    expect(template[today]).toBe(0);
  });
});