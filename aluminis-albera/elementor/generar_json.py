"""Genera plantillas de pagina de Elementor (.json) a partir del diseno de Aluminis l'Albera."""
import json, os, hashlib, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = '/home/user/curso-frontend-developer-Javascript/aluminis-albera/elementor'
BASE = os.environ.get('IMG_BASE', 'https://raw.githubusercontent.com/naniiqr/curso-frontend-developer-Javascript/claude/cool-maxwell-eomrra/aluminis-albera/img/')
os.makedirs(OUT, exist_ok=True)

# datos compartidos con la maqueta HTML
src = open(f'{HERE}/build.py').read()
exec(src[src.index('PRODUCTS = ['):src.index('def product_card')])
exec(src[src.index('PROJECTS = ['):src.index('# ----', src.index('PROJECTS = ['))])

SLUG = {'index': '/', 'productes': '/productes/', 'projectes': '/projectes/', 'sobre-nosaltres': '/sobre-nosaltres/', 'contacte': '/contacte/',
        'finestres-rpt-55': '/finestres-rpt-55/', 'portes-entrada-particular': '/portes-entrada-particular/',
        'portes-entrada-ocultec': '/portes-entrada-ocultec/', 'portes-entrada-comercial': '/portes-entrada-comercial/'}
def link(h):
    return SLUG.get(h.replace('.html', ''), '#')

BG, BG2, RED, MUTED, TXT, WHITE = '#0c0c0d', '#131315', '#e4152d', '#a9a9ae', '#cfcfd2', '#ffffff'
SANS, SERIF, SCRIPT = 'Inter', 'Cormorant Garamond', 'Caveat'
_n = [0]
def uid():
    _n[0] += 1
    return hashlib.md5(str(_n[0]).encode()).hexdigest()[:7]
def img_url(n):
    return BASE + n + ('' if n.endswith('.png') else '.jpg')
def sz(v, unit='px'):
    return {'unit': unit, 'size': v, 'sizes': []}
def pad(t, r=None, b=None, l=None):
    r = t if r is None else r; b = t if b is None else b; l = r if l is None else l
    return {'unit': 'px', 'top': str(t), 'right': str(r), 'bottom': str(b), 'left': str(l), 'isLinked': False}
def typo(prefix, size, weight=400, family=SANS, transform=None, spacing=None, lh=None, size_m=None):
    p = prefix
    d = {f'{p}typography_typography': 'custom', f'{p}typography_font_family': family,
         f'{p}typography_font_size': sz(size), f'{p}typography_font_weight': str(weight)}
    if size_m: d[f'{p}typography_font_size_mobile'] = sz(size_m)
    if transform: d[f'{p}typography_text_transform'] = transform
    if spacing is not None: d[f'{p}typography_letter_spacing'] = sz(spacing)
    if lh: d[f'{p}typography_line_height'] = sz(lh, 'em')
    return d
def icon(v):
    lib = 'fa-brands' if v.startswith('fab ') else 'fa-regular' if v.startswith('far ') else 'fa-solid'
    return {'value': v, 'library': lib}
def lnk(u):
    return {'url': u, 'is_external': '', 'nofollow': '', 'custom_attributes': ''}

# ---------------------------------------------------------------- widgets
def widget(t, settings):
    return {'id': uid(), 'elType': 'widget', 'widgetType': t, 'settings': settings, 'elements': []}
def heading(text, size=32, color=WHITE, tag='h2', align='left', weight=400, family=SANS, transform=None, spacing=None, size_m=None, url=None, mb=None, lh=1.15):
    s = {'title': text, 'header_size': tag, 'align': align, 'title_color': color, **typo('', size, weight, family, transform, spacing, lh, size_m or max(20, int(size * .72)))}
    if url: s['link'] = lnk(url)
    if mb is not None: s['_margin'] = pad(0, 0, mb, 0)
    return widget('heading', s)
def text(html, size=15, color=TXT, align='left', family=SANS, mb=None, weight=400):
    s = {'editor': html, 'text_color': color, 'align': align, **typo('', size, weight, family, lh=1.65)}
    if mb is not None: s['_margin'] = pad(0, 0, mb, 0)
    return widget('text-editor', s)
def eyebrow(t, color=MUTED):
    return heading(t, 11, color, 'span', transform='uppercase', spacing=3.5, mb=6)
def button(label, url, ghost=False, align='left', family=SANS, serif=False, size=12):
    s = {'text': label, 'link': lnk(url), 'align': align, 'size': 'md', 'button_text_color': WHITE,
         'background_color': 'rgba(0,0,0,0)' if ghost else ('#8f1a28' if serif else RED),
         'border_border': 'solid', 'border_width': pad(1), 'border_color': 'rgba(255,255,255,.4)' if ghost else ('#8f1a28' if serif else RED),
         'border_radius': pad(3 if serif else 2), 'text_padding': pad(14, 26),
         'selected_icon': icon('fas fa-arrow-right'), 'icon_align': 'right', 'icon_indent': sz(10),
         **typo('', 14 if serif else size, 400 if serif else 600, family, None if serif else 'uppercase', 0 if serif else 1)}
    return widget('button', s)
def buttons_html(items):
    out = ''
    for label, url, ghost in items:
        st = f'display:inline-block;margin:0 14px 10px 0;padding:14px 24px;font:600 12px Inter,sans-serif;letter-spacing:.08em;text-transform:uppercase;color:#fff;text-decoration:none;border:1px solid {"rgba(255,255,255,.4)" if ghost else RED};background:{"transparent" if ghost else RED};border-radius:2px'
        out += f'<a href="{url}" style="{st}">{label} &rarr;</a>'
    return widget('html', {'html': out})
