---
name: find-public-trade-leads
description: Collect a seven-part product and target-customer brief, research qualified foreign-trade prospects using public web sources, run a dedicated named procurement-contact search for every shortlisted company, verify company and contact evidence, score and deduplicate results, draft personalized outreach, and export a polished Chinese-language Excel workbook. Use when a user wants importers, distributors, wholesalers, brand owners, manufacturers, retailers, buyers, decision-makers, or other B2B prospects for any product and market, with optional Apollo enrichment only when public contact coverage remains inadequate.
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

Use public web search, official company pages, official catalogs, public registries, trade associations, exhibitor lists, and reputable business directories as the default research layer. Do not require paid enrichment, CRM mutations, or outbound platforms to produce the first useful workbook.

## 3. Discover, verify, and deduplicate

Search broadly, then verify the final shortlist.

For every retained company:

- verify company identity, market presence, website, address, business model, size band, product/category evidence, public email or contact route, and phone;
- run the dedicated contact-discovery pass in [references/research-workflow.md](references/research-workflow.md) after company qualification; company-level research does not count as contact research;
- search first for named procurement, purchasing, sourcing, category, product, merchandising, supplier-management, or buying contacts; for genuinely small owner-led firms, search the owner or managing director;
- verify a named person's current company assignment and relevant role before recommending them;
- populate `contact_status`, `contact_search_note`, and `contact_source_urls` for every retained row; these fields must never be blank;
- continue until either a named contact is supported or the required public search lanes are documented as exhausted;
- prefer official sources for final claims;
- use directories and search snippets only as discovery or clearly labeled secondary evidence;
- show `未找到具名采购联系人` instead of an empty contact-name cell when the public search is exhausted;
- never guess a person's name, title, email pattern, LinkedIn URL, phone, purchasing activity, certifications, revenue, or employee count;
- label named contacts as `已公开核实`, `仅二手来源`, or `待核实`;
- when no named buyer is verifiable, label the result as `未找到具名联系人；已提供部门渠道`, `未找到具名联系人；已提供公司渠道`, or `公开网页未找到可用联系人`;
- use a clearly labeled department or company-general route when no public buyer is verifiable.

Measure named-contact coverage before drafting outreach. If coverage is zero or below 50% of qualified companies after the public search pass, pause once to offer installation or connection of Apollo as an optional second pass. Explain that Apollo may require a paid plan or consume credits. Do not imply that Apollo is free, do not install or spend credits without user approval, and do not block the public-web workbook when the user declines or Apollo is unavailable.

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

Derive reachability from the actual contact path:

- 5: verified named buyer plus a public direct email or direct phone;
- 4: verified or credible named buyer plus a public company or department route;
- 3: relevant department email or department phone;
- 2: company-general email or switchboard;
- 1: contact form or website route only;
- 0: no usable public route.

Never award 4–5 points to a row that has no named contact.

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
- verify that every row has a nonblank contact status and contact-search note;
- verify that contact names, roles, and LinkedIn URLs have contact-specific source evidence;
- verify that rows without a named contact display an honest searched-not-found label and a usable fallback route when available;
- reconcile the named-contact count and reachability score with the actual contact fields;
- spot-check narrative customer fields and translate any avoidable foreign-language analysis into Chinese;
- confirm that source-original identifiers and target-language outreach remain unchanged;
- repair clipped or unreadable output;
- return only the final `.xlsx`, not builders, JSON, or preview files.

## 8. Handoff

Report:

- qualified, near-match, and excluded counts;
- top prospects and why they rank highly;
- named-contact coverage versus company-channel coverage;
- public contact-search coverage, unresolved companies, and whether Apollo was unavailable, offered, declined, or used with approval;
- source limitations and unresolved fields;
- output workbook path.

State that public fit does not prove active purchasing demand. Offer deeper background checks or revised outreach as a separate next step.
