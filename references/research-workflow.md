# Public-web research workflow

Read [public-contact-playbook.md](public-contact-playbook.md) before building market-specific source queries or starting contact discovery.

## Source order

Prefer:

1. official company website, catalog, product page, legal notice, contact page, careers page;
2. official registry, trade association, chamber, exhibitor list, certification directory;
3. reputable business directory or distributor directory;
4. professional-network public profile or search snippet;
5. other public secondary sources.

Use weak sources to discover candidates, not to prove strong claims.

## Query families

Translate product and buyer terms into the target market's language. Combine:

- product + distributor/importer/wholesaler;
- product category + private label/OEM/brand owner;
- product + catalog/PDF;
- reference brand + distributor/dealer;
- application + supplier/stockist;
- product + purchasing/category manager/contact;
- relevant trade fair + exhibitor;
- relevant association + member directory.

Record enough query logic in research notes for another agent to reproduce the search.

Before applying these query families, build the runtime market source map required by `public-contact-playbook.md`. Discover local registries, regulators, procurement portals, associations, trade fairs, professional networks, and business-language title variants for the actual country and industry. Do not reuse a source simply because it worked for a previous country or product.

## Qualification

Retain a company only when:

- it operates in the target market;
- its business model matches a requested customer type;
- public evidence shows direct product, category, application, or channel overlap;
- its size is inside or reasonably near the requested band;
- it has a reachable public company channel;
- it does not violate an exclusion.

Mark a result `Near Match` when one important criterion is uncertain but the company remains commercially plausible.

## Contact rules

Treat contact discovery as a separate required pass after the company shortlist is qualified. Do not stop because a general email or switchboard was found.

### Role ladder

Select the role order from the customer-type matrix in `public-contact-playbook.md`; do not apply one universal procurement-to-executive order. Consider the applicable families: procurement/imports/supply chain; buyer/category/merchandising/private label; product/product development; project/facilities/engineering/operations; technical specification or design; business-unit/commercial leadership; owner/managing director for smaller firms; and marketing/brand/channel/partnerships when commercially relevant. After named roles, retain a relevant department route and then a company-general route.

Translate every applicable role family into the target market's language before searching. Do not stop at a company channel or after one role family fails. Continue until a supported person is found or all role families relevant to that customer type are exhausted.

### Required public search lanes

For every retained company, run and record all eight source categories in `public-contact-playbook.md`. At minimum, make the following company-specific checks:

1. official site: team, management, about, contact, imprint, press, careers, supplier, and category pages;
2. domain query: `site:company-domain` plus local-language purchasing, sourcing, executive, product, category, marketing, brand, partnership, supplier, and buyer titles;
3. company-name query plus the same four role tiers;
4. LinkedIn or a relevant local public professional-network profile search that shows the exact person, current company, and role;
5. public PDFs, catalogs, press releases, exhibitor profiles, association pages, or job postings that name responsible staff.

Also check official registries or regulators, public procurement or award notices when commercially relevant, associations or chambers, trade events or speaker pages, partner or distributor networks, public news/interviews, and other local professional networks discovered in the market source map. Record `not relevant`, `not publicly accessible`, or `no result` rather than silently skipping a lane.

Populate the corresponding eight `public_source_lane_results` keys in the workbook input. Use a concise Chinese result for each lane. The free-text `contact_search_note` should summarize the localized role ladder and important limitations instead of being the only record that a lane was checked.

Use multiple role variants selected for the customer type. A search for only `procurement` is not enough. Record the best supported person from the highest relevant role tier, but keep searching public professional networks for an exact profile URL even after a named person is found.

### Verification and completion

Accept a named person only when public evidence supports:

- the person's name;
- current assignment to the exact company or resolved legal entity;
- a role in the procurement, executive, product/category, or marketing/business-development ladder.

Use `已公开核实` when official evidence supports the person and role. Use `仅二手来源` when a credible public professional or industry source supports both but the company site does not. Use `待核实` only when the person-company match is plausible but role currency remains uncertain; do not treat this as a verified buyer.

The contact pass is complete only when:

- a named contact and contact-specific source are recorded, plus the exact public professional-profile URL or an explicit not-found/login-wall note; or
- all named-person role families applicable to the customer type and all required public search lanes are recorded, `contact_status` explains the fallback, and the best department or company route is supplied.

Never leave `contact_status` or `contact_search_note` blank. When no person is found after the complete ladder, write `需通过Apollo插件优化搜索具名联系人` in the workbook contact cell and keep any recommended department explicitly labeled as a transfer target rather than a named person.

Never infer an email from a naming pattern. Never convert a general mailbox into a named person's email.

### Professional-profile and email completion

For every retained company:

1. search the exact contact name plus company and role on LinkedIn and any relevant local public professional network;
2. accept only an exact public profile URL supported by the person-company-role match;
3. search official team/contact pages, public staff directories, press releases, PDFs, event profiles, association pages, and public professional profiles for a direct business email;
4. preserve a department or company mailbox only as a fallback route and label it accurately;
5. if no public personal business email is supported, set `apollo_deep_research_prompt` to text beginning exactly `需尝试Apollo积分深度背调`.

Use these prompt patterns:

- named contact available: `需尝试Apollo积分深度背调：使用已核实或候选联系人的姓名、公司域名和公开职业主页进行People Enrichment，补全并复核商务邮箱；调用前确认积分成本。`
- no named contact available: `需尝试Apollo积分深度背调：使用公司域名、客户类型和已经搜索的当地语言角色词继续查找最高优先决策人，再补全并复核商务邮箱；调用前确认积分成本。`

### Optional Apollo second pass

Follow [apollo-routing.md](apollo-routing.md). Start public research without waiting for Apollo setup or a three-mode choice.

- When Apollo tools are absent, show the one-time, non-blocking registration and plugin recommendation only when the onboarding state says it has not been shown. Continue public research while showing it.
- When Apollo tools are detected, never repeat the registration or installation recommendation.
- Use People Search only when current Apollo documentation explicitly marks that exact action zero-credit. It may supplement a name, title, current company, or professional profile, but does not provide full email or phone details.
- Before Contacts Search, Company Search, enrichment, personal-email reveal, phone retrieval, waterfall enrichment, record-writing, or any unknown/positive-cost action, disclose the exact call scope and obtain explicit approval.
- If Apollo authentication fails, continue public research and record the mismatch without repeating the installation pitch.
- Verify any Apollo contact against company identity and role; label provenance and do not merge conflicting people silently.
- If the user declines a specific enrichment call or Apollo returns no useful result, continue with the best public/free workbook and preserve the unresolved status.

## Size evidence

Use explicit employee count, location count, warehouse footprint, or public company profile when available. Otherwise use a labeled size proxy such as:

- number of branches;
- management-team depth;
- warehouse or production footprint;
- job volume;
- catalog breadth.

Write `estimated` or `proxy` when exact headcount is unavailable.

## Evidence boundary

For each row, separate:

- `事实`: directly supported by the cited source.
- `推断`: why the fact suggests commercial fit.
- `未知`: any requested field that could not be verified.

Do not describe public product overlap as current demand, buying intent, or an active sourcing project.

Write the evidence summary, inference, uncertainty, size explanation, fit reason, risk, and next step in Simplified Chinese. Keep company names, personal names, addresses, contact routes, URLs, registered brands, and short source-original excerpts unchanged.

## Deduplication

Normalize:

- scheme and `www` in URLs;
- Unicode and punctuation;
- company suffixes;
- case and whitespace;
- country names.

Manually review subsidiaries, branches, dealer locations, marketplace storefronts, and group companies before merging.
