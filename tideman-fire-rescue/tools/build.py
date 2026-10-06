#!/usr/bin/env python3
"""Builds the Tideman Marine Fire Rescue landing.

    python3 tools/build.py [IMAGE_BASE_URL]

Outputs (in tideman-fire-rescue/):
  tideman-fire-rescue-elementor.json   Elementor template (classic Sections/Columns, NO custom CSS)
  index.html                           preview that renders the same Elementor settings
  tideman-fire-rescue-standalone.html  same preview with images inlined (single file)
  tests/test-hero-only.json            smallest real import test

All styling lives in native Elementor settings (typography, colours, backgrounds,
padding, widths per device) so the client can edit everything from the panel.
The copy comes from tools/content.py (taken from the client's PDF).
"""
import base64, hashlib, json, os, re, sys
from html import escape

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import content

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = (sys.argv[1] if len(sys.argv) > 1 else "https://YOUR-SITE.com/wp-content/uploads/tideman").rstrip("/")

# ------------------------------------------------------------------ design tokens
BLACK, INK, PANEL, CARD = "#0A0A0A", "#111214", "#16181B", "#0F1114"
AMBER, STEEL, WHITE, LEAD = "#F5A800", "#B3B9C0", "#F5F6F7", "#CFD3D8"
LINE = "rgba(255,255,255,0.14)"
DISPLAY, BODY = "Bebas Neue", "Inter"

# ------------------------------------------------------------------ tiny Elementor settings helpers
_n = 0
def nid():
    global _n
    _n += 1
    return hashlib.md5(f"tm-{_n}".encode()).hexdigest()[:7]

def SZ(v, unit="px"):
    return {"unit": unit, "size": v, "sizes": []}

def DIM(t, r=None, b=None, l=None, unit="px"):
    linked = r is None
    if linked: r = b = l = t
    return {"unit": unit, "top": str(t), "right": str(r), "bottom": str(b), "left": str(l), "isLinked": linked}

def typo(p, family=None, size=None, tablet=None, mobile=None, weight=None, lh=None, ls=None, tr=None, style=None):
    s = {f"{p}typography": "custom"}
    if family: s[f"{p}font_family"] = family
    if size is not None: s[f"{p}font_size"] = SZ(size)
    if tablet is not None: s[f"{p}font_size_tablet"] = SZ(tablet)
    if mobile is not None: s[f"{p}font_size_mobile"] = SZ(mobile)
    if weight: s[f"{p}font_weight"] = str(weight)
    if lh is not None: s[f"{p}line_height"] = SZ(lh, "em")
    if ls is not None: s[f"{p}letter_spacing"] = SZ(ls)
    if tr: s[f"{p}text_transform"] = tr
    if style: s[f"{p}font_style"] = style
    return s

def rich(html, color=WHITE):
    """<strong> gets a visible colour inline (editable in the WYSIWYG)."""
    return html.replace("<strong>", f'<strong style="color:{color}">')

def amber(html):
    return html.replace("<span>", f'<span style="color:{AMBER}">')

def img_url(src):
    return src.replace(content.IMG, BASE + "/")

def strip_p(html):
    return re.sub(r"</?p>", "", html)

# ------------------------------------------------------------------ widgets
def widget(wtype, s):
    return {"id": nid(), "elType": "widget", "widgetType": wtype, "settings": s, "elements": []}

def heading(text_, size, tablet, mobile, tag="h2", color=WHITE, family=DISPLAY, weight=400, lh=1.05, ls=0.5,
            tr="uppercase", align=None, margin=None, style=None):
    s = {"title": amber(text_), "header_size": tag, "title_color": color}
    s.update(typo("typography_", family, size, tablet, mobile, weight, lh, ls, tr, style))
    if align: s["align"] = align
    if margin: s["_margin"] = margin
    return widget("heading", s)

def text(html, color=STEEL, size=16, tablet=None, mobile=None, weight=None, lh=1.7, ls=None, tr=None, align=None, margin=None):
    s = {"editor": rich(html), "text_color": color}
    s.update(typo("typography_", BODY, size, tablet, mobile, weight, lh, ls, tr))
    if align: s["align"] = align
    if margin: s["_margin"] = margin
    return widget("text-editor", s)

def eyebrow(html):
    return text(f"<p>{strip_p(html)}</p>", AMBER, 12, weight=700, ls=3, tr="uppercase", lh=1.4)

def button(label, url, primary=True, align="left", align_mobile="justify"):
    s = {"text": label, "link": {"url": url, "is_external": "", "nofollow": "", "custom_attributes": ""},
         "align": align, "align_mobile": align_mobile,
         "text_color": BLACK if primary else WHITE,
         "background_color": AMBER if primary else "rgba(0,0,0,0)",
         "border_border": "solid", "border_width": DIM(2), "border_color": AMBER if primary else "rgba(255,255,255,0.4)",
         "border_radius": DIM(0), "text_padding": DIM(17, 30, 17, 30),
         "hover_color": AMBER, "button_background_hover_color": "rgba(0,0,0,0)", "button_hover_border_color": AMBER}
    s.update(typo("typography_", BODY, 13, weight=700, ls=2, tr="uppercase", lh=1.2))
    return widget("button", s)

def image(src, alt, border=True, bg=None, pad=None):
    s = {"image": {"url": img_url(src), "id": "", "alt": alt, "source": "library"}, "image_size": "full",
         "width": SZ(100, "%")}
    if border:
        s.update({"image_border_border": "solid", "image_border_width": DIM(1), "image_border_color": LINE})
    if bg:
        s.update({"_background_background": "classic", "_background_color": bg, "_padding": DIM(pad or 10)})
    return widget("image", s)

