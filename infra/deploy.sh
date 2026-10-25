#!/usr/bin/env bash
# Deploy the portfolio site to the host(s) in infra/inventory.ini.
#
# Checks everything the playbook needs up front, so a missing tool or file
# fails here with a fix, not halfway through a deploy.
# See docs/guides/deploying.md.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
INVENTORY="$SCRIPT_DIR/inventory.ini"

if [[ -t 1 && -z "${NO_COLOR:-}" ]]; then
    RED=$'\e[31m' GREEN=$'\e[32m' YELLOW=$'\e[33m' BOLD=$'\e[1m' RESET=$'\e[0m'
else
    RED="" GREEN="" YELLOW="" BOLD="" RESET=""
fi

info() { printf '%s==>%s %s\n' "$BOLD" "$RESET" "$*"; }
warn() { printf '%swarning:%s %s\n' "$YELLOW" "$RESET" "$*" >&2; }
die() {
    printf '%serror:%s %s\n' "$RED" "$RESET" "$1" >&2
    [[ $# -gt 1 ]] && printf '       %s\n' "${@:2}" >&2
    exit 1
}

usage() {
    cat <<EOF
Usage: infra/deploy.sh [options] [-- extra ansible-playbook args]

Syncs this repo (including data.json and assets/) to the host, builds the
site there with generate.py, and publishes it behind nginx.

Options:
  -i, --inventory FILE   inventory to deploy to (default: infra/inventory.ini)
  -l, --limit HOSTS      only deploy to these hosts/groups
  -c, --check            dry run: show what would change, change nothing
  -f, --fast             skip image processing (quick, not the final look)
  -v, --verbose          more Ansible output (repeat for more, e.g. -vvv)
  -h, --help             show this help

Examples:
  infra/deploy.sh
  infra/deploy.sh --check
  infra/deploy.sh --limit portfolio-host --fast
EOF
}

limit="" check=false fast=false verbosity="" extra=()

while [[ $# -gt 0 ]]; do
    case "$1" in
        -i | --inventory)
            [[ $# -ge 2 ]] || die "$1 needs a file path."
            INVENTORY="$(realpath -m "$2")"
            shift 2
            ;;
        -l | --limit)
            [[ $# -ge 2 ]] || die "$1 needs a host or group name."
            limit="$2"
            shift 2
            ;;
        -c | --check) check=true; shift ;;
        -f | --fast) fast=true; shift ;;
        -v | -vv | -vvv | -vvvv) verbosity+="${1#-}"; shift ;;
        --verbose) verbosity+="v"; shift ;;
        -h | --help) usage; exit 0 ;;
        --) shift; extra=("$@"); break ;;
        *) usage >&2; die "Unknown option: $1" ;;
    esac
done

# --- Preflight ---------------------------------------------------------------

info "Checking prerequisites"

for tool in ansible-playbook ansible-galaxy rsync ssh; do
    if ! command -v "$tool" >/dev/null 2>&1; then
        case "$tool" in
            ansible-*) die "$tool not found." \
                "Install Ansible: pip install -r infra/requirements.txt" ;;
            *) die "$tool not found." "Install it with your package manager." ;;
        esac
    fi
done

[[ -f "$INVENTORY" ]] || die "No inventory at ${INVENTORY#"$REPO_ROOT"/}." \
    "Create one from the example: cp infra/inventory.example.ini infra/inventory.ini" \
    "then set your host's address and SSH user in it."

[[ -f "$REPO_ROOT/data.json" ]] || die "data.json not found at the repo root." \
    "It's your site's content (gitignored). Create it first:" \
    "cp data.template.json data.json, then edit it."

if ! python3 -c 'import json, sys; json.load(open(sys.argv[1]))' "$REPO_ROOT/data.json" 2>/dev/null; then
    die "data.json isn't valid JSON." "Fix it, then check with: python3 generate.py --no-image-processing"
fi

if ! ansible-galaxy collection list ansible.posix 2>/dev/null | grep -q '^ansible\.posix '; then
    info "Installing the ansible.posix collection"
    ansible-galaxy collection install -r "$SCRIPT_DIR/requirements.yml" \
        || die "Couldn't install the ansible.posix collection." \
            "Try manually: ansible-galaxy collection install -r infra/requirements.yml"
fi

cd "$SCRIPT_DIR"

info "Checking SSH access to hosts"
ping_args=(-i "$INVENTORY" portfolio -m ansible.builtin.ping -o)
[[ -n "$limit" ]] && ping_args+=(--limit "$limit")
if ! ping_out="$(ansible "${ping_args[@]}" 2>&1)"; then
    printf '%s\n' "$ping_out" >&2
    die "Couldn't reach every host in the inventory." \
        "Check ansible_host / ansible_user in ${INVENTORY#"$REPO_ROOT"/}," \
        "and that 'ssh <user>@<host>' works without a password prompt."
fi

# --- Deploy ------------------------------------------------------------------

args=(-i "$INVENTORY" deploy.yml)
[[ -n "$limit" ]] && args+=(--limit "$limit")
[[ -n "$verbosity" ]] && args+=("-$verbosity")
$check && args+=(--check --diff)
if $fast; then
    warn "--fast: images won't be processed, so this isn't the final look."
    args+=(-e portfolio_image_processing=false)
fi
args+=("${extra[@]}")

if $check; then
    info "Dry run (nothing will change)"
else
    info "Deploying"
fi

start=$SECONDS
if ! ansible-playbook "${args[@]}"; then
    die "Deploy failed. See the failed task above." \
        "The live site is only replaced after a successful build, so it's unchanged" \
        "unless the failure came after 'Publish dist to web root'." \
        "Re-run with -vvv for more detail."
fi

if $check; then
    printf '%sDry run finished in %ds.%s\n' "$GREEN" $((SECONDS - start)) "$RESET"
else
    printf '%sDeployed in %ds.%s\n' "$GREEN" $((SECONDS - start)) "$RESET"
fi
