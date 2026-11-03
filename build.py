#!/usr/bin/env python3
"""Alaybeyoğlu Hukuk Bürosu statik site oluşturucusu.
Cloudflare Pages: pip install -r requirements.txt && python3 build.py
Output: dist/
"""
import html
import json
import re
import shutil
from datetime import datetime
from pathlib import Path
from urllib.parse import quote
import mistune

ROOT = Path(__file__).resolve().parent
DIST = ROOT / 'dist'
SITE = json.loads((ROOT / 'content' / 'site.json').read_text('utf-8'))
markdown = mistune.create_markdown(escape=True, plugins=['table', 'strikethrough', 'url'])

def h(v): return html.escape(str(v or ''), quote=True)
def field(key): return h(SITE.get(key, ''))
def slugify(text):
    mp = str.maketrans('çğıöşüÇĞİÖŞÜ', 'cgiosuCGIOSU')
    name = str(text).translate(mp).lower()
    return re.sub(r'-+', '-', re.sub(r'[^a-z0-9]+', '-', name)).strip('-')
def date_tr(value):
    try:
        d = datetime.strptime(value[:10], '%Y-%m-%d')
        return f'{d.day} {"Ocak Şubat Mart Nisan Mayıs Haziran Temmuz Ağustos Eylül Ekim Kasım Aralık".split()[d.month-1]} {d.year}'
    except: return str(value or '')
def write(path, content):
    p = DIST / path
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(content, encoding='utf-8')

def nav(active):
    links=[('/', 'Anasayfa'),('/hakkimizda/', 'Hakkımızda'),('/faaliyet-alanlari/', 'Faaliyet Alanları'),('/makaleler/', 'Makaleler'),('/iletisim/', 'İletişim')]
    items=''.join(f'<a class="nav-link {"is-active" if active==url else ""}" href="{url}">{label}</a>' for url,label in links)
    return f'''<header class="site-header" id="ust"><div class="nav-wrap container"><a href="/" class="brand" aria-label="Alaybeyoğlu Hukuk Bürosu anasayfa"><img src="/assets/monogram.webp" alt="" width="35" height="38"/><span class="brand-text"><strong>ALAYBEYOĞLU</strong><small>HUKUK BÜROSU</small></span></a><button id="menu-button" class="menu-button" aria-label="Menüyü aç" aria-expanded="false" aria-controls="site-nav"><span></span><span></span><span></span></button><nav id="site-nav" class="site-nav" aria-label="Ana menü">{items}</nav></div></header>'''

def footer():
    return f'''<footer class="footer"><div class="container footer-grid"><div class="footer-brand"><img src="/assets/monogram.webp" alt="" loading="lazy"/><div><strong>ALAYBEYOĞLU</strong><span>HUKUK BÜROSU</span></div><p>Hukuki bilgi, mesleki çalışma ve iletişim.</p></div><div class="footer-links"><span class="eyebrow">SAYFALAR</span><a href="/hakkimizda/">Hakkımızda</a><a href="/faaliyet-alanlari/">Faaliyet Alanları</a><a href="/makaleler/">Makaleler</a><a href="/iletisim/">İletişim</a></div><div class="footer-notice"><span class="eyebrow">BİLGİLENDİRME</span><p>Bu sitedeki içerikler genel bilgilendirme amaçlıdır; somut olay bakımından hukuki görüş veya danışmanlık yerine geçmez.</p></div></div><div class="container footer-bottom"><span>© {datetime.now().year} Alaybeyoğlu Hukuk Bürosu</span><a href="#ust">Yukarı çık ↑</a></div></footer>'''