def icon_list(items_, inline=False, size=15, icon="fas fa-check", icon_color=AMBER):
    s = {"icon_list": [{"text": t, "selected_icon": {"value": icon, "library": "fa-solid"}, "_id": nid()} for t in items_],
         "view": "inline" if inline else "traditional",
         "space_between": SZ(10 if inline else 12), "icon_color": icon_color, "icon_size": SZ(13),
         "text_color": WHITE, "text_indent": SZ(10)}
    s.update(typo("icon_typography_", BODY, size, weight=500, lh=1.5))
    return widget("icon-list", s)

def toggle(title, html):
    s = {"tabs": [{"tab_title": title, "tab_content": html, "_id": nid()}], "title_html_tag": "div",
         "selected_icon": {"value": "fas fa-plus", "library": "fa-solid"},
         "selected_active_icon": {"value": "fas fa-minus", "library": "fa-solid"},
         "icon_align": "right", "border_width": SZ(1), "border_color": LINE, "space_between": SZ(0),
         "title_color": AMBER, "tab_active_color": AMBER, "icon_color": AMBER, "icon_active_color": AMBER,
         "content_color": STEEL, "content_padding": DIM(16, 0, 4, 0)}
    s.update(typo("title_typography_", BODY, 12, weight=700, ls=2.5, tr="uppercase"))
    s.update(typo("content_typography_", BODY, 14, lh=1.65))
    return widget("toggle", s)

def form(fields):
    fl = []
    for cid, typ, label, opts, req, width in fields:
        f = {"custom_id": cid, "field_type": typ, "field_label": label, "placeholder": "", "width": str(width),
             "required": "true" if req else "", "_id": nid()}
        if typ == "select": f["field_options"] = opts
        if typ == "textarea": f["rows"] = "5"
        fl.append(f)
    s = {"form_name": "Fire Rescue Information Request", "form_fields": fl, "button_text": "Request Information",
         "button_size": "md", "submit_actions": ["email"], "email_to": "info@tideman-marine.com",
         "email_subject": "New Fire Rescue information request", "email_content": "[all-fields]",
         "email_from_name": "Tideman Marine Website", "success_message": "Thank you. Our team will contact you shortly.",
         "show_labels": "true", "label_position": "above", "column_gap": SZ(14), "row_gap": SZ(14),
         "label_color": STEEL, "field_text_color": WHITE, "field_background_color": INK,
         "field_border_color": LINE, "field_border_width": DIM(1), "field_border_radius": DIM(0),
         "button_background_color": AMBER, "button_text_color": BLACK, "button_border_border": "solid",
         "button_border_width": DIM(2), "button_border_color": AMBER, "button_border_radius": DIM(0),
         "button_background_hover_color": "rgba(0,0,0,0)", "button_hover_color": AMBER, "button_hover_border_color": AMBER,
         "button_text_padding": DIM(17, 30, 17, 30)}
    s.update(typo("label_typography_", BODY, 11, weight=700, ls=2, tr="uppercase"))
    s.update(typo("button_typography_", BODY, 13, weight=700, ls=2, tr="uppercase"))
    return widget("form", s)

# ------------------------------------------------------------------ layout
def column(size, *els, tablet=100, mobile=100, pad=None, pad_t=None, pad_m=None, margin=None, bg=None, border=None, valign=None, space=16):
    s = {"_column_size": round(size), "_inline_size": size, "_inline_size_tablet": tablet, "_inline_size_mobile": mobile,
         "space_between_widgets": space}
    if pad: s["padding"] = pad
    if pad_t: s["padding_tablet"] = pad_t
    if pad_m: s["padding_mobile"] = pad_m
    if margin: s["margin"] = margin
    if bg:
        s.update({"background_background": "classic", "background_color": bg})
    if border:
        w, c = border
        s.update({"border_border": "solid", "border_width": w, "border_color": c})
    if valign: s["content_position"] = valign
    return {"id": nid(), "elType": "column", "settings": s, "elements": list(els), "isInner": False}

def section(*cols, inner=False, bg=None, image_url=None, image_pos="center center", overlay=None, grad_bg=None,
            pad=None, pad_t=None, pad_m=None, width=1180, gap="no", valign=None, margin=None, border=None,
            min_h=None, min_h_m=None, z=None, anchor=None, vcontent=None, bg_resp=None, margin_t=None, margin_m=None):
    s = {"layout": "full_width" if inner else "boxed", "gap": gap, "structure": f"{min(len(cols), 6)}0"}
    if not inner: s["content_width"] = SZ(width)
    if pad: s["padding"] = pad
    if pad_t: s["padding_tablet"] = pad_t
    if pad_m: s["padding_mobile"] = pad_m
    if margin: s["margin"] = margin
    if margin_t: s["margin_tablet"] = margin_t
    if margin_m: s["margin_mobile"] = margin_m
    if bg:
        s.update({"background_background": "classic", "background_color": bg})
    if grad_bg:
        s.update({"background_background": "gradient", "background_color": grad_bg[0], "background_color_b": grad_bg[1],
                  "background_gradient_type": "linear", "background_gradient_angle": SZ(135, "deg")})
    if image_url:
        s.update({"background_background": "classic", "background_image": {"url": img_url(image_url), "id": "", "source": "library"},
                  "background_position": image_pos, "background_repeat": "no-repeat", "background_size": "cover"})
    if overlay:
        s.update(overlay)
    if bg_resp:
        s.update(bg_resp)
    if border:
        w, c = border
        s.update({"border_border": "solid", "border_width": w, "border_color": c})
    if valign: s["column_position"] = valign
    if vcontent: s["content_position"] = vcontent
    if min_h:
        s["height"] = "min-height"; s["custom_height"] = SZ(min_h)
        if min_h_m: s["custom_height_mobile"] = SZ(min_h_m)
    if z: s["z_index"] = z
    if anchor: s["_element_id"] = anchor
    cols = [dict(c, isInner=inner) for c in cols]
    return {"id": nid(), "elType": "section", "settings": s, "elements": cols, "isInner": inner}