def image(name, height=None, url=None, lightbox=False, align='center', mobile_h=None):
    s = {'image': {'url': img_url(name), 'id': ''}, 'image_size': 'full', 'align': align, 'width': sz(100, '%'),
         'link_to': 'file' if lightbox else ('custom' if url else 'none')}
    if lightbox: s['open_lightbox'] = 'yes'
    if url and not lightbox: s['link'] = lnk(url)
    if height:
        s['height'] = sz(height); s['object-fit'] = 'cover'
        s['height_mobile'] = sz(mobile_h or int(height * .7))
    return widget('image', s)
def icon_box(ic_, title, desc, pos='left', align='left', icon_color=RED, isize=30, tsize=13, dsize=12, tweight=600, tcolor=WHITE, dcolor=MUTED, family=SANS):
    s = {'selected_icon': icon(ic_), 'title_text': title, 'description_text': desc, 'position': pos, 'text_align': align, 'title_size': 'h3',
         'primary_color': icon_color, 'icon_size': sz(isize), 'icon_space': sz(14), 'title_color': tcolor, 'description_color': dcolor,
         **typo('title_', tsize, tweight, family), **typo('description_', dsize, 400, family)}
    return widget('icon-box', s)
def icon_list(items, color=RED, size=14):
    return widget('icon-list', {'icon_list': [{'text': t, 'selected_icon': icon('fas fa-check'), '_id': uid()} for t in items],
                                'icon_color': color, 'text_color': WHITE, 'space_between': sz(6), 'icon_size': sz(13), **typo('text_', 13)})
def html(h):
    return widget('html', {'html': h})
def spacer(h=20):
    return widget('spacer', {'space': sz(h)})
def divider(color='rgba(255,255,255,.12)'):
    return widget('divider', {'color': color, 'weight': sz(1), 'gap': sz(10)})
def accordion(items, serif=False):
    return widget('accordion', {'tabs': [{'tab_title': q, 'tab_content': f'<p>{a}</p>', '_id': uid()} for q, a in items],
        'title_color': WHITE, 'tab_active_color': RED, 'content_color': TXT, 'border_color': 'rgba(255,255,255,.12)', 'border_width': sz(1),
        'icon_color': RED, 'icon_active_color': RED, **typo('title_', 15), **typo('content_', 13.5)})

# ---------------------------------------------------------------- layout
def column(widgets, size=100, bg=None, p=None, valign='top', tablet=None, mobile=100, extra=None):
    s = {'_column_size': size, '_inline_size': None, 'content_position': valign if valign != 'top' else 'top',
         '_inline_size_mobile': mobile}
    if tablet: s['_inline_size_tablet'] = tablet
    if bg: s.update({'background_background': 'classic', 'background_color': bg})
    if p is not None: s['padding'] = p
    if extra: s.update(extra)
    return {'id': uid(), 'elType': 'column', 'settings': s, 'elements': widgets, 'isInner': False}
def section(cols, bg=None, p=(70, 0), gap='default', bgimg=None, overlay=None, minh=None, middle=False, extra=None, boxed=True, border=None):
    s = {'layout': 'boxed' if boxed else 'full_width', 'gap': gap, 'padding': pad(*p) if isinstance(p, tuple) else p,
         'padding_mobile': pad(40, 18), 'content_position': 'middle' if middle else 'top'}
    if boxed: s['content_width'] = sz(1180)
    if bg: s.update({'background_background': 'classic', 'background_color': bg})
    if bgimg:
        s.update({'background_background': 'classic', 'background_image': {'url': img_url(bgimg), 'id': ''}, 'background_position': 'center right',
                  'background_repeat': 'no-repeat', 'background_size': 'cover'})
    if overlay:
        s.update({'background_overlay_background': 'gradient', 'background_overlay_color': overlay[0], 'background_overlay_color_b': overlay[1],
                  'background_overlay_gradient_angle': sz(overlay[2], 'deg'), 'background_overlay_color_stop': sz(overlay[3], '%'),
                  'background_overlay_opacity': sz(1, '')})
    if minh:
        s.update({'height': 'min-height', 'custom_height': sz(minh), 'custom_height_mobile': sz(int(minh * .85))})
    if border:
        s.update({'border_border': 'solid', 'border_width': {'unit': 'px', 'top': '0', 'right': '0', 'bottom': '1', 'left': '0', 'isLinked': False}, 'border_color': border})
    if extra: s.update(extra)
    return {'id': uid(), 'elType': 'section', 'settings': s, 'elements': cols, 'isInner': False}
def row(widgets_list, size=None, **kw):
    """equal-width columns, one widget list per column"""
    n = len(widgets_list); size = size or round(100 / n, 2)
    tab = 50 if n >= 3 else None
    return section([column(w, size, tablet=tab) for w in widgets_list], **kw)

# ---------------------------------------------------------------- shared blocks
NAV = [('index', 'Inici'), ('productes', 'Productes'), ('projectes', 'Projectes'), ('sobre-nosaltres', 'Sobre nosaltres'), ('contacte', 'Contacte')]
def header(active):
    links = ''.join(f'<a href="{link(k)}" style="color:#fff;text-decoration:none;padding:8px 0;border-bottom:2px solid {RED if k == active else "transparent"}">{t}</a>' for k, t in NAV)
    nav = html(f'<nav style="display:flex;gap:30px;justify-content:center;flex-wrap:wrap;font:500 11px Inter,sans-serif;letter-spacing:.1em;text-transform:uppercase">{links}</nav>')
    return section([column([image('logo.png', None, url=link('index'))], 20, valign='middle', extra={'_element_width_': ''}),
                    column([nav], 55, valign='middle'),
                    column([button('Demana pressupost', link('contacte'), align='right', size=11)], 25, valign='middle')],
                   bg=BG, p=(14, 0), middle=True, border='rgba(255,255,255,.12)')