def layout(title, desc, active, body):
    title_tag = f'{h(title)} | Alaybeyoğlu Hukuk Bürosu' if title != 'Anasayfa' else 'Alaybeyoğlu Hukuk Bürosu'
    return f'''<!doctype html><html lang="tr"><head><meta charset="utf-8"/><meta name="viewport" content="width=device-width, initial-scale=1"/><meta name="theme-color" content="#f7f7f3"/><meta name="description" content="{h(desc)}"/><title>{title_tag}</title><link rel="icon" href="/assets/favicon.png" type="image/png"/><link rel="stylesheet" href="/assets/site.css"/><script defer src="/assets/site.js"></script></head><body>{nav(active)}<main id="main">{body}</main>{footer()}</body></html>'''

def page_heading(section, title, intro):
    return f'''<section class="page-heading"><div class="container"><div class="crumb"><a href="/">Ana Sayfa</a><span>/</span><span>{h(section)}</span></div><span class="eyebrow">ALAYBEYOĞLU HUKUK BÜROSU</span><h1>{title}</h1><p>{intro}</p></div></section>'''

def article_card(post):
    return f'''<article class="article-card" data-search="{h((post['title']+' '+post['category']+' '+post['summary']).lower())}" data-category="{h(post['category'])}"><div class="article-top"><span class="topic">{h(post['category'])}</span><time datetime="{h(post['date'])}">{h(date_tr(post['date']))}</time></div><h3><a href="/makaleler/{h(post['slug'])}/">{h(post['title'])}</a></h3><p>{h(post['summary'])}</p><div class="article-bottom"><span>{h(post['author'])}</span><a href="/makaleler/{h(post['slug'])}/" aria-label="{h(post['title'])} makalesini oku">Yazıyı oku <span aria-hidden="true">↗</span></a></div></article>'''

posts=[]
for file in sorted((ROOT/'content'/'makaleler').glob('*.json')):
    p=json.loads(file.read_text('utf-8'))
    if not p.get('published'): continue
    if not p.get('title') or not p.get('body'): continue
    p['slug']=slugify(file.stem)
    p.setdefault('category','Hukuki Bilgilendirme')
    p.setdefault('summary','')
    p.setdefault('date','')
    p.setdefault('author','Alaybeyoğlu Hukuk Bürosu')
    posts.append(p)
posts.sort(key=lambda a: a.get('date',''), reverse=True)

if DIST.exists(): shutil.rmtree(DIST)
DIST.mkdir()
shutil.copytree(ROOT/'assets', DIST/'assets')
# Google Search Console HTML doğrulama dosyalarını sitede kök dizine kopyala.
# Bu dosyalar GitHub deposunun köküne yüklenmelidir.
for verification_file in ROOT.glob('google*.html'):
    shutil.copy2(verification_file, DIST / verification_file.name)

latest=''.join(article_card(p) for p in posts[:3]) if posts else '<div class="empty-state"><span class="empty-symbol">✦</span><h3>Makalelerimiz</h3><p>Hukuki değerlendirmeler ve mesleki yazılar bu bölümde yayımlanacaktır.</p><a href="/makaleler/" class="text-link">Makaleler sayfası <span>↗</span></a></div>'

