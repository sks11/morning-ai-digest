"""Morning AI digest agent: gathers today's AI news, a local model writes the brief."""
import json, os, time, urllib.request, urllib.parse

MODEL = "qwen3:8b"


def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": "morning-ai-digest"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)


def hacker_news():
    since = int(time.time()) - 24 * 3600
    q = urllib.parse.urlencode({"query": "AI", "tags": "story",
                                "numericFilters": f"created_at_i>{since},points>50"})
    hits = get(f"https://hn.algolia.com/api/v1/search?{q}")["hits"][:10]
    return [f"{h['title']} ({h['points']} points) {h.get('url') or ''}" for h in hits]


def new_github_repos():
    week = time.strftime("%Y-%m-%d", time.gmtime(time.time() - 7 * 24 * 3600))
    q = urllib.parse.quote(f"topic:ai created:>{week}")
    items = get(f"https://api.github.com/search/repositories?q={q}&sort=stars&per_page=5")["items"]
    return [f"{r['full_name']} ({r['stargazers_count']} stars): {r['description']} {r['html_url']}" for r in items]


def ask_model(prompt):
    body = json.dumps({"model": MODEL, "prompt": prompt, "stream": False, "think": False}).encode()
    req = urllib.request.Request("http://localhost:11434/api/generate", body,
                                 {"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=1500) as r:
        return json.load(r)["response"].strip()


news, repos = hacker_news(), new_github_repos()
prompt = f"""You write a short morning AI briefing for a busy builder.
From the items below, pick the 5 that matter most today.
For each: a bold one-line headline, one plain-English sentence on why it matters (only say what the title tells you; never guess), and the link.
Then end with one line: "Try today:" plus one repo worth opening.
Markdown only. No intro.

HACKER NEWS (last 24h):
{chr(10).join(news)}

NEW AI REPOS ON GITHUB (this week):
{chr(10).join(repos)}
"""
started = time.time()
brief = ask_model(prompt)
print(brief)
cpus = os.cpu_count()
ram = round(os.sysconf("SC_PAGE_SIZE") * os.sysconf("SC_PHYS_PAGES") / 2**30)
print(f"\n---\n🖥️ **Free GitHub runner:** {cpus} CPUs · {ram} GB RAM  \n🤖 **Written by** {MODEL}, running on that machine in {time.time() - started:.0f}s  \n🔑 **API key:** none · 💸 **Bill:** $0")
