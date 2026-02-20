from __future__ import annotations

from datetime import datetime
from flask import Flask, jsonify, redirect, render_template, request, url_for

app = Flask(__name__)

LANGUAGES = ["rn", "fr"]

CATEGORIES = ["Music", "Sports", "Community", "Business", "Culture"]

EVENTS = [
    {
        "id": 1,
        "title": {"rn": "Igiteramo c'Umuziki wa Bujumbura", "fr": "Concert de Bujumbura"},
        "description": {
            "rn": "Igiteramo kinini c'abahanzi bo mu Burundi n'akarere.",
            "fr": "Grand concert avec des artistes du Burundi et de la région.",
        },
        "date": "2026-03-10",
        "time": "18:30",
        "category": "Music",
        "location": "Bujumbura Arena",
        "images": [
            "https://images.unsplash.com/photo-1516450360452-9312f5e86fc7?auto=format&fit=crop&w=1200&q=80",
            "https://images.unsplash.com/photo-1493225457124-a3eb161ffa5f?auto=format&fit=crop&w=900&q=80",
        ],
        "tags": ["live", "festival"],
    },
    {
        "id": 2,
        "title": {"rn": "Inkino z'Urwaruka", "fr": "Jeux de la Jeunesse"},
        "description": {
            "rn": "Imikino n'ibikorwa vyo guteza imbere urwaruka.",
            "fr": "Compétitions sportives et activités pour la jeunesse.",
        },
        "date": "2026-04-02",
        "time": "09:00",
        "category": "Sports",
        "location": "Stade Intwari",
        "images": [
            "https://images.unsplash.com/photo-1461896836934-ffe607ba8211?auto=format&fit=crop&w=1200&q=80",
            "https://images.unsplash.com/photo-1526232761682-d26e03ac148e?auto=format&fit=crop&w=900&q=80",
        ],
        "tags": ["youth", "tournament"],
    },
    {
        "id": 3,
        "title": {"rn": "Umusi w'Imiryango", "fr": "Journée de la Communauté"},
        "description": {
            "rn": "Umunsi wo guhura no gusangira ibikorwa vy'iterambere.",
            "fr": "Une journée communautaire de rencontres et d'initiatives locales.",
        },
        "date": "2026-02-22",
        "time": "11:00",
        "category": "Community",
        "location": "Parc Rusizi",
        "images": [
            "https://images.unsplash.com/photo-1529156069898-49953e39b3ac?auto=format&fit=crop&w=1200&q=80",
            "https://images.unsplash.com/photo-1531058020387-3be344556be6?auto=format&fit=crop&w=900&q=80",
        ],
        "tags": ["networking", "community"],
    },
    {
        "id": 4,
        "title": {"rn": "Forum y'Abadandaza", "fr": "Forum des Entrepreneurs"},
        "description": {
            "rn": "Ibiganiro ku bucuruzi n'udushasha tw'iterambere.",
            "fr": "Discussions sur le commerce et l'innovation locale.",
        },
        "date": "2026-05-18",
        "time": "14:00",
        "category": "Business",
        "location": "Kigobe Conference Hall",
        "images": [
            "https://images.unsplash.com/photo-1515187029135-18ee286d815b?auto=format&fit=crop&w=1200&q=80",
            "https://images.unsplash.com/photo-1552664730-d307ca884978?auto=format&fit=crop&w=900&q=80",
        ],
        "tags": ["innovation", "startup"],
    },
]

POSTS = [
    {
        "id": 1,
        "title": {"rn": "Inkuru z'Ibirori vya 2026", "fr": "Nouvelles des événements 2026"},
        "excerpt": {
            "rn": "Reba ibizokurikira vy'ingenzi muri uyu mwaka.",
            "fr": "Découvrez les grands rendez-vous de cette année.",
        },
        "content": {
            "rn": "Aha niho ubona amakuru yose ku birori binini bizoba muri Burundi.",
            "fr": "Voici toutes les informations sur les événements majeurs à venir au Burundi.",
        },
        "date": "2026-01-15",
        "category": "News",
        "image": "https://images.unsplash.com/photo-1521737604893-d14cc237f11d?auto=format&fit=crop&w=1000&q=80",
    },
    {
        "id": 2,
        "title": {"rn": "Aho wosohokera i Bujumbura", "fr": "Sorties à Bujumbura"},
        "excerpt": {
            "rn": "Aho hantu heza ho kwidagadurira no guhura.",
            "fr": "Les meilleurs endroits pour se divertir et se rencontrer.",
        },
        "content": {
            "rn": "Twateguye urutonde rw'ahantu hashimishije ushobora kugenderamwo.",
            "fr": "Nous avons préparé une liste de lieux incontournables à visiter.",
        },
        "date": "2026-01-28",
        "category": "Guide",
        "image": "https://images.unsplash.com/photo-1511795409834-ef04bbd61622?auto=format&fit=crop&w=1000&q=80",
    },
]

