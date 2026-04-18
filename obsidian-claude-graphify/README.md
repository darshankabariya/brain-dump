# Obsidian + Claude + graphify — Tutorial

A practical workflow for turning your codebases, papers, and notes into a persistent, navigable knowledge graph that Claude reads before answering — so you pay for understanding once, then ride the cache.

---

## One-time setup

### 1. Create a work vault

```bash
mkdir -p ~/vaults/work
```

Open Obsidian → "Open folder as vault" → pick `~/vaults/work`.

In **Settings → Core plugins**, make sure these are ON (they are by default):
- Graph view
- Canvas
- Backlinks
- Outgoing links

Install these **community plugins** (Settings → Community plugins → Browse):
- **Dataview** — lets the auto-generated `_COMMUNITY_*` notes run live queries
- **Templater** (optional) — for quick note templates

### 2. Per project: wire graphify to the vault

For each project you want to graph:

```bash
cd ~/work/logos-delivery
/graphify . --obsidian --obsidian-dir ~/vaults/work/logos-delivery
graphify hook install        # auto-rebuild on git commit (free for code changes)
graphify claude install      # adds graphify rules to this project's CLAUDE.md
```

Repeat for each project. Each gets its own subfolder inside the vault:

```
~/vaults/work/
  logos-delivery/
    _COMMUNITY_0.md
    _COMMUNITY_1.md
    <node-per-file>.md
    graph.canvas
  graphify/
    ...
  project-3/
    ...
```

### 3. Confirm it worked

Open Obsidian, hit **Ctrl/Cmd+G** for graph view. You should see clusters colored by community. Open `graph.canvas` for the structured layout.

---

## Daily workflow

### When you write code

1. Edit code normally.
2. `git commit` — hook rebuilds the graph (AST-only, zero tokens).
3. Obsidian notes update automatically. No manual step.

### When you add docs / papers / images (LLM needed)

```bash
/graphify <path> --update --obsidian --obsidian-dir ~/vaults/work/<project>
```

Only new/changed files hit the LLM. Cached files are free.

### When you drop a random link into your "raw" folder (Karpathy-style)

```bash
/graphify add https://arxiv.org/abs/2503.12345 --author "Some Author"
/graphify . --update --obsidian --obsidian-dir ~/vaults/work/research
```

This is how you build a long-lived research vault over months.

---

## Asking Claude questions efficiently

Once `graphify claude install` has run, your CLAUDE.md tells Claude: *"Before answering architecture questions, read GRAPH_REPORT.md."* You can now ask high-level questions **without Claude scanning files**.

### Good questions (use the graph)

- "What are the god nodes in logos-delivery?"
- "Trace how the auth flow connects to the payment flow."
- "What community does `SessionValidator` belong to, and what else is in that community?"
- "Compare the error handling patterns between project A and project B."
- "What are the surprising cross-community connections?"

### Anti-patterns (waste the graph)

- "Read every file in src/" — use the graph instead: "What's in the src/ community?"
- "Explain this one function" — Read tool is fine, no graph needed

### Using Obsidian alongside

While Claude answers, keep Obsidian open. When Claude says *"this connects to `AuthMiddleware`"*, click that note in Obsidian to see backlinks. The graph view highlights the node. It's a map + guide workflow:

- **Claude** = the guide (reads the graph, answers in plain language)
- **Obsidian** = the map (you navigate visually)

---

## Three organizing patterns — pick one

### Pattern A: One vault, one folder per project (recommended)

```
~/vaults/work/
  logos-delivery/
  graphify/
  project-3/
```

Each project has its own graph but they all live in one vault. Obsidian's graph view shows per-project clusters. Easy to switch context without switching vaults.

### Pattern B: Unified graph for related projects

If projects share concepts (e.g. microservices, research papers on the same topic):

```bash
mkdir ~/work/research-umbrella
cd ~/work/research-umbrella
ln -s ~/work/paper-notes .
ln -s ~/work/experiments .
ln -s ~/work/related-repos .
/graphify . --obsidian --obsidian-dir ~/vaults/research
```

One graph across all three — community detection finds connections you'd never ask about directly.

### Pattern C: Separate vaults per life-area

```
~/vaults/work/       (job projects)
~/vaults/research/   (papers + notes)
~/vaults/personal/   (journal, side projects)
```

Cleanest separation. Use this if you want each vault to have a different Obsidian theme/plugin set.

---

## Power moves

### 1. MCP server — let Claude query graphs live

```bash
/graphify ~/work/logos-delivery --mcp
```

Add to `~/Library/Application Support/Claude/claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "graphify-logos": {
      "command": "python3",
      "args": ["-m", "graphify.serve", "/Users/darshan/work/logos-delivery/graphify-out/graph.json"]
    }
  }
}
```

Now Claude Desktop can call `query_graph`, `get_neighbors`, `shortest_path` directly against the live graph.

### 2. Wiki for agent crawling

```bash
/graphify . --wiki
```

Generates `graphify-out/wiki/index.md` + one article per community. Perfect entry point for subagents in long sessions — they read `index.md` instead of your whole codebase.

### 3. Watch mode for agentic workflows

```bash
python3 -m graphify.watch ~/work/logos-delivery --debounce 3
```

Runs in the background. When agents write code, graph rebuilds automatically. Obsidian updates live.

---

## Backing up / moving graphs

All graph state lives in `<repo>/graphify-out/`. If you delete the repo, the context is **lost**. To preserve:

```bash
cp -r ~/work/logos-delivery/graphify-out ~/graphify-archives/logos-delivery/
```

To restore in a fresh clone:

```bash
cp -r ~/graphify-archives/logos-delivery/graphify-out ~/work/logos-delivery/
```

Queries (`query`, `path`, `explain`) only need `graph.json` — you can even query a graph without the original source files.

---

## Token economics cheat sheet

| Action | Cost |
|---|---|
| First `/graphify` on a repo | High (one-time) |
| `graphify update .` for code-only changes | Free (AST only) |
| Git hook rebuild | Free (AST only) |
| `graphify update` for new docs/papers/images | Low (only new files) |
| Claude answering via `GRAPH_REPORT.md` | Low (one file read) |
| Claude answering via raw file scanning | High (many files) |

**Rule of thumb:** pay once per repo, then ride the cache. The graph pays for itself after ~3–4 architecture questions.

---

## When NOT to use graphify

- Tiny repos (<20 files) — just read the files.
- One-off questions about a single function — direct file reads are faster.
- Pure refactoring where structure doesn't matter — just edit.

---

## Quick command reference

```bash
# First build
/graphify <path>                                   # full pipeline
/graphify <path> --obsidian --obsidian-dir <vault> # + Obsidian vault
/graphify <path> --mode deep                       # richer INFERRED edges
/graphify <path> --wiki                            # + agent-crawlable wiki

# Keeping fresh
/graphify <path> --update                          # incremental re-extraction
graphify hook install                              # auto-rebuild on git commit
python3 -m graphify.watch <path>                   # live-rebuild background watcher

# Querying
/graphify query "<question>"                       # BFS traversal
/graphify query "<question>" --dfs                 # follow a specific chain
/graphify path "ConceptA" "ConceptB"               # shortest path between nodes
/graphify explain "NodeName"                       # plain-language summary

# Corpus
/graphify add <url> --author "Name"                # fetch URL into ./raw

# Exports
/graphify <path> --svg                             # graph.svg for docs
/graphify <path> --graphml                         # for Gephi/yEd
/graphify <path> --neo4j                           # Cypher for Neo4j
/graphify <path> --mcp                             # start MCP server
```
