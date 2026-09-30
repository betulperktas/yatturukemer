# Kemer Yat Turu — Web Sitesi

Kemer Marina çıkışlı günlük lüks yat turu için tek sayfalık (one-page) tanıtım
ve rezervasyon yönlendirme sitesi. Saf statik HTML/CSS/JS — sunucu, veritabanı
veya derleme adımı gerektirmez.

**Canlı site:** https://kemeryattur.com.tr/
**Diller:** Türkçe (varsayılan), İngilizce, Rusça — sayfa içi dil değiştirme (JS)

---

## Dosya Yapısı

```
index.html              Ana sayfa: HTML + özel CSS + JS + 3 dil sözlüğü + JSON-LD + SVG ikon sprite'ı
phaselis-koyu.html      Koy detay sayfası (anahtar kelime odaklı içerik + SSS + JSON-LD)
cennet-koyu.html        Koy detay sayfası
akvaryum-koyu.html      Koy detay sayfası
korsan-magarasi.html    Koy detay sayfası
assets/tailwind.min.css Derlenmiş Tailwind CSS (cdn.tailwindcss.com yerine yerel — 23 KB)
                        NOT: içeriği index.html'e gömülüdür; dosya, yeni sınıf
                        eklenirse derlemeyi yenilemek için kaynak olarak durur.
assets/fonts.css        Yerel @font-face tanımları (Manrope 400-800 + Playfair 600/700)
assets/fonts/*.woff2    Self-host yazı tipleri (14 dosya, latin + latin-ext alt küme)
assets/koy-sayfa.css    Koy sayfalarının ortak stili (Tailwind'den bağımsız)
                        NOT: içeriği 4 koy sayfasına gömülüdür (kaynak olarak durur).
assets/koy-sayfa.js     Koy sayfaları için TR/EN/RU çeviri motoru + WhatsApp mesajları
images/*.webp           Sayfada kullanılan görseller (bkz. "Görsel Varyantları")
images/hero-yacht-1080.webp  Mobil (≤767 px) için küçültülmüş hero görseli (85 KB)
images/hero-yacht.jpg   Hero görselinin eski tarayıcı yedeği + og:image (SİLMEYİN)
images/logo.svg         Site logosu ve favicon
robots.txt              Tarama kuralları + AI botlarına (GPTBot, ClaudeBot vb.) izin
sitemap.xml             Site haritası: ana sayfa + 4 koy sayfası (görsel girdileriyle)
llms.txt                AI arama motorları için işletme özeti (GEO)
vercel.json             Önbellek (Cache-Control) ve güvenlik başlıkları
tools/ky-denetim.py     Site denetim betiği: JSON-LD, fiyat kalıntısı, HTML dengesi,
                        çeviri anahtar kapsamı (data-i18n/-alt/-aria, tr+en+ru) +
                        statik/sözlük uyumu, JS söz dizimi, eksik dosya referansı.
                        Çalıştır: python tools/ky-denetim.py
BASLAT.bat              Windows'ta çift tıkla → http://localhost:8000 yerel önizleme
```

### Görsel Varyantları

Aynı görselin farklı ekranlar için küçültülmüş sürümleri ayrı dosyalardadır;
sayfalar `<picture>`/`preload` ile doğru olanı indirir (mobil veri tasarrufu):