home=f'''<section class="hero"><div class="container hero-grid"><div class="hero-copy"><div class="hero-overline"><span class="hairline"></span> HUKUK BÜROSU <span class="hairline"></span></div><h1>Hukukun ışığında,<br/><em>özenli bir yaklaşım.</em></h1><p>{field('intro')}</p><div class="hero-actions"><a class="solid-btn" href="/hakkimizda/">Büromuzu tanıyın <span>↗</span></a><a class="underlined-link" href="/iletisim/">İletişime geçin <span>↗</span></a></div></div><div class="hero-art"><div class="art-lines" aria-hidden="true"></div><img class="hero-logo" src="/assets/full-logo.webp" alt="Alaybeyoğlu Hukuk Bürosu logosu"/><div class="hero-art-caption">HUKUK • GÜVEN • MESLEKİ ÖZEN</div></div></div><div class="container hero-footnote"><span>ALAYBEYOĞLU</span><span>İSTANBUL · ANADOLU YAKASI</span></div></section><section class="intro-section section-spacing"><div class="container intro-grid"><div><span class="eyebrow">HAKKIMIZDA</span><h2>Mesleki özen,<br/><em>insan odaklı yaklaşım.</em></h2></div><div class="intro-side"><p>{field('about')}</p><a class="text-link" href="/hakkimizda/">Büromuz hakkında <span>↗</span></a></div></div></section><section class="practice-section section-spacing"><div class="container"><div class="section-head"><div><span class="eyebrow">ÇALIŞMA ALANLARIMIZ</span><h2>Faaliyet alanları</h2></div><a class="text-link" href="/faaliyet-alanlari/">Tümünü incele <span>↗</span></a></div><div class="practice-grid"><a class="practice-item" href="/faaliyet-alanlari/"><span>01</span><h3>İş Hukuku</h3><span>↗</span></a><a class="practice-item" href="/faaliyet-alanlari/"><span>02</span><h3>Şirketler Hukuku</h3><span>↗</span></a><a class="practice-item" href="/faaliyet-alanlari/"><span>03</span><h3>İcra ve İflas Hukuku</h3><span>↗</span></a><a class="practice-item" href="/faaliyet-alanlari/"><span>04</span><h3>Gayrimenkul Hukuku</h3><span>↗</span></a></div></div></section><section class="articles-section section-spacing"><div class="container"><div class="section-head"><div><span class="eyebrow">YAZILARIMIZ</span><h2>Hukuki makaleler</h2></div><a class="text-link" href="/makaleler/">Tüm makaleler <span>↗</span></a></div><div class="articles-grid">{latest}</div></div></section><section class="contact-banner"><div class="container contact-banner-inner"><div><span class="eyebrow">İLETİŞİM</span><h2>Bizimle iletişime geçin.</h2></div><a class="light-btn" href="/iletisim/">İletişim bilgileri <span>↗</span></a></div></section>'''
write('index.html',layout('Anasayfa', 'Alaybeyoğlu Hukuk Bürosu: avukat profilleri, faaliyet alanları, hukuki makaleler ve iletişim.', '/',home))

about=f'''{page_heading('Hakkımızda','Hakkımızda','Alaybeyoğlu Hukuk Bürosu ve avukatlarımız hakkında bilgiler.')}<section class="section-spacing"><div class="container two-col about-content"><div><span class="eyebrow">BÜROMUZ</span><h2>Hukuki çalışma ve<br/><em>mesleki sorumluluk.</em></h2></div><div><p class="lead">{field('about')}</p><p>Hukuki uyuşmazlıkların değerlendirilmesinde, somut olayın özelliklerinin ve güncel mevzuatın dikkate alınması esastır.</p></div></div></section><section class="team-section section-spacing"><div class="container"><div class="section-head"><div><span class="eyebrow">EKİBİMİZ</span><h2>Avukatlarımız</h2></div></div><div class="team-grid"><article class="team-card"><div class="team-number">01 / AVUKAT</div><div class="team-avatar" aria-hidden="true">B</div><h3>{field('lawyer_1')}</h3><p>Avukat</p><div class="team-card-bottom">{field('lawyer_1_education')}</div></article><article class="team-card"><div class="team-number">02 / AVUKAT</div><div class="team-avatar" aria-hidden="true">Y</div><h3>{field('lawyer_2')}</h3><p>Avukat</p><div class="team-card-bottom">{field('lawyer_2_education')}</div></article></div></div></section>'''
write('hakkimizda/index.html',layout('Hakkımızda','Alaybeyoğlu Hukuk Bürosu hakkında ve avukatlarımız.', '/hakkimizda/',about))

