# Prompt Log

Key prompts used during the agent/LLM investigation of HTTPie Bug #3.

---

## 1. Graph-Guided Agent — Navigator Stage

**Prompt given to the Navigator node:**

```
You are investigating a bug in the HTTPie codebase.
Bug description: AttributeError in Session.update_headers when a header value is None.
Relevant context:
- obsidian/index.md (system structure overview)
- obsidian/hot.md (bug investigation focus)

Based on the system map and bug description, which modules are most likely
involved in this bug? Return a list of component names to investigate.
```

**Output:** `["httpie.sessions", "httpie.downloads", "httpie.client"]`

---

## 2. Graph-Guided Agent — SuspectRanker Stage

**Prompt given to the SuspectRanker node:**

```
Given the following candidate modules, rank them by likelihood of containing
the root cause of the bug, based on graph centrality and proximity to the
failing test (test_download_in_session):

Candidates: httpie.sessions, httpie.downloads, httpie.client

Return the candidates in descending order of suspicion.
```

**Output:** `["httpie.sessions", "httpie.downloads", "httpie.client"]`

---

## 3. Graph-Guided Agent — CodeReader Stage

**Prompt for each component read:**

```
Read the component page for <component_name> from the Obsidian vault.
Summarize the key functions and relationships relevant to the bug.
```

Components read: `httpie.sessions`, `httpie.downloads`, `httpie.client`

---

## 4. Graph-Guided Agent — Explainer Stage

**Prompt given to the Explainer node:**

```
Based on the components investigated:
- httpie.sessions: Session.update_headers calls value.decode('utf8')
- httpie.downloads: sets Accept-Encoding=None in request headers
- httpie.client: passes headers from downloads to sessions via get_response()

Produce a root-cause explanation and a fix proposal.
```

**Output:**
- Root cause: `Session.update_headers` calls `value.decode('utf8')` without
  checking for `None`; triggered when `downloads.py` sets `Accept-Encoding=None`.
- Fix proposal: `if value is None: continue`

---

## 5. Naive Baseline Agent

**Prompt given at each iteration:**

```
You are investigating a bug: AttributeError in httpie when using --session and --download.
Here is the content of <file.py>:

<raw file content>

Do you have enough information to identify the root cause?
If yes, explain it. If not, say "need more files".
```

Files read (in order): `__init__.py`, `__main__.py`, `cli.py`, `client.py`, `compat.py`

Result: `root_cause_found = False` after 5 iterations (sessions.py not reached).

---

## 6. Grphify Graph Analysis

**Prompt used to interpret the graph report:**

```
Given the Grphify hub-node report (artifacts/GRAPH_REPORT.md), identify:
1. The God Node (highest total degree)
2. The key execution path for Bug #3
3. Any anomalies (mixed responsibilities, orphan modules)
```

**Findings:** God Node = `core.py::main` (21 outgoing edges); Bug #3 path =
`downloads.py → client.py → sessions.py`; anomaly = `Session` class mixing
persistence + header-decode + auth + cookie concerns.