| Tam boy | 1080 px (mobil hero) | 800 px (kart) | 768 px (mobil hero) | 640 px (küçük kart) |
| --- | --- | --- | --- | --- |
| `hero-yacht.webp` (152 KB) | `hero-yacht-1080.webp` | — | — | — |
| `korsan-koyu.webp` (178 KB) | `korsan-koyu-1080.webp` | `korsan-koyu-800.webp` | `korsan-koyu-768.webp` | `korsan-koyu-640.webp` |
| `phaselis-koyu.webp` | — | `phaselis-koyu-800.webp` | `phaselis-koyu-768.webp` | `phaselis-koyu-640.webp` |
| `cennet-koyu.webp` | — | `cennet-koyu-800.webp` | `cennet-koyu-768.webp` | `cennet-koyu-640.webp` |
| `akvaryum-koyu.webp` | — | `akvaryum-koyu-800.webp` | `akvaryum-koyu-768.webp` | `akvaryum-koyu-640.webp` |
| `yat-kamara.webp` | — | `yat-kamara-800.webp` | — | — |
| `turkuaz-su.webp` | — | `turkuaz-su-800.webp` | — | — |
| `filo-yelkenli.webp` | — | `filo-yelkenli-800.webp` | — | — |
| `kemer-marina.webp` | `kemer-marina-1080.webp` | — | — | — |
| `yat-seyir.webp` (1400×1050) | — | `yat-seyir-800.webp` (800×600) | — | — |
| `ogle-yemegi.webp` (1050×1400) | — | `ogle-yemegi-800.webp` (600×800) | — | — |
| `meyve-tabagi.webp` (1050×1400) | — | `meyve-tabagi-800.webp` (600×800) | — | — |
| `meyve-tabagi-2.webp` (1050×1400) | — | `meyve-tabagi-2-800.webp` (600×800) | — | — |

Galeri görsellerinin (`yat-seyir`, `ogle-yemegi`, `meyve-tabagi`, `meyve-tabagi-2`)
kaynağı WhatsApp'tan gelen 1200–1512 px'lik JPEG'lerdir. Tam boy sürüm uzun kenarı
1400 px'e indirilir (lightbox için), kart sürümü (`-800`) uzun kenarı 800 px'dir;
bu nedenle dikey fotoğraflarda kart dosyası 600×800 olur. Kartlar `h-56`
(`sm:h-60`, `lg:h-64`) + `object-cover` ile aynı yükseklikte kırpılır.

`images/*.jpg` dosyalarının WebP dışındaki ham kopyaları `.gitignore` ile hariç
tutulur (yalnızca `hero-yacht.jpg` zorunlu olduğu için repoda kalır).

---

## Çok Dillilik (TR / EN / RU)

Beş sayfanın tamamı **Türkçe (varsayılan), İngilizce ve Rusça** olarak çalışır.
Mimari iki dosyaya ayrılmıştır:

| Sayfa | Çeviri sözlüğü | Motor |
| --- | --- | --- |
| `index.html` | `<script>` içindeki `translations` nesnesi | aynı betikteki `setLang()` |
| 4 koy sayfası | `assets/koy-sayfa.js` → `SHARED` + `PAGES.<koy>` | `assets/koy-sayfa.js` içindeki `setLang()` |

**Kurallar (yeni çeviri eklerken uyun):**

1. HTML'de metin **her zaman önce Türkçe** yazılır ve şu niteliklerle işaretlenir:
   - `data-i18n="anahtar"` — düz metin (`textContent` ile değişir)
   - `data-i18n-html="anahtar"` — içinde `<strong>` / `<a>` olan zengin metin (`innerHTML`)
   - `data-i18n-alt="anahtar"` — görsel `alt` metni
   - `data-i18n-aria="anahtar"` — `aria-label`
   - `data-wa="anahtar"` — WhatsApp bağlantısının mesajı (`WA_MESSAGES`)
2. Arama motorları JS çalıştırmadığı için **HTML'deki statik metin ile sözlükteki
   Türkçe değer birebir aynı olmalıdır** (kod denetimi bunu kontrol eder).
3. Her anahtar üç dilde de tanımlı olmalıdır; eksik anahtar denetim betiğiyle
   yakalanır (`data-i18n` anahtarı sözlükte yoksa metin Türkçe kalır).
4. Koy sayfaları kendi sözlüğünü `PAGES.<data-koy değeri>` altında tutar.
   `<html data-koy="korsan">` niteliği hangi sözlüğün yükleneceğini belirler.
5. Dil seçimi ana sayfa ve koy sayfaları arasında `localStorage('kemeryat_lang')`
   ile paylaşılır. Paylaşılabilir bağlantı: `korsan-magarasi.html?lang=en`.
