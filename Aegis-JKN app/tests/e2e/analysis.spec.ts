import { test, expect } from '@playwright/test';

test.describe('Graph Analysis', () => {
  test('should load a specific claim graph', async ({ page }) => {
    const claimId = 'claim-123';
    await page.goto(`/graph/${claimId}`);
    await expect(page).toHaveURL(new RegExp(`/graph/${claimId}`));
    // Check if graph container is rendered
    await expect(page.locator('.graph-container')).toBeVisible();
  });

  test('should allow interacting with graph nodes', async ({ page }) => {
    await page.goto('/graph/claim-123');
    const node = page.locator('.graph-node').first();
    await node.click();
    await expect(page.locator('.node-details')).toBeVisible();
  });

  test('should capture visual regression of the graph', async ({ page }) => {
    await page.goto('/graph/claim-123');
    await expect(page).toHaveScreenshot('graph-analysis-page.png');
  });
});