def solid_overlay(color, opacity):
    return {"background_overlay_background": "classic", "background_overlay_color": color,
            "background_overlay_opacity": SZ(opacity)}

def grad_overlay(c1, stop1, c2, stop2, angle=90):
    return {"background_overlay_background": "gradient", "background_overlay_color": c1,
            "background_overlay_color_stop": SZ(stop1, "%"), "background_overlay_color_b": c2,
            "background_overlay_color_b_stop": SZ(stop2, "%"), "background_overlay_gradient_type": "linear",
            "background_overlay_gradient_angle": SZ(angle, "deg"), "background_overlay_opacity": SZ(1)}

def PAD(t, b, side=0):
    return DIM(t, side, b, side)

# ------------------------------------------------------------------ page copy accessors
TREE = content.build_tree()
def _leaves(n, out):
    if n["t"] == "c":
        for k in n["kids"]: _leaves(k, out)
    else: out.append(n)
    return out
LV = [_leaves(s, []) for s in TREE["kids"]]          # LV[section][leaf]
def T_(si, i):  return LV[si][i].get("html") or LV[si][i].get("text") or ""
def items(si, i): return re.findall(r"<li>(.*?)</li>", LV[si][i]["html"], flags=re.S)
def split_even(xs, n):
    k, m = divmod(len(xs), n); out, p = [], 0
    for j in range(n):
        q = p + k + (1 if j < m else 0); out.append(xs[p:q]); p = q
    return out

H2 = dict(size=54, tablet=44, mobile=34, lh=1.02)
H3 = dict(size=30, tablet=26, mobile=24, lh=1.1, ls=0.6)
def h2(t_):  return heading(t_, tag="h2", **H2)
def h3(t_):  return heading(t_, tag="h3", **H3)
def body(html, **kw): return text(html, **kw)

def two_lists(lst):
    a, b = split_even(lst, 2)
    return section(column(50, icon_list(a), tablet=50, mobile=100), column(50, icon_list(b), tablet=50, mobile=100),
                   inner=True, gap="no", margin=DIM(0, 0, 8, 0))

def txt_col(size, *els, **kw):
    return column(size, *els, pad=DIM(0, 40, 0, 0), pad_t=DIM(0), pad_m=DIM(0), **kw)
def img_col(size, *els, **kw):
    return column(size, *els, pad=DIM(0, 0, 0, 40), pad_t=DIM(0), pad_m=DIM(0), **kw)

SEC_PAD = dict(pad=PAD(96, 96), pad_t=PAD(72, 72, 24), pad_m=PAD(56, 56, 18))

