# Global public-contact playbook

Use this playbook for every target market and product category. Keep the source categories and evidence rules fixed, but discover the actual websites, languages, role names, and industry sources at runtime. Do not hard-code one country's registry, one trade fair, or one professional network as a universal dependency.

## Contents

1. Build a market source map
2. Run the eight public source lanes
3. Adapt the role ladder to the customer type
4. Generate reproducible search queries
5. Verify and classify contact coverage
6. Use enrichment only as a last-mile option

## 1. Build a market source map

Before company discovery, resolve and record:

- the target market's primary business language, common secondary language, and local script;
- local product, application, customer-type, supplier, partnership, and decision-maker terms;
- the official corporate registry or equivalent legal-entity source when one is publicly accessible;
- relevant government or regulator directories, licence lists, certification directories, and public-company filings;
- national, regional, or international public-procurement and contract-award portals relevant to the market;
- industry associations, chambers, member directories, trade fairs, conferences, exhibitor lists, and speaker lists;
- local professional networks, news sources, job boards, distributor locators, partner directories, and business directories whose public pages are indexable without signing in;
- access limits and evidence weaknesses for every discovered source.

Use only pages that are publicly accessible without requiring the user to create an account, install a browser extension, or provide credentials. If a source presents a login wall, paid gate, CAPTCHA loop, or terms that prohibit the intended automated access, skip it and record the limitation. Never ask the user to bypass access controls.

Treat cross-border legal-entity, trademark, certification, or procurement databases as optional discovery and identity-resolution sources. Check their current access terms before use. Do not bulk scrape a public database whose terms restrict automation.

## 2. Run the eight public source lanes

Run these lanes for every retained company. Adapt page names and queries to the local language.

### Lane 1: official company pages

Check the home page, about, team, leadership, management, contact, legal notice, press, newsroom, careers, supplier, partner, product, category, branch, distributor, and investor pages. Inspect the sitemap or indexed page inventory when navigation hides relevant pages.

Best for company identity, current leadership, official roles, public business email, phone, and contact forms.

### Lane 2: search-engine-indexed pages and documents

Use domain-restricted and exact-company searches. Search public PDFs, catalogs, brochures, manuals, press releases, presentations, show guides, archived event pages, and other indexed documents.

Best for staff names, role history, direct business emails that were intentionally published, and contact-specific evidence not linked from the current navigation.

### Lane 3: official registries and regulators

Search the market's corporate registry, legal-entity register, securities filings, licence directory, regulator list, certification directory, or equivalent official source.

Best for exact legal identity, current or recent legal representatives, parent-subsidiary resolution, registered address, regulated activity, and brand ownership. Do not treat a legal representative as a buyer without role-specific evidence.

### Lane 4: associations, chambers, and member directories

Search relevant national and regional trade associations, chambers of commerce, cluster organizations, franchise networks, and member directories.

Best for discovering qualified companies, sector membership, locations, and sometimes named representatives or public routes. Verify final person and company claims on stronger sources when possible.

### Lane 5: trade fairs, conferences, exhibitors, and speakers

Search current and historical exhibitor directories, show guides, conference programs, speaker biographies, sponsor pages, webinars, and event PDFs.

Best for product-category fit, responsible sales/product/marketing leaders, public business emails, and recent company-role evidence.

### Lane 6: public procurement and contract awards

Search national, regional, municipal, multilateral-development-bank, and international-organization procurement notices and award documents when the customer type includes projects, institutions, facilities, government suppliers, or public buyers.

Best for named procurement contacts, project teams, department emails, phone numbers, equipment scope, timing, and incumbent suppliers. Do not generalize a notice-specific contact into a company-wide buying role.

### Lane 7: public commercial signals

Search company newsrooms, reputable news, interviews, podcasts, webinars, videos, job postings, partner announcements, distributor locators, reseller pages, service networks, product launches, and certification announcements.

Best for executives, product/category leaders, operations or project owners, marketing/channel leaders, reporting lines, and current initiatives. Treat job titles mentioned only in old content as potentially stale.

### Lane 8: public professional profiles and search snippets

Search LinkedIn and any relevant local professional network through publicly accessible profile pages or indexed search results. Search the exact name plus company and role after a candidate is found elsewhere, and also use role-plus-company searches for discovery.

Best for current name-company-title matching and profile URLs. If the full page requires login, retain only what the public result supports, label it as secondary evidence, and do not require registration. Never invent or approximate a profile URL.

## 3. Adapt the role ladder to the customer type

Start with the role family most likely to own the decision, then continue through the remaining relevant families.

