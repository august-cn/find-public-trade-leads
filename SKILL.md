---
name: find-public-trade-leads
description: Collect a seven-part product and target-customer brief, start with public-web research, non-blockingly recommend Apollo registration and plugin setup once when Apollo MCP is unavailable, stop setup prompts after the plugin is detected, optionally use zero-credit people search or individually approved credit enrichment for personal emails and phones, persist git-ignored project-local company history for cross-batch deduplication, verify prospects and decision-makers, draft outreach, and export a polished Chinese-language Excel workbook. Use when a user wants new or additional importers, distributors, wholesalers, brand owners, manufacturers, retailers, project buyers, executives, product or marketing decision-makers for any product and market.
---

# Find Public Trade Leads

Build a verified prospect workbook from a product brief. Use public web evidence as the required first layer. Treat Apollo as an optional contact-completion layer that never blocks public research and never spends credits without exact-call approval. Treat product fit as a prospecting hypothesis, never as proof of current purchasing demand.

## 1. Start public research and detect Apollo

Read [references/apollo-routing.md](references/apollo-routing.md). Do not ask the user to choose among three Apollo modes before research.

- Begin the public-web workflow as soon as the seven-part brief is complete; Apollo setup must not delay company discovery or contact research.
- Detect whether Apollo plugin/MCP tools are available in the current session.
- If Apollo is unavailable and the one-time recommendation has not been shown, recommend registering at Apollo and installing/connecting the Apollo plugin while public research continues. Explain that connected Apollo MCP can supplement named-contact discovery and, with separately approved credits, investigate fuller contact data including personal/business email and phone. Do not pause for an answer.
- After the Apollo plugin/MCP tools are detected, never show the registration or installation recommendation again. If authentication fails, continue publicly and report the connection issue without repeating the installation pitch.
- When Apollo is connected, use People Search only if current official documentation marks the exact action zero-credit. Use it after the public pass to supplement names, titles, current companies, and professional profiles.
- Before every credit-consuming action, disclose the exact action, record count, requested fields, known or maximum credit effect, and whether phone, personal-email reveal, or waterfall enrichment is included. Wait for explicit approval for that exact call.
- Never treat plugin installation, connection, prior approval, or general willingness to use Apollo as blanket spending permission.

## 2. Load project history and detect continuation

Read [references/continuation-search.md](references/continuation-search.md). Resolve the current Codex project root and load its local history at the start of every run.

- When the user asks to continue, find more, or run the next batch and history exists, reuse the last complete brief automatically. Apply only the changes stated in the current message.
- Exclude every previously qualified, near-match, and excluded company before selecting the new batch.
- Do not ask for the prior Excel and do not ask the seven questions again in continuation mode.
- When no project history exists, continue with the normal seven-part intake.
- Keep history local and git-ignored. Never commit or publish it.

## 3. Collect the seven-part brief

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

## 4. Build the search brief

Read [references/research-workflow.md](references/research-workflow.md).
Read [references/public-contact-playbook.md](references/public-contact-playbook.md) before generating market-specific source and contact queries.

Derive:

- product names, materials, applications, standards, and local-language synonyms;
- likely customer types and buying roles;
- a runtime market source map covering local languages, official registries, regulators, public procurement, associations, trade fairs, public professional networks, and access limitations;
- hard inclusions and exclusions;
- target size proxies;
- reference-brand channel clues;
- reproducible query families;
- a visible 100-point scoring model.

Use public web search, official company pages, official catalogs, public registries, trade associations, exhibitor lists, and reputable business directories as the default research layer. Do not require paid enrichment, CRM mutations, or outbound platforms to produce the first useful workbook.

## 5. Discover, verify, and deduplicate

Search broadly, then verify the final shortlist.

For every retained company:

- verify company identity, market presence, website, address, business model, size band, product/category evidence, public email or contact route, and phone;
- run the dedicated contact-discovery pass in [references/research-workflow.md](references/research-workflow.md) after company qualification; company-level research does not count as contact research;
- adapt the role ladder to the prospect's customer type using [references/public-contact-playbook.md](references/public-contact-playbook.md), then fill the best supported person instead of applying one fixed title order to every company;
- verify a named person's current company assignment and relevant role before recommending them;
- run a dedicated public professional-profile pass for every retained company, including LinkedIn or a relevant local network, and populate the exact public profile URL whenever the person-company-role match is supported;
- populate `contact_status`, `contact_search_note`, and `contact_source_urls` for every retained row; these fields must never be blank;
- populate all eight keys in `public_source_lane_results` with a checked result, `不适用`, or an access limitation; never omit a lane silently;
- continue down the full role ladder until either a named contact is supported or every required public search lane is documented as exhausted;
- run and record the eight public source lanes: official company pages; indexed pages and public documents; official registries and regulators; associations and chambers; trade fairs and speakers; public procurement and awards when relevant; public commercial signals; and public professional profiles;
- prefer official sources for final claims;
- use directories and search snippets only as discovery or clearly labeled secondary evidence;
- show `需通过Apollo插件优化搜索具名联系人` instead of an empty contact-name cell only after all role families applicable to that customer type are exhausted;
- never guess a person's name, title, email pattern, professional-profile URL, phone, purchasing activity, certifications, revenue, or employee count;
- label named contacts as `已公开核实`, `仅二手来源`, or `待核实`;
- when no named decision-maker is verifiable, label the result as `需通过Apollo插件优化搜索；当前仅提供部门渠道`, `需通过Apollo插件优化搜索；当前仅提供公司渠道`, or `需通过Apollo插件优化搜索；公开网页暂无可用联系人`;
- use a clearly labeled department or company-general route when no named decision-maker is verifiable;
- never treat a company-general or department mailbox as a person's email;
- when a public personal business email remains unavailable after the required email lanes, populate `apollo_deep_research_prompt` with a prompt beginning exactly `需尝试Apollo积分深度背调`.