areas=[
 ('01','İş Hukuku','İş ilişkileri, iş sözleşmeleri ve işçilik alacaklarına ilişkin hukuki uyuşmazlıklar.'),
 ('02','Aile Hukuku','Aile hukuku kapsamında doğan hukuki ilişkiler ve uyuşmazlıklar.'),
 ('03','Miras Hukuku','Mirasın paylaşılması, tereke ve miras ilişkilerinden kaynaklanan uyuşmazlıklar.'),
 ('04','Gayrimenkul Hukuku','Taşınmaz mülkiyeti, kira ve taşınmazlara ilişkin uyuşmazlıklar.'),
 ('05','Borçlar Hukuku','Sözleşmeler, sorumluluk ve borç ilişkilerinden doğan uyuşmazlıklar.'),
 ('06','İcra ve İflas Hukuku','İcra takipleri, iflas ve ilgili hukuki süreçler.'),
 ('07','Şirketler Hukuku','Şirket kuruluşları, ortaklık ilişkileri, ticari sözleşmeler ve şirketler hukukundan doğan uyuşmazlıklar.')
]
area_html=''.join(f'<article class="area-card"><span>{i}</span><h2>{name}</h2><p>{description}</p></article>' for i,name,description in areas)
practice=f'''{page_heading('Faaliyet Alanları','Faaliyet Alanları','Büronun hukuki çalışma alanlarına genel bir bakış.')}<section class="section-spacing"><div class="container"><div class="area-grid">{area_html}</div><p class="small-note">Bu sayfadaki çalışma alanları taslak olarak oluşturulmuştur. Yayından önce büro tarafından doğrulanacaktır.</p></div></section>'''
write('faaliyet-alanlari/index.html',layout('Faaliyet Alanları','Alaybeyoğlu Hukuk Bürosu faaliyet alanları.', '/faaliyet-alanlari/',practice))

category_names=sorted({p['category'] for p in posts})
filters=''.join(f'<button class="filter" data-filter="{h(c)}">{h(c)}</button>' for c in category_names)
article_list=''.join(article_card(p) for p in posts) if posts else '<div class="no-posts"><span class="empty-symbol">✦</span><h2>Makale arşivi hazırlanıyor.</h2><p>Yayımlanan makaleler burada başlık, tarih ve konu başlıklarına göre listelenecek.</p></div>'
articles=f'''{page_heading('Makaleler','Makaleler','Hukuki bilgilendirmeler, mesleki değerlendirmeler ve yazılar.')}<section class="section-spacing"><div class="container"><div class="article-toolbar"><label class="search-box"><span aria-hidden="true">⌕</span><input id="article-search" type="search" placeholder="Makalelerde ara" aria-label="Makalelerde ara"/></label><div class="filters"><button class="filter active" data-filter="all">Tümü</button>{filters}</div></div><div class="articles-grid list-grid" id="article-grid">{article_list}</div><p id="article-no-results" class="no-results" hidden>Aramanızla eşleşen makale bulunamadı.</p></div></section>'''
write('makaleler/index.html',layout('Makaleler','Alaybeyoğlu Hukuk Bürosu hukuki makaleleri ve yazıları.', '/makaleler/',articles))

for p in posts:
    rich=markdown(p['body'])
    article=f'''<section class="article-hero"><div class="container reading-width"><div class="crumb"><a href="/">Ana Sayfa</a><span>/</span><a href="/makaleler/">Makaleler</a><span>/</span><span>{h(p['category'])}</span></div><span class="eyebrow">{h(p['category'])}</span><h1>{h(p['title'])}</h1><div class="article-meta"><span>{h(p['author'])}</span><span class="dot"></span><time datetime="{h(p['date'])}">{h(date_tr(p['date']))}</time></div></div></section><section class="article-body-section"><div class="container reading-width"><article class="prose">{rich}</article><div class="article-disclaimer">Bu metin genel bilgilendirme amacıyla hazırlanmıştır. Somut uyuşmazlıklarda olayın özelliklerine göre değerlendirme yapılması gerekir.</div><a href="/makaleler/" class="text-link">← Tüm makalelere dön</a></div></section>'''
    write('makaleler/'+p['slug']+'/index.html',layout(p['title'],p['summary'] or p['title'],'/makaleler/',article))

