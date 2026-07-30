# Public-web research workflow

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

### Role order

Prefer public contacts in this order:

1. procurement, purchasing, sourcing, category management, product management;
2. merchandising, buying, supplier management, imports, private label, or relevant business-unit leadership;
3. owner or managing director for genuinely small or owner-led firms;
4. relevant department email or department phone;
5. company-general email, contact form, and switchboard.

Translate these role families into the target market's language before searching.

### Required public search lanes

For every retained company, run and record at least these lanes:

1. official site: team, management, about, contact, imprint, press, careers, supplier, and category pages;
2. domain query: `site:company-domain` plus local-language purchasing, sourcing, category, product, supplier, and buyer titles;
3. company-name query plus the same role terms;
4. public professional-network profiles or search snippets that show both current company and role;
5. public PDFs, catalogs, press releases, exhibitor profiles, association pages, or job postings that name responsible staff.

Use multiple role variants. A search for only `procurement` is not enough when the likely owner is a category manager, product manager, buyer, merchandise manager, import manager, or managing director.

### Verification and completion

Accept a named person only when public evidence supports:

- the person's name;
- current assignment to the exact company or resolved legal entity;
- a role relevant to buying, product, category, sourcing, supplier management, imports, or owner-led purchasing.

Use `已公开核实` when official evidence supports the person and role. Use `仅二手来源` when a credible public professional or industry source supports both but the company site does not. Use `待核实` only when the person-company match is plausible but role currency remains uncertain; do not treat this as a verified buyer.

The contact pass is complete only when either:

- a named contact and contact-specific source are recorded; or
- all required public search lanes are recorded in `contact_search_note`, `contact_status` explains the fallback, and the best department or company route is supplied.

Never leave `contact_status` or `contact_search_note` blank. When no person is found, write `未找到具名采购联系人` in the workbook contact cell and keep any recommended department explicitly labeled as a transfer target rather than a named person.

Never infer an email from a naming pattern. Never convert a general mailbox into a named person's email.

### Optional Apollo second pass

Public web research remains the default and must be completed first. If named-contact coverage is zero or below 50% of the qualified list, offer Apollo installation or connection once as an optional enrichment pass.

- State that Apollo may require a paid plan or consume credits.
- Do not install, connect, or spend credits without user approval.
- If Apollo is not installed, use the available plugin installation prompt rather than giving manual token or credential instructions.
- If the user declines, Apollo is unavailable, or no result is returned, continue with the public-web workbook and preserve the unresolved status.
- Verify any Apollo contact against company identity and role; label its provenance and do not merge conflicting people silently.

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