def footer():
    nav = ''.join(f'<a href="{link(k)}" style="color:#fff;text-decoration:none;margin-right:22px">{t}</a>' for k, t in NAV)
    return [section([column([image('logo.png', None, url=link('index'))], 18, valign='middle'),
                     column([html(f'<div style="font:500 10px Inter,sans-serif;letter-spacing:.08em;text-transform:uppercase">{nav}</div>')], 47, valign='middle'),
                     column([icon_box('fas fa-map-marker-alt', 'Figueres (Girona)', '', isize=16, tsize=12, tweight=400)], 20, valign='middle'),
                     column([html('<div style="text-align:right;font:12px Inter,sans-serif"><a href="#" style="color:#fff;margin-left:14px">Facebook</a><a href="#" style="color:#fff;margin-left:14px">Instagram</a><a href="#" style="color:#fff;margin-left:14px">LinkedIn</a></div>')], 15, valign='middle')],
                    bg='#0a0a0b', p=(30, 0), middle=True, border='rgba(255,255,255,.12)'),
            section([column([html('<div style="text-align:right;font:10px Inter,sans-serif;color:#a9a9ae"><a href="#" style="color:#a9a9ae;margin-left:18px">Av&iacute;s legal</a><a href="#" style="color:#a9a9ae;margin-left:18px">Pol&iacute;tica de privacitat</a><a href="#" style="color:#a9a9ae;margin-left:18px">Cookies</a></div>')])],
                    bg='#0a0a0b', p=(10, 0))]
def cta(title='Tens un projecte en ment?', sub="Parlem-ne i t'oferim una solució a mida.", serif=False, big=False):
    fam = SERIF if serif else SANS
    left = [heading(title, 40 if big else 28, family=fam, mb=8), text(sub, 15, '#dddddd', mb=18), button('Demana pressupost', link('contacte'), serif=serif, family=fam)]
    contacts = [icon_box('fas fa-phone', "Truca'ns", '972 50 00 00', isize=22, tsize=12, dsize=11),
                icon_box('fab fa-whatsapp', 'WhatsApp', "Envia'ns un missatge", isize=22, tsize=12, dsize=11),
                icon_box('fas fa-envelope', 'Escriu-nos', 'info@aluminisalbera.com', isize=22, tsize=12, dsize=11)]
    script = [heading('Junts<br>construïm<br>millors espais', 30, WHITE, 'div', 'right', 500, SCRIPT, size_m=24)]
    return section([column(left, 45, valign='middle'), column(contacts, 35, valign='middle'), column(script, 20, valign='middle')],
                   bgimg='sunset', overlay=(BG, 'rgba(12,12,13,0)', 90, 55), p=(48, 0), middle=True, bg='#160a0d')
def crumbs(*items):
    out = ' &nbsp;/&nbsp; '.join(f'<a href="{link(h)}" style="color:#a9a9ae;text-decoration:none">{t}</a>' if h else f'<span style="color:#a9a9ae">{t}</span>' for h, t in items)
    return html(f'<div style="font:11px Inter,sans-serif;margin-bottom:14px">{out}</div>')
def hero(img, title, lead='', btns=None, cr=None, eb='', script=None, minh=560, serif=False, pos='center right'):
    fam = SERIF if serif else SANS
    w = []
    if cr: w.append(cr)
    if eb: w.append(eyebrow(eb))
    w.append(heading(title, 60 if minh > 450 else 52, WHITE, 'h1', weight=400 if serif else 300, family=fam, mb=18))
    if lead: w.append(text(lead, 15, '#e6e6e8', mb=24))
    if btns: w.append(btns)
    cols = [column(w, 55, valign='middle')]
    if script: cols.append(column([heading(script, 28, WHITE, 'div', 'right', 500, SCRIPT)], 45, valign='bottom'))
    else: cols.append(column([spacer(10)], 45))
    sec = section(cols, bgimg=img, overlay=(BG, 'rgba(12,12,13,0.15)', 90, 45), minh=minh, p=(70, 0), middle=True, bg=BG)
    sec['settings']['background_position'] = pos
    return sec
def usp(items, serif=False):
    n = len(items)
    return section([column([icon_box(i, b, s)], round(100 / n, 2), tablet=50) for i, b, s in items], bg=BG2, p=(30, 0), border='rgba(255,255,255,.12)')
def sec_head(title, sub='', right=None, serif=False, eb=''):
    fam = SERIF if serif else SANS
    left = ([eyebrow(eb)] if eb else []) + [heading(title, 36 if serif else 30, family=fam, weight=400 if serif else 500, mb=6)] + ([text(sub, 14, MUTED)] if sub else [])
    cols = [column(left, 70, valign='middle')]
    if right: cols.append(column([right], 30, valign='middle'))
    return section(cols, p=(0, 0, 24, 0) if False else (60, 0, 10, 0))
def link_text(label, url):
    return html(f'<div style="text-align:right"><a href="{url}" style="color:#fff;text-decoration:none;font:600 11px Inter,sans-serif;letter-spacing:.06em;text-transform:uppercase">{label} &rarr;</a></div>')

def tile(name, title, tag, url, desc=None, height=210):
    ws = [image(name, height, url=url), spacer(6), heading(title, 12, WHITE, 'h3', weight=600, transform='uppercase', spacing=.4, url=url, mb=2),
          text(tag, 11.5, MUTED, mb=0)]
    if desc: ws.append(text(desc, 12.5, MUTED))
    ws.append(spacer(10))
    for w in ws[2:]:
        if w['widgetType'] != 'spacer': w['settings']['_padding'] = pad(0, 14, 0, 14)
    return column(ws, 25, bg=BG2, tablet=50, extra={'padding': pad(0, 0, 0, 0)})