Use only public pages that do not require the user to register, install an extension, provide credentials, or bypass access controls. Skip login walls, paid gates, and sources whose terms prohibit the intended automated access. Do not make any named platform, registry, trade fair, or country-specific source a universal dependency.

Measure named-contact and public-personal-email coverage before drafting outreach. If a named contact or personal email is still missing after the public search pass, preserve the best public route and write the Apollo deep-research prompt in that row. When Apollo MCP is available, run only currently documented zero-credit People Search without approval; request exact-call approval before company search, enrichment, email reveal, phone retrieval, waterfall enrichment, or any action with unknown or positive credit cost. Never install, register, connect, or spend credits automatically merely because information is missing.

Normalize domains and legal suffixes. Deduplicate by:

1. registrable domain plus market;
2. normalized legal or trading name plus market;
3. manual review of branches, subsidiaries, group companies, and marketplace sellers.

Apply these rules both within the current batch and against the project history loaded in section 2. Count historical matches as duplicates skipped; do not recycle them as new qualified or near-match leads.

Exclude companies that violate the user's hard filters. Keep near matches separate when qualified coverage is insufficient.

## 6. Score and select

Score observable fit:

- product/category overlap: 30
- customer type and channel fit: 20
- cooperation-model fit: 15
- supply/logistics fit: 10
- size fit: 10
- evidence quality: 10
- reachability: 5

Derive reachability from the actual contact path:

- 5: verified named decision-maker plus a public direct email or direct phone;
- 4: verified or credible named decision-maker plus a public company or department route;
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

## 7. Draft outreach

Write one personalized draft per retained company in the market's business language unless the user requests another language.

Ground the opening in a verified company fact. State the sender's product and cooperation fit without claiming the prospect is currently buying. Use the named buyer only when publicly verified; otherwise address the relevant department or company team. End with one low-friction next step.

Do not send messages or enroll contacts in campaigns.

## 8. Enforce Chinese workbook language

Use Simplified Chinese for the workbook interface and research analysis by default, even when the target market uses another language.

Write in Chinese:

- every worksheet name, report title, column header, field label, instruction, note, score label, tier, status, and legend;
- customer type, size band, size evidence, product evidence summary, fit reason, risk, confidence, evidence boundary, next step, exclusion reason, and research note;
- contact, email, and phone type labels;
- factual summaries and inferences. When source wording matters, write the Chinese summary first and place a short original-language excerpt after it.

Keep these fields in their source-original form:

- company and legal names, contact person names, postal addresses, email addresses, phone numbers, websites, source URLs, public professional-profile URLs, and registered brand or product names;
- outreach subject and body written in the target market's business language.

Translate a contact title or department into Chinese; add the original title in parentheses only when it improves identification. Never translate, rewrite, or infer an email address, URL, phone number, personal name, or postal address.

Before export, review every narrative field in the input JSON. Translate avoidable foreign-language analysis into Chinese instead of relying only on Chinese column headers.

## 9. Export the workbook

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
  --preview-dir <preview-directory> \
  --project-root <current-project-root>
```

Use the exact executable and dependency paths returned by the workspace dependency loader. Do not install packages.

After a successful workbook build, `run_build.py` records the completed batch in the current project's git-ignored history automatically. Confirm that history recording succeeded before handoff.

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
- verify that contact names, roles, and public professional-profile URLs have contact-specific source evidence;
- verify that every company has a recorded public professional-network search result, even when no exact profile is found;
- verify that every company has all eight structured `public_source_lane_results` entries and that each entry records a result, `不适用`, or an access limitation;
- verify that rows without a named contact display an honest searched-not-found label only after the full role ladder is exhausted and retain a usable fallback route when available;
- verify that every row without a public personal email contains a prompt beginning `需尝试Apollo积分深度背调`;
- reconcile the named-contact count and reachability score with the actual contact fields;
- spot-check narrative customer fields and translate any avoidable foreign-language analysis into Chinese;
- confirm that source-original identifiers and target-language outreach remain unchanged;
- repair clipped or unreadable output;
- return only the final `.xlsx`, not builders, JSON, or preview files.

## 10. Handoff

Report:

- qualified, near-match, and excluded counts;
- top prospects and why they rank highly;
- named-contact coverage versus company-channel coverage;
- public contact-search and professional-profile coverage, unresolved companies, missing personal-email prompts, Apollo availability, and whether free search or individually approved enrichment was used;
- batch ID, historical company count, and duplicates skipped;
- source limitations and unresolved fields;
- output workbook path.

State that public fit does not prove active purchasing demand. Offer deeper background checks or revised outreach as a separate next step.
