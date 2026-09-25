# -*- coding: utf-8 -*-
"""Kemer Yat Turu - site denetim betigi (calistirmak icin: python tools/ky-denetim.py)

Kontroller:
  1) JSON-LD bloklari gecerli mi?
  2) Sitede fiyat/tutar ifadesi kaldi mi? (kalmamali)
  3) HTML etiket dengesi
  4) index.html  : data-i18n / -html / -alt / -aria anahtarlari tr/en/ru sozluklerinde var mi?
                   (opsiyonel) statik metin = TR sozluk degeri mi?
  5) koy sayfalari: data-i18n anahtarlari assets/koy-sayfa.js icindeki
                   SHARED + PAGES.<sayfa> sozluklerinde (tr/en/ru) var mi?
                   statik metin = TR sozluk degeri mi?
  6) JS soz dizimi (esprima kuruluysa)
  7) Referans verilen yerel dosyalar (gorsel/css/js) diskte var mi?

Cikis kodu 0 = tum kontroller gecti, 1 = en az bir sorun var.
"""
import io
import os
import re
import sys
import glob
import json
import html as htmllib
from html.parser import HTMLParser

try:
    sys.stdout.reconfigure(errors="replace")
except Exception:
    pass

SITE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HTML_FILES = ["index.html", "phaselis-koyu.html", "cennet-koyu.html",
              "akvaryum-koyu.html", "korsan-magarasi.html"]
KOY_FILES = [("korsan-magarasi.html", "korsan"), ("phaselis-koyu.html", "phaselis"),
             ("cennet-koyu.html", "cennet"), ("akvaryum-koyu.html", "akvaryum")]
PRICE = re.compile(r"(\d[\.,]?\d*\s*(?:\$|USD|EUR|€|TL|₺))|(?:\$\s*\d)|(?:kişi başı\s*\d)|(?:per person)", re.I)
VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta",
        "param", "source", "track", "wbr", "path", "use", "circle", "rect", "line",
        "polygon", "polyline", "ellipse", "stop"}
sorun = []


def oku(f):
    return io.open(os.path.join(SITE, f), encoding="utf-8").read()


def norm(s):
    return re.sub(r"\s+", " ", s).strip()


def balanced(text, start):
    depth = 0
    for i in range(start, len(text)):
        if text[i] == "{":
            depth += 1
        elif text[i] == "}":
            depth -= 1
            if depth == 0:
                return text[start + 1:i]
    return ""


def inner_text(t, pos, tag):
    depth = 1
    for mm in re.finditer(r"</?%s\b" % tag, t[pos:], re.I):
        depth += 1 if not mm.group(0).startswith("</") else -1
        if depth == 0:
            return t[pos:pos + mm.start()]
    return ""


def js_lang_block(section, lang):
    m = re.search(r"\n\s{4}%s:\s*\{" % lang, section)
    if not m:
        return None
    out = {}
    for k, v in re.findall(r'([A-Za-z0-9_]+):\s*"((?:[^"\\]|\\.)*)"', balanced(section, m.end() - 1)):
        out[k] = v.replace('\\"', '"').replace("\\\\", "\\")
    return out


class Balance(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self, convert_charrefs=True)
        self.stack = []
        self.errors = []

    def handle_starttag(self, tag, attrs):
        if tag not in VOID:
            self.stack.append((tag, self.getpos()[0]))

    def handle_endtag(self, tag):
        if tag in VOID:
            return
        if not self.stack:
            self.errors.append("fazla kapanis </%s> satir %d" % (tag, self.getpos()[0]))
            return
        t, ln = self.stack.pop()
        if t != tag:
            self.errors.append("uyusmazlik <%s> (satir %d) / </%s> (satir %d)" % (t, ln, tag, self.getpos()[0]))


# --------------------------------------------------------------------------- 1
print("1) JSON-LD GECERLILIGI")
for f in HTML_FILES:
    t = oku(f)
    blocks = re.findall(r'<script type="application/ld\+json">(.*?)</script>', t, re.S)
    hata = []
    for i, b in enumerate(blocks):
        try:
            json.loads(b)
        except Exception as e:
            hata.append("blok %d: %s" % (i + 1, e))
    print("   %-22s blok=%d %s" % (f, len(blocks), "OK" if not hata else "HATA " + " | ".join(hata)))
    sorun.extend(hata)

# --------------------------------------------------------------------------- 2
print("2) FIYAT KALINTISI (sitede fiyat olmamali)")
bulundu = 0
for f in sorted(glob.glob(os.path.join(SITE, "*.html"))) + [os.path.join(SITE, "llms.txt")]:
    for ln, line in enumerate(io.open(f, encoding="utf-8").read().splitlines(), 1):
        for m in PRICE.finditer(line):
            bulundu += 1
            print("   !! %s:%d -> %s" % (os.path.basename(f), ln, m.group(0).strip()))
if not bulundu:
    print("   TEMIZ")
sorun.append("fiyat kalintisi") if bulundu else None

# --------------------------------------------------------------------------- 3
print("3) HTML ETIKET DENGESI")
for f in HTML_FILES:
    p = Balance()
    p.feed(oku(f))
    left = ["<%s> satir %d" % (t, ln) for t, ln in p.stack]
    if p.errors or left:
        print("   %-22s SORUN: %s" % (f, "; ".join((p.errors + left)[:4])))
        sorun.append("html dengesi: " + f)
    else:
        print("   %-22s OK" % f)

