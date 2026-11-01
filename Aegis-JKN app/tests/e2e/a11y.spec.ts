import { test, expect } from '@playwright/test';
import AxeBuilder from '@axe-core/playwright';

test.describe('Accessibility Scans', () => {
  const pagesToScan = [
    { name: 'Dashboard', path: '/dashboard' },
    { name: 'Analysis', path: '/graph/claim-123' },
    { name: 'Simulation', path: '/simulation' },
    { name: 'Login', path: '/login' },
  ];

  for (const pageInfo of pagesToScan) {
    test(`Accessibility scan for ${pageInfo.name}`, async ({ page }) => {
      await page.goto(pageInfo.path);
      const accessibilityScanResults = await new AxeBuilder({ page }).analyze();
      expect(accessibilityScanResults.violations).toEqual([]);
    });
  }
});
