# Morning AI Digest

A free AI agent that runs every morning on GitHub Actions.

- **Free machine:** public repos get standard GitHub-hosted runners free — 4 CPUs, 16 GB RAM.
- **Free AI:** an open model (Qwen3 8B via Ollama) runs on that machine. No API key, no bill.
- **Delivered:** it posts the digest as an Issue, and GitHub emails it to you.

## Use it
1. Fork this repo (keep it public).
2. Actions tab → enable workflows.
3. Watch the repo (Watch → All activity) so new issues email you.
4. Change the time in `.github/workflows/digest.yml` (`cron`, UTC). Click **Run workflow** to test now.

Note: GitHub pauses scheduled workflows in public repos after 60 days with no repo activity — one commit turns it back on.
