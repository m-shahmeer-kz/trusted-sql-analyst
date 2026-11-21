"""Build docs/index.html from results/*.json so every number on the page is a measured one.

Run:  python docs/build.py            (AGENSI_URL points to the listing)
"""
import html
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEV = json.loads((ROOT / "results" / "dev_results.json").read_text())
BLIND = json.loads((ROOT / "results" / "holdout2_blind_results.json").read_text())
AB = json.loads((ROOT / "results" / "ab_test.json").read_text())
CHECK = (ROOT / "examples" / "check-fanout-revenue-by-genre.md").read_text()
AGENSI_URL = "https://www.agensi.io/skills/trusted-sql-analyst-text-to-sql-that-double-checks"
PRICE = "$9.99"
GH = "https://github.com/m-shahmeer-kz/trusted-sql-analyst"
e = html.escape

ds, bs = DEV["summary"], BLIND["summary"]
mech_g = bs["genuine_catches"]["sql-mechanics"].replace("/", " / ")
mean_g = bs["genuine_catches"]["business-meaning"].replace("/", " / ")
dev_case = {c["id"]: c for c in DEV["cases"]}["C01"]
wrong_rev = dev_case["wrong_preview"][0][1]
right_rev = dev_case["right_preview"][0][1]

buy = (f'<a class="btn solid" href="{AGENSI_URL}" target="_blank" rel="noopener">Get it on Agensi · {PRICE} ↗</a>'
       if AGENSI_URL else '<span class="btn solid off">Coming soon on Agensi</span>')

blind_rows = ""
for c in BLIND["cases"]:
    mark = "✅ caught" if c.get("genuine_catch") else "— missed"
    blind_rows += (f"<tr><td>{e(c['id'])}</td><td>{e(c['category'])}</td><td>{e(c['mistake'])}</td>"
                   f"<td>{mark}</td></tr>")

GROUPS = [
    ("Joins", "Fan-out double counting (SUM/AVG/COUNT after a one-to-many join, with the measured factor) · rows dropped by INNER JOIN · join without a condition · LEFT JOIN undone by WHERE · COUNT(*) after LEFT JOIN"),
    ("NULLs", "NOT IN with a NULL in the subquery · = NULL · negative filters (<>, NOT LIKE) that drop NULL rows · AVG skipping NULLs"),
    ("Text & values", "'usa' vs 'USA' vs 'USA ' · values that do not exist (closest matches shown) · LIKE that also matches other categories · list columns ('a,b,c') matched with =" ),
    ("Dates", "BETWEEN / <= that drops the last day when values have a time · = on a timestamp · dates stored as non-ISO text"),
    ("Grouping & maths", "Columns neither grouped nor aggregated · grouping by a name that merges different people · integer division · AND/OR without brackets · LIMIT without ORDER BY"),
    ("Result checks", "Empty result: which filter emptied it · duplicate groups · groups that do not add up · NULL groups · impossible percentages"),
]
groups_html = "".join(f'<div class="card"><h3>{a}</h3><p>{b}</p></div>' for a, b in GROUPS)

