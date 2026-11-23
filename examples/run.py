"""Minimal example: run the willhaben-jobs-scraper Actor and print one line per job posting.

Usage: APIFY_TOKEN=... python run.py   (pip install apify-client)
"""
import os
import sys

from apify_client import ApifyClient

token = os.environ.get("APIFY_TOKEN")
if not token:
    sys.exit("Set the APIFY_TOKEN environment variable first.")

client = ApifyClient(token)

# Job titles hold characters the Windows console code page cannot print: write UTF-8.
sys.stdout.reconfigure(encoding="utf-8")

run_input = {
    "keywords": "Buchhalter",
    "location": "Graz",
    "maxItems": 100,
}

# 1024 MB is enough for this Actor and keeps the start fee low.
run = client.actor("bibian/willhaben-jobs-scraper").call(run_input=run_input, memory_mbytes=1024)

count = 0
for job in client.dataset(run.default_dataset_id).iterate_items():
    count += 1
    # Austrian job ads state a minimum pay: salaryMin is that floor, salaryMax is always empty.
    if job.get("salaryMin"):
        salary = f"from {job['salaryMin']} {job['salaryCurrency']}/{job['salaryPeriod']}"
    else:
        salary = "salary not stated"
    place = job.get("city") or job.get("locationLabel")
    posted = (job.get("datePosted") or "")[:10]
    print(f"{job['title']} | {job.get('companyName') or 'confidential'} | {place}, {job.get('region')} | {job['employmentType']} | {salary} | {posted}")
print(f"{count} job postings")
