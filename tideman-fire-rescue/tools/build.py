#!/usr/bin/env python3
"""Builds index.html and the Elementor template JSON from ONE content tree.

    python3 tools/build.py [IMAGE_BASE_URL]

IMAGE_BASE_URL is where the images will live in WordPress (media library
folder). Default is a placeholder you can find/replace in the JSON.
"""
import hashlib, json, os, sys
from html import escape

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = (sys.argv[1] if len(sys.argv) > 1 else "https://YOUR-SITE.com/wp-content/uploads/tideman").rstrip("/")
CSS = open(os.path.join(ROOT, "styles.css"), encoding="utf-8").read()

_ids = set()
def _id(seed):
    n = 0
    while True:
        h = hashlib.md5(f"{seed}{n}".encode()).hexdigest()[:7]
        if h not in _ids:
            _ids.add(h); return h
        n += 1

# ---------------------------------------------------------------- node helpers
def C(cls, *kids, eid=None):            # container
    return {"t": "c", "cls": cls, "kids": [k for k in kids if k], "eid": eid}
def H(text, tag="h2", cls=""):          # heading
    return {"t": "h", "text": text, "tag": tag, "cls": cls}
def T(html, cls=""):                    # text editor
    return {"t": "p", "html": html, "cls": cls}
def B(text, href, cls=""):              # button
    return {"t": "b", "text": text, "href": href, "cls": cls}
def I(src, alt, cls=""):                # image
    return {"t": "i", "src": src, "alt": alt, "cls": cls}
def RAW(html):                          # html widget
    return {"t": "r", "html": html}
def F(cls=""):                          # form
    return {"t": "f", "cls": cls}
def UL(items):
    return "<ul>" + "".join(f"<li>{i}</li>" for i in items) + "</ul>"
def P(*paras):
    return "".join(f"<p>{p}</p>" for p in paras)

IMG = "assets/img/"      # relative in the HTML preview, BASE in the JSON

FORM_FIELDS = [
    ("name", "text", "Name", "", True, 50),
    ("department", "text", "Department / Organization", "", True, 50),
    ("email", "email", "Email", "", True, 50),
    ("phone", "tel", "Phone", "", False, 50),
    ("mission", "select", "Primary Mission", "Marine firefighting\nSearch and rescue\nFlood response\nDive operations\nEmergency medical response\nHarbor and port response\nOther", False, 100),
    ("message", "textarea", "Tell us about your department's requirements", "", False, 100),
]

# ---------------------------------------------------------------- content
def series_item(title, paras_before, sub, paras_after, list_items=None, list_intro=None, list_pos=None):
    kids = [H(title, "h3"), *[T(p) for p in paras_before], H(sub, "h4")]
    kids += [T(p) for p in paras_after]
    return C("tm-series-item", *kids)