def grid_rows(cells, per=4, gap='narrow'):
    rows = []
    for i in range(0, len(cells), per):
        chunk = cells[i:i + per]
        for c in chunk: c['settings']['_column_size'] = round(100 / per, 2)
        rows.append(section(chunk, p=(6, 0), gap=gap))
    return rows
def photo_grid(names, per=4, h=230, lightbox=True, gap='narrow'):
    cells = [column([image(n, h, lightbox=lightbox)], 100 / per, tablet=50, mobile=50) for n in names]
    return grid_rows(cells, per, gap)

def page_json(title, content, header_active):
    content = [header(header_active)] + content + footer()
    return {'version': '0.4', 'title': title, 'type': 'page', 'content': content,
            'page_settings': {'template': 'elementor_canvas', 'hide_title': 'yes', 'background_background': 'classic', 'background_color': BG}}
def save(fname, title, content, active):
    json.dump(page_json(title, content, active), open(f'{OUT}/{fname}.json', 'w'), ensure_ascii=False, indent=1)

# ================================================================ PAGES
def p_index():
    c = [hero('hero-home', 'Espais que milloren la <span style="color:#e4152d">teva vida</span>',
              "Finestres, portes, tancaments i pèrgoles d'alumini i PVC per a habitatges, comços i projectes professionals.",
              buttons_html([('Demana pressupost', link('contacte'), False), ('Veure projectes', link('projectes'), True)]), eb='Més que tancaments'),
         usp([('fas fa-gem', "+30 anys d'experiència", 'Al teu costat des del primer dia.'), ('fas fa-cog', 'Fabricació a mida', 'Solucions adaptades a cada projecte.'),
              ('fas fa-hard-hat', 'Instal·lació pròpia', 'Equip professional i qualificat.'), ('fas fa-leaf', 'Compromís i sostenibilitat', 'Eficiència energètica i respecte pel medi ambient.')]),
         sec_head('Els nostres productes', right=link_text('Veure tots els productes', link('productes')))]
    cells = [tile(p[3], p[1], p[2], link(p[5]) if p[5] else link('productes')) for p in PRODUCTS]
    cells.append(tile('prod-refine', 'Refine', 'Sin necesidad de escuadras', '#'))
    c += grid_rows(cells)
    c.append(sec_head('Projectes que parlen <span style="color:#e4152d">per nosaltres</span>', "Descobreix alguns dels nostres treballs i deixa't inspirar per les possibilitats.", link_text('Veure tots els projectes', link('projectes'))))
    c.append(section([column([image(i, 230, url=link('projectes')), text(f'<b style="color:#fff">{t}</b><br><span style="font-size:11px;color:#a9a9ae">{s}</span>', 12.5)], 33.33, tablet=50) for t, s, i, _ in PROJECTS[:3]], gap='narrow', p=(6, 0)))
    c.append(section([column([heading("Per què escollir Aluminis l'Albera?", 20, weight=500, mb=18)], 100)], bg=BG2, p=(40, 0, 0, 0)))
    c.append(section([column([icon_box(i, b, s)], 25, tablet=50) for i, b, s in [('fas fa-gem', 'Qualitat garantida', 'Treballem amb els millors marques del mercat.'),
        ('fas fa-users', 'Assessorament personalitzat', "T'ajudem a trobar la millor solució."), ('fas fa-file-signature', 'Complim terminis', 'Serietàt i compromís en cada projecte.'),
        ('fas fa-leaf', 'Solucions sostenibles', 'Més benestar, més eficiència energètica.')]], bg=BG2, p=(10, 0, 40, 0)))
    half = lambda img, t, d, u, bg='#e9e9ea': column([image(img, 190), ], 25, tablet=50)
    c.append(section([column([image('seg-particulars', 190)], 20, tablet=50),
                      column([text('<span style="color:#444;font-size:11px">Solucions per a</span>', 11, '#444', mb=0), heading('particulars', 24, '#111', 'h3', weight=600, mb=6),
                              text('Més confort, seguretat i disseny per a la teva llar.', 12, '#333', mb=8), html(f'<a href="{link("productes")}" style="color:{RED};font:600 12px Inter,sans-serif;text-decoration:none">Saber més</a>')], 30, bg='#e9e9ea', valign='middle', p=pad(20, 28, 20, 28), tablet=50),
                      column([text('<span style="color:#444;font-size:11px">Solucions per a</span>', 11, '#444', mb=0), heading('professionals', 24, '#111', 'h3', weight=600, mb=6),
                              text('Equip professional i estructures per a comços, oficines i grans projectes.', 12, '#333', mb=8), html(f'<a href="{link("projectes")}" style="color:{RED};font:600 12px Inter,sans-serif;text-decoration:none">Saber més</a>')], 30, bg='#e9e9ea', valign='middle', p=pad(20, 28, 20, 28), tablet=50),
                      column([image('seg-professionals', 190)], 20, tablet=50)], boxed=False, gap='no', p=(0, 0), bg='#e9e9ea'))
    c.append(sec_head('Instagram', right=None))
    c += photo_grid([f'insta-{n:02d}' for n in range(1, 19)], per=6, h=190, lightbox=False, gap='narrow')
    c.append(cta())
    save('inici', 'Inici', c, 'index')

