# Nest Kenya — Instagram Posting System

Queues and auto-publishes Instagram posts for Nest Kenya via the Instagram
Graph API, with on-brand captions generated straight from the Nest Kenya
project portfolio.

**Not connected to Instagram yet?** Start with [SETUP.md](SETUP.md) — it
walks through the one-time Meta/Instagram Business account setup this
system needs.

## What's here

- `instagram_poster/client.py` — Instagram Graph API wrapper (create media
  container, poll video processing, publish, check daily publish quota).
- `instagram_poster/queue.py` — a JSON-file queue of posts waiting to go out
  (`data/posts_queue.json`).
- `instagram_poster/scheduler.py` — publishes whatever in the queue is due;
  meant to run on a cron schedule (see SETUP.md step 9).
- `instagram_poster/projects.py` — reads `data/nest_kenya_projects.csv` (the
  53-project Nest Kenya portfolio) and writes an on-brand caption per
  project, using the audience/voice guidelines from the `nest-kenya-audience`
  skill and the brand palette from the Canva brand doc.
- `instagram_poster/cli.py` — command-line interface.

## Quick start

```
pip install -r requirements.txt
cp .env.example .env   # fill in credentials, see SETUP.md

python -m instagram_poster.cli projects
python -m instagram_poster.cli queue-project 15 --media-url "https://..." --time "2026-09-20 09:00"
python -m instagram_poster.cli add --type IMAGE --media-url "https://..." --caption "..." --time "2026-09-20 09:00"
python -m instagram_poster.cli list
python -m instagram_poster.cli run-once
```

Media (photos/videos/reels) must be hosted at a public URL — Instagram's API
publishes from a URL, not a file upload. See SETUP.md step 7.

## Tests

```
pip install -r requirements.txt pytest
pytest tests/
```