def build_tree():
    wrap = lambda *k, cls="": C(f"tm-wrap {cls}".strip(), *k)

    topbar = C("tm-topbar", wrap(
        T("<p>Fire &amp; Rescue Boats · Built from HDPE</p>"),
        T("<p>Built to Last</p>")))

    nav = C("tm-nav", wrap(
        H('TIDEMAN <span>MARINE</span>', "div", "tm-brand"),
        T('<p><a href="#f-series">F-Series</a><a href="#missions">Missions</a><a href="#hdpe">Why HDPE</a>'
          '<a href="#series">Other Series</a><a href="#contact">Contact</a></p>', "tm-menu"),
        B("Request Information", "#contact", "tm-small")), eid="top")

    hero = C("tm-hero", wrap(C("tm-hero-copy",
        T("<p>Fire Rescue · Emergency Response</p>", "tm-eyebrow"),
        H("Fire Boats and Rescue Boats Built for <span>Emergency Response</span>", "h1"),
        T(P("Tideman Marine designs and manufactures mission-ready <strong>fire boats and rescue boats</strong> "
            "for fire departments, municipalities, emergency response agencies, harbor authorities, and public "
            "safety organizations. Built from durable HDPE, Tideman Marine boats provide rugged, low-maintenance "
            "platforms for marine firefighting, search and rescue, flood response, dive operations, emergency "
            "medical response, and public safety missions."), "tm-lead"),
        C("tm-row tm-gap-s", B("Request Information", "#contact"), B("Explore the F-Series", "#f-series", "tm-ghost")))))

    stats = C("tm-stats", wrap(C("tm-g4 tm-stats-grid",
        C("tm-stat", H("23'", "div"), T("<p>Overall length</p>")),
        C("tm-stat", H("8'6\"", "div"), T("<p>Beam</p>")),
        C("tm-stat", H("HDPE", "div"), T("<p>Hull construction</p>")),
        C("tm-stat", H("Shallow", "div"), T("<p>Draft design</p>")))))

    intro = C("tm-sec", wrap(C("tm-split tm-flip",
        C("tm-gap-m",
          T("<p>Mission-ready platforms</p>", "tm-eyebrow"),
          T(P("From compact, shallow-draft <strong>rescue boats</strong> to larger, fully outfitted "
              "<strong>fire boats</strong>, Tideman Marine platforms can be configured around the specific "
              "equipment, personnel, waterways, and response requirements of each department.",
              "Whether responding on lakes, rivers, harbors, coastal waters, flood zones, or shallow waterways, "
              "Tideman Marine builds <strong>fire and rescue boats</strong> around the mission."))),
        C("", I(IMG + "square-underway.jpg", "Tideman Marine fire rescue boat underway in a harbor", "tm-media")))), )

    f_series = C("tm-sec tm-alt", wrap(C("tm-split",
        C("tm-gap-m",
          T("<p>F-Series</p>", "tm-eyebrow"),
          H("F-Series Flat Series <span>Fire Boats and Rescue Boats</span>", "h2"),
          T(P("The Tideman Marine <strong>F-Series, or Flat Series</strong>, is a versatile HDPE platform that can "
              "be configured for fire rescue and emergency response operations. Its shallow-draft design makes the "
              "Flat Series particularly well suited for departments that need access to rivers, lakes, flood zones, "
              "shorelines, and other areas where water depth or submerged hazards may limit conventional rescue vessels.",
              "Configured as a <strong>rescue boat</strong>, the F-Series can support marine firefighting, search and "
              "rescue, flood response, dive operations, emergency medical response, victim recovery, and public safety missions.",
              "The featured General Arrangement (GA) print showcases a <strong>23' long × 8'6\" beam Tideman Marine "
              "F-Series Flat Series</strong> platform outfitted specifically for fire rescue operations.",
              "The Flat Series provides emergency response teams with a rugged and versatile <strong>rescue boat</strong> "
              "platform designed around shallow-water access, stability, deck space, and mission flexibility.",
              "The featured configuration incorporates:")),
          T(UL(["23' overall length", "8'6\" beam", "HDPE hull construction", "Flat Series shallow-draft hull design",
                "Enclosed patrol-style cabin", "Large working and rescue deck", "Side boarding and dive door access",
                "Outboard propulsion", "Emergency lighting and electronics", "Rescue and recovery equipment storage",
                "Configurable equipment and personnel arrangements"]), "tm-checks"),
          T(P("This F-Series configuration demonstrates how a Tideman Marine platform can be outfitted as a "
              "purpose-built <strong>fire department rescue boat</strong> for professional emergency response."))),
        C("", I(IMG + "square-dock-day.jpg", "Tideman Marine F-Series fire rescue boat docked on calm blue water", "tm-media")))), eid="f-series")

    ga = C("tm-sec tm-blueprint", wrap(C("tm-gap-m",
        T("<p>General Arrangement</p>", "tm-eyebrow"),
        C("tm-ga", I(IMG + "ga-drawing.png", "General Arrangement drawing of the 23' F-Series Flat Series fire rescue boat")),
        T("<p>General Arrangement (GA) · 23' × 8'6\" F-Series Flat Series</p>", "tm-caption"))))

    search = C("tm-sec", wrap(C("tm-split",
        C("tm-gap-m",
          T("<p>Search and rescue</p>", "tm-eyebrow"),
          H("Rescue Boats for <span>Search and Rescue</span>", "h2"),
          T(P("Rapid access, stability, durability, and usable deck space can make a critical difference during a "
              "marine emergency. Tideman Marine <strong>rescue boats</strong> can be configured for quick deployment "
              "of firefighters, rescue personnel, divers, medical teams, and specialized emergency equipment.")),
          H("Shallow-Water Rescue Boats for Fire Departments", "h3"),
          T(P("Shallow-water <strong>rescue boats</strong> can be particularly important during emergencies in rivers, "
              "marshes, lakes, flood zones, coastal areas, and other low-water environments.",
              "The shallow-draft F-Series Flat Series helps emergency crews access areas where deeper-draft vessels "
              "may have difficulty operating.",
              "Depending on department requirements, a shallow-water <strong>fire department rescue boat</strong> "
              "can be configured with:")),
          T(UL(["Open rescue and recovery areas", "Dive and boarding doors", "Patient recovery areas",
                "Medical equipment storage", "Rescue equipment storage", "Emergency and scene lighting",
                "Navigation and communications electronics", "Searchlights", "Tow points", "Specialized seating",
                "Enclosed or open helm arrangements", "Firefighting equipment"]), "tm-checks"),
          T(P("These capabilities make the Flat Series a versatile platform for flood rescue, shoreline response, "
              "victim recovery, dive operations, and other <strong>boat fire rescue</strong> missions."))),
        C("", I(IMG + "square-dock-night.jpg", "Tideman Marine rescue boat at a lit harbor dock at night", "tm-media")))))

    missions = C("tm-sec tm-alt", wrap(C("tm-gap-xl",
        C("tm-narrow tm-gap-m",
          T("<p>Municipal fire departments</p>", "tm-eyebrow"),
          H("Municipal Fire Department <span>Rescue Boats</span>", "h2"),
          T(P("Tideman Marine builds <strong>fire department rescue boats</strong> around the needs of municipal, "
              "regional, state, and other public safety agencies.",
              "Rather than limiting departments to a single standard configuration, Tideman Marine can develop the "
              "vessel arrangement around the crew, equipment, operating environment, and mission.",
              "Tideman Marine <strong>fire and rescue boats</strong> can support:"))),
        C("tm-g4 tm-mission-grid", *[
            C("tm-mission", H(f"{i:02d}", "div", "tm-num"), H(m, "h3"))
            for i, m in enumerate(["Marine firefighting", "Search and rescue", "Flood response", "Dive team deployment",
                                   "Emergency medical response", "Victim recovery", "Harbor and marina response",
                                   "Public safety patrol", "Vessel assistance", "Disaster response",
                                   "Personnel and equipment transport"], 1)]),
        T(P("This flexibility allows one <strong>fire and rescue boat</strong> to support multiple emergency response missions."),
          "tm-narrow"))), eid="missions")

    firefight = C("tm-sec tm-firefight", wrap(C("tm-gap-l",
        C("tm-narrow tm-gap-m",
          T("<p>Marine firefighting</p>", "tm-eyebrow"),
          H("Fire Boats for <span>Marine Firefighting</span>", "h2"),
          T(P("For departments requiring dedicated marine firefighting capability, Tideman Marine <strong>fire boats</strong> "
              "can be configured with equipment for responding to vessel fires, marina incidents, waterfront structure "
              "fires, port emergencies, and other incidents on or near the water.")),
          H("Fire Boats with Pumps, Monitors and Rescue Equipment", "h3"),
          T(P("Depending on vessel size, mission, and department requirements, Tideman Marine <strong>fire boats</strong> "
              "can be outfitted with:"))),
        T(UL(["Fire suppression pumps", "Fire monitors and water cannons", "Hose connections and deployment systems",
              "Emergency and scene lighting", "Searchlights", "Communications systems", "Navigation electronics",
              "Rescue and recovery equipment", "Dive equipment", "Medical equipment", "Equipment storage",
              "Specialized seating", "Command and helm stations"]), "tm-checks tm-equip"),
        T(P("These capabilities allow a Tideman Marine <strong>rescue fire boat</strong> to serve as a multipurpose "
            "emergency response asset for fire departments, ports, harbors, marinas, industrial waterfront facilities, "
            "and other marine operations."), "tm-narrow"))))

    def card(i, title, text):
        return C("tm-card", H(f"{i:02d}", "div", "tm-num"), H(title, "h3"), T(f"<p>{text}</p>"))
    hdpe = C("tm-sec", wrap(C("tm-gap-xl",
        C("tm-split tm-flip",
          C("tm-gap-m",
            T("<p>HDPE construction</p>", "tm-eyebrow"),
            H("HDPE Fire Boats <span>and Rescue Boats</span>", "h2"),
            T(P("Tideman Marine constructs its vessels using High-Density Polyethylene (HDPE), providing characteristics "
                "that are particularly well suited for professional <strong>fire boats and rescue boats</strong>.",
                "Emergency response vessels may encounter docks, submerged objects, debris, rocky shorelines, shallow "
                "water, saltwater, and other demanding conditions. HDPE provides departments with a rugged hull material "
                "designed for these real-world marine environments.")),
            H("Why HDPE Works for Fire Boats and Rescue Boats", "h3")),
          C("", I(IMG + "square-deck-detail.jpg", "Deck detail of a Tideman Marine HDPE rescue boat with life ring and equipment case", "tm-media"))),
        C("tm-g4 tm-gap-m",
          card(1, "Impact Resistance", "HDPE provides excellent impact resistance for operations around docks, debris, rocky shorelines, and other demanding environments."),
          card(2, "Corrosion Resistance", "HDPE does not corrode from exposure to freshwater or saltwater, making it well suited for long-term marine service."),
          card(3, "Low Maintenance", "The HDPE hull does not require the same corrosion protection associated with many traditional marine materials."),
          card(4, "No Electrolysis", "HDPE is nonconductive and is not subject to galvanic corrosion."),
          card(5, "Naturally Buoyant", "HDPE itself is naturally buoyant, an important characteristic for a marine hull material."),
          card(6, "Shallow-Water Capability", "HDPE construction works particularly well with rugged, shallow-draft workboat designs such as the F-Series Flat Series."),
          card(7, "Long Service Life", "HDPE is designed to provide years of demanding marine service with relatively low hull maintenance."),
          card(8, "Repairability", "If damage does occur, HDPE can be welded and repaired.")),
        T(P("For departments whose <strong>rescue boats</strong> may encounter submerged debris, damaged docks, rocky shorelines, "
            "flood-related hazards, or other challenging conditions, HDPE can provide an important operational advantage."),
          "tm-narrow"))), eid="hdpe")

    def more(*parts):
        """Collapsed block: all remaining copy stays in the DOM, behind a Read more toggle."""
        return T("<details><summary>Read more</summary>" + "".join(parts) + "</details>", "tm-more tm-checks tm-one")
    def pp(x): return f"<p>{x}</p>"
    def h4(x): return f"<h4>{x}</h4>"

    def scard(letter, title, lead, *rest):
        return C("tm-scard",
                 H(letter, "div", "tm-letter"),
                 H(title, "h3"),
                 T(pp(lead), "tm-lead-s"),
                 more(*rest))

    i_cards = C("tm-g3 tm-gap-l",
        scard("I", "I-Series Inland Patrol Fire Boats and Rescue Boats",
              "The <strong>I-Series Inland Patrol</strong> is a strong option for fire departments operating on lakes, rivers, harbors, and inland waterways.",
              pp("Configured as a <strong>fire rescue boat</strong>, the Inland Patrol can support marine firefighting, search and rescue, dive operations, emergency medical response, harbor patrol, and personnel transport."),
              h4("Inland Patrol Rescue Boats for Emergency Response"),
              pp("An I-Series Inland Patrol <strong>rescue boat</strong> can be configured with equipment such as fire pumps and monitors, emergency lighting, searchlights, rescue equipment storage, electronics, communications equipment, dive access, and specialized crew seating."),
              pp("This combination makes the Inland Patrol an option for departments that need one boat to perform both routine public safety and emergency response missions.")),
        scard("I", "I-Series Inland Utility Fire Boats and Rescue Boats",
              "For departments that prioritize deck space, stability, and equipment capacity, the <strong>I-Series Inland Utility</strong> provides another versatile platform for <strong>fire boats and rescue boats</strong>.",
              pp("The Inland Utility can provide valuable working space for pumps, hoses, rescue equipment, divers, medical personnel, and recovered victims."),
              h4("Inland Utility Fire Department Rescue Boats"),
              pp("An Inland Utility <strong>fire department rescue boat</strong> could be particularly well-suited for:"),
              UL(["Flood response", "Shallow-water rescue", "Dive operations", "Equipment transport", "Victim recovery",
                  "Emergency medical response", "Marine firefighting", "Disaster response"]),
              pp("Its open-working platform also provides departments with flexibility in determining where specialized fire and rescue equipment should be positioned.")),
        scard("I", "I-Series Inland Landing Craft Rescue Boats",
              "The <strong>I-Series Inland Landing Craft</strong> provides another approach to emergency response by offering direct access between the vessel and shoreline.",
              h4("Landing Craft Rescue Boats for Flood and Disaster Response"),
              pp("A bow ramp can make it easier to move rescue personnel, equipment, patients, and emergency supplies between the <strong>rescue boat</strong> and shore."),
              pp("This can make an Inland Landing Craft particularly useful for:"),
              UL(["Flood response", "Disaster response", "Evacuations", "Shoreline rescue", "Emergency equipment deployment",
                  "Personnel transport", "Medical response", "Access to isolated areas"]),
              pp("For departments responding where roads, docks, or conventional access points have been compromised, a landing craft-style <strong>rescue boat</strong> can provide additional mission flexibility.")))

    c_cards = C("tm-g3 tm-gap-l",
        scard("C", "C-Series Coastal Patrol Fire Boats and Rescue Boats",
              "For departments operating in larger harbors, ports, coastal waterways, and more demanding marine environments, the <strong>C-Series Coastal Patrol</strong> provides a larger platform for a highly capable <strong>fire boat</strong>.",
              pp("The Coastal Series can provide additional room and payload capacity for larger firefighting systems, rescue equipment, medical equipment, electronics, crew accommodations, and command systems."),
              h4("Coastal Fire Boats for Ports and Harbors"),
              pp("A C-Series Coastal Patrol <strong>fire rescue boat</strong> can be configured for:"),
              UL(["Marine firefighting", "Port and harbor response", "Search and rescue", "Dive operations", "Vessel assistance",
                  "Emergency medical response", "Coastal patrol", "Extended emergency response missions"]),
              pp("For departments covering large harbors, coastal areas, ports, or more exposed waterways, the C-Series provides another option for a highly capable <strong>fire and rescue boat</strong>.")),
        scard("C", "C-Series Coastal Utility Fire Boats",
              "The <strong>C-Series Coastal Utility</strong> provides a substantial working deck for departments requiring a heavy-duty <strong>fire boat</strong> with room for firefighting and rescue systems.",
              h4("Coastal Utility Fire Boats with Working Deck Space"),
              pp("The working deck can be configured around equipment such as:"),
              UL(["Fire pumps", "Fire monitors", "Hose storage", "Dive equipment", "Rescue gear", "Medical equipment",
                  "Generators", "Emergency equipment", "Specialized storage"]),
              pp("For a department looking for a working <strong>fire boat</strong> rather than a traditional patrol-style layout, the Coastal Utility provides another highly configurable HDPE platform.")),
        scard("C", "C-Series Coastal Landing Craft Fire and Rescue Boats",
              "The <strong>C-Series Coastal Landing Craft</strong> can provide fire and rescue agencies with a heavy-duty emergency response platform capable of moving personnel and equipment directly to a shoreline.",
              h4("Coastal Landing Craft Rescue Boats for Emergency Access"),
              pp("A Coastal Landing Craft <strong>fire and rescue boat</strong> could be especially valuable for agencies responsible for islands, coastal communities, industrial waterfronts, ports, or areas where emergency crews need the ability to bring personnel and equipment directly ashore."),
              pp("Potential missions include:"),
              UL(["Disaster response", "Evacuation", "Search and rescue", "Firefighting support", "Equipment deployment",
                  "Emergency personnel transport", "Shoreline access", "Recovery operations"])))

    series = C("tm-sec tm-alt", wrap(C("tm-gap-xl",
        C("tm-narrow tm-gap-m",
          T("<p>More platforms</p>", "tm-eyebrow"),
          H("Other Tideman Marine Series for <span>Fire Boats and Rescue Boats</span>", "h2"),
          T(P("While the <strong>F-Series Flat Series</strong> provides an excellent shallow-draft platform for fire rescue operations, other Tideman Marine boat series can also be configured as <strong>fire boats and rescue boats</strong>.",
              "The right platform depends on the department's waterways, crew size, equipment, operating conditions, required range, and primary mission."))),
        C("tm-gap-m", H("I-Series <span>Inland</span>", "h3", "tm-series-title"), i_cards),
        C("tm-gap-m", H("C-Series <span>Coastal</span>", "h3", "tm-series-title"), c_cards))), eid="series")

    config = C("tm-sec", wrap(C("tm-gap-l",
        C("tm-narrow tm-gap-m",
          T("<p>Built around your mission</p>", "tm-eyebrow"),
          H("Fire Boats and Rescue Boats <span>Configured Around Your Department</span>", "h2"),
          T(P("Every fire department operates differently. A coastal department may require a substantial firefighting system, larger crew capacity, and an enclosed cabin, while an inland department may prioritize shallow draft, open deck space, rapid victim recovery, and trailerability.",
              "Tideman Marine can configure <strong>fire boats and rescue boats</strong> around the specific requirements of the department and its operating environment.",
              "Available configurations can include:"))),
        T(UL(["Shallow-water rescue boats", "Municipal fire boats", "Fire department rescue boats", "Search and rescue boats",
              "Flood response boats", "Dive support boats", "Harbor and port response boats", "Fire suppression boats",
              "Multi-purpose emergency response boats", "Coastal rescue boats"]), "tm-tags"),
        T(P("From the <strong>23' F-Series Flat Series</strong> featured on this page to larger Inland and Coastal platforms, Tideman Marine provides departments with the ability to select the hull, layout, propulsion, cabin, equipment, and rescue features that best support their mission."),
          "tm-narrow"))))

    cta = C("tm-sec tm-cta", wrap(C("tm-g2 tm-gap-xl tm-top",
        C("tm-gap-m",
          T("<p>Contact</p>", "tm-eyebrow"),
          H("Request Information About Tideman Marine <span>Fire Boats and Rescue Boats</span>", "h2"),
          T(P("Contact Tideman Marine to discuss your department's operational requirements. Our team can help identify the Tideman Marine platform, hull configuration, propulsion package, layout, and mission equipment best suited for your department's marine firefighting, fire rescue, search and rescue, flood response, or emergency response operations."))),
        C("tm-panel", F("tm-form")))), eid="contact")

    footer = C("tm-footer", wrap(
        T("<p>© Tideman Marine. Built to Last.</p>"),
        T('<p><a href="#top">Back to top ↑</a></p>')))

    return C("tm-page", topbar, nav, hero, stats, intro, f_series, ga, search, missions, firefight, hdpe, series, config, cta, footer, eid="tm-page")