phone=SITE.get('phone','').strip()
email=SITE.get('email','').strip()
addr=SITE.get('address','').strip()
map_url=SITE.get('map_url','').strip()
rows=[]
if phone: rows.append(f'<div class="contact-row"><span>TELEFON</span><a href="tel:{h(re.sub(r"[^+0-9]", "",phone))}">{h(phone)}</a></div>')
if email: rows.append(f'<div class="contact-row"><span>E-POSTA</span><a href="mailto:{h(email)}">{h(email)}</a></div>')
instagram=SITE.get('instagram','').strip().lstrip('@')
if instagram: rows.append(f'<div class="contact-row"><span>INSTAGRAM</span><a href="https://www.instagram.com/{h(instagram)}/" target="_blank" rel="noopener noreferrer">@{h(instagram)}</a></div>')
if addr: rows.append(f'<div class="contact-row"><span>ADRES</span><strong>{h(addr)}</strong></div>')
if not rows: rows.append('<div class="contact-pending">Telefon, e-posta ve açık adres bilgileri yayına alınmadan önce eklenecek.</div>')
if map_url.startswith('https://'): rows.append(f'<a class="text-link" href="{h(map_url)}" target="_blank" rel="noopener noreferrer">Adresi haritada ara <span>↗</span></a>')
contact=f'''{page_heading('İletişim','İletişim','Alaybeyoğlu Hukuk Bürosu iletişim ve adres bilgileri.')}<section class="section-spacing"><div class="container contact-main"><div><span class="eyebrow">İLETİŞİM BİLGİLERİ</span><h2>Bir sorunuz mu var?</h2><p>Büromuzla iletişime geçmek için aşağıdaki bilgileri kullanabilirsiniz.</p><div class="contact-details">{''.join(rows)}</div></div><div class="contact-art" aria-label="Alaybeyoğlu Hukuk Bürosu logosu"><img src="/assets/monogram.webp" alt=""/><span>ALAYBEYOĞLU</span><small>HUKUK BÜROSU</small><div class="contact-art-location">İSTANBUL · ANADOLU YAKASI</div></div></div></section>'''
write('iletisim/index.html',layout('İletişim','Alaybeyoğlu Hukuk Bürosu iletişim bilgileri.', '/iletisim/',contact))

# Google Search Console için site haritası: ana sayfalar ve yayındaki tüm makaleler.
# Yeni makale yayımlandığında dosya otomatik güncellenir.
from xml.sax.saxutils import escape as xml_escape
site_url = 'https://alaybeyogluhukukburosu.netlify.app'
index_files = sorted(DIST.rglob('index.html'))
url_paths = []
for index_file in index_files:
    relative = index_file.parent.relative_to(DIST)
    path = '/' if str(relative) == '.' else '/' + relative.as_posix() + '/'
    url_paths.append(path)
url_paths.sort(key=lambda path: (path != '/', path))
sitemap_xml = '<?xml version="1.0" encoding="UTF-8"?>\n'
sitemap_xml += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
for path in url_paths:
    sitemap_xml += '  <url><loc>' + xml_escape(site_url + path) + '</loc></url>\n'
sitemap_xml += '</urlset>\n'
write('sitemap.xml', sitemap_xml)
write('robots.txt', 'User-agent: *\nAllow: /\nSitemap: ' + site_url + '/sitemap.xml\n')
write('_headers','/*\n  X-Content-Type-Options: nosniff\n  Referrer-Policy: strict-origin-when-cross-origin\n  X-Frame-Options: DENY\n')
print('Site başarıyla hazırlandı:',len(posts),'yayımlanmış makale,',len(list(DIST.rglob('index.html'))),'sayfa')