# ------------------------------------------------------------------ sections
def build_sections():
    out = []

    # 0 HERO ---------------------------------------------------------------
    out.append(section(
        column(52, eyebrow(T_(0, 0)),
               heading(T_(0, 1), 74, 56, 40, tag="h1", lh=1.0),
               text(T_(0, 2), LEAD, 18, mobile=16),
               section(column(50, button(T_(0, 3), "#contact"), tablet=50, mobile=100),
                       column(50, button(T_(0, 4), "#f-series", primary=False), tablet=50, mobile=100),
                       inner=True, gap="no", margin=DIM(8, 0, 0, 0)),
               tablet=80, mobile=100, space=22),
        image_url=content.IMG + "hero.jpg", image_pos="center right",
        overlay=grad_overlay(BLACK, 38, "rgba(10,10,10,0)", 74, 90),
        pad=PAD(100, 150), pad_t=PAD(80, 400, 24), pad_m=PAD(56, 235, 18), min_h=720, valign="middle", vcontent="center",
        bg_resp={"background_size_tablet": "contain", "background_position_tablet": "bottom center", "background_repeat_tablet": "no-repeat",
                 "background_size_mobile": "contain", "background_position_mobile": "bottom center", "background_repeat_mobile": "no-repeat"}))

    # 1 STATS --------------------------------------------------------------
    vals = [(T_(1, 0), T_(1, 1)), (T_(1, 2), T_(1, 3)), (T_(1, 4), T_(1, 5)), (T_(1, 6), T_(1, 7))]
    def stat(i, v, l):
        last = i == 3
        return column(25, heading(v, 46, 40, 32, tag="div", color=AMBER, lh=1.0),
                      text(f"<p>{strip_p(l)}</p>", STEEL, 12, ls=2, tr="uppercase", lh=1.4), tablet=50, mobile=50, space=2,
                      pad=DIM(26, 28, 26, 28), bg=PANEL, border=(DIM(0, 0 if last else 1, 1 if i > 1 else 0, 0), LINE))
    out.append(section(*[stat(i, v, l) for i, (v, l) in enumerate(vals)], width=1180,
                       margin=DIM(-64, 0, 0, 0), margin_t=DIM(0), margin_m=DIM(0), z=5, border=(DIM(3, 0, 0, 0), AMBER)))

    # 2 INTRO --------------------------------------------------------------
    out.append(section(
        txt_col(52, eyebrow(T_(2, 0)), body(T_(2, 1))),
        img_col(48, image(content.IMG + "square-underway.jpg", LV[2][2]["alt"])),
        bg=BLACK, gap="no", valign="middle", **SEC_PAD))

    # 3 F-SERIES -----------------------------------------------------------
    out.append(section(
        txt_col(56, eyebrow(T_(3, 0)), h2(T_(3, 1)), body(T_(3, 2)), icon_list(items(3, 3)), body(T_(3, 4))),
        img_col(44, image(content.IMG + "square-dock-day.jpg", LV[3][5]["alt"])),
        bg=INK, gap="no", valign="middle", anchor="f-series", **SEC_PAD))

    # 4 GENERAL ARRANGEMENT ------------------------------------------------
    out.append(section(
        column(100, eyebrow(T_(4, 0)), image(content.IMG + "ga-drawing.png", LV[4][1]["alt"], border=False, bg="#FFFFFF", pad=10),
               text(f"<p>{strip_p(T_(4, 2))}</p>", STEEL, 12, ls=2, tr="uppercase")),
        image_url=content.IMG + "bg-blueprint.jpg", overlay=solid_overlay(BLACK, 0.85),
        pad=PAD(80, 80), pad_t=PAD(64, 64, 24), pad_m=PAD(48, 48, 18)))

    # 5 SEARCH & RESCUE ----------------------------------------------------
    out.append(section(
        txt_col(56, eyebrow(T_(5, 0)), h2(T_(5, 1)), body(T_(5, 2)), h3(T_(5, 3)), body(T_(5, 4)),
               two_lists(items(5, 5)), body(T_(5, 6))),
        img_col(44, image(content.IMG + "square-dock-night.jpg", LV[5][7]["alt"])),
        bg=BLACK, gap="no", valign="middle", **SEC_PAD))

    # 6 MISSIONS -----------------------------------------------------------
    pairs = [(strip_p(T_(6, 3 + 2 * k)), T_(6, 4 + 2 * k)) for k in range(11)]
    def mcard(num, title, size=25, tablet=50):
        return column(size, heading(num, 18, 18, 18, tag="div", color=AMBER, ls=2),
                      heading(title, 24, 22, 22, tag="h3", lh=1.1, ls=0.6),
                      pad=DIM(24, 22, 24, 22), margin=DIM(6), bg=CARD, border=(DIM(1), LINE),
                      tablet=tablet, mobile=100, space=22)
    mrows = []
    for r_, row in enumerate([pairs[0:4], pairs[4:8], pairs[8:11]]):
        cs = [mcard(n, t) if not (r_ == 2 and k == 2) else mcard(n, t, 50, 100) for k, (n, t) in enumerate(row)]
        mrows.append(section(*cs, inner=True, gap="no", margin=DIM(0, -6, 0, -6)))
    out.append(section(
        column(100,
               section(column(66, eyebrow(T_(6, 0)), h2(T_(6, 1)), body(T_(6, 2))), inner=True, gap="no", margin=DIM(0, 0, 18, 0)),
               *mrows,
               section(column(66, body(T_(6, 25), margin=DIM(14, 0, 0, 0))), inner=True, gap="no")),
        bg=INK, anchor="missions", **SEC_PAD))

    # 7 MARINE FIREFIGHTING ------------------------------------------------
    lists3 = split_even(items(7, 5), 3)
    cols3 = [column(33.33, icon_list(l), tablet=50 if k < 2 else 100, mobile=100) for k, l in enumerate(lists3)]
    out.append(section(
        column(100,
               section(column(62, eyebrow(T_(7, 0)), h2(T_(7, 1)), body(T_(7, 2)), h3(T_(7, 3)), body(T_(7, 4))),
                       inner=True, gap="no", margin=DIM(0, 0, 18, 0)),
               section(*cols3, inner=True, gap="wide", margin=DIM(0, 0, 18, 0)),
               section(column(62, body(T_(7, 6))), inner=True, gap="no")),
        image_url=content.IMG + "bg-water.jpg", overlay=grad_overlay(BLACK, 45, "rgba(10,10,10,0.55)", 100, 90), **SEC_PAD))

    # 8 HDPE ---------------------------------------------------------------
    def hcard(k):
        b = 5 + 3 * k
        return column(25, heading(strip_p(T_(8, b)), 18, 18, 18, tag="div", color=AMBER, ls=2),
                      heading(T_(8, b + 1), 26, 24, 22, tag="h3", lh=1.1, ls=0.6),
                      text(T_(8, b + 2), STEEL, 14, lh=1.6),
                      pad=DIM(26, 22, 26, 22), margin=DIM(6), bg=PANEL, border=(DIM(1), LINE), tablet=50, mobile=100, space=12)
    out.append(section(
        column(100,
               section(txt_col(52, eyebrow(T_(8, 0)), h2(T_(8, 1)), body(T_(8, 2)), h3(T_(8, 3))),
                       img_col(48, image(content.IMG + "square-deck-detail.jpg", LV[8][4]["alt"])),
                       inner=True, gap="no", valign="middle", margin=DIM(0, 0, 36, 0)),
               section(*[hcard(k) for k in range(4)], inner=True, gap="no", margin=DIM(0, -6, 0, -6)),
               section(*[hcard(k) for k in range(4, 8)], inner=True, gap="no", margin=DIM(0, -6, 0, -6)),
               section(column(66, body(T_(8, 29), margin=DIM(18, 0, 0, 0))), inner=True, gap="no")),
        bg=BLACK, anchor="hdpe", **SEC_PAD))

    # 9 OTHER SERIES -------------------------------------------------------
    h4_style = f'<h4 style="color:{AMBER};font-family:Inter,sans-serif;font-size:16px;font-style:italic;font-weight:600;margin:18px 0 8px">'
    def scard(h_, lead, tg):
        return column(33.33, h3(T_(9, h_)), body(T_(9, lead), size=15),
                      toggle("Read more", T_(9, tg).replace("<h4>", h4_style)),
                      pad=DIM(28, 26, 24, 26), margin=DIM(8), bg=PANEL, border=(DIM(4, 0, 0, 0), AMBER), tablet=100, mobile=100, space=14)
    def series_row(title_i, cards):
        return [section(column(100, heading(T_(9, title_i), 36, 32, 28, tag="h3", lh=1.05)), inner=True, gap="no", margin=DIM(28, 0, 8, 0)),
                section(*[scard(*c) for c in cards], inner=True, gap="no", margin=DIM(0, -8, 0, -8))]
    out.append(section(
        column(100,
               section(column(66, eyebrow(T_(9, 0)), h2(T_(9, 1)), body(T_(9, 2))), inner=True, gap="no"),
               *series_row(3, [(5, 6, 7), (9, 10, 11), (13, 14, 15)]),
               *series_row(16, [(18, 19, 20), (22, 23, 24), (26, 27, 28)])),
        bg=INK, anchor="series", **SEC_PAD))

    # 10 CONFIGURED AROUND YOUR DEPARTMENT --------------------------------
    out.append(section(
        column(100,
               section(column(66, eyebrow(T_(10, 0)), h2(T_(10, 1)), body(T_(10, 2))), inner=True, gap="no", margin=DIM(0, 0, 22, 0)),
               icon_list(items(10, 3), inline=True, size=14),
               section(column(66, body(T_(10, 4), margin=DIM(22, 0, 0, 0))), inner=True, gap="no")),
        bg=BLACK, **SEC_PAD))

    # 11 CONTACT ------------------------------------------------------------
    out.append(section(
        txt_col(45, eyebrow(T_(11, 0)), h2(T_(11, 1)), body(T_(11, 2))),
        column(55, form(content.FORM_FIELDS), pad=DIM(30), bg=PANEL, border=(DIM(0, 0, 0, 4), AMBER)),
        grad_bg=("#14161A", BLACK), border=(DIM(3, 0, 0, 0), AMBER), gap="no", anchor="contact", **SEC_PAD))
    return out

