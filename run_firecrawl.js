// run_firecrawl.js
import dotenv from "dotenv";
import fetch from "node-fetch";

dotenv.config();

const apiKey = process.env.FIRECRAWL_API_KEY;
const url = process.argv[2];

if (!apiKey || !url) {
  console.error("❌ FIRECRAWL_API_KEY or target URL is missing.");
  process.exit(1);
}

const startCrawl = async () => {
  try {
    const response = await fetch("https://api.firecrawl.dev/v1/crawl", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${apiKey}`,
      },
      body: JSON.stringify({
        url,
        includeSubdomains: false,
        markdown: true,
        output: {
          markdown: true,
        },
      }),
    });

    if (!response.ok) {
      const errorText = await response.text();
      throw new Error(`Failed to start crawl: ${response.status} – ${errorText}`);
    }

    const { jobId, ...rest } = await response.json();
    console.log("🔥 Full crawl response:", { jobId, ...rest });
    console.log(`🚀 Crawl started. Job ID: ${jobId}`);
    return jobId;
  } catch (err) {
    console.error("❌ Error starting crawl:", err.message);
    process.exit(1);
  }
};

const pollCrawlStatus = async (jobId, interval = 5000, maxRetries = 30) => {
  const endpoint = `https://api.firecrawl.dev/v1/crawl/${jobId}`;
  let retries = 0;

  while (retries < maxRetries) {
    try {
      const response = await fetch(endpoint, {
        headers: {
          Authorization: `Bearer ${apiKey}`,
        },
      });

      if (!response.ok) {
        const text = await response.text();
        throw new Error(`Failed to fetch job status: ${response.status} – ${text}`);
      }

      const data = await response.json();

      if (data.status === "complete" && data.markdown) {
        console.log("✅ Crawl complete!");
        console.log(data.markdown);
        return;
      } else if (data.status === "error") {
        console.error("❌ Crawl failed:", data);
        return;
      } else {
        console.log(`⏳ Still processing... (${retries + 1}/${maxRetries})`);
      }
    } catch (err) {
      console.error("❌ Error crawling:", err.message);
    }

    retries++;
    await new Promise((resolve) => setTimeout(resolve, interval));
  }

  console.error("❌ Crawl timed out.");
};

const run = async () => {
  const jobId = await startCrawl();
  await pollCrawlStatus(jobId);
};

run();