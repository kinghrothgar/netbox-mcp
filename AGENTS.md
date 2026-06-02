# Repo: netbox-mcp (fork)

Fork of `simonpainter/netbox-mcp` maintained at `kinghrothgar/netbox-mcp`.
FastMCP server exposing read-only NetBox API tools.

- Source lives in the `netbox_mcp/` package. Each NetBox app has its own
  module under `netbox_mcp/tools/` (`circuits.py`, `dcim.py`, `tenancy.py`,
  `ipam.py`, ...). Shared infra is `client.py`, `helpers.py`, `server.py`,
  `__main__.py`.
- `Dockerfile` is the container image build context for the homelab. Build
  with `docker build .` from this directory.
- Consumed by the `lab` repo (`tk/lib/netbox-mcp/`), which pins the
  published image tag. When bumping the package, rebuild the image, push a
  new tag, and bump `kinghrothgar/netbox-mcp:<tag>` in
  `lab/tk/lib/netbox-mcp/config.libsonnet`.
- Do not install host software. Toolchain comes from `PATH`.

## Commit Messages

Conventional Commits 1.0.0: `<type>[scope][!]: <description>` then optional
body and footers (<https://www.conventionalcommits.org/en/v1.0.0/>).

Accepted types: `feat`, `fix`, `docs`, `chore`, `refactor`, `build`, `ci`,
`perf`, `test`, `revert`. Lowercase. Do not invent new types.

Mapping for this repo:

- `feat` / `fix` — changes to MCP tool behaviour or coverage.
- `chore` — dependency pin bumps, formatting sweeps.
- `build` — `Dockerfile` changes.
- `refactor` — package restructuring with no behaviour change.
- `docs` — `README.md`, `AGENTS.md`, `CONTRIBUTING.md`,
  `.github/copilot-instructions.md`.

Scope is required in practice. Common scopes: a NetBox app name when
changes are confined to one (`circuits`, `dcim`, `tenancy`, `ipam`,
`virtualization`, ...); `app` when the change spans multiple tool
modules or touches shared infra (`client.py`, `helpers.py`, `server.py`,
`__main__.py`); `dockerfile`, `docs`, or `repo` (for repo-wide config
like `.gitignore`).

Description: imperative mood, lowercase first letter, no trailing period,
≤72 chars. Be specific.

Be concise. Most commits need only the subject line. Add a body only when
the *why* isn't obvious from the diff; 1–3 short sentences or a few terse
bullets, wrapped at ~72 columns. Don't re-list the diff.

## Git Operations

Use git non-destructively. May create new commits. Must not push,
force-push, rewrite history, or run anything that can discard local work
without explicit human authorisation.

Forbidden without explicit human authorisation: `git push` (any form),
`git commit --amend` (except to fix the agent's own just-made commit before
push), `git rebase`, `git reset --hard`, `git restore`/`git checkout --`
that discards changes, `git clean`, `git branch -D`/`--force`,
`git tag -d`/`--force`, `git filter-branch`/`filter-repo`,
`git update-ref`, `git reflog expire`/`delete`, `git stash drop`/`clear`,
any other `--force`/`-f` invocation.
