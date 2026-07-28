# Workbook input contract

Pass one UTF-8 JSON object to `scripts/run_build.py`.

## Top-level shape

```json
{
  "brief": {},
  "sender": {},
  "leads": [],
  "near_matches": [],
  "excluded": [],
  "generated_at": "YYYY-MM-DD"
}
```

## `brief`

Required string fields:

- `product`
- `target_market`
- `cooperation_model`
- `supply_capability`
- `customer_size`
- `reference_brands`
- `exclusions`

Optional:

- `target_count` number, default 20
- `product_sources` array of URLs or uploaded file names
- `research_notes` string
- `outreach_language` string

## `sender`

Optional strings:

- `name`
- `title`
- `company`
- `email`
- `phone`
- `website`

Use placeholders in drafts when sender contact details are absent.

## `leads`

Each lead supports:

```json
{
  "priority": 1,
  "company": "Company name",
  "legal_name": "Legal name",
  "customer_type": "Distributor",
  "size_band": "Medium",
  "size_evidence": "Fact or proxy",
  "address": "Full address",
  "country": "Country",
  "website": "https://example.com",
  "product_evidence": "Verified overlap",
  "contact_name": "",
  "contact_title": "",
  "contact_status": "verified public | secondary-source only | not found",
  "email": "",
  "email_type": "named public | department | company general | form | not found",
  "phone": "",
  "phone_type": "direct | department | switchboard | not found",
  "linkedin": "",
  "fit_reason": "Inference, not demand claim",
  "risks": "Uncertainty or barrier",
  "confidence": "High | Medium | Low",
  "verified_date": "YYYY-MM-DD",
  "source_urls": ["https://example.com/page"],
  "evidence_boundary": "Fact / Inference / Unknown",
  "next_step": "Suggested next verification or contact action",
  "outreach_subject": "Subject",
  "outreach_body": "Personalized draft",
  "scores": {
    "product_overlap": 0,
    "channel_fit": 0,
    "cooperation_fit": 0,
    "supply_fit": 0,
    "size_fit": 0,
    "evidence_quality": 0,
    "reachability": 0
  }
}
```

Score maxima are 30, 20, 15, 10, 10, 10, and 5.

## `near_matches`

Use the same lead shape. Include `near_match_reason`.

## `excluded`

Each item supports:

```json
{
  "company": "Company name",
  "website": "https://example.com",
  "reason": "Hard exclusion or identity conflict",
  "source_url": "https://example.com/page"
}
```

## Empty data

- Use empty strings or empty arrays for unknown values.
- Never use guessed values.
- Keep URLs as plain text so the workbook remains auditable.