# ------------------------------------------------------------------ preview renderer (reads the same settings)
def u(v):  return v.replace(BASE + "/", content.IMG)
def dim(d): return " ".join(f"{d[k]}{d['unit']}" for k in ("top", "right", "bottom", "left"))
def szs(d): return f"{d['size']}{d['unit']}"
def get(s, k, dev):
    return s.get(k + {"": "", "t": "_tablet", "m": "_mobile"}[dev])
def tcss(s, p, dev):
    d = []
    for k, prop, fn in (("font_family", "font-family", lambda v: f"'{v}',sans-serif"), ("font_size", "font-size", szs),
                        ("font_weight", "font-weight", str), ("line_height", "line-height", szs),
                        ("letter_spacing", "letter-spacing", szs), ("text_transform", "text-transform", str),
                        ("font_style", "font-style", str)):
        v = get(s, p + k, dev)
        if v is not None: d.append(f"{prop}:{fn(v)}")
    return ";".join(d)

class R:
    def __init__(self): self.css = {"": [], "t": [], "m": []}
    def add(self, dev, sel, decl):
        if decl: self.css[dev].append(f"{sel}{{{decl}}}")

def bgcss(s):
    d = []
    bg = s.get("background_background")
    if bg == "classic":
        if s.get("background_color"): d.append(f"background-color:{s['background_color']}")
        if s.get("background_image"):
            d.append(f"background-image:url('{u(s['background_image']['url'])}');background-position:{s.get('background_position', 'center center')};background-repeat:no-repeat;background-size:cover")
    elif bg == "gradient":
        d.append(f"background:linear-gradient({s['background_gradient_angle']['size']}deg,{s['background_color']},{s['background_color_b']})")
    return ";".join(d)

def bordercss(s):
    if s.get("border_border"):
        return f"border-style:solid;border-width:{dim(s['border_width'])};border-color:{s['border_color']}"
    return ""

