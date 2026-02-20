from __future__ import annotations

from collections import Counter, defaultdict
from datetime import datetime
from math import ceil
from typing import Any
from urllib.parse import quote

from flask import Flask, Response, jsonify, redirect, render_template, request, session, url_for

app = Flask(__name__)
app.secret_key = "dev-secret-change-me"

LANGUAGES = ["rn", "fr"]
DEFAULT_LANG = "rn"
ADMIN_USER = "admin"
ADMIN_PASS = "admin123"

EVENT_CATEGORIES = ["Music", "Sports", "Community", "Business", "Culture"]
POST_CATEGORIES = ["News", "Guide", "Community"]
MEDIA_CATEGORIES = ["Music", "Sports", "Community", "Culture"]

SITE_META = {
    "rn": {
        "title": "Burundi Events Hub",
        "description": "Menya ibikorwa n'ibirori biza kuba mu Burundi.",
    },
    "fr": {
        "title": "Burundi Events Hub",
        "description": "Découvrez les événements à venir au Burundi.",
    },
}

EVENTS = [
    {
        "id": 1,
        "slug": "concert-bujumbura-2026",
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
    },
    {
        "id": 2,
        "slug": "jeux-jeunesse-intwari",
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
    },
    {
        "id": 3,
        "slug": "journee-communaute-rusizi",
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
    },
]