6. `hreflang` etiketleri (`tr`, `en`, `ru`, `x-default`) her sayfanın başında
   tanımlıdır; `?lang=` parametresini işaret eder (içerik istemci tarafında
   değiştiği için şu an tek URL vardır — bkz. "Bekleyen SEO / GEO Kararları" #6).

---

## Yerel Önizleme

**Kod denetimi:** her değişiklikten sonra `python tools/ky-denetim.py` çalıştırın.
Betik; JSON-LD geçerliliğini, fiyat kalıntısı olup olmadığını, HTML etiket dengesini,
çeviri anahtarlarının üç dilde tanımlı olup olmadığını, HTML'deki statik metin ile
sözlükteki Türkçe değerin birebir aynı olup olmadığını ve eksik dosya referanslarını
kontrol eder (`pip install esprima` kuruluysa JS söz dizimini de doğrular).

**Kolay yol (Windows):** `BASLAT.bat` dosyasına çift tıklayın → tarayıcı
`http://localhost:8000` adresinde açılır.

**Diğer:** klasörü herhangi bir statik sunucuyla yayınlayın:

```bash
python -m http.server 8000     # Python
npx serve .                    # Node.js
```

> Not: `index.html`'i doğrudan çift tıklayarak (`file://`) açmak yerine sunucu
> üzerinden açın; `robots.txt`/`sitemap.xml` ve göreli yollar o zaman doğru çalışır.

---

## Yayına Alma

1. Tüm dosyaları (`*.html`, `robots.txt`, `sitemap.xml`, `llms.txt`, `vercel.json`,
   `assets/` ve `images/`) barındırma (hosting) kök dizinine yükleyin.
2. Vercel / Netlify gibi statik barındırmada `vercel.json` dosyası önbellek ve
   güvenlik başlıklarını otomatik uygular (Netlify bu dosyayı yok sayar; orada
   `_headers` dosyası gerekir).
3. Yayın sonrası kontrol listesi:
   - `https://kemeryattur.com.tr/robots.txt` ve `/sitemap.xml` tarayıcıda açılıyor mu?
   - 4 koy sayfası da (`/phaselis-koyu.html` vb.) 200 dönüyor mu?
   - `images/` ve `assets/` klasörleri 404 vermiyor mu? (Bir kez sürükle-bırak
     yüklemesinde bu klasörler eksik kalmıştı; mutlaka kontrol edin.)
   - Google Search Console'a `sitemap.xml` gönderildi mi?
   - `index.html` içindeki canonical / og / sitemap adresleri alan adıyla birebir mi?
   - Sosyal medya bağlantıları gerçek hesaplara işaret ediyor mu? (Footer'daki
     Instagram/Facebook adresleri şu an `https://www.instagram.com/` ve
     `https://www.facebook.com/` şeklinde **yer tutucudur**.)

---

## Yapılan SEO / GEO Çalışmaları

- Görseller WebP'ye çevrildi: **5.12 MB → 1.13 MB (%78 küçülme)**; hero,
  `image-set()` ile WebP sunar, desteklemeyen tarayıcıda JPG'ye düşer.
- Tailwind CDN betiği kaldırıldı → yerel `assets/tailwind.min.css` (JIT derleme yok).
- Font Awesome CDN'i **tamamen kaldırıldı**: 100 KB render-blocking CSS + 3 webfont
  (~300 KB) yerine ikonlar sayfaya gömülü **SVG sprite** olarak taşınıyor
  (39 ikon ≈ 21 KB, gzip'te çok daha az). Böylece 4 ağ isteği ve ikonların
  geç yüklenmesi (FOIT) ortadan kalktı.
- Mobil için ayrı hero görseli: `images/hero-yacht-1080.webp` (274 KB → 87 KB);
  `@media (max-width: 767px)` ve media'lı `preload` ile yalnızca gerekli sürüm indirilir.
- `vercel.json` ile önbellek başlıkları: görseller 30 gün, `assets/` 1 gün +
  `stale-while-revalidate`, HTML'ler doğrulamalı (içerik güncellemesi anında görünür).
- 4 koy için ayrı detay sayfası: `phaselis-koyu.html`, `cennet-koyu.html`,
  `akvaryum-koyu.html`, `korsan-magarasi.html`. Her biri kendi başlık/açıklama/canonical'ı,
  `TouristAttraction` + `BreadcrumbList` + `FAQPage` JSON-LD'si, görünür SSS'si ve
  ana sayfaya dönüş bağlantısı içerir.
- Ana sayfadaki "Gittiğimiz Koylar" kartları **tıklanabilir**: kart başlığı
  anahtar kelime içeren bağlantı metni olarak koy sayfasına gider, kartın tamamı
  tıklanır (stretched-link) ve alt kısımda "Detaylı bilgi" ipucu bulunur.
  Footer'a "Koy Rehberi" bağlantı bloğu eklendi.
- Başlık 49 karakter, açıklama 147 karakter (TR/EN/RU üç dil için ayrı).
- Tek `<h1>`, başlık seviyesi atlaması yok, tüm görsellerde `alt`, tüm çapalar çalışıyor.
- `robots.txt` (yapay zekâ tarayıcılarına açık), `sitemap.xml`, `llms.txt` eklendi;
  sitemap'te 5 URL (ana sayfa + 4 koy sayfası) ve her URL için görsel girdisi var.
- JSON-LD: `LocalBusiness` + `TouristAttraction` + `FAQPage` (görsel URL'leri sayfayla
  tutarlı; **sitede fiyat/tarife bilgisi yayınlanmaz**, `Offer` ve `priceRange` kaldırıldı).
- Mobil dokunma hedefleri en az 44 px; 390 px'te yatay taşma yok.
- **Ana başlıklar anahtar kelimeli** hâle getirildi (TR/EN/RU): örn. "Gittiğimiz Koylar"
  → "Kemer Yat Turu Rotası: Phaselis, Cennet, Akvaryum ve Korsan Mağarası";
  "Fix Tur Detayları…" → "Kemer Tekne Turu: Program, Menü ve Konfor".
  **Kural:** başlık metni hem görünür statik HTML'de hem `data-i18n` sözlüğünde aynı
  olmalıdır — arama motoru JS çalıştırmadan statik metni okur. Değişiklik için
  `ky-seo-fix.py` kullanılabilir (sözlükte TR/EN/RU sırasını otomatik doğrular).
- **Etkisiz meta etiketleri kaldırıldı:** `keywords`, `geo.region`, `geo.placename`,
  `geo.position`, `ICBM`. Google bunları yok sayar; gerçek lokal sinyaller
  LocalBusiness JSON-LD, Google Business Profile ve tutarlı NAP'tır.
- `sameAs` yalnızca **gerçek profil** URL'leri içindir. Profil olmayan `wa.me` ve
  Google Maps *arama* linki buradan çıkarıldı (gerçek profiller gelince eklenecek).
- `robots.txt`'e Perplexity-User, Meta-ExternalAgent, MistralAI-User, DuckAssistBot,
  Amazonbot, YouBot eklendi. Not: `User-agent: * / Allow: /` kuralı zaten hiçbir botu
  engellemiyor; tek tek yazmanın amacı hangi tarayıcılara açık olduğumuzu belgelemek.

### Son Tur (fiyat kaldırma + çok dillilik + performans)

- **Sitedeki tüm fiyat bilgisi kaldırıldı** (ana sayfa, 4 koy sayfası, `llms.txt`,
  JSON-LD `Offer`/`priceRange`/`makesOffer`, SSS, meta açıklamalar; TR/EN/RU).
  Yerine `#program` bölümündeki "Fiyat için WhatsApp'tan yazın" kutusu,
  `waMessages.price` mesajı ve SSS'te "Fiyat ve müsaitlik bilgisini nasıl alabilirim?"
  sorusu geldi. `#fiyatlar` anchor'ı geriye dönük uyumluluk için `#program`'a taşındı.
- **4 koy sayfası TR/EN/RU çevrildi** (`assets/koy-sayfa.js`, 5 dilde kapsama denetimi
  yapıldı; `?lang=en` bağlantıları, `hreflang`, dil değiştirici butonlar, `data-i18n-*`).
- **Google Fonts CDN kaldırıldı, fontlar self-host edildi** (`assets/fonts/*.woff2`,
  latin + latin-ext). Sayfa başında render-blocking harici CSS isteği kalmadı;
  ölçülen 2.160 ms'lik font bloğu ortadan kalktı. Kritik başlık fontu `preload` edilir.
- **Tailwind ve koy-sayfa.css sayfalara gömüldü**: render-blocking CSS isteği 0.
- **Scroll dinleyicisindeki forced reflow giderildi** (rAF + yalnızca eşik geçişinde
  DOM güncelleme).
- **Görsel ağırlığı düştü:** `hero-yacht.webp` 268 KB → 152 KB; kart/mobil kırpımlar
  (800/768/640 px) eklendi; koy hero'ları artık `<picture>` ile mobilde küçük sürümü
  indiriyor. Korsan Mağarası görseli, mağarayı yanlış gösterdiği için
  `images/korsan-koyu.webp` ile değiştirildi ve "tekneyle içine girilir" bilgisi
  tüm sayfalarda düzeltildi.

### Son Eklenen: Yat İçi (Kamara) Görseli

- Ana sayfa `#hakkimizda` bölümündeki görsel kümesine **yat içi fotoğrafı** eklendi:
  `images/yat-kamara.webp` (900×675) tam boy ve kart sürümü
  `images/yat-kamara-800.webp` (800×600, ~33 KB). Görsel, `h-40 w-56`
  (`md:h-48 md:w-64`) ölçüsünde, `hidden sm:block` ile sağ üstte ve `object-cover`
  ile gösterilir (dar ekranlarda `filo-yelkenli` fotoğrafını örtmemesi için gizlenir).
- Kaynak JPEG (`images/yat-kamara.jpg`) yerel arşiv olarak durur; `.gitignore`
  kuralı gereği (`images/*.jpg`) depoya girmez.
- Alt metni TR/EN/RU üç dilde `alt_kabin` anahtarıyla verilir (statik `alt` = TR değeri).

### Son Eklenen: Fotoğraf Galerisi (Kütüphane) — `#galeri`

- Ana sayfaya, Rotalar ile Tur Programı arasına yeni bir **galeri (fotoğraf
  kütüphanesi)** bölümü eklendi (`<section id="galeri">`, koyu `bg-ocean-950`
  zemin). Dört gerçek tur fotoğrafı yan yana (masaüstünde `lg:grid-cols-4`,
  tablette `sm:grid-cols-2`, telefonda tek kolon) gösterilir; üst üste
  yığılmaz.
- Her fotoğraf bir `<button class="galeri-kart">`dır: tıklanınca aynı karenin
  tam boy WebP'si **büyütme penceresinde (lightbox)** açılır. Pencere; önceki/
  sonraki düğmeleri, `1 / 4` sayacı, kapatma düğmesi ve altyazı içerir.
  Kart üzerinde **yalnızca altyazı** görünür (rozet/etiket yok); "büyüt"
  davranışı görselin kendisinden ve `zoom-in` imlecinden anlaşılır.
  - Klavye: `Esc` kapatır, `←`/`→` gezer (sarmalı), `Tab` pencere içinde
    döner (odak tuzağı). Mobilde yatay kaydırma da önceki/sonraki fotoğrafa geçer.
  - Erişilebilirlik: `role="dialog"` + `aria-modal`, açılışta odak kapatma
    düğmesine gider, kapanışta odak tıklanan karta döner, arka plan kaydırması
    kilitlenir. Düğmeler 44 px dokunma hedefidir.
  - Kısa ekranlarda (yatay telefon) pencere kendi içinde kaydırılır; görsel
    `max-height: 74vh` ile ekrana sığar.
- Eklenen görseller: `images/yat-seyir.webp` (seyirdeki yat),
  `images/ogle-yemegi.webp` (öğle yemeği sofrası),
  `images/meyve-tabagi.webp` + `images/meyve-tabagi-2.webp` (güverte meyve
  ikramları) — her biri `-800` kart sürümüyle birlikte.
- Çeviri: `nav_gallery`, `gallery_kicker`, `gallery_title`, `gallery_sub`,
  `gal_cap1..4`, `gal_zoom1..4`, `alt_gal1..4`,
  `lb_close`, `lb_prev`, `lb_next`, `gal_dialog` anahtarları TR/EN/RU
  sözlüklerine eklendi. `setLang()` artık `data-i18n-aria` (aria-label)
  anahtarlarını da çevirir; lightbox açıkken dil değişirse altyazı ve
  etiketler anında güncellenir.
- Yeni Tailwind sınıfı gerekmedi: galeri ve lightbox stilleri sayfadaki özel
  CSS bloğunda (`.galeri-kart`, `.galeri-yazi`, `#galeri-lightbox`, `.lb-*`)
  tanımlıdır; `assets/tailwind.min.css` yeniden derlenmeden çalışır.
- `tools/ky-denetim.py` güçlendirildi: anahtar taraması artık
  `data-i18n-alt` / `data-i18n-aria` anahtarlarını ve **üç dilin tamamını**
  (yalnızca TR değil) kapsıyor.

### Son Değişiklik: E-posta Kaldırıldı + Koy Sayfası Çeviri Açıkları

- Sitedeki **e-posta adresi tamamen kaldırıldı**; iletişim yalnızca telefon
  (`+90 532 113 92 44`) ve WhatsApp üzerinden yürür. Kaldırılan yerler:
  - `index.html` JSON-LD `"email"` alanı (satır ~172; `telephone` korundu),
  - `index.html` footer iletişim listesindeki `mailto:` bağlantısı,
  - dört koy sayfasının (`phaselis-koyu.html`, `cennet-koyu.html`,
    `akvaryum-koyu.html`, `korsan-magarasi.html`) footer'ındaki `mailto:`
    bağlantısı,
  - `llms.txt` ve bu README'deki `E-posta:` satırları.
  Bunun yerine hiçbir görünür e-posta metni ve `mailto:` bağlantısı kalmaz.
  Yeni bir adres eklenmek istenirse JSON-LD, 5 footer, `llms.txt` ve README
  birlikte güncellenmelidir.
- **Bulunan ve düzeltilen çeviri açıkları:** `assets/koy-sayfa.js` içinde üç
  dilde tanımlı olan `foot_wa` (footer WhatsApp bağlantısı) ve `nav_call`
  (mobil alt sabit çubuktaki "Hemen Ara") anahtarları HTML'de hiç
  kullanılmıyordu; bu yüzden EN/RU sayfalarda metinler Türkçe kalıyordu.
  Anahtarlar dört koy sayfasında bağlandı. Sabit çubukta `setLang()`
  `innerHTML` yazdığı için metin `<span data-i18n="nav_call">` içine alındı;
  böylece telefon ikonu (SVG) silinmiyor.
- Doğrulama: `tools/ky-denetim.py` tüm kontrolleri geçti (JSON-LD geçerli,
  üç dilde eksik anahtar yok, statik/dize uyuşmazlığı 0, 43 yerel dosya
  referansı yerinde). Chromium ile 80 dosyada e-posta izi taraması (ikili
  dosyalar dahil) **0 bulgu**; 5 sayfada `mailto:` sayısı 0; 4 koy sayfası
  TR/EN/RU'da footer ve sabit çubuk metinleri doğru, ikonlar korunuyor.

### Son Değişiklik: Filo Sayısı İddiası ve Galeri Rozeti Kaldırıldı

- "12 lüks yat" / "12 yat" / "Флот из 12 роскошных яхт" gibi **filo büyüklüğü
  iddiaları siteden tamamen kaldırıldı**; artık sayı verilmeden "lüks yat
  filosu" deniyor. Kaldırılan yerler: `index.html` `og:description` ve JSON-LD
  `description`, hero rozeti (`hero_badge`), "Hakkımızda" metni
  (`about_text1`; "12 profesyonel kaptan" ifadesi dahil), footer tanıtımı
  (`footer_about`), dört koy sayfasındaki "Filomuz:" satırı (`side_fleet_v`),
  Phaselis giriş paragrafı (`sec3_p1`) ve `llms.txt`. Üç dilin tamamı
  güncellendi; statik HTML metinleri sözlüklerle birebir aynı tutuldu.
- Hero'daki **"12 / Lüks Yat" istatistik kartı kaldırıldı**; kalan iki kart
  ("18 Yıllık Deneyim", "4.9 Misafir Puanı") için ızgara `grid-cols-3` →
  `grid-cols-2` oldu. Kullanılmayan `trust_1`, `trust_1_label` anahtarları üç
  dilden silindi. "Hakkımızda" fotoğrafının üzerindeki rozet artık sayısız:
  `about_badge` = "Lüks Yat Filosu" / "Luxury Yacht Fleet" / "Роскошный флот"
  (eskiden büyük "12" + "lüks yat" idi). "Lüks Filo" özellik kartının açıklaması
  (`feat1_desc`) da sayıdan arındırıldı.
- Galeri kartlarındaki **"Büyüt" rozeti** (`.galeri-zoom` CSS'i ve `gal_zoom`
  anahtarı) ile bölüm altındaki **"Büyütmek için fotoğrafa dokunun · ← → ile
  gezinin, Esc ile kapatın" ipucu** (`gallery_hint`) kaldırıldı; TR/EN/RU
  anahtarları da silindi. Kart üstünde artık yalnızca altyazı var. Ekran
  okuyucu için düğme adları (`gal_zoom1..4`, `data-i18n-aria`) korundu.
- Büyütme penceresi (lightbox) davranışı değişmedi: tıklama, `Esc`, `←`/`→`,
  odak tuzağı, sayaç ve altyazı aynen çalışır.
- Doğrulama: `tools/ky-denetim.py` tüm kontrolleri geçti; filo bağlamında
  hiçbir metinde `12` kalmadığı, kartlarda rozet/ipucu bulunmadığı ve
  lightbox'ın TR/EN/RU'da çalıştığı Chromium ile doğrulandı.

---

## Bekleyen SEO / GEO Kararları (karar verilmeden uygulanmayacak)

Aşağıdakiler **uydurma veri** gerektirdiği veya iş kararı olduğu için bilinçli olarak
yapılmadı. Yanıtlar netleşince uygulanacak:

1. **Fiyat bilgisi siteden tamamen kaldırıldı (karar verildi ve uygulandı).**
   Ana sayfa + 4 koy sayfası + `llms.txt` + JSON-LD (`Offer`, `priceRange`) içindeki tüm
   tutarlar (108 $ / 650 $ / +40 $) silindi. Fiyat artık yalnızca WhatsApp/telefon ile
   veriliyor: `#program` bölümündeki "Fiyat için WhatsApp'tan yazın" kutusu,
   `waMessages.price` mesajı ve SSS "Fiyat ve müsaitlik bilgisini nasıl alabilirim?"
   sorusu bu akışı taşır. Fiyat bilgisi geri eklenmek istenirse TR/EN/RU üç dilde ve
   JSON-LD ile birlikte güncellenmelidir.
2. **`aggregateRating` doğrulanmalı.** `index.html` JSON-LD'sinde `ratingValue: 4.9`,
   `reviewCount: 412` var; sayfada görünen tek değer "4.9 Misafir Puanı" ve **hiç yorum
   yok**. Google yapısal veri politikası gereği puan/yorum gerçek ve doğrulanabilir
   olmalı. Kaynak (Google Business Profile / Tripadvisor) varsa `sameAs` + yorum bölümü
   eklenmeli; yoksa `aggregateRating` kaldırılmalı.
3. **Kaynaksız iddialar.** "%64'ü bizi tavsiye ederek geri döner" ifadesi (TR/EN/RU)
   kaynak gerektiriyor; aksi hâlde kaldırılmalı.
4. **Program tutarsızlıkları.** Cennet Koyu kartında "90 dk mola" yazıyor ama programda
   `12:30 → 13:45` (75 dk). Ayrıca programın son satırı "15:30 Korsan Mağarası & marina
   dönüşü" — doğru süreler teyit edilip tek bir kaynaktan güncellenmeli.
5. **Dönüş saati çelişkisi.** Site genelinde (TR/EN/RU + JSON-LD + SSS) **15:30**, fakat
   `llms.txt` **17:30** yazıyor. Hangisi doğruysa `llms.txt` veya site düzeltilmeli.
6. **EN/RU'ya ayrı URL gerekiyor.** Şu anki TR/EN/RU değişimi **client-side** olduğu için
   Google yalnızca Türkçe içeriği görüyor. İndekslenebilir çok dillilik için `/en`, `/ru`
   alt yolları + `hreflang` + `x-default` gerekir. Bu, mevcut mimaride büyük bir iş.
   **Güncel durum:** 4 koy sayfası da TR/EN/RU olarak çevrildi (`assets/koy-sayfa.js`,
   `data-i18n` + `?lang=en` bağlantıları + `hreflang`); eksik olan tek şey ayrı URL'ler.
7. **Domain ve yönlendirme.** `canonical`, `og:url`, `og:image` ve `sitemap.xml`
   `https://kemeryattur.com.tr` işaret ediyor. Domain bağlı değilse Google canonical'ı
   takip edip sayfayı bulamaz; bağlandığında `*.vercel.app` → asıl alan adına **308
   yönlendirme** eklenmeli (bugün `vercel.json`'da yönlendirme YOK — domain canlı değilken
   eklemek siteyi erişilemez yapar).
8. **Sosyal medya / kurumsal kimlik.** Footer'daki Instagram ve Facebook bağlantıları
   hâlâ genel ana sayfalara gidiyor; gerçek profil adresleri gelince değiştirilmeli ve
   `sameAs`'e eklenmeli. TÜRSAB/işletme belge numarası da yok.
9. **GEO için "Hızlı Bilgi" tablosu.** Her tur sayfasının üstüne kalkış/dönüş/süre/rota/
   dahil-hariç/çocuk politikası/iptal bilgisi içeren alıntılanabilir kısa bir
   tablo eklenmesi önerilir (yeni görsel blok — tasarım onayı gerektirir).

---



Font Awesome CDN'i kullanılmıyor. İkonlar sayfanın `<body>` başındaki gizli
`<svg>` sprite'ında `#i-<ad>` kimlikleriyle tanımlıdır ve sayfada şöyle kullanılır:

```html
<svg class="i" viewBox="0 0 512 512" aria-hidden="true"><use href="#i-phone"></use></svg>
```

**ÇOK ÖNEMLİ:** Kullanılan her `<svg>` kendi `viewBox`'ını taşımak zorundadır.
`viewBox` yoksa CSS'teki `width:auto`, gerçek oran yerine tarayıcının varsayılan
**300 px** genişliğine düşer ve flex satırları (butonlar, rozetler) bozulur.
Koy sayfalarında (`assets/koy-sayfa.css`) ikonlar `.btn svg{width:17px}` /
`.eyebrow svg{width:15px}` ile sabitlendiği için orada bu sorun görülmez.

Yeni bir ikon eklemek için:

1. `TEMP/ky-icons/` klasörüne ilgili Font Awesome 6.5.2 SVG'sini
   `stil-ad.svg` biçiminde koyun (örn. `solid-camera.svg`).
2. Sprite'a `<symbol id="i-camera" viewBox="...">…</symbol>` ekleyin.
3. Kullanırken `<svg class="i" viewBox="…">` ile birlikte yazın (bkz. yukarıdaki uyarı).

`index.html`, `phaselis-koyu.html` vb. dosyaları **doğrudan elle düzenlemek
yerine** üreteç betikleriyle üretmek daha güvenlidir; üretim betikleri:
`koy-uret.py` (koy sayfaları), `koy-dogrula.py` (koy sayfası doğrulama),
`ky-fa-svg.py` (Font Awesome → SVG sprite dönüşümü),
`ky-seo-fix.py` (meta temizliği + başlık metinleri; sözlükte TR/EN/RU sırasını
doğrular, JSON-LD'yi yazmadan önce parse eder ve önce `TEMP/ky-yedek2`'ye yedek alır),
`ky-baslik-dogrula.py` (başlıkların dört kaydını birebir karşılaştırır, mojibake
kontrolü yapar), `ky-site-dogrula.py` (site geneli doğrulama).

---

## Önemli: Tailwind Sınıfı Eklerken

`assets/tailwind.min.css` **derlenmiş** bir dosyadır. HTML'de **yeni** bir
Tailwind sınıfı kullanırsanız (örnek: `bg-ocean-700`, `mt-13` gibi daha önce
kullanılmamış bir sınıf) o sınıf CSS'te bulunmaz ve etkisiz kalır. Böyle bir
değişiklik yapmadan önce CSS dosyasının yeniden üretilmesi gerekir.
Mevcut sınıfların değerlerini değiştirmek sorun değildir.

---

## İletişim

- Telefon / WhatsApp: +90 532 113 92 44 (`+905321139244`)
- Adres: Kemer Marina, Liman Cad., 07980 Kemer / Antalya