def widget_html(w, r):
    s, i, t = w["settings"], w["id"], w["widgetType"]
    sel = f".elementor-element-{i}"
    cont = f"{sel}>.elementor-widget-container"
    if s.get("_margin"): r.add("", cont, f"margin:{dim(s['_margin'])}")
    if s.get("_padding"): r.add("", cont, f"padding:{dim(s['_padding'])}")
    if s.get("_background_color"): r.add("", cont, f"background:{s['_background_color']}")
    if s.get("align"): r.add("", sel, f"text-align:{s['align']}")
    wrap = lambda cls, inner: (f'<div class="elementor-element elementor-element-{i} elementor-widget elementor-widget-{cls}">'
                               f'<div class="elementor-widget-container">{inner}</div></div>')
    if t == "heading":
        tag = s["header_size"]
        for dev in ("", "t", "m"):
            d = tcss(s, "typography_", dev)
            if dev == "": d += f";color:{s['title_color']}"
            r.add(dev, f"{sel} .elementor-heading-title", d)
        return wrap("heading", f'<{tag} class="elementor-heading-title">{s["title"]}</{tag}>')
    if t == "text-editor":
        for dev in ("", "t", "m"):
            d = tcss(s, "typography_", dev)
            if dev == "": d += f";color:{s['text_color']}"
            r.add(dev, sel, d)
        return wrap("text-editor", s["editor"])
    if t == "button":
        d = (f"background:{s['background_color']};color:{s['text_color']};border:{s['border_width']['top']}px solid {s['border_color']};"
             f"border-radius:0;padding:{dim(s['text_padding'])};{tcss(s, 'typography_', '')}")
        r.add("", f"{sel} .elementor-button", d)
        r.add("", f"{sel} .elementor-button:hover", f"color:{s['hover_color']};background:{s['button_background_hover_color']};border-color:{s['button_hover_border_color']}")
        if s.get("align_mobile") == "justify": r.add("m", f"{sel} .elementor-button", "display:block;text-align:center")
        return wrap("button", f'<div class="elementor-button-wrapper"><a class="elementor-button elementor-button-link elementor-size-sm" href="{s["link"]["url"]}">'
                              f'<span class="elementor-button-content-wrapper"><span class="elementor-button-text">{escape(s["text"])}</span></span></a></div>')
    if t == "image":
        im = s["image"]
        d = f"width:{szs(s['width'])};height:auto;display:block"
        if s.get("image_border_border"): d += f";border:1px solid {s['image_border_color']}"
        r.add("", f"{sel} img", d)
        return wrap("image", f'<img src="{u(im["url"])}" alt="{escape(im["alt"])}">')
    if t == "icon-list":
        inline = s["view"] == "inline"
        r.add("", f"{sel} ul", "list-style:none;margin:0;padding:0" + (";display:flex;flex-wrap:wrap;gap:10px" if inline else ""))
        r.add("", f"{sel} li", f"display:flex;align-items:flex-start;color:{s['text_color']};{tcss(s, 'icon_typography_', '')}"
                              + (f";background:{PANEL};border:1px solid {LINE};padding:11px 18px" if inline else f";margin-bottom:{szs(s['space_between'])}"))
        r.add("", f"{sel} li:last-child", "margin-bottom:0")
        r.add("", f"{sel} .elementor-icon-list-icon", f"color:{s['icon_color']};width:{szs(s['icon_size'])};margin-right:{szs(s['text_indent'])};flex:none;margin-top:.35em")
        svg = '<svg viewBox="0 0 512 512" width="1em" height="1em" fill="currentColor"><path d="M173.9 439.4l-166.4-166.4c-10-10-10-26.2 0-36.2l36.2-36.2c10-10 26.2-10 36.2 0L192 312.7 432.1 72.6c10-10 26.2-10 36.2 0l36.2 36.2c10 10 10 26.2 0 36.2L210.1 439.4c-10 10-26.2 10-36.2 0z"/></svg>'
        lis = "".join(f'<li class="elementor-icon-list-item"><span class="elementor-icon-list-icon">{svg}</span><span class="elementor-icon-list-text">{x["text"]}</span></li>' for x in s["icon_list"])
        return wrap("icon-list", f'<ul class="elementor-icon-list-items">{lis}</ul>')
    if t == "toggle":
        tab = s["tabs"][0]
        r.add("", f"{sel} .elementor-tab-title", f"display:flex;align-items:center;justify-content:space-between;cursor:pointer;padding:16px 0 0;border-top:1px solid {s['border_color']};color:{s['title_color']};{tcss(s, 'title_typography_', '')}")
        r.add("", f"{sel} .elementor-tab-title:after", f"content:'+';display:grid;place-items:center;width:26px;height:26px;border:1px solid {s['icon_color']};color:{s['icon_color']};font-size:18px;letter-spacing:0")
        r.add("", f"{sel} .elementor-tab-title.elementor-active:after", f"content:'\\2212';background:{s['icon_active_color']};color:#0A0A0A")
        r.add("", f"{sel} .elementor-tab-content", f"display:none;padding:{dim(s['content_padding'])};color:{s['content_color']};{tcss(s, 'content_typography_', '')}")
        r.add("", f"{sel} .elementor-tab-content p", "margin:0 0 12px")
        r.add("", f"{sel} .elementor-tab-content ul", "margin:0 0 12px;padding-left:20px")
        return wrap("toggle", f'<div class="elementor-toggle"><div class="elementor-toggle-item"><div class="elementor-tab-title" role="button" tabindex="0">'
                              f'<span class="elementor-toggle-title">{escape(tab["tab_title"])}</span></div><div class="elementor-tab-content">{tab["tab_content"]}</div></div></div>')
    if t == "form":
        r.add("", f"{sel} .elementor-form-fields-wrapper", f"display:flex;flex-wrap:wrap;gap:{szs(s['row_gap'])}")
        r.add("", f"{sel} .elementor-field-group", "display:grid;gap:6px;align-content:start")
        r.add("", f"{sel} label", f"color:{s['label_color']};{tcss(s, 'label_typography_', '')}")
        r.add("", f"{sel} .elementor-field", f"width:100%;background:{s['field_background_color']};color:{s['field_text_color']};border:1px solid {s['field_border_color']};border-radius:0;padding:14px 16px;font:inherit;font-size:15px")
        r.add("", f"{sel} .elementor-field-textual:focus", f"outline:none;border-color:{AMBER}")
        r.add("", f"{sel} .elementor-button", f"background:{s['button_background_color']};color:{s['button_text_color']};border:2px solid {s['button_border_color']};border-radius:0;padding:{dim(s['button_text_padding'])};cursor:pointer;{tcss(s, 'button_typography_', '')}")
        r.add("", f"{sel} .elementor-button:hover", f"background:{s['button_background_hover_color']};color:{s['button_hover_color']};border-color:{s['button_hover_border_color']}")
        rows = []
        for f in s["form_fields"]:
            typ, cid, w_ = f["field_type"], f["custom_id"], f["width"]
            req = " required" if f["required"] else ""
            if typ == "textarea": fld = f'<textarea id="f-{cid}" class="elementor-field elementor-field-textual" rows="5"{req}></textarea>'
            elif typ == "select": fld = f'<select id="f-{cid}" class="elementor-field">' + "".join(f"<option>{escape(o)}</option>" for o in f["field_options"].split("\n")) + "</select>"
            else: fld = f'<input id="f-{cid}" type="{typ}" class="elementor-field elementor-field-textual"{req}>'
            r.add("", f"{sel} .fg-{cid}", "flex:1 1 calc(50% - 7px)" if w_ == "50" else "flex:1 1 100%")
            r.add("m", f"{sel} .fg-{cid}", "flex:1 1 100%")
            rows.append(f'<div class="elementor-field-group fg-{cid}"><label for="f-{cid}">{escape(f["field_label"])}</label>{fld}</div>')
        rows.append(f'<div class="elementor-field-group" style="flex:1 1 100%"><button type="submit" class="elementor-button">{escape(s["button_text"])}</button></div>')
        return wrap("form", '<form class="elementor-form" onsubmit="return false"><div class="elementor-form-fields-wrapper">' + "".join(rows) + "</div></form>")
    raise ValueError(t)

