#!/usr/bin/env python3
"""Check all external URLs in resources.json and report broken/redirected ones."""

import json
import urllib.request
import urllib.error
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed

TIMEOUT = 10
HEADERS = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"}


def check_url(item):
    rid, url = item
    try:
        req = urllib.request.Request(url, headers=HEADERS, method="HEAD")
        with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
            final_url = resp.url
            status = resp.status
            redirected = final_url.rstrip("/") != url.rstrip("/")
            return rid, url, status, final_url if redirected else None, None
    except urllib.error.HTTPError as e:
        # Some servers reject HEAD — try GET
        if e.code == 405:
            try:
                req = urllib.request.Request(url, headers=HEADERS)
                with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
                    return rid, url, resp.status, None, None
            except Exception as e2:
                return rid, url, None, None, str(e2)
        # 403 = bot-blocking (Cloudflare etc) — treat as warning, not broken
        if e.code == 403:
            return rid, url, 403, f"(bot-blocked, URL likely valid)", None
        return rid, url, e.code, None, f"HTTP {e.code}"
    except Exception as e:
        return rid, url, None, None, str(e)


def main():
    with open("resources.json") as f:
        resources = json.load(f)["resources"]

    urls = [(r["id"], r["url"]) for r in resources if r.get("url")]

    print(f"Checking {len(urls)} URLs...\n")

    ok = []
    broken = []
    redirected = []

    with ThreadPoolExecutor(max_workers=8) as pool:
        futures = {pool.submit(check_url, item): item for item in urls}
        for future in as_completed(futures):
            rid, url, status, new_url, error = future.result()
            if error:
                broken.append((rid, url, error))
            elif new_url:
                redirected.append((rid, url, new_url, status))
            else:
                ok.append((rid, url, status))

    # Sort by ID for consistent output
    ok.sort(); broken.sort(); redirected.sort()

    print(f"✅  OK ({len(ok)})")
    for rid, url, status in ok:
        print(f"   {rid}  {status}  {url}")

    if redirected:
        print(f"\n⚠️   Redirected ({len(redirected)}) — consider updating the URL")
        for rid, url, new_url, status in redirected:
            print(f"   {rid}  {status}  {url}")
            print(f"         → {new_url}")

    if broken:
        print(f"\n❌  Broken ({len(broken)})")
        for rid, url, error in broken:
            print(f"   {rid}  {error}")
            print(f"         {url}")

    if broken:
        sys.exit(1)


if __name__ == "__main__":
    main()
