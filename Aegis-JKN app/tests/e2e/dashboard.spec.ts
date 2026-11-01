import { test, expect } from '@playwright/test';

test.describe('Dashboard Navigation', () => {
  test.beforeEach(async ({ page }) => {
    // Fast-track to dashboard via cookie/localStorage if needed
    await page.goto('/dashboard');
  });

  test('should render dashboard key metrics', async ({ page }) => {
    await expect(page.getByRole('heading', { name: /dashboard/i })).toBeVisible();
    await expect(page.locator('.metric-card')).toHaveCount(3);
  });

  test('should navigate to Graph Analysis page', async ({ page }) => {
    await page.click('nav >> text=Graph Analysis');
    await expect(page).toHaveURL(/.*graph/);
  });

  test('should navigate to Simulation page', async ({ page }) => {
    await page.click('nav >> text=Simulation');
    await expect(page).toHaveURL(/.*simulation/);
  });
});