def p_productes():
    c = [hero('hero-home', 'Els nostres <span style="color:#e4152d">productes</span>', "Tot el que necessites per tancar, protegir i embellir els teus espais, fabricat a mida amb alumini i PVC.",
              None, crumbs(('index', 'Inici'), (None, 'Productes')), minh=380)]
    c.append(section([column([spacer(10)])], p=(20, 0, 0, 0)))
    cells = [tile(p[3], p[1], p[2], link(p[5]) if p[5] else '#', p[6], 220) for p in PRODUCTS]
    c += grid_rows(cells, per=3, gap='wider')
    c.append(section([column([eyebrow('Refine'), heading("Sense necessitat d'escaires", 32, weight=400, mb=14),
                              text("Una solució de tancament neta i precisa que simplifica el muntatge i millora l'acabat final.", 15, TXT, mb=18), button('Demana informació', link('contacte'))], 50, valign='middle'),
                      column([image('prod-refine', 320)], 50, valign='middle')], bg=BG2, p=(70, 0), gap='extended'))
    c.append(cta("No trobes el que busques?", "Fem solucions a mida per a qualsevol projecte."))
    save('productes', 'Productes', c, 'productes')

def p_projectes():
    S = dict(family=SERIF)
    c = [hero('portes-hero', 'Projectes', 'La primera impressió de casa teva, feta a mida.', button('Demana pressupost', link('contacte'), serif=True, family=SERIF),
              crumbs(('index', 'Inici'), (None, 'Projectes')), minh=520, serif=True),
         section([column([icon_box('fas fa-clone', 'Disseny personalitzat', "Portes d'entrada fetes a mida per adaptar-se al teu estil i espai.", 'top', 'center', WHITE, 32, 22, 13, 400, family=SERIF)], 33.33, tablet=100),
                  column([icon_box('fas fa-palette', 'Colors i acabats', "Una àmplia gamma de colors, textures i acabats d'alta qualitat.", 'top', 'center', WHITE, 32, 22, 13, 400, family=SERIF)], 33.33, tablet=100),
                  column([icon_box('fas fa-sun', 'Llum i caràcter', "Amb o sense vidre, per aconseguir l'equilibri perfecte entre privacitat i llum natural.", 'top', 'center', WHITE, 32, 22, 13, 400, family=SERIF)], 33.34, tablet=100)], bg=BG2, p=(44, 0)),
         section([column([image('portes-entrada', 560)], 50, tablet=100),
                  column([eyebrow('Refine'), heading('Una entrada que parla de tu', 40, family=SERIF, mb=18),
                          text("Les nostres portes d'entrada combinen disseny, funcionalitat i altes prestacions per oferir-te una solució pensada per a tu.", 14, TXT, mb=12),
                          text("Fabriquem portes d'alumini a mida, amb una àmplia gamma de dissenys, colors i acabats, que s'integren perfectament amb l'arquitectura de la teva llar, sigui moderna o tradicional.", 14, TXT, mb=12),
                          text("Pots optar per dissenys totalment tancats o amb elements de vidre, per aportar llum, amplitud i un caràcter únic a l'entrada.", 14, TXT, mb=12),
                          text("Cada porta es personalitza fins al darrer detall per reflectir el teu estil i donar la benvinguda a casa teva amb caràcter.", 14, TXT, mb=20),
                          button('Descobreix el producte', link('portes-entrada-ocultec'), serif=True, family=SERIF)], 50, valign='middle', p=pad(50, 56, 50, 56))],
                 p=(0, 0), gap='no', boxed=False, bg=BG),
         sec_head('Projectes que parlen per nosaltres', "Portes d'entrada que combinen disseny, funcionalitat i estil, integrades en habitatges i espais comercials amb personalitat.", serif=True, eb='Projectes')]
    cards = [('portes-particular', "Portes d'Entrada Particular", 'portes-entrada-particular'), ('portes-ocultec', "Portes d'Entrada Particular OCULTEC", 'portes-entrada-ocultec'),
             ('portes-comercial', "Portes d'Entrada Comercial", 'portes-entrada-comercial')]
    c.append(section([column([image(i, 480, url=link(h)), html(f'<div style="margin-top:-90px;position:relative;padding:0 24px 24px;background:linear-gradient(0deg,#08080a,transparent)"><div style="font:400 28px/1.1 Cormorant Garamond,serif;color:#fff;margin-bottom:8px">{t}</div><a href="{link(h)}" style="color:#d6283a;font:400 15px Cormorant Garamond,serif;text-decoration:none">Veure galeria &rarr;</a></div>')], 33.33, tablet=100) for i, t, h in cards],
                     gap='narrow', p=(6, 0), boxed=False))
    c.append(section([column([eyebrow('Projecte'), heading('Parlem del teu projecte', 42, family=SERIF, mb=10), text("T'assessorem per trobar la solució de portes d'entrada que millor s'adapti al teu habitatge. Sense compromis.", 15, TXT, mb=20),
                              button('Demana pressupost', link('contacte'), serif=True, family=SERIF)], 55, valign='middle'), column([spacer(10)], 45)],
                     bgimg='sunset', overlay=(BG, 'rgba(12,12,13,0)', 90, 55), p=(80, 0), bg='#1c0c10'))
    c.append(cta(serif=True))
    save('projectes', 'Projectes', c, 'projectes')