| Customer type | Preferred role order |
| --- | --- |
| Importer, distributor, wholesaler | procurement/imports/sourcing/supply chain; category/product; commercial leadership; owner or managing director; channel/business development |
| Retailer or ecommerce operator | buyer/category/merchandising/assortment/private label; sourcing; product; commercial leadership |
| Brand owner | sourcing/private label; product/product development; category; brand/commercial leadership; founder or managing director |
| Manufacturer | procurement/supply chain/materials; plant/operations/engineering when technically relevant; business-unit leadership; owner or managing director |
| Project buyer, contractor, integrator | project procurement; project/facilities/engineering/operations; commercial leadership; managing director |
| Consultant, designer, or specifier | technical/specification/design/project leadership; product approval or vendor management; project procurement when applicable; managing director for smaller firms |
| Facility or service operator | equipment/facilities/operations/project; procurement; general manager or owner; partnerships |
| Small owner-led company | owner/founder/managing director; product/category; procurement; commercial or marketing leadership |
| Larger multi-unit company | regional or business-unit procurement; category/product; operations/facilities; relevant commercial leadership; avoid defaulting to the group CEO |

Include marketing, brand, partnerships, channel, or business-development leadership only when the product and cooperation model make those roles commercially relevant or when higher-priority roles cannot be verified. Do not present a fallback executive or marketing contact as a verified procurement owner.

Distinguish buying authority from specification influence. A consultant, designer, architect, engineer, or technical adviser may influence product selection without issuing the purchase order; label that role as a specifier or influencer unless public evidence supports procurement authority.

## 4. Generate reproducible search queries

Generate each query in the target market's primary language, a common secondary business language when relevant, and English when companies in that market commonly publish English pages.

Use templates such as:

```text
site:{company-domain} ({local-role-terms})
site:{company-domain} ({local-contact-terms}) ({product-or-category-terms})
site:{company-domain} filetype:pdf ({local-contact-terms} OR "@{company-domain}")
"{legal-company-name}" "{local-role-term}"
"{brand-name}" "{local-role-term}"
"{company-name}" ({conference-term} OR {exhibitor-term} OR {speaker-term})
"{company-name}" ({association-term} OR {member-term} OR {partner-term})
"{company-name}" ({tender-term} OR {contract-award-term})
site:{public-professional-network} "{company-name}" "{local-role-term}"
```

Search both legal and trading names. Use multiple local title variants and abbreviations. Do not assume that English titles are used in every market.

## 5. Verify and classify contact coverage

Accept a named contact only when evidence supports the person's name, current company assignment, and commercially relevant role. Prefer current official evidence; use credible event, association, professional-profile, or press evidence as secondary support.

Prefer evidence published or updated within the previous 24 months. Accept an undated current official team or leadership page when the page is live and internally consistent. Treat older dated evidence as historical unless a newer source confirms the assignment, and record the date limitation instead of silently presenting it as current.

Classify each retained company:

- `A — 具名联系人＋公开直接联系方式`: verified named decision-maker plus a publicly published personal business email or direct phone;
- `B — 具名联系人＋公开转交渠道`: verified or credible named decision-maker plus a department or company route;
- `C — 具名联系人但无直接渠道`: supported name and role, but only a profile or contact-specific source is available;
- `D — 仅部门或公司渠道`: the complete public search found no supported person, but a department or company route exists;
- `E — 公开来源仍未解决`: the required lanes were exhausted and no usable route was found.

Do not keep an `E` result in the qualified list because qualification requires a reachable public company channel. Place it in near matches when commercial fit remains plausible and the only material gap is reachability, or exclude it when other required evidence is also insufficient.

Store the classification in `contact_status` using the existing Chinese status vocabulary, and list the completed lanes, role families, public-network result, and limitations in `contact_search_note`.

Never:

- infer a person's email from a company pattern;
- relabel a department or general mailbox as a personal email;
- merge same-name people without company-role evidence;
- treat an old title as current without marking the uncertainty;
- use a search snippet alone to claim a direct email or phone;
- lower the evidence threshold to reach the requested lead count.

## 6. Use enrichment only as a last-mile option

Complete the public workflow first. Preserve the best supported person and public route even when a personal email is missing.

Apply [apollo-routing.md](apollo-routing.md). Public research starts immediately. Use Apollo People Search only when the plugin/MCP is connected and current official documentation marks the exact action zero-credit. Use enrichment only after explicit approval for the exact credit-consuming call. If no enrichment tool is installed, connected, available, or approved, export the public-web workbook normally. Do not block delivery.

If the user has already prohibited registration, plugin installation, paid tools, or enrichment, do not offer installation again during the same task. When Apollo tools are detected, stop registration and installation prompts permanently for normal runs. Preserve the row-level deep-research prompt for future use and record the service as declined or unavailable.

Generate the row-level prompt from the evidence already found:

- named person available: include the verified name, company domain, current role, and exact public professional-profile URL when available;
- no named person available: include the company domain, customer type, localized role families searched, and remaining target role families;
- always state that the service may consume credits and must show cost before execution.
