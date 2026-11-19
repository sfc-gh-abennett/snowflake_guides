# Snowflake Guides

Best-practices guides for building on Snowflake. Each guide has a technical README, a plain-language ELI5 companion, a worked example built on synthetic data, and local tests that check the worked example's numbers.

Pair-programmed by SE Community + Cortex Code

> **No support provided.** Reference only; validate before production use. These guides are not official Snowflake documentation. Every claim links to the official docs it relies on.

## Guides

| Guide | Purpose | Topics |
| --- | --- | --- |
| [Decide in the Gateway, Enforce in Snowflake](guide-app-access-governance/) | Move access enforcement out of app code and into Snowflake so every query runs as an identity Snowflake can govern and audit | External OAuth, workload identity, agent identity, row access policies, entitlements as code, App Runtime, Snowflake Postgres |

## Conventions

- All names and data in worked examples are synthetic.
- Each guide carries a **Last verified** date and expires at most 60 days later. An expired guide may describe outdated behavior.
- Run a guide's tests from its folder: `uv run --with pyyaml --with pytest pytest tests -q`

## Maintainer

[@sfc-gh-abennett](https://github.com/sfc-gh-abennett)

## License

[Apache License 2.0](LICENSE)