def p_about():
    faq = [("Fabriqueu a mida?", "Sí. Cada projecte es dissenya i es fabrica segons les mides, els colors i els acabats que necessites, tant per a obra nova com per a rehabilitació."),
           ("Us ocupeu també de la instal·lació?", "Disposem d'equip propi de muntatge. Així coordinem tot el procés, de la presa de mides a la instal·lació final, i responem d'un únic resultat."),
           ("Quins materials utilitzeu?", "Treballem amb alumini amb trencament de pont tèrmic i PVC de les millors marques del mercat, combinats amb vidres adaptats a cada necessitat d'aïllament i seguretat."),
           ("Quant triga un projecte?", "Depèn de la tipologia i de la mida, però sempre et donem un termini clar des del pressupost i el complim."),
           ("Oferiu garantia i servei posterior?", "Sí. Tots els treballs tenen garantia i ens mantenim al teu costat un cop acabada l'obra, amb manteniment i atenció personalitzada.")]
    c = [hero('seg-professionals', 'Més de 30 anys construint <span style="color:#e4152d">millors espais</span>', "Som una empresa familiar de l'Empordà especialitzada en tancaments d'alumini i PVC fabricats a mida.",
              buttons_html([('Parlem del teu projecte', link('contacte'), False), ('Veure projectes', link('projectes'), True)]), crumbs(('index', 'Inici'), (None, 'Sobre nosaltres')), script='Junts construïm<br>millors espais', minh=400),
         section([column([eyebrow('La nostra història'), heading('Experiència que et dona tranquil·litat', 34, mb=18),
                          text("Aluminis l'Albera va nèixer fa més de tres dècades a Figueres amb una idea clara: oferir tancaments ben fets, amb un tracte proper i honest. Des d'aleshores hem crescut de la mà dels nostres clients, sempre mantenint l'esperit d'empresa familiar.", 15, TXT, mb=12),
                          text("Avui fabriquem i instal·lem finestres, portes d'entrada, persianes, pèrgoles, baranes i mampares per a particulars, comços i grans projectes professionals de tot l'Empordà i les comarques gironines.", 15, TXT, mb=12),
                          text("Treballem amb les millors marques del mercat i amb un equip propi, de manera que controlem tot el procés: de l'assessorament inicial fins al darrer detall de la instal·lació.", 15, TXT, mb=20),
                          button('Parlem del teu projecte', link('contacte'))], 50, valign='middle'),
                  column([image('seg-particulars', 400)], 50, valign='middle')], p=(80, 0), gap='extended'),
         section([column([eyebrow('El que ens mou'), heading('Missió i visió', 30, weight=500, mb=24)], 100)], bg=BG2, p=(70, 0, 10, 0)),
         section([column([heading('01', 30, RED, 'div', weight=300, mb=10), heading('La nostra missió', 18, WHITE, 'h3', weight=500, mb=10),
                          text("Crear espais més confortables, segurs i eficients mitjançant solucions de tancament d'alta qualitat, adaptades a l'estil i a les necessitats de cada persona i de cada projecte.", 13.5, TXT)], 50, bg=BG, p=pad(30, 28, 30, 28)),
                  column([heading('02', 30, RED, 'div', weight=300, mb=10), heading('La nostra visió', 18, WHITE, 'h3', weight=500, mb=10),
                          text("Ser l'empresa de referència en tancaments d'alumini i PVC a les comarques gironines, reconeguda per la qualitat del producte, la proximitat del servei i la confiança dels clients.", 13.5, TXT)], 50, bg=BG, p=pad(30, 28, 30, 28))],
                 bg=BG2, p=(0, 0, 70, 0), gap='wide'),
         sec_head('Per què confiar en nosaltres', 'Experiència, qualitat i proximitat en cada fase del projecte.')]
    why = [('fas fa-gem', 'Qualitat garantida', 'Treballem amb els millors marques del mercat i seleccionem cada material amb criteri. Totes les nostres obres compten amb garantia.'),
           ('fas fa-users', 'Assessorament personalitzat', "Escoltem les teves necessitats, visitem l'espai i t'ajudem a triar la solució que millor s'adapta al teu habitatge o negoci."),
           ('fas fa-file-signature', 'Compliment de terminis', 'Planifiquem cada obra amb rigor i ens comprometem amb unes dates clares des del primer pressupost.'),
           ('fas fa-leaf', 'Solucions sostenibles', "Perfils amb trencament de pont tèrmic i vidres d'alt rendiment que milloren l'aïllament i redueixen el consum energètic."),
           ('fas fa-cog', 'Fabricació a mida', 'Cada peça es dissenya i es fabrica segons les teves mides, colors i acabats. Sense solucions estàndard forçades.'),
           ('fas fa-hard-hat', 'Instal·lació pròpia', "El nostre equip professional i qualificat s'encarrega del muntatge i deixa l'obra neta i a punt.")]
    for k in (0, 3):
        c.append(section([column([icon_box(i, b, s)], 33.33, tablet=100) for i, b, s in why[k:k + 3]], p=(14, 0), gap='wide'))
    c.append(sec_head('Com treballem', "Un procés clar i transparent perquè sàpigues en tot moment en quin punt és el teu projecte."))
    steps = [('01', 'Assessorament', "Escoltem les teves necessitats, visitem l'espai i prenem mides. Sense compromis."), ('02', 'Disseny i pressupost', 'Et proposem la millor solució en materials, colors i acabats, amb un pressupost detallat.'),
             ('03', 'Fabricació', 'Fabriquem cada peça a mida amb materials de qualitat i un control rigorós.'), ('04', 'Instal·lació', 'El nostre equip ho munta, ho ajusta i ho deixa tot a punt i net.')]
    c.append(section([column([divider(RED), heading(n, 30, RED, 'div', weight=300, mb=8), heading(t, 15, WHITE, 'h3', weight=600, mb=6), text(d, 12.5, MUTED)], 25, tablet=50) for n, t, d in steps], p=(10, 0, 70, 0), gap='wide'))
    c.append(section([column([heading('Preguntes freqüents', 30, weight=500, mb=18, align='center'), accordion(faq)], 100)], bg=BG2, p=(70, 180, 70, 180), extra={'padding_tablet': pad(60, 40), 'padding_mobile': pad(40, 18)}))
    c.append(cta())
    save('sobre-nosaltres', 'Sobre nosaltres', c, 'sobre-nosaltres')

