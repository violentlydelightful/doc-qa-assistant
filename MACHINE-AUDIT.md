# Machine Self-Sufficiency Audit (2026-06-16)

## Self-sufficient on this box? -> With caveats

## Issues found
- **Git:** OK. Repo with `origin` (github.com/violentlydelightful/doc-qa-assistant). On `main`, clean, in sync with `origin/main`. Backed up.
- **Mac dependency:** None. Standard Flask app; no `/Users/` paths, no launchd/osascript. Listens on localhost:5001.
- **Secrets/auth:** No secret files in repo. `config.py` loads via `python-dotenv` `load_dotenv()` from a local `.env` (`OPENAI_API_KEY`, `SECRET_KEY`). This project does NOT use 1Password. App degrades gracefully: without `OPENAI_API_KEY` it runs in keyword-matching "demo mode" (per `run.py`). No Mac-only secret file dependency.
- **Runnability:** `requirements.txt` present but no `venv`/`.venv` (MISSING). Needs a venv + `pip install -r requirements.txt`. `uploads/` is gitignored (kept via .gitkeep pattern).

## Fixed this pass
- None needed.

## Outstanding (needs Brad)
- Create a venv and `pip install -r requirements.txt`.
- Optionally create `.env` with `OPENAI_API_KEY` (and `SECRET_KEY`) for full AI mode; otherwise it runs in demo mode. Key is not stored in the repo — supply from a provider dashboard / password manager.
