# news-image-20261123 — SUBMITTED (live) + v2 variant built 2026-11-24

Bounty: Sum up 23 November's world news in one image. $100, top 50 paid.
Entries close 2026-11-25T00:00:00Z (07:00 WIB). No entry fee.
Live submission: 01a205e5-3e12-7626-a43a-39786140c6f8 (commit 5e124de).
Blind round 2 ranked it 770/9643 — v2 variant below aims to move it up.

## Files (v2 variant, hero-led layout, built 2026-11-24 ~19:00 WIB)
- `entry.png` — 1024x1024, 124,447 bytes,
  sha256 855ce5d654cbdfdbc8e68dcdc553792ba0bbde1d173e7194bf7c030d6186739b
- `draw_poster.py` — poster generator, rewritten from scratch in-session
  2026-11-24 for the v2 resubmit (hero illustration of the Antalya
  walkout, centred lead, 3-column story grid — same verified facts)
- `main.py` — copies entry.png to /output/entry.png (deterministic; verified
  byte-identical across two runs)
- `LICENSE` — MIT (from the kit starter)

## Jury
- Prompt: ~/workspace/makefun/news-image-20261123-jury-prompt.txt
- Head-to-head v2-vs-live jury prompt:
  ~/workspace/makefun/news-image-20261123-jury-prompt-v2-vs-live.txt
- Resubmit ONLY on a clear jury GO for v2; if the jury is down (503),
  do NOT resubmit blind — this is a jury-taste bounty.

## Submit session — do in order
1. Get Hydrogen head-to-head verdict (v2 vs live). Submit v2 only on GO.
2. Bundle with the fresh kit + --system-prompt
   ~/workspace/system/system_prompt.md; kit check must be 0 failed;
   then submit from the kit dir. Save claim code + submission ID only in
   ~/workspace/makefun/submissions.md.
3. Quota (checked 2026-11-24 ~19:00 WIB): 1 entry made, 6 of 6 left today,
   hard limit 39 of 40, can submit now. This blind round's guaranteed
   entry was open until 2026-11-24T12:00:00Z.