def column_html(c, r):
    s, i = c["settings"], c["id"]
    sel = f".elementor-element-{i}"
    r.add("", sel, f"width:{s['_inline_size']}%")
    r.add("t", sel, f"width:{s['_inline_size_tablet']}%")
    r.add("m", sel, f"width:{s['_inline_size_mobile']}%")
    d = []
    if s.get("padding"): d.append(f"padding:{dim(s['padding'])}")
    if s.get("margin"): d.append(f"margin:{dim(s['margin'])}")
    d.append(bgcss(s)); d.append(bordercss(s))
    if s.get("content_position") == "center": d.append("align-content:center")
    r.add("", f"{sel}>.elementor-element-populated", ";".join(x for x in d if x))
    if s.get("padding_tablet"): r.add("t", f"{sel}>.elementor-element-populated", f"padding:{dim(s['padding_tablet'])}")
    if s.get("padding_mobile"): r.add("m", f"{sel}>.elementor-element-populated", f"padding:{dim(s['padding_mobile'])}")
    r.add("", f"{sel}>.elementor-widget-wrap>.elementor-widget:not(:last-child)", f"margin-bottom:{s['space_between_widgets']}px")
    kids = "".join(element_html(k, r) for k in c["elements"])
    return f'<div class="elementor-column elementor-element elementor-element-{i}"><div class="elementor-widget-wrap elementor-element-populated">{kids}</div></div>'

def section_html(sec, r):
    s, i = sec["settings"], sec["id"]
    sel = f".elementor-element-{i}"
    d = []
    if s.get("padding"): d.append(f"padding:{dim(s['padding'])}")
    if s.get("margin"): d.append(f"margin:{dim(s['margin'])}")
    d.append(bgcss(s)); d.append(bordercss(s))
    if s.get("z_index"): d.append(f"z-index:{s['z_index']}")
    r.add("", sel, ";".join(x for x in d if x))
    if s.get("padding_tablet"): r.add("t", sel, f"padding:{dim(s['padding_tablet'])}")
    if s.get("padding_mobile"): r.add("m", sel, f"padding:{dim(s['padding_mobile'])}")
    for dev, suf in (("t", "_tablet"), ("m", "_mobile")):
        if s.get("margin" + suf): r.add(dev, sel, f"margin:{dim(s['margin' + suf])}")
        if s.get("background_size" + suf):
            r.add(dev, sel, f"background-size:{s['background_size' + suf]};background-position:{s.get('background_position' + suf, 'center center')};background-repeat:no-repeat")
    cont = f"{sel}>.elementor-container"
    if s.get("content_width"): r.add("", cont, f"max-width:{szs(s['content_width'])}")
    if s.get("custom_height"):
        r.add("", cont, f"min-height:{szs(s['custom_height'])}")
        if s.get("custom_height_mobile"): r.add("m", cont, f"min-height:{szs(s['custom_height_mobile'])}")
    pos = {"middle": "center", "top": "flex-start", "bottom": "flex-end"}.get(s.get("column_position"))
    if pos: r.add("", cont, f"align-items:{pos}")
    ov = ""
    if s.get("background_overlay_background"):
        a = f"{sel}>.elementor-background-overlay"
        if s["background_overlay_background"] == "gradient":
            r.add("", a, f"background:linear-gradient({s['background_overlay_gradient_angle']['size']}deg,{s['background_overlay_color']} {s['background_overlay_color_stop']['size']}%,{s['background_overlay_color_b']} {s['background_overlay_color_b_stop']['size']}%)")
        else:
            r.add("", a, f"background:{s['background_overlay_color']};opacity:{s['background_overlay_opacity']['size']}")
        ov = '<div class="elementor-background-overlay"></div>'
    kind = "inner" if sec["isInner"] else "top"
    boxed = "boxed" if s["layout"] == "boxed" else "full_width"
    aid = f' id="{s["_element_id"]}"' if s.get("_element_id") else ""
    cols = "".join(column_html(c, r) for c in sec["elements"])
    return (f'<section class="elementor-section elementor-{kind}-section elementor-section-{boxed} elementor-element elementor-element-{i}"{aid}>{ov}'
            f'<div class="elementor-container elementor-column-gap-{s["gap"]}">{cols}</div></section>')

