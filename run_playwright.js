// run_playwright.js

import { chromium } from 'playwright';
import fs from 'fs';
import path from 'path';
import TurndownService from 'turndown';

const startUrl = process.argv[2];
const outputFile = process.argv[3] || 'data/output.md';

if (!startUrl) {
  console.error("❌ Please provide a URL as an argument.");
  process.exit(1);
}

const turndownService = new TurndownService();
const visited = new Set();
const maxDepth = 3;

function sanitizeFilename(url) {
  return url.replace(/[^a-zA-Z0-9]/g, '_').slice(0, 100);
}

async function crawl(page, url, depth) {
  if (depth > maxDepth || visited.has(url)) return;
  visited.add(url);

  try {
    console.log(`🌐 Visiting (depth ${depth}): ${url}`);
    await page.goto(url, { waitUntil: 'networkidle' });

    const html = await page.content();
    const markdown = turndownService.turndown(html);
    const fileName = sanitizeFilename(url) + '.md';
    const outputDir = path.dirname(outputFile);
    if (!fs.existsSync(outputDir)) fs.mkdirSync(outputDir, { recursive: true });
    fs.appendFileSync(outputFile, `\n\n# Page: ${url}\n\n${markdown}`);

    if (depth < maxDepth) {
      const baseUrl = new URL(startUrl).origin;
      const links = await page.$$eval(
        'a',
        (anchors, base) =>
          anchors
            .map(a => a.href)
            .filter(href => href.startsWith(base) && !href.includes('#')),
        baseUrl
      );

      for (const link of links) {
        if (!visited.has(link)) {
          await crawl(page, link, depth + 1);
        }
      }
    }
  } catch (err) {
    console.error(`❌ Error scraping ${url}: ${err.message}`);
  }
}

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage();
  await crawl(page, startUrl, 0);
  await browser.close();
})();