def p_contact():
    inp = 'width:100%;box-sizing:border-box;padding:13px 14px;background:#1a1a1d;border:1px solid rgba(255,255,255,.12);color:#fff;font:14px Inter,sans-serif;border-radius:2px'
    lab = 'display:block;font:11px Inter,sans-serif;letter-spacing:.08em;text-transform:uppercase;color:#a9a9ae;margin-bottom:6px'
    form = f'''<form action="#" method="post" style="display:grid;gap:16px;grid-template-columns:1fr 1fr">
<label style="{lab}">Nom<input name="nom" required placeholder="El teu nom" style="{inp};margin-top:6px"></label>
<label style="{lab}">Telèfon<input name="tel" type="tel" placeholder="600 00 00 00" style="{inp};margin-top:6px"></label>
<label style="{lab};grid-column:1/-1">Correu electrònic<input name="email" type="email" required placeholder="nom@correu.com" style="{inp};margin-top:6px"></label>
<label style="{lab};grid-column:1/-1">Què t'interessa?<select name="tipus" style="{inp};margin-top:6px"><option>Finestres</option><option>Portes d'entrada</option><option>Persianes</option><option>Pèrgoles i exteriors</option><option>Baranes i mampares</option><option>Altres</option></select></label>
<label style="{lab};grid-column:1/-1">Missatge<textarea name="missatge" rows="5" placeholder="Explica'ns breument el teu projecte" style="{inp};margin-top:6px"></textarea></label>
<label style="grid-column:1/-1;font:12px Inter,sans-serif;color:#cfcfd2"><input type="checkbox" required> He llegit i accepto la política de privacitat.</label>
<button type="submit" style="grid-column:1/-1;justify-self:start;padding:15px 28px;background:{RED};color:#fff;border:0;border-radius:2px;font:600 12px Inter,sans-serif;letter-spacing:.08em;text-transform:uppercase;cursor:pointer">Demana pressupost &rarr;</button></form>'''
    c = [hero('hero-home', 'Parlem del teu <span style="color:#e4152d">projecte</span>', "Explica'ns què necessites i t'assessorarem per trobar la millor solució. Sense compromis.", None, crumbs(('index', 'Inici'), (None, 'Contacte')), minh=380),
         section([column([html(form)], 60),
                  column([icon_box('fas fa-phone', "Truca'ns", '972 50 00 00', isize=24, tsize=15, dsize=12), divider(),
                          icon_box('fab fa-whatsapp', 'WhatsApp', "Envia'ns un missatge", isize=24, tsize=15, dsize=12), divider(),
                          icon_box('fas fa-envelope', 'Escriu-nos', 'info@aluminisalbera.com', isize=24, tsize=15, dsize=12), divider(),
                          icon_box('fas fa-map-marker-alt', 'On som', 'Figueres (Girona)', isize=24, tsize=15, dsize=12),
                          html('<div style="margin-top:14px;aspect-ratio:16/9;border:1px solid rgba(255,255,255,.12);display:grid;place-items:center;color:#a9a9ae;font:12px Inter,sans-serif;background:#131315">Substitueix aquest bloc pel teu mapa (Google Maps)</div>')], 40, bg=BG2, p=pad(26, 26, 26, 26))],
                 p=(70, 0), gap='extended'),
         ]
    save('contacte', 'Contacte', c, 'contacte')

