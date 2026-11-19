# Decide in the Gateway, Enforce in Snowflake: Identity-Aware Access for Custom Apps: Maintenance Instructions

Pair-programmed by SE Community + Cortex Code

## Architecture

README.md (the guide), ELI5.md (plain-language companion), WORKED-EXAMPLE.md
(synthetic fixture, complete configuration, acceptance checks), and
tests/test_worked_example.py. No deployment scripts or account objects.

Sections: (1) A Filter Is Not Enforcement, (2) Propagate the Real Identity, (3) Entitlements as Code,
(4) Enforce and Prove It in Snowflake, (5) What the Gateway Still Does, (6) Optional: Snowflake-Native
Hosting for Internal Apps. The worked example covers Sections 1-5; Section 6 has no fixture.

## Conventions

- Every technical claim links to official Snowflake documentation or a public Snowflake blog post.
- Practitioner quotes use blockquote format with attribution and a link.
- Each section opens with why it matters, then practices, then a summary table.
- README code samples are at most 10 lines; complete configurations live only in WORKED-EXAMPLE.md.
- The worked example stays on one synthetic scenario. Keep fixture, configuration, checks, and acceptance cases consistent.
- Preview features are labeled Preview with their cost stated.
- No customer names, people, account identifiers, meeting references, or commercial figures in any file.
- README metadata is the single source for verification and expiry dates (expiry at most 60 days after verification).

## Key Commands

Run from this directory:

```bash
uv run --with pyyaml --with pytest pytest tests -q
python3 <se-guide-builder>/scripts/check_guide.py . --denylist <private denylist>
```

## Review Focus

Re-check these first; they are Preview, recently changed, or gated:

- External OAuth `EXTERNAL_OAUTH_SCOPE_DELIMITER` (docs say Support must enable it; the CREATE and ALTER pages disagree)
- `IS_AGENTIC`, `QUERY_HISTORY.agent_type`, and `ACCESS_HISTORY.agents_info` (new columns; a BCR replaced `invoker_identity`)
- Terraform provider source (`snowflakedb/snowflake`) and whether organization-user resources exist yet
- App Runtime: serverless compute and Python are Preview; caller's-rights rules; billing service types
- Snowflake Postgres: access roles (Preview), the 32-database and 64-role limits, mirroring tiers and the no-primary-key behavior
- `ACCESS_HISTORY` (3 hours) and `GRANTS_TO_ROLES` (2 hours) latency

Keep the row access policy argument name distinct from the mapping-table columns in every example.

## Re-verification

Renew only after re-checking each core claim against current documentation and
release notes. Update **Last verified** and **Expires** together, and keep review
evidence outside this directory. Formatting fixes do not reset the clock.