def element_html(el, r):
    return section_html(el, r) if el["elType"] == "section" else widget_html(el, r)

PREVIEW_BASE = """*{box-sizing:border-box}html{scroll-behavior:smooth}body{margin:0;background:#0A0A0A;font-family:Inter,sans-serif}
img{max-width:100%}a{text-decoration:none}
.elementor-section{position:relative}
.elementor-container{display:flex;margin:0 auto;position:relative;width:100%}
.elementor-section-full_width>.elementor-container{max-width:none}
.elementor-column{position:relative;min-height:1px;display:flex}
.elementor-widget-wrap{position:relative;width:100%;flex-wrap:wrap;align-content:flex-start;display:flex}
.elementor-widget-wrap>.elementor-element{width:100%}
.elementor-column-gap-narrow>.elementor-column>.elementor-element-populated{padding:5px}
.elementor-column-gap-default>.elementor-column>.elementor-element-populated{padding:10px}
.elementor-column-gap-extended>.elementor-column>.elementor-element-populated{padding:15px}
.elementor-column-gap-wide>.elementor-column>.elementor-element-populated{padding:20px}
.elementor-column-gap-wider>.elementor-column>.elementor-element-populated{padding:30px}
.elementor-background-overlay{position:absolute;inset:0;pointer-events:none}
.elementor-heading-title{margin:0;padding:0}
.elementor-widget-text-editor p{margin:0 0 16px}.elementor-widget-text-editor p:last-child{margin-bottom:0}
.elementor-button{display:inline-block;text-align:center;transition:.2s}
.elementor-widget-container{position:relative}
@media (max-width:1024px){.elementor-container{flex-wrap:wrap}}
@media (max-width:767px){.elementor-container{flex-wrap:wrap}}
"""
PREVIEW_JS = """<script>document.querySelectorAll('.elementor-tab-title').forEach(function(t){function go(){var on=t.classList.toggle('elementor-active');t.nextElementSibling.style.display=on?'block':'none';}
t.addEventListener('click',go);t.addEventListener('keydown',function(e){if(e.key==='Enter'||e.key===' '){e.preventDefault();go();}});});</script>"""
FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
         '<link href="https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">')

def render_page(sections):
    r = R()
    body_html = "".join(section_html(s, r) for s in sections)
    css = PREVIEW_BASE + "".join(r.css[""]) + "@media (max-width:1024px){" + "".join(r.css["t"]) + "}@media (max-width:767px){" + "".join(r.css["m"]) + "}"
    return ("<!DOCTYPE html>\n<html lang=\"en\">\n<head>\n<meta charset=\"UTF-8\">\n<meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">\n"
            "<title>Fire Boats and Rescue Boats | Tideman Marine</title>\n"
            "<meta name=\"description\" content=\"Tideman Marine designs and manufactures mission-ready fire boats and rescue boats built from durable HDPE for fire departments, municipalities, harbor authorities, and public safety organizations.\">\n"
            f"{FONTS}\n<style>\n{css}\n</style>\n</head>\n<body>\n{body_html}\n{PREVIEW_JS}\n</body>\n</html>\n")

def template(content_, title):
    return {"content": content_, "page_settings": [], "version": "0.4", "title": title, "type": "page"}

def main():
    sections = build_sections()
    html = render_page(sections)
    open(os.path.join(ROOT, "index.html"), "w", encoding="utf-8").write(html)

    def b64(p):
        ext = os.path.splitext(p)[1][1:].replace("jpg", "jpeg")
        return f"data:image/{ext};base64," + base64.b64encode(open(os.path.join(ROOT, p), "rb").read()).decode()
    open(os.path.join(ROOT, "tideman-fire-rescue-standalone.html"), "w", encoding="utf-8").write(
        re.sub(r"assets/img/[\w.-]+", lambda m: b64(m.group(0)), html))

    p1 = os.path.join(ROOT, "tideman-fire-rescue-elementor.json")
    json.dump(template(sections, "Fire Rescue Boats - Tideman Marine"), open(p1, "w", encoding="utf-8"), ensure_ascii=False, separators=(",", ":"))
    os.makedirs(os.path.join(ROOT, "tests"), exist_ok=True)
    json.dump(template([sections[0]], "Test hero only"), open(os.path.join(ROOT, "tests", "test-hero-only.json"), "w", encoding="utf-8"), ensure_ascii=False, separators=(",", ":"))
    print("OK html", len(html), "bytes | json", os.path.getsize(p1), "bytes | image base:", BASE)

main()