def p_rpt():
    c = [hero('rpt-hero', 'Finestres<br><span style="color:#e4152d">RPT 55</span>', "Màxim aïllament, disseny i eficiència per al teu confort diari. La solució ideal tant per a habitatges com per a projectes professionals.",
              buttons_html([('Demana pressupost', link('contacte'), False), ('Descarrega catàleg', '#', True)]), crumbs(('index', 'Inici'), ('productes', 'Productes'), (None, 'Finestres RPT 55')),
              eb="Finestres d'alumini", script='Més confort<br>més vida', minh=480),
         usp([('fas fa-temperature-low', 'Aïllament tèrmic', "d'alt rendiment"), ('fas fa-volume-mute', 'Aïllament acústic', 'fins a 45 dB'), ('fas fa-leaf', 'Eficiència energètica', 'i sostenibilitat'),
              ('fas fa-gem', 'Disseny actual', 'i personalitzat'), ('fas fa-cog', 'Alta durabilitat', 'i baix manteniment')]),
         section([column([image('rpt-profile', 480)], 50, tablet=100),
                  column([html('<div style="text-align:right;font:10px Inter,sans-serif"><a href="#" style="color:#cfcfd2;margin-left:16px;text-decoration:none">&#128196; Colors acabats i texturats</a><a href="#" style="color:#cfcfd2;margin-left:16px;text-decoration:none">&#128196; Acabats fusta texturats</a></div>'),
                          eyebrow('Sèrie RPT 55'), heading('Prestacions que marquen <span style="color:#e4152d">la diferència</span>', 32, weight=500, mb=14),
                          text("La sèrie RPT 55 ofereix un excel·lent equilibri entre prestacions tècniques, disseny i preu. Amb trencament de pont tèrmic, garanteix un alt nivell d'aïllament tèrmic i acústic, contribuint a l'estalvi energètic i al benestar de la llar.", 13, TXT, mb=14),
                          icon_list(["Perfils d'alumini amb trencament de pont tèrmic (RPT)", "Gran varietat d'acabats i colors", "Compatible amb diferents tipus de vidre", "Disseny minimalista i línies modernes", "Solució ideal per a obra nova i rehabilitació"])], 50, valign='middle', p=pad(40, 50, 40, 50))],
                 boxed=False, gap='no', p=(0, 0), bg=BG),
         sec_head('Detalls que inspiren', right=link_text('Veure més imatges', '#galeria'))]
    c += photo_grid([f'rpt-detail-{n}' for n in range(1, 5)], per=4, h=190, lightbox=True)
    rows = [('Sèrie', 'RPT 55'), ('Trencament de pont tèrmic', 'Sí'), ('Aïllament tèrmic (Uw)', 'Fins a 1,4 W/m²K'), ('Aïllament acústic', 'Fins a 45 dB'), ('Profunditat del marc', '55 mm'),
            ('Gruix de vidre', 'Fins a 36 mm'), ('Acabats', 'Qualsevol RAL, anoditzat, imitació fusta'), ('Tipologies', 'Fixes, practicables, oscil·lobatents, corredisses')]
    tbl = '<table style="width:100%;border-collapse:collapse;font:12px Inter,sans-serif;color:#fff">' + ''.join(f'<tr><td style="padding:10px 0;border-bottom:1px solid rgba(255,255,255,.12);color:#cfcfd2;width:48%">{a}</td><td style="padding:10px 0;border-bottom:1px solid rgba(255,255,255,.12)">{b}</td></tr>' for a, b in rows) + '</table>'
    c.append(section([column([heading('Característiques tècniques', 22, weight=500, mb=16), html(tbl)], 40, p=pad(50, 40, 50, 0)),
                      column([eyebrow('Solucions per a'), heading('Habitatges, comços i <span style="color:#e4152d">projectes professionals</span>', 30, weight=500, mb=14),
                              text("Treballem amb arquitectes, constructors i particulars per oferir solucions a mida, amb la màxima qualitat i un assessorament personalitzat en tot el procés.", 12.5, TXT, mb=18),
                              button('Demana pressupost', link('contacte'))], 60, bg='#141416', valign='middle', p=pad(50, 50, 50, 50))], p=(30, 0), gap='no', bg=BG))
    c.append(section([column([eyebrow('Projectes realitzats'), heading('Finestres RPT 55', 52, weight=300, mb=8, tag='h2'), text("Descobreix alguns dels nostres projectes i com la sèrie RPT 55 s'adapta a cada espai i necessitat.", 14, MUTED)], 65, valign='middle'),
                      column([heading('Qualitat<br>en cada projecte', 26, WHITE, 'div', 'right', 500, SCRIPT)], 35, valign='middle')], p=(70, 0, 20, 0), extra={'_element_id': 'galeria'}))
    c += photo_grid([f'rpt-g{n:02d}' for n in range(1, 21)], per=4, h=230)
    c.append(section([column([button('Veure més projectes', link('projectes'), ghost=True, align='center')])], p=(30, 0, 70, 0)))
    c.append(cta())
    save('finestres-rpt-55', 'Finestres RPT 55', c, 'productes')

def p_gallery(fname, title, key, imgs):
    tabs = [('portes-entrada-particular', 'Particular', 'particular'), ('portes-entrada-ocultec', 'Particular OCULTEC', 'ocultec'), ('portes-entrada-comercial', 'Comercial', 'comercial')]
    th = ''.join(f'<a href="{link(h)}" style="display:inline-block;padding:12px 22px;font:14px Inter,sans-serif;color:{WHITE if k == key else MUTED};text-decoration:none;border-bottom:2px solid {RED if k == key else "transparent"}">{t}</a>' for h, t, k in tabs)
    c = [section([column([crumbs(('index', 'Inici'), ('projectes', 'Projectes'), (None, title)), heading(title, 54, weight=400, family=SERIF, mb=14, lh=1.05),
                          html(f'<div style="border-bottom:1px solid rgba(255,255,255,.12);margin-bottom:6px">{th}</div>')], 100)], p=(60, 0, 20, 0))]
    c += photo_grid(imgs, per=3, h=300, gap='default')
    c.append(section([column([text(f'{len(imgs)} fotografies', 12, MUTED, 'center')])], p=(10, 0, 40, 0)))
    c.append(section([column([heading('Vols una porta a mida?', 38, family=SERIF, mb=8), text("T'assessorem per trobar la solució de portes d'entrada que millor s'adapti al teu habitatge. Sense compromis.", 15, TXT, mb=20),
                              button('Demana pressupost', link('contacte'), serif=True, family=SERIF)], 55, valign='middle'), column([spacer(10)], 45)],
                     bgimg='sunset', overlay=(BG, 'rgba(12,12,13,0)', 90, 55), p=(70, 0), bg='#1c0c10'))
    save(fname, title, c, 'projectes')

p_index(); p_productes(); p_projectes(); p_about(); p_contact(); p_rpt()
p_gallery('portes-entrada-ocultec', "Portes d'Entrada Particular OCULTEC", 'ocultec', [f'oc-g{n:02d}' for n in range(1, 22)])
p_gallery('portes-entrada-particular', "Portes d'Entrada Particular", 'particular', ['portes-particular', 'portes-entrada', 'oc-g03', 'oc-g06', 'oc-g09', 'oc-g12', 'oc-g15', 'oc-g18', 'oc-g21'])
p_gallery('portes-entrada-comercial', "Portes d'Entrada Comercial", 'comercial', ['portes-comercial', 'rpt-g17', 'rpt-g18', 'rpt-g19', 'rpt-g20', 'rpt-g02'])
print(sorted(os.listdir(OUT)))