# ---------------------------------------------------------------- HTML renderer (mimics Elementor DOM)
def render_html(n):
    cls = n.get("cls", "")
    if n["t"] == "c":
        a = f' id="{n["eid"]}"' if n.get("eid") else ""
        return f'<div class="e-con e-flex {cls}"{a}>' + "".join(render_html(k) for k in n["kids"]) + "</div>"
    w = lambda name, inner: (f'<div class="elementor-element elementor-widget elementor-widget-{name} {cls}">'
                             f'<div class="elementor-widget-container">{inner}</div></div>')
    if n["t"] == "h":
        return w("heading", f'<{n["tag"]} class="elementor-heading-title">{n["text"]}</{n["tag"]}>')
    if n["t"] == "p":
        return w("text-editor", n["html"])
    if n["t"] == "b":
        return w("button", f'<div class="elementor-button-wrapper"><a class="elementor-button elementor-button-link elementor-size-sm" href="{n["href"]}">'
                           f'<span class="elementor-button-content-wrapper"><span class="elementor-button-text">{escape(n["text"])}</span></span></a></div>')
    if n["t"] == "i":
        return w("image", f'<img src="{n["src"]}" alt="{escape(n["alt"])}">')
    if n["t"] == "f":
        rows = []
        for cid, typ, label, ph, req, width in FORM_FIELDS:
            r = " required" if req else ""
            if typ == "textarea": fld = f'<textarea id="f-{cid}" name="{cid}" class="elementor-field"{r}></textarea>'
            elif typ == "select": fld = f'<select id="f-{cid}" name="{cid}" class="elementor-field">' + "".join(f"<option>{escape(o)}</option>" for o in ph.split("\n")) + "</select>"
            else: fld = f'<input id="f-{cid}" name="{cid}" type="{typ}" class="elementor-field"{r}>'
            rows.append(f'<div class="elementor-field-group elementor-col-{width}"><label for="f-{cid}">{escape(label)}</label>{fld}</div>')
        rows.append('<div class="elementor-field-group elementor-col-100"><button type="submit" class="elementor-button">Request Information</button></div>')
        return w("form", '<form class="elementor-form" onsubmit="return false"><div class="elementor-form-fields-wrapper">' + "".join(rows) + "</div></form>")
    raise ValueError(n)