POSTS = [
    {
        "id": 1,
        "slug": "nouvelles-evenements-2026",
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
        "slug": "sorties-bujumbura",
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
    {"id": 3, "type": "video", "category": "Culture", "src": "https://www.youtube.com/embed/dQw4w9WgXcQ", "thumb": EVENTS[1]["images"][0], "caption": "Cultural highlights"},
]

SPONSORS = [
    {"name": "Visit Burundi", "url": "#", "description": "Tourism partner"},
    {"name": "Bujumbura Arena", "url": "#", "description": "Venue partner"},
]
GUIDES = [
    {"title": "Top music venues", "type": "music", "body": "Discover live spots across Bujumbura."},
    {"title": "Travel tips", "type": "travel", "body": "Best routes and safe transport ideas."},
]
FAQS = [
    {"q": "How do I submit an event?", "a": "Use the contact page or request admin access."},
    {"q": "Are events free?", "a": "Some are free and some are ticketed. Check each event detail page."},
]

ANALYTICS: dict[str, Any] = {
    "page_views": Counter(),
    "event_views": Counter(),
    "post_views": Counter(),
    "visitors": set(),
}
MESSAGES: list[dict[str, str]] = []


def lang_or_default(lang: str) -> str:
    return lang if lang in LANGUAGES else DEFAULT_LANG


def text_by_lang(data: dict[str, str], lang: str) -> str:
    return data.get(lang) or data.get(DEFAULT_LANG) or next(iter(data.values()))


def normalize_event(item: dict[str, Any], lang: str) -> dict[str, Any]:
    return {
        **item,
        "title_text": text_by_lang(item["title"], lang),
        "description_text": text_by_lang(item["description"], lang),
    }


def normalize_post(item: dict[str, Any], lang: str) -> dict[str, Any]:
    return {
        **item,
        "title_text": text_by_lang(item["title"], lang),
        "excerpt_text": text_by_lang(item["excerpt"], lang),
        "content_text": text_by_lang(item["content"], lang),
    }


def paginate(items: list[Any], page: int, per_page: int = 6) -> tuple[list[Any], int]:
    total_pages = max(1, ceil(len(items) / per_page))
    page = max(1, min(page, total_pages))
    start = (page - 1) * per_page
    return items[start : start + per_page], total_pages


def seo_payload(lang: str, title: str | None = None, description: str | None = None, image: str | None = None) -> dict[str, str]:
    base = SITE_META[lang]
    return {
        "title": title or base["title"],
        "description": description or base["description"],
        "og_image": image or "https://images.unsplash.com/photo-1470229722913-7c0e2dbbafd3?auto=format&fit=crop&w=1200&q=80",
        "url": request.url,
    }


@app.before_request
def track_page_views():
    ANALYTICS["page_views"][request.path] += 1
    ANALYTICS["visitors"].add(request.headers.get("X-Forwarded-For", request.remote_addr or "unknown"))


@app.context_processor
def shared_context():
    current_lang = lang_or_default(request.view_args.get("lang", DEFAULT_LANG) if request.view_args else DEFAULT_LANG)
    return {
        "event_categories": EVENT_CATEGORIES,
        "post_categories": POST_CATEGORIES,
        "media_categories": MEDIA_CATEGORIES,
        "current_year": datetime.now().year,
        "lang": current_lang,
    }


@app.get("/")
def root_redirect():
    return redirect(url_for("home", lang=DEFAULT_LANG))


@app.get("/<lang>/")
def home(lang: str):
    lang = lang_or_default(lang)
    featured = normalize_event(EVENTS[0], lang)
    cards = [normalize_event(e, lang) for e in sorted(EVENTS, key=lambda x: x["date"])[:6]]
    posts = [normalize_post(p, lang) for p in POSTS[:3]]
    return render_template("home.html", featured=featured, events=cards, posts=posts, seo=seo_payload(lang))


@app.get("/<lang>/events")
def events_page(lang: str):
    lang = lang_or_default(lang)
    page = request.args.get("page", 1, type=int)
    cards = [normalize_event(e, lang) for e in sorted(EVENTS, key=lambda x: x["date"])]
    paged, total_pages = paginate(cards, page)
    return render_template("events.html", events=paged, page=page, total_pages=total_pages, seo=seo_payload(lang, "Events"))


@app.get("/<lang>/events/<slug>")
def event_detail(lang: str, slug: str):
    lang = lang_or_default(lang)
    found = next((e for e in EVENTS if e["slug"] == slug), None)
    if not found:
        return redirect(url_for("events_page", lang=lang))
    ANALYTICS["event_views"][slug] += 1
    event = normalize_event(found, lang)
    related = [normalize_event(e, lang) for e in EVENTS if e["id"] != found["id"]][:3]
    return render_template(
        "event_detail.html",
        event=event,
        related=related,
        seo=seo_payload(lang, event["title_text"], event["description_text"], event["images"][0]),
    )


@app.get("/<lang>/blog")
def blog_page(lang: str):
    lang = lang_or_default(lang)
    page = request.args.get("page", 1, type=int)
    query = request.args.get("q", "").strip().lower()
    category = request.args.get("category", "all")

    filtered = [normalize_post(p, lang) for p in sorted(POSTS, key=lambda x: x["date"], reverse=True)]
    if category != "all":
        filtered = [p for p in filtered if p["category"].lower() == category.lower()]
    if query:
        filtered = [p for p in filtered if query in p["title_text"].lower() or query in p["excerpt_text"].lower()]
    paged, total_pages = paginate(filtered, page, per_page=4)
    return render_template("blog.html", posts=paged, page=page, total_pages=total_pages, q=query, category=category, seo=seo_payload(lang, "Blog"))


@app.get("/<lang>/blog/<slug>")
def blog_post(lang: str, slug: str):
    lang = lang_or_default(lang)
    found = next((p for p in POSTS if p["slug"] == slug), None)
    if not found:
        return redirect(url_for("blog_page", lang=lang))
    ANALYTICS["post_views"][slug] += 1
    post = normalize_post(found, lang)
    related = [normalize_post(p, lang) for p in POSTS if p["id"] != found["id"]][:2]
    return render_template("blog_post.html", post=post, related=related, seo=seo_payload(lang, post["title_text"], post["excerpt_text"], post["image"]))


@app.get("/<lang>/media")
def media_page(lang: str):
    lang = lang_or_default(lang)
    return render_template("media.html", media_items=MEDIA, seo=seo_payload(lang, "Media Gallery"))


@app.get("/<lang>/about")
def about_page(lang: str):
    return render_template("about.html", seo=seo_payload(lang_or_default(lang), "About"))


@app.route("/<lang>/contact", methods=["GET", "POST"])
def contact_page(lang: str):
    lang = lang_or_default(lang)
    sent = False
    if request.method == "POST":
        MESSAGES.append({
            "name": request.form.get("name", ""),
            "email": request.form.get("email", ""),
            "phone": request.form.get("phone", ""),
            "message": request.form.get("message", ""),
        })
        sent = True
    return render_template("contact.html", sent=sent, seo=seo_payload(lang, "Contact"))


@app.get("/<lang>/sponsors")
def sponsors_page(lang: str):
    return render_template("sponsors.html", sponsors=SPONSORS, seo=seo_payload(lang_or_default(lang), "Sponsors"))


@app.get("/<lang>/guides")
def guides_page(lang: str):
    return render_template("guides.html", guides=GUIDES, seo=seo_payload(lang_or_default(lang), "Local Guides"))


@app.get("/<lang>/faqs")
def faqs_page(lang: str):
    return render_template("faqs.html", faqs=FAQS, seo=seo_payload(lang_or_default(lang), "FAQs"))


@app.get("/api/<lang>/events")
def events_api(lang: str):
    lang = lang_or_default(lang)
    query = request.args.get("q", "").lower().strip()
    category = request.args.get("category", "all")
    sort = request.args.get("sort", "date_asc")
    cards = [normalize_event(e, lang) for e in EVENTS]
    if category != "all":
        cards = [e for e in cards if e["category"].lower() == category.lower()]
    if query:
        cards = [e for e in cards if query in e["title_text"].lower() or query in e["description_text"].lower()]
    cards.sort(key=lambda i: i["date"], reverse=sort == "date_desc")
    return jsonify(cards)


@app.get("/api/<lang>/blog")
def blog_api(lang: str):
    lang = lang_or_default(lang)
    q = request.args.get("q", "").lower().strip()
    category = request.args.get("category", "all")
    data = [normalize_post(p, lang) for p in POSTS]
    if category != "all":
        data = [p for p in data if p["category"].lower() == category.lower()]
    if q:
        data = [p for p in data if q in p["title_text"].lower() or q in p["excerpt_text"].lower()]
    return jsonify(data)


@app.get("/api/media")
def media_api():
    category = request.args.get("category", "all")
    media_type = request.args.get("type", "all")
    results = MEDIA
    if category != "all":
        results = [m for m in results if m["category"].lower() == category.lower()]
    if media_type != "all":
        results = [m for m in results if m["type"] == media_type]
    return jsonify(results)


@app.route("/admin/login", methods=["GET", "POST"])
def admin_login():
    error = ""
    if request.method == "POST":
        if request.form.get("username") == ADMIN_USER and request.form.get("password") == ADMIN_PASS:
            session["admin"] = True
            return redirect(url_for("admin_dashboard"))
        error = "Invalid credentials"
    return render_template("admin_login.html", error=error, seo=seo_payload(DEFAULT_LANG, "Admin Login"))


def require_admin() -> bool:
    return bool(session.get("admin"))


@app.route("/admin", methods=["GET", "POST"])
def admin_dashboard():
    if not require_admin():
        return redirect(url_for("admin_login"))

    action = request.form.get("action")
    if action == "add_category":
        target = request.form.get("target")
        name = request.form.get("name", "").strip()
        if target == "event" and name and name not in EVENT_CATEGORIES:
            EVENT_CATEGORIES.append(name)
        if target == "post" and name and name not in POST_CATEGORIES:
            POST_CATEGORIES.append(name)
    if action == "add_event":
        new_id = max(e["id"] for e in EVENTS) + 1
        slug = quote(request.form.get("slug", f"event-{new_id}"))
        EVENTS.append(
            {
                "id": new_id,
                "slug": slug,
                "title": {"rn": request.form.get("title_rn", ""), "fr": request.form.get("title_fr", "")},
                "description": {"rn": request.form.get("desc_rn", ""), "fr": request.form.get("desc_fr", "")},
                "date": request.form.get("date", "2026-01-01"),
                "time": request.form.get("time", "10:00"),
                "category": request.form.get("category", EVENT_CATEGORIES[0]),
                "location": request.form.get("location", "TBD"),
                "images": [request.form.get("image", "https://images.unsplash.com/photo-1470229722913-7c0e2dbbafd3?auto=format&fit=crop&w=1200&q=80")],
            }
        )
    if action == "delete_event":
        delete_id = request.form.get("id", type=int)
        EVENTS[:] = [e for e in EVENTS if e["id"] != delete_id]

    summary = {
        "events": len(EVENTS),
        "posts": len(POSTS),
        "media": len(MEDIA),
        "views": sum(ANALYTICS["page_views"].values()),
        "visitors": len(ANALYTICS["visitors"]),
    }
    top_events = ANALYTICS["event_views"].most_common(5)
    top_posts = ANALYTICS["post_views"].most_common(5)
    return render_template(
        "admin.html",
        summary=summary,
        events=EVENTS,
        posts=POSTS,
        media_items=MEDIA,
        event_categories=EVENT_CATEGORIES,
        post_categories=POST_CATEGORIES,
        top_events=top_events,
        top_posts=top_posts,
        messages=MESSAGES,
        seo=seo_payload(DEFAULT_LANG, "Admin Dashboard"),
    )


@app.post("/admin/logout")
def admin_logout():
    session.pop("admin", None)
    return redirect(url_for("admin_login"))


@app.get("/sitemap.xml")
def sitemap():
    now = datetime.utcnow().date().isoformat()
    urls = [url_for("home", lang=lang, _external=True) for lang in LANGUAGES]
    for lang in LANGUAGES:
        urls.extend(url_for("events_page", lang=lang, _external=True) for _ in [0])
        urls.extend(url_for("blog_page", lang=lang, _external=True) for _ in [0])
        urls.extend(url_for("media_page", lang=lang, _external=True) for _ in [0])
        urls.extend(url_for("event_detail", lang=lang, slug=e["slug"], _external=True) for e in EVENTS)
        urls.extend(url_for("blog_post", lang=lang, slug=p["slug"], _external=True) for p in POSTS)
    xml = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for item in urls:
        xml.append(f"<url><loc>{item}</loc><lastmod>{now}</lastmod></url>")
    xml.append("</urlset>")
    return Response("\n".join(xml), mimetype="application/xml")


@app.get("/robots.txt")
def robots():
    body = "User-agent: *\nAllow: /\nDisallow: /admin\nSitemap: /sitemap.xml\n"
    return Response(body, mimetype="text/plain")


if __name__ == "__main__":
    app.run(debug=True)
