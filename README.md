# How to Scrape Willhaben Jobs: Austria Job Postings, Salary Floors and Full Descriptions (Willhaben Jobs API)

> **Run it now, no code: [willhaben-jobs-scraper on the Apify Store](https://apify.com/bibian/willhaben-jobs-scraper)** &nbsp;|&nbsp; $0.0012 per job posting ($1.20 per 1,000) &nbsp;|&nbsp; no login, no proxy to set up

Willhaben Jobs (willhaben.at/jobs) is the job section of willhaben.at, Austria's largest classifieds portal: about 14,800 live Stellenanzeigen on 22 November 2026, from trades, retail and logistics to IT, health care, banking and the public service. There is no public feed of them. This guide shows how to export them as a clean dataset instead of writing a scraper: one row per posting with employer, place, working time, the salary the employer states, publication and expiry dates, the employer's own apply link and the full description in plain text. It uses a free-to-try Apify Actor, from the console or from code, with no login and nothing to configure.

Searches this page answers: Willhaben Jobs scraper, willhaben.at/jobs scraper, willhaben Jobs API, Austria job postings dataset, Austrian job postings export, how to scrape willhaben jobs, Stellenanzeigen Österreich Daten, apprenticeship (Lehre) postings Austria, monitor new job postings in Austria daily.

## What you get from the Willhaben Jobs scraper

- **The whole board, newest first.** With nothing typed in, the run returns the latest postings. Add a keyword, a town, a district or a state, one of the 17 job fields, a working time, a position (apprenticeship, internship, management...), an employer type, or paste any willhaben.at/jobs search URL.
- **The first publication date, not the renewal date.** willhaben lists a posting under the day its employer last renewed it, and employers renew hundreds of old postings every night. `datePosted` is the first publication, `renewedAt` keeps the site's own date, and `publishedWithin` filters on the first publication.
- **A salary floor on most postings.** Austrian job ads have to state a minimum pay: 80 of the 89 distinct postings read for this guide carried one. It comes as `salaryMin` with `EUR` and a period (`hour`, `day`, `month` or `year`); `salaryMax` is always empty because the site publishes a single amount.
- **The employer behind the posting.** With descriptions on, each row adds the employer's industry, size and website, the state and district, the expiry date and the employer's own apply link.
- **A daily watch that charges only for what is new.** Tick `onlyNew` and schedule the Actor: each run delivers, and bills, only the postings no earlier run of that search delivered.
- **No personal data collected on purpose.** The contact person an employer enters is never read, e-mail addresses and phone numbers are removed from descriptions, the apply link is cleaned, and an employer that reads as a private person is left out (`companyName` is `null` and `confidentialCompany` is `true`).

Export the dataset as JSON, CSV or Excel, or read it through the Apify API. A real sample (five postings from a live run on 23 November 2026, 00:49 UTC, descriptions shortened to 300 characters, no personal data) is in [`sample-output.json`](sample-output.json).

## Output fields

The unified job fields (the same names as the other job scrapers in this series, following schema.org `JobPosting`) come first; the willhaben-specific fields come after them.

| Field | What it is |
|---|---|
| `id`, `sourceId`, `source` | Stable identifier (`willhaben.at:<posting number>`), the posting number on the site, and `willhaben.at`; the same from one run to the next |
| `url`, `title` | Public page of the posting and the job title as published |
| `companyName`, `companyUrl`, `confidentialCompany` | Employer name and its willhaben company page; `companyName` is `null` and `confidentialCompany` is `true` when the employer is hidden or named like a private person |
| `locationLabel`, `city`, `region`, `postalCode`, `country` | Place as displayed, town, state (Bundesland), postal code (only when the posting has one place and one code), and `AT`, `DE` or `CH` |
| `remote` | `remote`, `hybrid`, `onsite` or `unknown`: `hybrid` when the employer ticked "remote work possible", otherwise only when the title or text says so in so many words |
| `employmentType` | `full_time`, `part_time`, `freelance`, `internship`, `apprenticeship`, `temporary` or `unknown`, from the working time the employer ticks and the position |
| `salaryMin`, `salaryMax`, `salaryCurrency`, `salaryPeriod` | The stated pay: the amount, always `null`, `EUR`, and `hour`, `day`, `month` or `year` |
| `datePosted`, `validThrough` | First publication (ISO 8601 with Vienna's offset) and expiry day (with descriptions) |
| `experienceLevel`, `industry`, `skills` | The position the site files the posting under (`Mitarbeiter:in`, `Praktikum`...), the employer's industry (with descriptions), and an empty list |
| `locations`, `district`, `countryAssumed` | Every place the posting lists, the district (with descriptions), and `true` when no place names a country and `AT` was assumed |
| `employmentModes`, `employmentTime`, `overpayPossible` | The site's own words (`Vollzeit`, `Teilzeit`, `Geringfügig`, `Freiberuflich`; `ab sofort`, `befristet`), and whether the employer pays above the stated salary |
| `renewedAt`, `isRenewed` | When the employer last renewed the posting, and whether that is a later day than the first publication |
| `companyId`, `companyWebsite`, `companySize`, `jobCategories`, `applyUrl` | The employer's id, website and size (`501-1000`), the categories the posting is filed under, and the employer's own application page |
| `description` | Plain-text description, when `includeDescriptions` is on (default) |
| `searchUrl`, `scrapedAt` | The search the row came from, extraction time |

Five real rows from the sample run:

| Title | Employer | Place | Contract | Salary | Posted |
|---|---|---|---|---|---|
| Referent/in Gebarungsprüfung | Land Oberösterreich | Linz | full_time | EUR 3,810 / month | 2026-11-20 |
| Elektroplaner Industrieanlagen (m/w/d) | VACE Engineering GmbH | Gänserndorf | full_time | EUR 63,000 / year | 2026-11-21 |
| Ferialpraktikant Verkauf (m/w/d) Forstauer Straße 2c, 5550 Radstadt | HOFER KG | Radstadt | internship | EUR 2,396 / month | 2026-11-20 |
| Personalverrechner (M/W/D) | C&D Foods | Birkfeld | full_time (hybrid) | EUR 3,600 / month | 2026-11-20 |
| Paketfahrer | DEX Logistik GmbH | Innsbruck | full_time | EUR 2,200 / month | 2026-11-20 |

## Use cases

- **Monitor the Austrian job market.** Which employers, roles, states and districts are hiring, day after day, with the salary floor Austrian employers have to state.
- **Feed a job alert or an aggregator.** A stable `id`, the first publication date and the employer's own apply link on every row, and `onlyNew` so each scheduled run only pays for fresh postings.
- **Track trades, staffing agencies and apprenticeships.** Filter on job field (trades, health care, IT, logistics...), on employer type (companies or staffing agencies) or on position (apprenticeship, internship, management).
- **Benchmark pay.** Compare the stated minimum pay by trade, state or employer, in euros per hour, month or year.
- **Copy a search from the site.** Do the search on willhaben.at/jobs, paste its address in **Search URLs** and get exactly the postings you saw.

## Input

| Field | What it does |
|---|---|
| `keywords` | A job title or skill (`Buchhalter`, `Elektriker`). The site looks for the words in the title and the text of the posting. |
| `location` | A town, a district (Bezirk) or a state (Bundesland): `Graz`, `Landeck`, `Tirol`. Several, separated by commas, make one search each, merged without duplicates. Empty means all of Austria. |
| `jobField` | One of the 17 fields the site files its postings under, by name: `it`, `trades_crafts`, `health_care_social`, `logistics_transport`, `sales_retail`, `hospitality_tourism`, `finance_accounting`, `engineering_architecture`, `public_service`, `administration`, `education_research`, `consulting_legal`, `facility_security_cleaning`, `management`, `marketing_media_culture`, `human_resources`, `production_manufacturing`. |
| `employmentType` | `any`, `full_time`, `part_time`, `marginal` (Geringfügig) or `freelance`, as the site's own working-time filter sets it. |
| `positionLevel` | `any`, `staff`, `team_lead`, `management`, `project_management`, `internship`, `apprenticeship` or `traineeship`. |
| `companyType` | `any`, `direct_employer` (companies hiring for themselves) or `agency` (staffing agencies). |
| `publishedWithin` | `any`, `1` (24 hours), `3` or `7` days, counted from the first publication of the posting. Applies to every search, pasted URLs included. |
| `searchUrls` | Search pages copied from willhaben.at/jobs, for example `https://www.willhaben.at/jobs/suche?keyword=koch&location=Wien`, or the site's own pages such as `willhaben.at/jobs/suche/kellner-in/wien`. The page and page-size parameters are ignored. A single posting, a company page or another site is refused with a message. |
| `maxItems` | The run stops once this many postings are saved (default 50). |
| `onlyNew` | For scheduled runs: skip postings an earlier run of this same search already delivered, without opening them. |
| `includeDescriptions` | Open each posting page to add the description, industry, size, state, district, expiry date and apply link (default on). Off, 90 postings come per request and a run is much faster. |

The fields make a search of their own when you fill them in; they do not narrow a pasted URL (except `publishedWithin`). Leave everything empty to read the whole board, newest first.

Ready-to-copy inputs. The searches below were run on the Apify cloud on 23 November 2026 (capped at 10 postings, without `onlyNew`) and each returned 10 postings.

Accountants in Graz:

```json
{
  "keywords": "Buchhalter",
  "location": "Graz",
  "maxItems": 100
}
```

Apprenticeships (Lehre) first published in the last week:

```json
{
  "positionLevel": "apprenticeship",
  "publishedWithin": "7",
  "maxItems": 200
}
```

A daily watch on the whole board, listing fields only, charged only for what is new (set it on a daily schedule):

```json
{
  "publishedWithin": "1",
  "onlyNew": true,
  "includeDescriptions": false,
  "maxItems": 1000
}
```

Exactly the postings of a search page you copied from the site:

```json
{
  "searchUrls": ["https://www.willhaben.at/jobs/suche?keyword=koch&location=Wien"],
  "maxItems": 200
}
```

## Three ways to use it

### 1. Apify console, no code

1. Open [the Actor page](https://apify.com/bibian/willhaben-jobs-scraper) and click **Try for free** (a free Apify account is enough). The form is already filled with full-time postings first published in the last 3 days, and 50 postings.
2. Add a keyword, a place or a job field, or paste a search URL, then click **Start**.
3. When the run finishes, open the **Output** tab, then **Export** as CSV, Excel or JSON.
4. For a daily watch, open **Schedules**, create a daily schedule for the Actor, and tick `onlyNew` with `publishedWithin` set to `1` in the input.

### 2. Apify API with JavaScript

```bash
npm install apify-client
export APIFY_TOKEN="your token from Apify console, Settings, Integrations"
node examples/run.js
```

```js
import { ApifyClient } from 'apify-client';

const client = new ApifyClient({ token: process.env.APIFY_TOKEN });

const run = await client.actor('bibian/willhaben-jobs-scraper').call({
    keywords: 'Buchhalter',
    location: 'Graz',
    maxItems: 100,
}, { memory: 1024 });

const { items } = await client.dataset(run.defaultDatasetId).listItems();
for (const job of items) {
    console.log(`${job.title} | ${job.companyName} | ${job.city}, ${job.region} | ${job.employmentType} | from ${job.salaryMin} ${job.salaryCurrency}/${job.salaryPeriod}`);
}
```

The complete file is [`examples/run.js`](examples/run.js) (ES module, Node 18 or later).

### 3. Apify API with Python

```bash
pip install apify-client
export APIFY_TOKEN="your token from Apify console, Settings, Integrations"
python examples/run.py
```

```python
import os
from apify_client import ApifyClient

client = ApifyClient(os.environ["APIFY_TOKEN"])

run = client.actor("bibian/willhaben-jobs-scraper").call(
    run_input={"keywords": "Buchhalter", "location": "Graz", "maxItems": 100},
    memory_mbytes=1024,
)

for job in client.dataset(run.default_dataset_id).iterate_items():
    print(f"{job['title']} | {job['companyName']} | {job['city']}, {job['region']} | {job['employmentType']} | from {job['salaryMin']} {job['salaryCurrency']}/{job['salaryPeriod']}")
```

The complete file is [`examples/run.py`](examples/run.py). Never put your token in the code: read it from the `APIFY_TOKEN` environment variable as above. On Windows, the complete file switches the console output to UTF-8, because Austrian postings hold characters its default code page cannot print.

## Pricing

Pay per result: **$0.0012 per job posting** ($1.20 per 1,000 postings), plus a start fee of $0.0025 per GB of run memory, with no monthly subscription. These are the free-plan prices; paid Apify plans get lower ones (the Store page shows the lowest tier, from $0.96 per 1,000). A run that saves 100 postings costs about $0.12 plus the start fee. Apify's free plan includes monthly credits, enough to try it. Prices are those shown on the [Store page](https://apify.com/bibian/willhaben-jobs-scraper) when this guide was written (23 November 2026); the Store page is the reference.

## Limits and honest notes

- **The board holds about 15,000 postings** (about 14,800 on 22 November 2026). Reading all of them with descriptions takes about 4 hours at one page per second; without descriptions, about 3 minutes. About 200 to 400 postings are first published on a working day, far fewer at weekends.
- **Speed.** The pre-filled run (50 postings with descriptions) took 60 seconds; ten postings took 12 to 18 seconds in the tests behind the inputs above, and 1 second without descriptions.
- **Renewals make old postings look new.** The site lists postings by renewal day, so a search without `publishedWithin` also returns postings first published long before: the pasted-URL search above returned five first published in February 2020. Set `publishedWithin` to keep only the first publications of the last 24 hours, 3 days or week. That filter reads the site's whole window of renewals, several thousand postings for a week, so it takes minutes rather than seconds on a full pass.
- **The salary is a floor.** `salaryMax` is always `null`, and `overpayPossible` says when the employer pays above the stated amount. A pay in a unit the Actor does not know is left empty rather than converted.
- **Some fields need the posting page.** `region` (partly), `district`, `postalCode`, `industry`, `validThrough` and `applyUrl` come from the posting page: they are filled with `includeDescriptions` on, not without it. `postalCode` is also empty when a posting lists several places or codes (it was filled on 21 of the 50 postings of the pre-filled run).
- **Postings with several places.** `locations` lists them all and `city` is the first one it can read. In the Buchhalter / Graz test, 2 of the 10 postings carried Spittal an der Drau as their place because they list Spittal, Graz and Wien: read `locations` if you need all of them.
- **Employers named like a private person are left out on a best-effort basis.** The test is on the name alone, so a sole trader whose name carries a title or a profession word, or an employer that only shows a first name, can still appear in `companyName`. If you need to exclude private persons for certain, check that column yourself.
- **Named contacts in descriptions.** E-mail addresses and phone numbers are removed, and so are most contact names, but a name written after "Kontakt" or "Ansprechpartner" can remain: 8 of the 79 descriptions read for this guide. Do not republish descriptions without your own check.
- **Descriptions** are the employers' text, mostly German, sometimes English or another language. The Actor does not translate them.
- **Ties in the site's order.** A list sorted by renewal time has ties (hundreds of postings renewed in the same second at night): on a full read of the board a few postings per thousand can be listed twice or missed by the site. The Actor drops the doubles, and a second run catches most of what was missed.
- **Jobs only.** Real estate, cars and the marketplace of willhaben.at are not covered.
- This is an unofficial tool, not affiliated with willhaben. Check the rules that apply to your use of the data, for example the GDPR.

## FAQ

**Do I need an account, cookies or a proxy for willhaben Jobs?**  
No. The Actor reads publicly visible pages only, at most one request per second.

**Why do some postings show a `datePosted` from months ago?**  
Because that is when they were first published; their employers renew them, so the site lists them as if new. Use `publishedWithin` to keep only the recent first publications.

**Why is `salaryMax` always empty?**  
Because Austrian job ads state a minimum pay and the site publishes a single amount. The Actor never guesses a range.

**Can I find apprenticeships and internships?**  
Yes. Set `positionLevel` to `apprenticeship` (Lehre), `internship` (Praktikum) or `traineeship`; `employmentType` is then `apprenticeship` or `internship` on the rows.

**How do I get only new postings every day?**  
Set `publishedWithin` to `1`, tick `onlyNew` and schedule the Actor daily. Each run delivers, and charges, only what no earlier run of the same search already delivered.

**Can I export to Excel or a database?**  
Yes: JSON, CSV, Excel and XML downloads, the Apify API, or integrations such as Google Sheets, webhooks and Zapier.

## Auf Deutsch

**Willhaben Jobs Scraper: die Stellenanzeigen von willhaben.at/jobs als Datensatz, mit Arbeitgeber, Ort, Arbeitszeit, Mindestgehalt, Veröffentlichungsdatum und vollständigem Anzeigentext, ohne Login.** Exportiert die österreichischen Stellenanzeigen von willhaben nach JSON, CSV oder Excel: Titel, Firma, Ort, Bundesland, Bezirk, Vollzeit, Teilzeit, geringfügig oder freiberuflich, Lehre und Praktikum, das angegebene Mindestgehalt, erste Veröffentlichung (nicht das Datum der Erneuerung), Ablaufdatum, Bewerbungslink des Arbeitgebers und der Text der Anzeige. Suche nach Stichwort (`keywords`), Ort (`location`), Berufsfeld, Arbeitszeit, Position oder Arbeitgeberart, füge die Adresse einer Suche von der Website ein und nutze `onlyNew`, um bei jedem täglichen Lauf nur die neuen Anzeigen zu erhalten und zu bezahlen.

## Related Actors

- [JobScout24 Scraper · Swiss Jobs, No Login](https://apify.com/bibian/jobscout24-jobs-scraper): one of Switzerland's large job boards, the same one-schema approach.
- [Jobup Scraper · Swiss Jobs, No Login](https://apify.com/bibian/jobup-jobs-scraper): the job board of French-speaking Switzerland.
- [Germany Jobs Scraper · 7 Boards, One Schema](https://apify.com/bibian/germany-jobs-scraper): German-language job boards in one run.

## Feedback

Need another board, filter or field? Open an issue in the Issues tab of the Actor on Apify and say what you need: requests are read, and the most asked ones are built next.
