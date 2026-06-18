# Original Extensions

## Extension A – Knowledge-Driven Investigation

Instead of reading source files directly, the graph-guided workflow first navigates through the Obsidian knowledge vault (`index.md`, `hot.md`, and component pages). This significantly reduces context size and focuses the investigation.

## Extension B – Centrality-Based Suspect Ranking

The project includes a suspect-ranking stage that prioritizes investigation targets according to graph connectivity and architectural relevance. Highly connected nodes are considered more likely to participate in bug propagation paths.

## Extension C – Multi-Stage Investigation Pipeline

The workflow is divided into specialized stages:

* Navigator
* Suspect Ranker
* Code Reader
* Explainer

This separation reduces unnecessary code reads and keeps the investigation focused.

## Extension D – Impact Report

We analyzed the potential impact of future modifications to `Session.update_headers()`.

Potential consequences include:

* Session persistence failures
* Incorrect header storage
* Download subsystem regressions
* Reintroduction of the original bug

## Extension E – Additional Quality Metric

In addition to tokens, files read, and iterations, we measured root-cause success. The graph-guided workflow successfully identified the root cause, while the naive workflow failed to do so.
