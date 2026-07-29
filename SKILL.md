---
name: find-public-trade-leads
description: Collect a seven-part product and target-customer brief, research qualified foreign-trade prospects using public web sources only, verify company and contact evidence, score and deduplicate results, draft personalized outreach, and export a polished Chinese-language Excel workbook while preserving source-original identifiers and outreach text. Use when a user wants importers, distributors, wholesalers, brand owners, manufacturers, retailers, buyers, or other B2B prospects for any product and market without relying on paid sales-intelligence or enrichment plugins.
---

# Find Public Trade Leads

Build a verified prospect workbook from a product brief. Use public web evidence only. Treat product fit as a prospecting hypothesis, never as proof of current purchasing demand.

## 1. Collect the seven-part brief

Read [references/intake-form.md](references/intake-form.md).

Before research, require:

1. Product
2. Target market
3. Cooperation model
4. Supply capability
5. Target customer size
6. Reference brands or competitors
7. Exclusions

Accept the product as text, a public URL, or uploaded files. If files are attached, extract product names, applications, materials, specifications, certifications, packaging, MOQ, and differentiation before building search terms.

If any required field is missing, return only the compact intake form and wait. Do not research from an incomplete brief. Treat target count as optional and default to 20.

If all seven fields are present, normalize them into the data contract and proceed without reconfirming routine assumptions.

## 2. Build the search brief

Read [references/research-workflow.md](references/research-workflow.md).

Derive:

- product names, materials, applications, standards, and local-language synonyms;
- likely customer types and buying roles;
- hard inclusions and exclusions;
- target size proxies;
- reference-brand channel clues;
- reproducible query families;
- a visible 100-point scoring model.

Use only public web search, official company pages, official catalogs, public registries, trade associations, exhibitor lists, and reputable business directories. Do not require or invoke paid enrichment, credit-consuming databases, CRM mutations, or outbound platforms.

## 3. Discover, verify, and deduplicate

Search broadly, then verify the final shortlist.

For every retained company:

- verify company identity, market presence, website, address, business model, size band, product/category evidence, public email or contact route, and phone;
- prefer official sources for final claims;
- use directories and search snippets only as discovery or clearly labeled secondary evidence;
- keep unsupported fields empty;
- never guess a person's name, title, email pattern, LinkedIn URL, phone, purchasing activity, certifications, revenue, or employee count;
- label named contacts as `verified public`, `secondary-source only`, or `not found`;
- use a department or company-general channel when no public buyer is verifiable.

Normalize domains and legal suffixes. Deduplicate by:

1. registrable domain plus market;
2. normalized legal or trading name plus market;
3. manual review of branches, subsidiaries, group companies, and marketplace sellers.

Exclude companies that violate the user's hard filters. Keep near matches separate when qualified coverage is insufficient.

## 4. Score and select

Score observable fit:

- product/category overlap: 30
- customer type and channel fit: 20
- cooperation-model fit: 15
- supply/logistics fit: 10
- size fit: 10
- evidence quality: 10
- reachability: 5

Use formulas in the workbook for totals and tiers:

- `High`: 85–100
- `Medium`: 70–84
- `Explore`: below 70

Do not inflate weak evidence to fill the requested quota. Report shortfalls visibly.

## 5. Draft outreach

Write one personalized draft per retained company in the market's business language unless the user requests another language.

Ground the opening in a verified company fact. State the sender's product and cooperation fit without claiming the prospect is currently buying. Use the named buyer only when publicly verified; otherwise address the relevant department or company team. End with one low-friction next step.

Do not send messages or enroll contacts in campaigns.

## 6. Enforce Chinese workbook language

Use Simplified Chinese for the workbook interface and research analysis by default, even when the target market uses another language.

Write in Chinese:

- every worksheet name, report title, column header, field label, instruction, note, score label, tier, status, and legend;
- customer type, size band, size evidence, product evidence summary, fit reason, risk, confidence, evidence boundary, next step, exclusion reason, and research note;
- contact, email, and phone type labels;
- factual summaries and inferences. When source wording matters, write the Chinese summary first and place a short original-language excerpt after it.

Keep these fields in their source-original form:

- company and legal names, contact person names, postal addresses, email addresses, phone numbers, websites, source URLs, LinkedIn URLs, and registered brand or product names;
- outreach subject and body written in the target market's business language.

Translate a contact title or department into Chinese; add the original title in parentheses only when it improves identification. Never translate, rewrite, or infer an email address, URL, phone number, personal name, or postal address.

Before export, review every narrative field in the input JSON. Translate avoidable foreign-language analysis into Chinese instead of relying only on Chinese column headers.

## 7. Export the workbook

Read [references/data-contract.md](references/data-contract.md).

Create `lead-workbook-input.json` in a writable task output directory. Populate every source URL and evidence boundary. Then:

1. Load workspace spreadsheet dependencies.
2. Run:

```bash
python3 <skill-dir>/scripts/run_build.py \
  --node <bundled-node> \
  --node-modules <bundled-node_modules> \
  --input <lead-workbook-input.json> \
  --output <output.xlsx> \
  --preview-dir <preview-directory>
```

Use the exact executable and dependency paths returned by the workspace dependency loader. Do not install packages.

The workbook must contain:

- `需求与说明`
- `合格客户`
- `开发信`
- `证据与评分`
- `待探索客户` when needed
- `已排除` when needed

After generation:

- inspect the workbook summary and key ranges;
- scan for formula errors;
- view every rendered sheet;
- verify that worksheet names, titles, headers, labels, legends, notes, statuses, tiers, and explanatory fields are in Chinese;
- spot-check narrative customer fields and translate any avoidable foreign-language analysis into Chinese;
- confirm that source-original identifiers and target-language outreach remain unchanged;
- repair clipped or unreadable output;
- return only the final `.xlsx`, not builders, JSON, or preview files.

## 8. Handoff

Report:

- qualified, near-match, and excluded counts;
- top prospects and why they rank highly;
- named-contact coverage versus company-channel coverage;
- source limitations and unresolved fields;
- output workbook path.

State that public fit does not prove active purchasing demand. Offer deeper background checks or revised outreach as a separate next step.