page = f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Trusted SQL Analyst · is your SQL answer right?</title>
<meta name="description" content="AI-agent skill that turns plain-English questions into SQL, then double-checks the answer: database map, glossary, 25 automatic trap checks, a second-query cross-check and a plain-English answer with its assumptions.">
<meta property="og:type" content="website">
<meta property="og:title" content="Trusted SQL Analyst · is your SQL answer right?">
<meta property="og:description" content="Plain-English questions to SQL answers that are double-checked. Blind-tested on three real databases.">
<meta property="og:url" content="https://m-shahmeer-kz.github.io/trusted-sql-analyst/">
<meta property="og:image" content="https://m-shahmeer-kz.github.io/trusted-sql-analyst/assets/og.png">
<meta property="og:image:width" content="1200"><meta property="og:image:height" content="627">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="assets/logo.png">
<style>
:root{{--bg:#060607;--card:#111113;--line:#26262b;--text:#f2f2f3;--mute:#9a9aa2;--ok:#7ee2a8;--bad:#ff8a8a}}
*{{box-sizing:border-box}}html{{-webkit-text-size-adjust:100%}}
body{{margin:0;background:var(--bg);color:var(--text);font:15px/1.6 system-ui,-apple-system,"Segoe UI",Roboto,sans-serif}}
.wrap{{max-width:1040px;margin:0 auto;padding:40px 20px 70px}}
h1{{font-size:clamp(32px,5.4vw,52px);line-height:1.04;margin:0 0 12px;letter-spacing:-.025em}}
h2{{font-size:clamp(20px,3vw,27px);margin:48px 0 10px;letter-spacing:-.01em}}
p,li{{color:#d6d6da}}.sub{{color:var(--mute);max-width:800px}}a{{color:var(--text)}}
code{{font:13px ui-monospace,SFMono-Regular,Menlo,monospace;background:#17171a;border:1px solid var(--line);border-radius:5px;padding:1px 5px;overflow-wrap:anywhere}}
pre{{background:#0d0d0f;border:1px solid var(--line);border-radius:12px;padding:14px;overflow:auto;max-height:430px;white-space:pre-wrap}}
pre code{{background:none;border:0;padding:0}}
.grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:12px}}
.card{{background:var(--card);border:1px solid var(--line);border-radius:16px;padding:16px 18px}}
.card h3{{margin:0 0 6px;font-size:16px}}.card p{{margin:0;font-size:14px}}
.stat b{{display:block;font-size:30px;line-height:1.1}}.stat span{{color:var(--mute);font-size:13px}}
.vs{{display:grid;grid-template-columns:1fr 1fr;gap:12px}}@media(max-width:640px){{.vs{{grid-template-columns:1fr}}}}
.vs .card b{{font-size:42px;display:block;line-height:1.1}}.bad{{color:var(--bad)}}.ok{{color:var(--ok)}}
.tbl{{overflow-x:auto}}table{{border-collapse:collapse;width:100%;font-size:14px;margin:10px 0}}
th,td{{border-bottom:1px solid var(--line);padding:8px;text-align:left;vertical-align:top}}th{{color:var(--mute);font-weight:500}}
.btns{{display:flex;flex-wrap:wrap;gap:8px;margin:16px 0}}
.btn{{display:inline-block;padding:10px 18px;border:1px solid var(--line);border-radius:999px;text-decoration:none;font-size:14px}}
.btn.solid{{background:var(--text);color:#000;border-color:var(--text);font-weight:600}}.btn.off{{opacity:.75;cursor:default}}
.steps{{counter-reset:s;list-style:none;padding:0}}.steps li{{counter-increment:s;margin:8px 0;padding-left:34px;position:relative}}
.steps li:before{{content:counter(s);position:absolute;left:0;top:1px;width:24px;height:24px;border-radius:50%;border:1px solid var(--line);text-align:center;font-size:13px;line-height:23px;color:var(--mute)}}
details summary{{cursor:pointer;color:var(--mute)}}
</style></head>
<body><div class="wrap">
<p class="sub" style="letter-spacing:.12em;text-transform:uppercase;font-size:12px">AI-agent skill · Claude Code · Codex · Cursor · Gemini CLI</p>
<h1>Is your SQL answer right?</h1>
<p class="sub">Trusted SQL Analyst turns plain-English questions into SQL, then double-checks the answer like a careful senior analyst.
It maps the database first, keeps a glossary of what columns and business terms mean, runs 25 automatic checks for silent
mistakes, proves the number with a second query written a different way, and explains the result in plain English with its
assumptions. Read-only and local: SQLite, DuckDB, CSV/Parquet/Excel folders, Postgres and MySQL.</p>
<div class="btns">{buy}<a class="btn" href="#demo">See the demo</a><a class="btn" href="#tested">Blind test results</a><a class="btn" href="{GH}">GitHub ↗</a></div>

<h2 id="demo">The query ran fine. The number was 9× too high.</h2>
<p class="sub">"Revenue by genre" on the Chinook music-store database. Summing the invoice total after joining to invoice lines repeats every invoice once per line - a classic AI-written SQL mistake that returns a confident number.</p>
<div class="vs">
 <div class="card"><span class="sub">Rock revenue, plausible-looking SQL</span><b class="bad">{wrong_rev:,.2f}</b>
  <p>The check: <b style="display:inline;font-size:15px">FAIL</b> - "each Invoice row appears 5.44 times on average after the joins (2,240 joined rows for 412 invoices)".</p></div>
 <div class="card"><span class="sub">Rock revenue, corrected</span><b class="ok">{right_rev:,.2f}</b>
  <p>Summed from invoice lines at their own grain. Check: PASS; the 24 genres add up to the true total 2,328.60; a second query by another route agrees.</p></div>
</div>
<p>The raw check output for the wrong query:</p>
<pre><code>{e(CHECK)}</code></pre>

<h2 id="tested">Tested honestly</h2>
<p class="sub">A separate AI agent that had never seen the tool wrote 24 new realistic wrong queries (with the correct query for each) on three real databases.
The checker was frozen and run once.</p>
<div class="grid">
 <div class="card stat"><b>{mech_g}</b><span>SQL-mechanics mistakes caught in the blind test (joins, NULLs, dates, text, grouping, division)</span></div>
 <div class="card stat"><b>{mean_g}</b><span>business-meaning mistakes (wrong column or definition) - not detectable from SQL; the skill handles these with the glossary and the second-query step</span></div>
 <div class="card stat"><b>{bs['right_false_alarms']} / {bs['cases']}</b><span>correct queries that got a REVIEW note</span></div>
 <div class="card stat"><b>{ds['wrong_caught']} / {ds['cases']}</b><span>wrong queries flagged in the 32 development cases (0 correct queries flagged)</span></div>
</div>
<details><summary>All 24 blind cases</summary>
<div class="tbl"><table><tr><th>Case</th><th>Type</th><th>Mistake (written by the test agent)</th><th>Result</th></tr>{blind_rows}</table></div></details>
<p class="sub">With and without the skill: two fresh agents answered the same 12 business questions; both got {AB['with_skill_correct']} / {AB['questions']}.
A strong model working carefully does not need the skill to be accurate on questions like these - the measured value is catching mistakes
before you trust a number, and answers that state their assumptions and checks. Databases: Chinook, Northwind (609,283 order lines) and Sakila.</p>

<h2>What it checks</h2>
<div class="grid">{groups_html}</div>

<h2>How your agent uses it</h2>
<ol class="steps">
<li>Maps the database once: tables, keys, measured joins (orphans, NULL keys, one-to-many), messy values, how dates are stored.</li>
<li>Pins down the question with a glossary: metric definition, grain, time window, what "active" or "revenue" means here.</li>
<li>Writes the SQL with the trap list in mind.</li>
<li>Runs the checks on the query and its real result - with numbers, not guesses.</li>
<li>Proves the number with a second query by a different route and compares them.</li>
<li>Answers in plain English: the number, how it was calculated, the assumptions, the checks done, and the SQL.</li>
</ol>

<h2>Good to know</h2>
<div class="grid">
 <div class="card"><h3>Read-only</h3><p>Refuses INSERT/UPDATE/DELETE/DDL, file-reading functions and multiple statements; every query has a timeout.</p></div>
 <div class="card"><h3>Review other SQL</h3><p>Paste a query from a colleague or another AI: you get the problems, the measured impact and a fixed query.</p></div>
 <div class="card"><h3>Small install</h3><p><code>pip install sqlglot</code> (+ duckdb for files, SQLAlchemy for servers). Tested on SQLite and DuckDB.</p></div>
 <div class="card"><h3>Honest limits</h3><p>It cannot know your business meaning; a PASS is never proof the question was understood. That is why the glossary and the second query exist.</p></div>
</div>

<div class="btns" style="margin-top:34px">{buy}<a class="btn" href="{GH}">GitHub ↗</a></div>
<p class="sub">Made by <a href="https://m-shahmeer-kz.github.io/">Muhammad Shahmeer</a> · Data Science MSc, University of Naples Federico II · © 2026, all rights reserved.</p>
</div></body></html>
"""
(ROOT / "docs" / "index.html").write_text(page)
print("wrote docs/index.html", len(page))
