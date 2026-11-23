# news-image-20261123 — BUILD ONLY (not submitted)

Bounty: Sum up 23 November's world news in one image. $100, top 50 paid.
Entries close 2026-11-25T00:00:00Z (07:00 WIB). No entry fee. 0 submissions
at build time (checked 2026-11-23 ~02:42 WIB).

## Files
- `entry.png` — 1024x1024, 134,597 bytes,
  sha256 2b8a5e763fe794ad45d27b22f46be2c6487dd0f0039b4dd06249dbd464a714a5
- `draw_poster.py` — poster generator, rewritten from scratch in-session
  2026-11-23 ~07:48 WIB for kit authorship (thinking_reproduces)
- `main.py` — copies entry.png to /output/entry.png (deterministic; verified
  byte-identical across two runs)
- `LICENSE` — MIT (from the kit starter)

## Jury
- Prompt: ~/workspace/makefun/news-image-20261123-jury-prompt.txt
- Hydrogen quota resets ~15:30 WIB 2026-11-23. Get the verdict first, then submit.

## Submit session — do in order
1. Get Hydrogen verdict with the jury prompt above. Submit only on GO.
2. Competition opens 2026-11-23T00:00:00Z (07:00 WIB) — submit only after that.
3. WARNING: the build session predates the opening, and the kit check says
   "a session recorded before the opening is rejected by thinking_in_window".
   Decide how to handle the transcript window (e.g. re-run/verify the build
   in a post-opening session so the bundled transcript is in-window) before
   bundling. Do NOT bundle a pre-opening session blindly.
4. Create a fresh GitHub repo AFTER opening (repo_created_after_open), commit
   this work on top of a clean `makefun init` root (drand anchor), add
   .makefun/owner.json with wallet HtPfd3ke1Uq8Dbk2oyW3RmQjmz3PhBVaudQQXkCf8qVz.
5. Bundle with the fresh kit (~/workspace/makefun/news-image-20261123-kit-v36/)
   + --system-prompt ~/workspace/system/system_prompt.md; kit check must be
   0 failed; then submit. Save claim code + submission ID only in
   ~/workspace/makefun/submissions.md.
