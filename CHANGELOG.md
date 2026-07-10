# CHANGELOG

<!-- version list -->

## v1.1.0 (2026-07-10)

### Code Style

- Migrate to ruff, harden CI, and align to .github portfolio standard
  ([`dac0882`](https://github.com/danielvm-git/big-counter/commit/dac088253411362932568dfb842d0dab3acd6fb3))

### Continuous Integration

- Harden workflows with permissions, concurrency, and timeouts
  ([`549082a`](https://github.com/danielvm-git/big-counter/commit/549082a0d40c097845f228a8270eb450a020f9ba))

### Documentation

- Add bts toolchain to agent configs
  ([`3d7bd7f`](https://github.com/danielvm-git/big-counter/commit/3d7bd7f8fbd5522f878e8d323ecc928cb81c99c8))

- **agents**: Consolidate agent configs with CI + observability reference
  ([`78eb475`](https://github.com/danielvm-git/big-counter/commit/78eb475ef54912b1ddffd6ba08071a9402b8848e))

- **audit**: Re-audit plan — READY verdict
  ([`526f220`](https://github.com/danielvm-git/big-counter/commit/526f220ab2e5b84b45ba702b0bd56525b02febdc))

- **conventions**: Adopt solo-git workflow mode
  ([`29c5e27`](https://github.com/danielvm-git/big-counter/commit/29c5e27276612f2c7e257fb23673672956108a29))

- **specs**: Add OKF epics, hard gates, and integration plan
  ([`bcb4d35`](https://github.com/danielvm-git/big-counter/commit/bcb4d35b399820804d653aa1bcf3f60436dd2d9d))

- **specs**: Add rollout one-pager reference
  ([`96b92db`](https://github.com/danielvm-git/big-counter/commit/96b92db47a810114dcbb540fc78b1d44da8603db))

- **specs**: Sync full spec suite from parallel session
  ([`9038631`](https://github.com/danielvm-git/big-counter/commit/9038631a314f19d7a441ea6ca966bec627a8ee93))

- **state**: Begin BUILD phase — activate e01
  ([`26e7f03`](https://github.com/danielvm-git/big-counter/commit/26e7f030c57fc0f9dc638557e45653d3190c2602))

### Features

- **deploy**: Add BigBase MCP deployment entry point
  ([`d92e778`](https://github.com/danielvm-git/big-counter/commit/d92e778f0e29659a2bbeb97fb6d368ed542ce416))

- **provider**: Add DeepSeek as default LLM provider
  ([`6bcea3a`](https://github.com/danielvm-git/big-counter/commit/6bcea3ac4392d8f58ccedcddf3437bfb77bc63ff))

- **ruler**: Ship BCP Ruler as OKF bundle with graph visualization
  ([`681bde8`](https://github.com/danielvm-git/big-counter/commit/681bde86798f2d10b00882aa41f35fa510857bf9))

### Refactoring

- **mcp**: Extract create_mcp_server for BigBase deployment
  ([`0696674`](https://github.com/danielvm-git/big-counter/commit/0696674fee805d2321e1e390fb67729af12863c4))


## v1.0.1 (2026-07-02)

### Bug Fixes

- **ci**: Add black/isort/mypy to dev deps, pass GH_TOKEN for semantic-release
  ([`c24cb05`](https://github.com/danielvm-git/big-counter/commit/c24cb056b4cc0b40f1383c0957e0a5debc8059b1))


## v1.0.0 (2026-07-02)

- Initial Release
