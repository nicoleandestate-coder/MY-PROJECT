"""Loads Nest Kenya's project portfolio (data/nest_kenya_projects.csv) and
turns a row into an on-brand Instagram caption.

The CSV is the same portfolio Nicole keeps in
"NEST KENYA PROJECTS" / Nest_Kenya_Projects on Drive - re-export it there and
copy it over `data/nest_kenya_projects.csv` whenever the portfolio is updated.
"""
import csv
import os

PROJECTS_FILE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "nest_kenya_projects.csv")

# From NEST_Kenya_Canva_Prompts.docx - keeps generated posts visually on-brand.
BRAND = {
    "colors": {
        "navy": "#1A2744",
        "cream": "#F5EDE0",
        "indigo": "#1E1152",
        "purple_primary": "#4A1DA8",
        "purple_accent": "#8B2FC9",
        "purple_light": "#C4B5FD",
        "lavender_tint": "#EDE9FE",
    },
    "fonts": {
        "headline": "Playfair Display",
        "subheading": "Cormorant Garamond",
        "body": "Inter",
    },
    "handle": "@nestkenya",
    "website": "nestkenyaproperties.com",
}

HASHTAGS = (
    "#NestKenya #NairobiRealEstate #KenyaInvestment #DiasporaInvestor "
    "#OffPlanKenya #NairobiProperty #InvestInKenya #RealEstateKenya"
)


def load_projects() -> list:
    with open(PROJECTS_FILE, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def get_project(project_number: str) -> dict:
    for row in load_projects():
        if row["#"] == str(project_number):
            return row
    raise KeyError(f"No project numbered {project_number} in {PROJECTS_FILE}")


def _price_line(row: dict) -> str:
    price = (row.get("Price Range (KSh)") or "").strip()
    if not price or price == "TBC":
        return "Pricing on request"
    return price


def generate_caption(row: dict) -> str:
    """Feature-post caption: educates first (area + access + amenities),
    then names the fear-reducing detail (developer/status), then a soft CTA -
    matches Nest Kenya's "insider, educational-first" voice.
    """
    name = row["Project Name"].strip()
    area = row["Area / Neighbourhood"].strip()
    road = (row.get("Specific Road / Address") or "").strip()
    beds = (row.get("Bedroom Types") or "").strip()
    amenities = (row.get("Key Amenities") or "").strip()
    nearby = (row.get("Nearby Amenities") or "").strip()
    status = (row.get("Project Status") or "").strip()
    developer = (row.get("Developer") or "").strip()
    price = _price_line(row)

    location = f"{road}, {area}" if road and road != "TBC" else area

    lines = [
        f"FEATURED PROJECT: {name}",
        f"📍 {location}",
    ]
    if beds and beds != "TBC":
        lines.append(f"🛏 {beds}")
    lines.append(f"💰 {price}")
    if amenities:
        lines.append(f"✨ {amenities}")
    if nearby:
        lines.append(f"🗺 Close to: {nearby}")

    lines.append("")
    if developer and developer not in ("TBC", ""):
        lines.append(
            f"Built by {developer} — {status.lower() if status else 'in development'}. "
            "Every project we feature has been vetted for title, developer track record, "
            "and legal structure for foreign ownership, because the #1 thing holding "
            "investors back isn't the opportunity — it's not knowing who to trust."
        )
    else:
        lines.append(
            "If you've been watching Nairobi's property market for a while but haven't "
            "pulled the trigger, this is the kind of opportunity worth a closer look — "
            "vetted for title and legal structure so you can invest with confidence, "
            "wherever in the world you're investing from."
        )

    lines.append("")
    lines.append("DM \"NAIROBI\" or tap the link in bio to get the full due-diligence pack on this project.")
    lines.append("")
    lines.append(HASHTAGS)

    return "\n".join(lines)
