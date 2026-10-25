# Deploying your site

`infra/deploy.sh` puts your site on a server behind nginx. In one run it:

1. Installs nginx, Python, and rsync on the server (first run only).
2. Copies this repo to the server, including your `data.json` and `assets/`.
3. Builds the site there with `generate.py`, images fully processed.
4. Publishes the result to `/var/www/portfolio`, which nginx serves.

If the build fails, the live site stays as it was.

## What you need

- **A server**: any Debian or Ubuntu machine, VM, or LXC container with
  systemd. You need SSH access as a user that can `sudo`, ideally with an SSH
  key, so there's no password prompt. Docker containers usually don't run
  systemd, so they won't work.
- **On your computer**: Python 3, `rsync`, and `ssh`.
- A working `data.json`. Check it first with
  `python3 generate.py --no-image-processing`.

## One-time setup

From the repo root, with your venv active:

```bash
pip install -r infra/requirements.txt               # installs Ansible
cp infra/inventory.example.ini infra/inventory.ini  # your server's details
```

Edit `infra/inventory.ini`:

```ini
[portfolio]
portfolio-host ansible_host=203.0.113.5 ansible_user=deploy

[portfolio:vars]
portfolio_server_name=example.com www.example.com
```

- `ansible_host`: the server's IP or hostname.
- `ansible_user`: the SSH user. Leave it out to use your local username.
- `portfolio_server_name`: your domain(s). `_` (the default) answers for any
  name, which is fine if this server only hosts this site.

`inventory.ini` is gitignored, so your server details stay out of the repo.
Keep the group name `[portfolio]`; the playbook and script look for it.

Check that `ssh deploy@203.0.113.5` (with your own values) logs in without a
password prompt before deploying.

## Deploying

```bash
infra/deploy.sh
```

Run it from anywhere; it finds the repo itself. The first run takes a few
minutes for package installs. After that, most of the time goes to image
processing, about a minute.

Options:

| Option | What it does |
|---|---|
| `-c`, `--check` | Dry run: shows what would change and changes nothing. The build step is skipped in a dry run. |
| `-f`, `--fast` | Skips image processing. Faster, but images lose the retro look, so redeploy without it before showing anyone. |
| `-l`, `--limit HOST` | Deploys to one host from the inventory only. |
| `-i`, `--inventory FILE` | Uses a different inventory file. |
| `-v` (up to `-vvvv`) | More detail from Ansible, for debugging. |
| `-- ARGS` | Passes anything after `--` straight to `ansible-playbook`. |

To change content later, edit `data.json` or `assets/` locally and run
`infra/deploy.sh` again.

## Settings

Defaults are in `infra/group_vars/all.yml`. Override any of them per host in
`inventory.ini`, under `[portfolio:vars]` or on the host's line.

| Variable | Default | Meaning |
|---|---|---|
| `portfolio_server_name` | `_` | Domain(s) nginx answers for. |
| `portfolio_listen_port` | `80` | Port nginx listens on. |
| `portfolio_web_root` | `/var/www/portfolio` | Where the built site is served from. |
| `portfolio_home` | `/opt/portfolio` | Where the source copy and venv live on the server. |
| `portfolio_image_processing` | `true` | Set `false` to skip image processing (same as `--fast`). |

## HTTPS

The deploy only sets up plain HTTP on port 80. For HTTPS, either run
[certbot](https://certbot.eff.org/) with its nginx plugin on the server once
the site is up, or put the server behind a proxy that handles TLS
(Cloudflare, Caddy, a reverse proxy on the container's host).

## When something goes wrong

The script checks the common problems before deploying and prints a fix for
each one:

| Message | Fix |
|---|---|
| `ansible-playbook not found` | `pip install -r infra/requirements.txt`, with your venv active. |
| `No inventory at infra/inventory.ini` | Copy `infra/inventory.example.ini` to `infra/inventory.ini` and fill it in. |
| `data.json not found` / `isn't valid JSON` | Create or fix `data.json`, then check it with `python3 generate.py --no-image-processing`. |
| `Couldn't reach every host` | Check `ansible_host` and `ansible_user`, and that plain `ssh` to the server works without a password. |

If the playbook itself fails, the failed task is printed above the error:

- **Sync repo to host**: rsync must be installed locally. The server gets it on
  the first run.
- **Install Python requirements**: the server can't reach PyPI, or has no
  prebuilt wheel for Pillow on its CPU/OS. Try a newer Debian/Ubuntu release.
- **Build site**: `generate.py` failed on the server. The error is in the
  output, usually a `data.json` problem. Reproduce it locally with
  `python3 generate.py`.
- **Test nginx config**: the generated nginx config is invalid, usually a bad
  `portfolio_server_name`. The new files are already published, but nginx isn't
  restarted, so it keeps serving the previous config until this is fixed and
  you deploy again.
- **`Missing sudo password`**: your SSH user needs a password for sudo. Add
  `-- --ask-become-pass` to the command, or allow passwordless sudo.

Re-run with `-vvv` for the full details of any failure.