# --------------------------------------------------------------------------- 4
print("4) index.html SOZLUK KAPSAMI ve statik metin uyumu")
idx = oku("index.html")
govde = re.search(r"const translations = \{(.*?)\n\};", idx, re.S).group(1)
IDX = {}
for lg in ("tr", "en", "ru"):
    blk = re.search(r"\n  %s: \{(.*?)\n  \}" % lg, govde, re.S)
    IDX[lg] = dict(re.findall(r'^\s{4}([A-Za-z0-9_]+): "(.*?)",?$', blk.group(1), re.M)) if blk else {}
idx_tr = IDX["tr"]
keys = set(re.findall(r'data-i18n(?:-html|-alt|-aria)?="([A-Za-z0-9_]+)"', idx))
print("   anahtar=%d (data-i18n / -html / -alt / -aria)" % len(keys))
for lg in ("tr", "en", "ru"):
    yok = sorted(k for k in keys if k not in IDX[lg])
    print("   %s: sozluk=%d eksik=%s" % (lg, len(IDX[lg]), ", ".join(yok) if yok else "yok"))
    if yok:
        sorun.append("index %s eksik anahtar" % lg)
uyus = 0
for m in re.finditer(r"<(span|b|small|h1|h2|p|li|strong|div|summary|a)\b([^>]*?)>", idx, re.I):
    km = re.search(r'data-i18n="([A-Za-z0-9_]+)"', m.group(2))
    if not km:
        continue
    static = norm(htmllib.unescape(inner_text(idx, m.end(), m.group(1))))
    if static and km.group(1) in idx_tr and norm(idx_tr[km.group(1)]) != static:
        uyus += 1
        print("   !! %s: HTML=%s | TR=%s" % (km.group(1), static[:60], idx_tr[km.group(1)][:60]))
print("   statik/sozluk uyusmazligi: %d" % uyus)
sorun.append("index statik uyusmazlik") if uyus else None

# --------------------------------------------------------------------------- 5
print("5) koy sayfalari SOZLUK KAPSAMI ve statik metin uyumu")
js = oku(os.path.join("assets", "koy-sayfa.js"))
m = re.search(r"var SHARED = \{", js)
SHARED = {lg: js_lang_block(balanced(js, m.end() - 1), lg) for lg in ("tr", "en", "ru")}
PAGES = {}
for pm in re.finditer(r"PAGES\.(\w+) = \{", js):
    blk = balanced(js, pm.end() - 1)
    PAGES[pm.group(1)] = {lg: js_lang_block(blk, lg) for lg in ("tr", "en", "ru")}

for f, pkey in KOY_FILES:
    t = oku(f)
    used = set(re.findall(r'data-i18n(?:-html|-alt|-aria)?="([A-Za-z0-9_]+)"', t))
    tr = dict(SHARED["tr"] or {})
    tr.update(PAGES.get(pkey, {}).get("tr") or {})
    eksik = []
    for lg in ("tr", "en", "ru"):
        have = set((SHARED[lg] or {}).keys()) | set((PAGES.get(pkey, {}).get(lg) or {}).keys())
        yok = sorted(used - have)
        if yok:
            eksik.append("%s -> %s" % (lg, ", ".join(yok)))
    uyus = 0
    for m2 in re.finditer(r"<(span|b|small|h1|h2|p|li|strong|div|summary|a)\b([^>]*?)>", t, re.I):
        km = re.search(r'data-i18n(?:-html)?="([A-Za-z0-9_]+)"', m2.group(2))
        if not km:
            continue
        static = norm(htmllib.unescape(inner_text(t, m2.end(), m2.group(1))))
        if static and km.group(1) in tr and norm(tr[km.group(1)]) != static:
            uyus += 1
            print("   !! %s [%s] HTML=%s | TR=%s" % (f, km.group(1), static[:50], tr[km.group(1)][:50]))
    print("   %-22s anahtar=%d eksik=%s uyusmazlik=%d"
          % (f, len(used), "yok" if not eksik else " | ".join(eksik), uyus))
    if eksik or uyus:
        sorun.append("koy sozluk: " + f)

# --------------------------------------------------------------------------- 6
print("6) JS SOZ DIZIMI")
try:
    import esprima
    for ad, kod in (("assets/koy-sayfa.js", js), ("index.html (gomulu)", re.search(r"<script>(.*?)</script>", idx, re.S).group(1))):
        try:
            esprima.parseScript(kod)
            print("   %-22s OK" % ad)
        except Exception as e:
            print("   %-22s HATA: %s" % (ad, e))
            sorun.append("js: " + ad)
except ImportError:
    print("   atlandi (esprima kurulu degil: pip install esprima)")

# --------------------------------------------------------------------------- 7
print("7) YEREL DOSYA REFERANSLARI")
refs = set()
for f in HTML_FILES:
    t = oku(f)
    refs |= set(re.findall(r'(?:src|href)="((?:images|assets)/[^"]+)"', t))
    refs |= set(re.findall(r"url\('((?:images|assets)/[^']+)'\)", t))
    refs |= set(re.findall(r'srcset="((?:images|assets)/[^"]+)"', t))
for r in sorted(refs):
    if not os.path.exists(os.path.join(SITE, r.replace("/", os.sep))):
        print("   !! EKSIK: %s" % r)
        sorun.append("eksik dosya: " + r)
print("   %d referans kontrol edildi" % len(refs))

print("=" * 72)
print("SONUC:", "TUM KONTROLLER GECTI" if not sorun else "SORUNLAR: " + "; ".join(sorun))
sys.exit(0 if not sorun else 1)


