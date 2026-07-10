---
name: property-research
description: Research real estate properties for a client from online sources (listing sites, public real estate marketplaces, Facebook Marketplace/group posts pasted in by the user, classifieds) and deliver a client-ready property roadmap. Use when asked to "research properties for [client]", "find listings", "check facebook marketplace/groups for houses", "build a property roadmap", or "put together a comps/shortlist" for a buyer or renter.
---

# Property Research & Roadmap

Turns a client's home-search brief into (1) a vetted shortlist of properties pulled from
public online sources and (2) a client-facing roadmap document with next steps and a timeline.

## Step 1 — Get the client brief

Before searching, confirm these fields. If the user already gave them in their message, don't
re-ask — just restate your understanding in one line and proceed. Only use `AskUserQuestion` for
fields that materially change the search and are genuinely missing (location and budget almost
always matter; the rest can default to "flexible").

- Client name (for labeling the roadmap only — never needed for the search itself)
- Location(s): city/neighborhood/zip, plus any radius or "must be near X" constraints
- Budget range (purchase price or rent) — and whether it's a **hard ceiling** or a **flexible
  target** the client will exceed for the right property (e.g. "will pay market value"). Get this
  explicitly; don't assume a stated number is a hard cutoff.
- Property type: single-family, condo, multi-family, land, etc.
- Must-haves vs. nice-to-haves (beds/baths, sqft, yard, parking, school district, move-in date)
- Deal type: buy, rent, or off-market/investment lead

## Step 2 — Search public sources

Use `WebSearch` / `WebFetch` against public listing sources. Pick sources based on the client's
market:

- **US default:** Zillow, Redfin, Realtor.com, Apartments.com, local MLS-adjacent broker sites,
  Craigslist/local classifieds.
- **Kenya:** BuyRentKenya (buyrentkenya.com), Jiji Kenya (jiji.co.ke), plus Facebook Marketplace
  and local estate-agent Facebook groups (see the Facebook note below — group/marketplace posts
  still need to be pasted in, they can't be crawled).

Site-restrict searches (e.g. `site:buyrentkenya.com`, `site:jiji.co.ke`) and query by
neighborhood/estate + price + bed/bath to cut down noise. Note Jiji listing prices are often
negotiable asking prices, not fixed — flag this in the shortlist rather than treating them as firm.

For each candidate property capture: address (or approximate location if the source hides it),
price, beds/baths, sqft, listing source + URL, days on market if shown, and one or two lines on
why it fits (or doesn't) the brief.

### Facebook posts specifically

Facebook Marketplace and group listings sit behind a login wall and generally **cannot be
crawled or searched directly** — don't attempt to guess or fabricate a Facebook URL or post
content. Handle it like this:

- If the user pastes in a post's text, screenshot, or a direct link they're already viewing,
  treat that as a source: extract price/details from it and fold it into the shortlist like any
  other listing, but mark the source as "Facebook (client-provided)" since it can't be
  re-verified independently.
- If the user asks you to "check Facebook" without providing content, tell them Facebook content
  isn't reachable from here and ask them to paste in the post(s) or forward the listing link/text
  — then continue with the public-source search in the meantime rather than blocking on it.
- Never invent Facebook posts, groups, sellers, or prices to fill a gap.

## Step 3 — Score and shortlist

Rank properties against the brief's must-haves first, then nice-to-haves. How to handle budget
depends on what Step 1 established:

- **Hard ceiling:** drop anything over budget or missing a must-have, unless the user asked for
  stretch options — if so, label them clearly as stretch/compromise picks in a separate section
  rather than mixing them in unlabeled.
- **Flexible/market-value budget:** don't drop over-budget properties into a separate "stretch"
  section — merge everything into one shortlist ranked by fit against the must-haves (title/deed
  status, access, utilities, amenities — not price), and let price be one visible column rather
  than a filter. Still call out anything unusually far from the stated range so the client isn't
  surprised.

Either way, missing must-have information (e.g. a listing that never mentions utilities or title
status) should lower a property's rank and get flagged as needing verification — don't assume
it's fine just because the price fits.

## Step 4 — Deliver the roadmap

Use `references/roadmap-template.md` as the structure. Fill it in with the client brief, the
shortlist (as a table), and a dated action plan (e.g. "This week: schedule showings for the top
3", "Week 2: submit pre-approval if not already done", follow-up dates). Keep the tone practical
— this is a working document for the agent and client, not marketing copy.

Default delivery: write the filled-in markdown to a file and, if the user wants something
polished to hand to the client, render it as an Artifact (see the `artifact-design` skill for
styling guidance) instead of a plain markdown dump. Ask which they want if it's unclear whether
this roadmap is for internal use or client-facing.