MEDIA = [
    {"id": 1, "type": "image", "category": "Music", "src": EVENTS[0]["images"][0], "caption": "Concert vibes"},
    {"id": 2, "type": "image", "category": "Community", "src": EVENTS[2]["images"][0], "caption": "Community day"},
    {"id": 3, "type": "image", "category": "Sports", "src": EVENTS[1]["images"][0], "caption": "Youth games"},
]


def pick_lang() -> str:
    lang = request.args.get("lang", "rn")
    return lang if lang in LANGUAGES else "rn"


def normalized_event(event: dict, lang: str) -> dict:
    return {
        "id": event["id"],
        "title": event["title"][lang],
        "description": event["description"][lang],
        "date": event["date"],
        "time": event["time"],
        "category": event["category"],
        "location": event["location"],
        "images": event["images"],
        "tags": event["tags"],
    }


@app.context_processor
def inject_globals():
    return {"categories": CATEGORIES, "current_year": datetime.now().year}


@app.route("/")
def home():
    lang = pick_lang()
    featured = normalized_event(EVENTS[0], lang)
    events = [normalized_event(event, lang) for event in EVENTS]
    posts = POSTS[:3]
    return render_template("home.html", lang=lang, featured=featured, events=events, posts=posts)


@app.route("/events")
def events():
    lang = pick_lang()
    event_cards = [normalized_event(event, lang) for event in EVENTS]
    return render_template("events.html", lang=lang, events=event_cards)


@app.route("/events/<int:event_id>")
def event_detail(event_id: int):
    lang = pick_lang()
    event = next((item for item in EVENTS if item["id"] == event_id), None)
    if not event:
        return redirect(url_for("events", lang=lang))
    current = normalized_event(event, lang)
    related = [normalized_event(item, lang) for item in EVENTS if item["id"] != event_id][:3]
    return render_template("event_detail.html", lang=lang, event=current, related=related)


@app.route("/blog")
def blog():
    lang = pick_lang()
    return render_template("blog.html", lang=lang, posts=POSTS)


@app.route("/blog/<int:post_id>")
def blog_post(post_id: int):
    lang = pick_lang()
    post = next((item for item in POSTS if item["id"] == post_id), None)
    if not post:
        return redirect(url_for("blog", lang=lang))
    related = [item for item in POSTS if item["id"] != post_id][:2]
    return render_template("blog_post.html", lang=lang, post=post, related=related)


@app.route("/media")
def media():
    lang = pick_lang()
    return render_template("media.html", lang=lang, media_items=MEDIA)


@app.route("/about")
def about():
    return render_template("about.html", lang=pick_lang())


@app.route("/contact")
def contact():
    return render_template("contact.html", lang=pick_lang(), sent=False)


@app.post("/contact")
def send_contact():
    return render_template("contact.html", lang=pick_lang(), sent=True)


@app.route("/admin")
def admin_dashboard():
    return render_template("admin.html", events=EVENTS, posts=POSTS, media_items=MEDIA)


@app.route("/api/events")
def events_api():
    lang = pick_lang()
    query = request.args.get("q", "").lower().strip()
    category = request.args.get("category", "all")
    sort = request.args.get("sort", "date_asc")

    filtered = [normalized_event(event, lang) for event in EVENTS]
    if category != "all":
        filtered = [event for event in filtered if event["category"].lower() == category.lower()]
    if query:
        filtered = [
            event
            for event in filtered
            if query in event["title"].lower() or query in event["description"].lower() or query in event["location"].lower()
        ]

    reverse = sort == "date_desc"
    filtered.sort(key=lambda item: item["date"], reverse=reverse)
    return jsonify(filtered)


if __name__ == "__main__":
    app.run(debug=True)
