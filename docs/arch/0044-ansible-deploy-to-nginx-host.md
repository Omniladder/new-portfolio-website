# 0044 — Ansible deploys the site to an nginx host, built on the host

**Status:** Accepted.

## Context

The site is static files in `dist/`, but nothing put them on a server. The
content that matters most, `data.json` and `assets/`, is gitignored
([[0009-data-json-gitignored-with-tracked-example]],
[[0013-assets-gitignored-with-tracked-placeholders]]), so a host can't just
`git clone` the repo and build it.

## Decision

- Deployment lives in `infra/`, as an Ansible playbook (`deploy.yml`) with two
  roles. `nginx` installs nginx, writes one site config (`portfolio.conf.j2`)
  serving the web root, and disables the distro's default site. `portfolio`
  creates a `portfolio` system user, rsyncs the working tree to
  `/opt/portfolio/src`, installs `requirements.txt` into a venv, runs
  `generate.py`, and rsyncs `dist/` into `/var/www/portfolio`.
- The working tree is synced with rsync rather than cloned, so `data.json`
  and `assets/` reach the host. Paths `generate.py` doesn't read (`docs/`,
  `tests/`, `infra/`, `hidden/`, caches, `.git/`, `dist/`) are excluded.
- The site is built on the host, not the controller. Only a successful build
  is published, so a failing `generate.py` leaves the live site as it was.
- Published builds process images (no `--no-image-processing`, see
  [[0043-no-image-processing-flag]]). `portfolio_image_processing: false`
  (`deploy.sh --fast`) exists for throwaway deploys only.
- `infra/deploy.sh` is the entry point people run. It checks tools, the
  inventory, `data.json`, the `ansible.posix` collection, and SSH access
  before running the playbook, and says how to fix each failure.
- `infra/inventory.ini` is per-fork and gitignored; `inventory.example.ini`
  is the tracked starting point, the same pattern as `data.json`.
- Ansible is controller-only tooling, pinned in `infra/requirements.txt`,
  not in the site's `requirements.txt` / `requirements-dev.txt`.
- Target is Debian/Ubuntu (apt, `sites-enabled/`) with systemd, reachable
  over SSH with sudo: a VM, a bare server, or an LXC container. Docker
  containers without systemd aren't supported.

## Consequences

- One command (`infra/deploy.sh`) goes from a local edit of `data.json` to
  the live site.
- Each deploy rebuilds from scratch on the host, including the ~45 s image
  pass.
- HTTPS isn't set up. Add certbot or put the host behind a TLS-terminating
  proxy; a later ADR should record which.
- Agents must not run a real deploy unless asked; it's outward-facing.
  `deploy.sh --check` is the safe way to verify a change to `infra/`.

## Keywords

deploy, Ansible, infra, nginx, deploy.sh, inventory.ini, rsync, web root,
server, hosting, container, LXC, playbook
