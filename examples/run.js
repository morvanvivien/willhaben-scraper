// Minimal example: run the willhaben-jobs-scraper Actor and print one line per job posting.
// Usage: APIFY_TOKEN=... node run.js   (Node 18 or later, npm install apify-client)
import { ApifyClient } from 'apify-client';

const token = process.env.APIFY_TOKEN;
if (!token) {
    console.error('Set the APIFY_TOKEN environment variable first.');
    process.exit(1);
}

const client = new ApifyClient({ token });

const input = {
    keywords: 'Buchhalter',
    location: 'Graz',
    maxItems: 100,
};

// 1024 MB is enough for this Actor and keeps the start fee low.
const run = await client.actor('bibian/willhaben-jobs-scraper').call(input, { memory: 1024 });
const { items } = await client.dataset(run.defaultDatasetId).listItems();

console.log(`${items.length} job postings`);
for (const job of items) {
    // Austrian job ads state a minimum pay: salaryMin is that floor, salaryMax is always empty.
    const salary = job.salaryMin
        ? `from ${job.salaryMin} ${job.salaryCurrency}/${job.salaryPeriod}`
        : 'salary not stated';
    console.log(`${job.title} | ${job.companyName ?? 'confidential'} | ${job.city ?? job.locationLabel}, ${job.region} | ${job.employmentType} | ${salary} | ${job.datePosted?.slice(0, 10)}`);
}
