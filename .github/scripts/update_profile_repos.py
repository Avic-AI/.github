#!/usr/bin/env python3
"""Rewrite the public-repo list in profile/README.md.

Only repositories GitHub reports as public are listed: the API is asked for
type=public and each result is checked again for visibility == "public", so a
private repo name can never reach the landing page. Forks and this .github
repo are left out. Text outside the public-repos markers is not touched.

Env: GH_TOKEN (any token; public data only), ORG (defaults to Avic-AI).
"""
import json, os, sys, urllib.request
from pathlib import Path

ORG = os.environ.get("ORG", "Avic-AI")
README = Path(__file__).resolve().parents[2] / "profile" / "README.md"
START, END = "<!-- public-repos:start -->", "<!-- public-repos:end -->"


def public_repos():
    repos, page = [], 1
    while True:
        req = urllib.request.Request(
            f"https://api.github.com/orgs/{ORG}/repos?type=public&per_page=100&page={page}",
            headers={"Accept": "application/vnd.github+json",
                     **({"Authorization": f"Bearer {os.environ['GH_TOKEN']}"} if os.environ.get("GH_TOKEN") else {})})
        batch = json.load(urllib.request.urlopen(req))
        repos += batch
        if len(batch) < 100:
            return repos
        page += 1


def cell(text):
    return (text or "").replace("|", "\\|").replace("\n", " ").strip()


def render(repos):
    shown = sorted((r for r in repos
                    if r.get("visibility") == "public" and not r.get("private")
                    and not r.get("fork") and r["name"] != ".github"),
                   key=lambda r: r["name"].lower())
    if not shown:
        return "_No public repositories yet._"
    rows = ["| Repository | Description | Language |", "|---|---|---|"]
    for r in shown:
        name = f'[**{r["name"]}**]({r["html_url"]})' + (" _(archived)_" if r.get("archived") else "")
        rows.append(f'| {name} | {cell(r.get("description"))} | {cell(r.get("language")) or "—"} |')
    return "\n".join(rows)


def main():
    text = README.read_text()
    if text.count(START) != 1 or text.count(END) != 1:
        sys.exit(f"{README} must contain exactly one {START} and one {END}")
    head, rest = text.split(START)
    _, tail = rest.split(END)
    new = f"{head}{START}\n{render(public_repos())}\n{END}{tail}"
    if new != text:
        README.write_text(new)
        print("profile/README.md updated")
    else:
        print("profile/README.md unchanged")


if __name__ == "__main__":
    main()
