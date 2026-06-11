# Graphify Agent — EX04: Reverse Engineering, Debugging and Token-Efficient Agentic AI

## Chosen Repository & Bug Justification

We chose **[HTTPie](https://github.com/jakubroztocil/httpie)** via its **BugsInPy** entry (`projects/httpie`) as our base repository. HTTPie is a real-world, multi-module command-line HTTP client (CLI argument parsing, HTTP client/session handling, downloads, output formatting, and plugins) — large and structured enough to produce a meaningful Grphify graph, architectural block diagram, and OOP schema, while still being approachable for two people. Within this codebase, we picked **Bug #3**: in `httpie/sessions.py`, `Session.remove_cookies`/header-update logic calls `value.decode('utf8')` on header values without checking for `None`, causing an `AttributeError` whenever a session has explicitly unset headers (covered by `tests/test_sessions.py::TestSession::test_download_in_session`). This bug is small and localized — a one-line guard fix — yet it sits inside the session/config layer, which connects to several other modules (CLI, client, downloads), making it a good focal point for `hot.md` and the graph-guided agent. BugsInPy provides a reproducible buggy/fixed commit pair and a ready-to-run failing test, which we use for the agent investigation, the fix verification, and the token-efficiency comparison (Tasks C–E).

## Problem / Bug Description

*(To be completed after investigation — see `obsidian/hot.md`.)*

## Research Questions

*(To be completed — see Phase 2/3 findings.)*

## Architecture Overview

*(To be completed from Grphify/reverse-engineering output.)*

## Agent Workflow

*(To be completed — CrewAI/LangGraph workflow description.)*

## Grphify & Obsidian Usage

*(To be completed.)*

## Reverse Engineering Process

*(To be completed.)*

## Bug Description, Root Cause & Fix

*(To be completed.)*

## Before / After Comparison

*(To be completed.)*

## Token Efficiency Comparison

*(To be completed — see `reports/token_comparison.md`.)*

## Original Extensions

*(To be completed.)*

## Run Instructions

*(To be completed.)*
