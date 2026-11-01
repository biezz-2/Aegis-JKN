import { test, expect } from '@playwright/test';

test.describe('Simulation Tool', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/simulation');
  });

  test('should allow configuring simulation parameters', async ({ page }) => {
    await page.fill('input[name="iteration-count"]', '100');
    await page.selectOption('select[name="algorithm"]', 'mhgsl');
    await expect(page.locator('button:has-text("Run Simulation")')).toBeEnabled();
  });

  test('should display simulation results after execution', async ({ page }) => {
    await page.click('button:has-text("Run Simulation")');
    // Wait for simulation to finish (assuming loading state exists)
    await page.waitForSelector('.simulation-results');
    await expect(page.locator('.results-summary')).toBeVisible();
  });
});
