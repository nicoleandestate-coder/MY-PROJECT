# Setup: connecting this system to Instagram

This system publishes to Instagram through Meta's **Instagram Graph API**.
Meta requires a few things to exist on their side before any app (including
this one) can post on your behalf. None of this can be automated from
outside Meta's own dashboards — you have to click through it once. It takes
about 15–20 minutes.

## 1. Convert your Instagram account to a Business or Creator account

- Instagram app → Settings → Account type and tools → Switch to Professional
  Account → choose **Business**.

## 2. Link it to a Facebook Page

The Graph API publishes through a Facebook Page connected to your Instagram
Business account, even though nothing gets posted to Facebook itself.

- If you don't have a Facebook Page for Nest Kenya yet, create one at
  facebook.com/pages/create.
- In the Instagram app: Settings → Account → Linked accounts → Facebook →
  connect the Page.

## 3. Create a Meta Developer App

- Go to developers.facebook.com/apps → **Create App** → type **Business**.
- Add the **Instagram Graph API** product to the app.

## 4. Get a long-lived access token with the right permissions

- In the app's Graph API Explorer (developers.facebook.com/tools/explorer),
  select your app, then generate a User Access Token with these permissions:
  `instagram_basic`, `instagram_content_publish`, `pages_show_list`,
  `pages_read_engagement`.
- Exchange the short-lived token for a **long-lived token** (60 days) via:
  `GET /oauth/access_token?grant_type=fb_exchange_token&client_id={app-id}&client_secret={app-secret}&fb_exchange_token={short-lived-token}`
- Long-lived tokens expire after 60 days. For a set-and-forget system, put a
  reminder on your calendar to refresh it (Meta doesn't currently support
  fully non-expiring tokens for this API), or look into a System User token
  on a Meta Business Account, which doesn't expire.

## 5. Find your Instagram Business Account ID

- `GET /me/accounts?access_token={your-token}` → find your Page, note its
  `id`.
- `GET /{page-id}?fields=instagram_business_account&access_token={your-token}`
  → this returns your `instagram_business_account.id`. That's the ID this
  system needs.

## 6. Fill in `.env`

```
cp .env.example .env
```

```
INSTAGRAM_ACCESS_TOKEN=<the long-lived token from step 4>
INSTAGRAM_BUSINESS_ACCOUNT_ID=<the ID from step 5>
```

## 7. Media must be hosted at a public URL

Instagram's API does not accept file uploads — every post needs a publicly
reachable `image_url` or `video_url` (JPEG for images; MP4/MOV for
video/reels, H.264, max ~1GB / 60 min for reels). Options:
- Export from Canva and upload to any public host (Cloudinary, S3, even a
  public Google Drive/Dropbox direct-download link).
- Keep a public folder of ready-to-post assets.

## 8. Install dependencies and try it

```
pip install -r requirements.txt
python -m instagram_poster.cli projects                 # see the Nest Kenya portfolio
python -m instagram_poster.cli queue-project 15 \
  --media-url "https://your-host.com/galaxy-one.jpg" \
  --time "2026-09-20 09:00"                              # auto-writes the caption, queues the post
python -m instagram_poster.cli list
python -m instagram_poster.cli run-once                  # publishes anything due now
```

## 9. Automate it

Add a cron entry (adjust the path) so due posts actually go out without you
running the command by hand:

```
*/15 * * * * cd /path/to/MY-PROJECT && /path/to/venv/bin/python -m instagram_poster.cli run-once >> logs/scheduler.log 2>&1
```

## Limits worth knowing

- Instagram caps posting at **25 published items per rolling 24 hours** per
  account — `scheduler.run_once()` checks this via
  `content_publishing_limit` before posting and just skips the run if you're
  at the cap.
- Reels/video containers process asynchronously; the scheduler polls
  `status_code` until `FINISHED` before publishing (up to 5 minutes, then
  gives up and marks the post failed so it's not silently lost).