# ---------------------------------------------------------------- Elementor JSON
def to_el(n, inner=False):
    seed = n.get("cls", "") + str(n.get("text", n.get("html", n.get("href", ""))))[:40]
    cls = n.get("cls", "")
    if n["t"] == "c":
        s = {"content_width": "full", "flex_direction": "column", "_css_classes": cls}
        if n.get("eid"): s["_element_id"] = n["eid"]
        return {"id": _id(seed), "elType": "container", "settings": s,
                "elements": [to_el(k, True) for k in n["kids"]], "isInner": inner}
    def wd(typ, s):
        s["_css_classes"] = cls
        return {"id": _id(seed), "elType": "widget", "widgetType": typ, "settings": s, "elements": []}
    if n["t"] == "h":
        return wd("heading", {"title": n["text"], "header_size": n["tag"]})
    if n["t"] == "p":
        return wd("text-editor", {"editor": n["html"]})
    if n["t"] == "b":
        return wd("button", {"text": n["text"], "link": {"url": n["href"], "is_external": "", "nofollow": "", "custom_attributes": ""}})
    if n["t"] == "i":
        return wd("image", {"image": {"url": n["src"].replace(IMG, BASE + "/"), "id": "", "alt": n["alt"], "source": "library"}, "image_size": "full"})
    if n["t"] == "f":
        fields = []
        for cid, typ, label, opts, req, width in FORM_FIELDS:
            f = {"custom_id": cid, "field_type": typ, "field_label": label, "placeholder": "", "width": str(width),
                 "required": "true" if req else "", "_id": _id("f" + cid)}
            if typ == "select": f["field_options"] = opts
            if typ == "textarea": f["rows"] = "5"
            fields.append(f)
        return wd("form", {"form_name": "Fire Rescue Information Request", "form_fields": fields, "button_text": "Request Information",
                           "button_size": "md", "submit_actions": ["email"], "email_to": "info@tideman-marine.com",
                           "email_subject": "New Fire Rescue information request", "email_content": "[all-fields]",
                           "email_from_name": "Tideman Marine Website", "success_message": "Thank you. Our team will contact you shortly.",
                           "show_labels": "true", "label_position": "above"})
    raise ValueError(n)

def css_for(img_base):
    """CSS with the image variables resolved for this target."""
    v = (f".tm-page{{--tm-hero:url('{img_base}hero.jpg');--tm-water:url('{img_base}bg-water.jpg');"
         f"--tm-blueprint:url('{img_base}bg-blueprint.jpg');}}\n")
    return v + CSS

FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
         '<link href="https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">')

PREVIEW_BASE = """
html{scroll-behavior:smooth} body{margin:0;background:#0a0a0a}
.e-con{display:flex;flex-direction:column;width:100%}
.elementor-widget-button .elementor-button{text-align:center}
"""

def main():
    tree = build_tree()
    # ---- HTML
    css_local = css_for(IMG)          # relative paths from styles.css? -> inline <style> sits in index.html
    html = ("<!DOCTYPE html>\n<html lang=\"en\">\n<head>\n<meta charset=\"UTF-8\">\n"
            "<meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">\n"
            "<title>Fire Boats and Rescue Boats | Tideman Marine</title>\n"
            "<meta name=\"description\" content=\"Tideman Marine designs and manufactures mission-ready fire boats and rescue boats built from durable HDPE for fire departments, municipalities, harbor authorities, and public safety organizations.\">\n"
            f"{FONTS}\n<style>{PREVIEW_BASE}</style>\n<style>\n{css_local}</style>\n</head>\n<body>\n"
            + render_html(tree) + "\n</body>\n</html>\n")
    open(os.path.join(ROOT, "index.html"), "w", encoding="utf-8").write(html)

    # ---- Elementor JSON
    style_widget = {"id": _id("style"), "elType": "widget", "widgetType": "html",
                    "settings": {"html": FONTS + "\n<style>\n" + css_for(BASE + "/") + "</style>"}, "elements": []}
    page = to_el(tree)
    page["elements"].insert(0, style_widget)
    tpl = {"content": [page], "page_settings": {"hide_title": "yes"}, "version": "0.4",
           "title": "Fire Rescue Boats - Tideman Marine", "type": "page"}
    out = os.path.join(ROOT, "tideman-fire-rescue-elementor.json")
    json.dump(tpl, open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("OK", len(html), "bytes html;", os.path.getsize(out), "bytes json; image base:", BASE)

main()
