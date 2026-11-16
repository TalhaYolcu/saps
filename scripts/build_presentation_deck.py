"""
Build PowerPoint Presentation Deck (docs/SAPS_Presentation.pptx)
=================================================================

Constructs an expanded 26-slide, 16:9 widescreen presentation deck for
the CSE 476/575 (Prof. Dr. Hasari Çelebi) term project presentation.
Embeds all generated publication figures, NVIDIA Sionna benchmarks, and
the demonstration video.
Injects comprehensive, professional Turkish speaker notes into every slide
so the presenter can deliver a flawless 25-30 minute presentation using
PowerPoint Presenter View.
"""

from __future__ import annotations

import os
from pathlib import Path

from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

_ROOT = Path(__file__).resolve().parent.parent
_RESULTS = _ROOT / "results"
_DOCS = _ROOT / "docs"
_DOCS.mkdir(parents=True, exist_ok=True)

# Color Palette (Dark Academic High-Tech Theme)
BG_DARK = RGBColor(11, 19, 43)        # #0b132b
CARD_BG = RGBColor(28, 37, 65)        # #1c2541
CARD_BORDER = RGBColor(58, 80, 107)   # #3a506b
CYAN = RGBColor(0, 210, 255)          # #00d2ff
GREEN = RGBColor(16, 185, 129)        # #10b981
WHITE = RGBColor(248, 250, 252)       # #f8fafc
LIGHT_GRAY = RGBColor(203, 213, 225)  # #cbd5e1
GOLD = RGBColor(245, 158, 11)         # #f59e0b
RED = RGBColor(239, 68, 68)           # #ef4444


def apply_background(slide):
    """Set slide background color to dark navy."""
    bg = slide.background
    fill = bg.fill
    fill.solid()
    fill.fore_color.rgb = BG_DARK


def add_slide_header(slide, title_text: str, category_text: str = "CSE 476/575 TERM PROJECT"):
    """Add standardized top header and category label to slide."""
    apply_background(slide)

    # Category label
    cat_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(11.7), Inches(0.4))
    tf_c = cat_box.text_frame
    tf_c.word_wrap = True
    p_c = tf_c.paragraphs[0]
    p_c.text = category_text.upper()
    p_c.font.size = Pt(11)
    p_c.font.bold = True
    p_c.font.color.rgb = CYAN

    # Main slide title
    title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.7), Inches(11.7), Inches(0.7))
    tf_t = title_box.text_frame
    tf_t.word_wrap = True
    p_t = tf_t.paragraphs[0]
    p_t.text = title_text
    p_t.font.size = Pt(23)
    p_t.font.bold = True
    p_t.font.color.rgb = WHITE


def add_card(slide, left, top, width, height, title="", border_color=CARD_BORDER, bg_color=CARD_BG):
    """Draw a styled container card."""
    card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
    card.fill.solid()
    card.fill.fore_color.rgb = bg_color
    card.line.color.rgb = border_color
    card.line.width = Pt(1.5)

    if title:
        tb = slide.shapes.add_textbox(left + Inches(0.2), top + Inches(0.15), width - Inches(0.4), Inches(0.4))
        p = tb.text_frame.paragraphs[0]
        p.text = title
        p.font.size = Pt(14)
        p.font.bold = True
        p.font.color.rgb = CYAN

    return card


def set_speaker_notes(slide, notes_text: str):
    """Inject formatted speaker notes into PowerPoint Presenter View."""
    notes_slide = slide.notes_slide
    tf = notes_slide.notes_text_frame
    tf.text = notes_text.strip()


def build_deck():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    # =========================================================================
    # SLIDE 1: Title Slide
    # =========================================================================
    s1 = prs.slides.add_slide(blank_layout)
    apply_background(s1)

    t_box = s1.shapes.add_textbox(Inches(1.0), Inches(1.3), Inches(11.3), Inches(3.2))
    tf = t_box.text_frame
    tf.word_wrap = True

    p0 = tf.paragraphs[0]
    p0.text = "CSE 476/575: MOBILE COMMUNICATIONS & AI/ML — TERM PROJECT"
    p0.font.size = Pt(14)
    p0.font.bold = True
    p0.font.color.rgb = CYAN

    p1 = tf.add_paragraph()
    p1.text = "Semantic-Driven Agentic Protocol Stack (SAPS)\nfor Mobile AI Agents"
    p1.font.size = Pt(35)
    p1.font.bold = True
    p1.font.color.rgb = WHITE

    p2 = tf.add_paragraph()
    p2.text = "Redesigning the 6-Layer Internet Protocol Stack for Autonomous M2M Reasoning"
    p2.font.size = Pt(16)
    p2.font.color.rgb = LIGHT_GRAY

    # Metadata card
    add_card(s1, Inches(1.0), Inches(4.8), Inches(11.3), Inches(1.9))
    meta_box = s1.shapes.add_textbox(Inches(1.3), Inches(4.95), Inches(10.7), Inches(1.6))
    m_tf = meta_box.text_frame

    mp1 = m_tf.paragraphs[0]
    mp1.text = "Ders Yürütücüsü: Prof. Dr. Hasari Çelebi  |  Dönem: Güz 2026"
    mp1.font.size = Pt(14)
    mp1.font.bold = True
    mp1.font.color.rgb = GOLD

    mp2 = m_tf.add_paragraph()
    mp2.text = "Proje Yürütücüsü / Sunan: Yakup Yolcu  |  Yüksek Lisans Dönem Projesi"
    mp2.font.size = Pt(13)
    mp2.font.color.rgb = WHITE

    mp3 = m_tf.add_paragraph()
    mp3.text = "Testbed & İmplementasyon: Python & PyTorch Testbed (30/30 Test Geçti) + NVIDIA Sionna 3GPP Desteği"
    mp3.font.size = Pt(12)
    mp3.font.color.rgb = GREEN

    set_speaker_notes(
        s1,
        """⏱️ [Hedef Süre: 00:00 - 01:00]
🎯 [Temel Mesaj]: Projenin hedefini ve 6G vizyonundaki yerini net şekilde özetlemek.

🎙️ [Konuşma Metni]:
Sayın Prof. Dr. Hasari Çelebi Hocam ve değerli çalışma arkadaşlarım, hepiniz hoş geldiniz.
Bugün sizlere CSE 476/575 dersi kapsamında geliştirdiğimiz dönem projemizi sunmaktan büyük memnuniyet duyuyorum:
"Semantic-Driven Agentic Protocol Stack", kısaca SAPS.

Bildiğiniz üzere 1970'lerde ve 80'lerde temelleri atılan mevcut TCP/IP ve HTTP protokol ailesi, insan kullanıcıların web sayfalarını gezmesi ve dosyaları bit-bit hatasız indirmesi amacıyla tasarlandı. Ancak 6G ve ötesi mobil ağlarda artık internetin birincil aktörleri insanlar değil; otonom İHA'lar, robotik filolar ve işbirlikçi yapay zeka ajanları olacak. 

Bu çalışmada, klasik 5 katmanlı internet mimarisini yapay zeka ajanlarının anlamsal muhakeme ihtiyaçlarına göre baştan tasarladık ve üzerine yeni bir "Ajan Niyet ve Muhakeme Katmanı" ekleyerek 6 katmanlı uçtan uca eksiksiz bir protokol yığını inşa ettik. Ayrıca simülasyonlarımızda standart fading modellerinin yanı sıra NVIDIA Sionna 3GPP TR 38.901 kanal modellerini de entegre ederek endüstri standardı 5G/6G ortamlarında doğruladık.

Şimdi bu paradigmanın neden kaçınılmaz olduğuna birlikte bakalım."""
    )

    # =========================================================================
    # SLIDE 2: The Paradigm Shift
    # =========================================================================
    s2 = prs.slides.add_slide(blank_layout)
    add_slide_header(s2, "Paradigma Dönüşümü: İnsan Web'inden Ajanik İnternet'e", "1. Motivasyon")

    # Left: Human Web
    add_card(s2, Inches(0.8), Inches(1.6), Inches(5.6), Inches(5.2), title="Geleneksel İnsan Web'i (TCP/IP & HTTP)")
    tb_s2_l = s2.shapes.add_textbox(Inches(1.0), Inches(2.3), Inches(5.2), Inches(4.3))
    tf_l = tb_s2_l.text_frame
    tf_l.word_wrap = True

    pts_l = [
        "Birincil Aktör: Web gezen, video izleyen insan son kullanıcılar.",
        "İletişim Modeli: Statik IP adresli sunucular üzerinden istemci-sunucu istek/yanıt.",
        "Temel Gereksinim: Katı bit-seviyesinde doğruluk (bit-exactness). Tek bir bit hatası dosyayı bozar.",
        "Gecikme Toleransı: 100ms - 300ms insan algı eşiği.",
        "Veri Formatı: Ayrıntılı ASCII/JSON serileştirme ve büyük HTTP başlıkları.",
        "Hata Yönetimi: Tüm paketler kayıpta eşit önemdedir; hepsi tekrar iletilir (Blind ARQ).",
    ]
    for idx, pt in enumerate(pts_l):
        p = tf_l.paragraphs[0] if idx == 0 else tf_l.add_paragraph()
        p.text = f"•  {pt}"
        p.font.size = Pt(12.5)
        p.font.color.rgb = LIGHT_GRAY

    # Right: Agentic Web
    add_card(s2, Inches(6.8), Inches(1.6), Inches(5.7), Inches(5.2), title="Yeni Nesil Ajanik İnternet (SAPS)", border_color=CYAN)
    tb_s2_r = s2.shapes.add_textbox(Inches(7.0), Inches(2.3), Inches(5.3), Inches(4.3))
    tf_r = tb_s2_r.text_frame
    tf_r.word_wrap = True

    pts_r = [
        "Birincil Aktör: Otonom yapay zeka ajanları (dronlar, mobil robotlar, LLM kümeleri).",
        "İletişim Modeli: Makineden makineye muhakeme vektörleri ve sürekli token akışı.",
        "Temel Gereksinim: Anlamsal bilgi korunumu (Semantic preservation) & sınırlı gecikme.",
        "Gecikme Toleransı: Kritik otonom kararlar için 10ms altı uçtan uca süre.",
        "Veri Formatı: Doğrudan tensör ve KV-cache kuantizasyonu (JSON yok).",
        "Hata Yönetimi: Önemsiz dolgu kelimeleri atlanır; yalnızca yüksek entropili kritik bilgiler yinelenir.",
    ]
    for idx, pt in enumerate(pts_r):
        p = tf_r.paragraphs[0] if idx == 0 else tf_r.add_paragraph()
        p.text = f"✔  {pt}"
        p.font.size = Pt(12.5)
        p.font.color.rgb = WHITE if (idx == 2 or idx == 3) else GREEN
        p.font.bold = (idx == 2 or idx == 3)

    set_speaker_notes(
        s2,
        """⏱️ [Hedef Süre: 01:00 - 02:15]
🎯 [Temel Mesaj]: İnsan odaklı ağlar ile yapay zeka ajanları arasındaki zıtlığı ve neden yeni bir yığına ihtiyaç olduğunu vurgulamak.

🎙️ [Konuşma Metni]:
Hocam, bu slaytta günümüz interneti ile geleceğin ajan ağları arasındaki derin zıtlığı görüyoruz.
Sol tarafta gördüğümüz klasik internet altyapısı, insan algısına göre şekillenmiştir. İnsan gözü 100-200 milisaniyelik bir gecikmeyi fark etmez; ancak bir dosyayı indirirken tek bir bitin dahi bozulmaması esastır. Bu yüzden TCP, bir paket kaybolduğunda akışı durdurur ve o paketi yeniden iletir.

Fakat sağ taraftaki Ajanik İnternet'e baktığımızda durum tamamen tersine dönüyor:
Otonom bir drone veya otonom araç sürüş sistemini düşünelim. Burada karar alma döngüsünün 10 milisaniyenin altında tamamlanması gerekir. Bir cümledeki "the" veya "bir" gibi dolgu sözcükleri kaybolsa bile, downstream dil modeli veya karar motoru cümlenin anlamını %99 başarıyla kavrayabilir. Ancak klasik TCP gibi o dolgu kelimesi için 100 milisaniye boyunca akışı durdurup yeniden iletim yaparsak (head-of-line blocking), drone engele çarpabilir.

Dolayısıyla yapay zeka ajanları için önemli olan bit-seviyesinde aynılık değil, anlamsal bilginin (semantic meaning) en düşük gecikmeyle hedefe ulaşmasıdır."""
    )

    # =========================================================================
    # SLIDE 3: Theoretical Foundations (Shannon & Weaver)
    # =========================================================================
    s3 = prs.slides.add_slide(blank_layout)
    add_slide_header(s3, "Teorik Temeller: Weaver & Shannon'ın 3 İletişim Seviyesi", "1. Teorik Altyapı")

    levels = [
        ("Seviye A: Teknik İletişim Seviyesi (Technical Level)", 
         "Klasik Shannon Problemi (1948): 'Semboller alıcıya ne kadar hatasız ve bit-birebir aktarılabilir?'\n"
         "• 1G'den 5G'ye kadar tüm telekomünikasyon bu seviyeyi çözmeye odaklandı (QAM, OFDM, LDPC, Turbo kodlar).\n"
         "• İletilen sembollerin taşıdığı anlam veya alıcıdaki etkisi tamamen göz ardı edilir (Agnostic bits).",
         LIGHT_GRAY, CARD_BG),
        ("Seviye B: Anlamsal İletişim Seviyesi (Semantic Level)", 
         "SAPS & 6G Vizyonu (Weaver 1949): 'İletilen semboller hedef anlamı ne kadar kesin ifade ediyor?'\n"
         "• Semantik Entropi: Her bit eşit değerde değildir. Kritik niyet ve hedef koordinatları yüksek değere sahiptir.\n"
         "• Deep-JSCC ile kaynak ve kanal kodlama tek bir sinir ağı mimarisinde birleştirilir.",
         CYAN, CARD_BG),
        ("Seviye C: Pragmatik / Etkililik Seviyesi (Effectiveness Level)", 
         "Ajan Muhakemesi & Görev Başarısı: 'Alınan anlam, alıcı ajanın eylemlerini hedefe ne kadar etkili yönlendiriyor?'\n"
         "• İletişim sadece veri taşımak için değil, ortak görev hedefine (task goal) ulaşmak için yürütülür.\n"
         "• SAPS Katman 6 (AIRL), ajanlar arası niyet sözleşmeleriyle Seviye C'yi doğrudan protokol yığınına entegre eder.",
         GREEN, CARD_BG),
    ]

    for idx, (title, desc, col, bg) in enumerate(levels):
        top_y = Inches(1.6 + idx * 1.8)
        add_card(s3, Inches(0.8), top_y, Inches(11.7), Inches(1.6), title=title, border_color=col, bg_color=bg)
        tb = s3.shapes.add_textbox(Inches(1.0), top_y + Inches(0.55), Inches(11.3), Inches(0.95))
        p = tb.text_frame.paragraphs[0]
        p.text = desc
        p.font.size = Pt(12.5)
        p.font.color.rgb = LIGHT_GRAY

    set_speaker_notes(
        s3,
        """⏱️ [Hedef Süre: 02:15 - 03:45]
🎯 [Temel Mesaj]: Projenin Claude Shannon ve Warren Weaver'ın 1949 tarihli teorik çerçevesine dayandığını göstererek akademik derinliği hissettirmek.

🎙️ [Konuşma Metni]:
Hocam, çalışmamızın teorik temeli iletişim teorisinin kurucuları Claude Shannon ve Warren Weaver'ın 1949'daki üç seviyeli iletişim modeline dayanıyor.

Shannon bildiğiniz gibi Seviye A'yı, yani Teknik Seviyeyi tanımlamıştı: 'Gönderilen semboller fiziksel kanaldan ne kadar hatasız geçer?' 1G'den 5G'ye kadar hücresel ağlar ve TCP/IP ailesi tamamen bu Seviye A'yı optimize etti. İçeriğin bir video mu, bir koordinat mı olduğu umursanmaksızın bitler taşındı.

Ancak Weaver, Seviye B ve Seviye C'yi tanımlamıştı:
Seviye B Semantik İletişimdir: İletilen sembol hedef anlamı doğru aktarıyor mu?
Seviye C ise Etkililik / Pragmatik İletişimdir: İletilen bilgi, alıcının görevi başarıyla yerine getirmesini sağlıyor mu?

İşte SAPS, mobil iletişimi yalnızca Seviye A'ya sıkışıp kalmaktan kurtarıp, Seviye B (Semantik) ve Seviye C (Pragmatik) seviyelerine yükseltmektedir. Katman 6 ile ajanların görevi ve niyetini modelliyor, Katman 4 ve 1 ile anlamsal entropiyi ve sinirsel fiziksel iletimi yönetiyoruz."""
    )

    # =========================================================================
    # SLIDE 4: 4 Major Bottlenecks of Traditional Protocols
    # =========================================================================
    s4 = prs.slides.add_slide(blank_layout)
    add_slide_header(s4, "Geleneksel Protokollerin Yapay Zeka Ajanlarındaki 4 Büyük Darboğazı", "1. Problem Tanımı")

    b_cards = [
        ("1. Serileştirme & JSON Darboğazı", 
         "Yüksek boyutlu KV-cache ve tensörlerin JSON/Protobuf metnine dönüştürülmesi, radyo iletiminden önce %60'a varan işlemci ve gecikme yükü yaratır.", RED),
        ("2. Kör ARQ & Yeniden İletim Fırtınaları", 
         "TCP ve QUIC, kaybolan anlamsız bir boşluk veya dolgu kelimesiyle kritik bir engel koordinatını aynı aciliyetle ele alır; tüm veri akışını kilitler.", RED),
        ("3. Statik IP & Topolojik Katılık", 
         "IP yönlendirmesi coğrafi/topolojik adrese göre yapılır. Ajanların ise IP adresine değil; boş GPU VRAM'ine ve uygun ağırlıklara sahip uç düğümlere ihtiyacı vardır.", GOLD),
        ("4. Fiziksel Katmandaki Uçurum Etkisi (Cliff Effect)", 
         "Klasik dijital modülasyonlar (QAM/OFDM), mobil sönümleme SNR eşiğinin altına indiği an aniden çöker; paket kaybı %20'yi aşınca iletişim sıfırlanır.", GOLD),
    ]

    for idx, (title, desc, col) in enumerate(b_cards):
        col_x = Inches(0.8) if idx % 2 == 0 else Inches(6.8)
        row_y = Inches(1.6) if idx < 2 else Inches(4.3)
        add_card(s4, col_x, row_y, Inches(5.7), Inches(2.4), title=title, border_color=col)
        tb = s4.shapes.add_textbox(col_x + Inches(0.3), row_y + Inches(0.75), Inches(5.1), Inches(1.45))
        p = tb.text_frame.paragraphs[0]
        p.text = desc
        p.font.size = Pt(13)
        p.font.color.rgb = LIGHT_GRAY

    set_speaker_notes(
        s4,
        """⏱️ [Hedef Süre: 03:45 - 05:00]
🎯 [Temel Mesaj]: Geleneksel HTTP/3 + TCP/QUIC mimarisinin neden çöktüğünü 4 somut teknik darboğazla açıklamak.

🎙️ [Konuşma Metni]:
Mevcut internet mimarisini mobil yapay zeka ajanlarında çalıştırdığımızda karşımıza çıkan 4 büyük teknik darboğaz şunlardır:

1. Serileştirme Yükü: Bir LLM'in dikkat matrisini veya tensörünü göndermek için JSON veya Protobuf'a çevirmek muazzam bir CPU yükü ve gecikme üretir.
2. Kör Yeniden İletim (Blind ARQ): TCP bir virgül veya dolgu kelimesi kaybolduğunda dahi tüm hattı bekletir. Bu durum mobil sönümlemeli kanallarda yeniden iletim fırtınalarına ve kuyruk gecikmelerinin patlamasına yol açar.
3. Statik IP Katılığı: Bir ajan '192.168.1.50' IP'sine bağlanmak istemez; '80 GB VRAM'i ve Llama-3 modeli yüklü olan en yakın uç sunucuya' bağlanmak ister. IP protokolü bu semantik niyetten tamamen habersizdir.
4. Uçurum Etkisi (Cliff Effect): 16-QAM veya 64-QAM gibi dijital modülasyonlarda kanal SNR'ı eşiğin 1 dB altına düştüğü an paketler tamamen bozulur ve çözülemez hale gelir.

SAPS, bu 4 darboğazın her birini kendi katmanlarında kökten çözmektedir."""
    )

    # =========================================================================
    # SLIDE 5: SAPS Architecture Overview: The 6 Layers
    # =========================================================================
    s5 = prs.slides.add_slide(blank_layout)
    add_slide_header(s5, "SAPS Sistem Mimarisi: 6 Katmanın Uçtan Uca Yeniden Tasarımı", "2. Mimari Genel Bakış")

    layers_data = [
        ("Katman 6 (YENİ)", "AIRL", "Agent Intent & Reasoning", "Ajanlar arası görev sözleşmesi, niyet anonsu ve dinamik offload"),
        ("Katman 5", "Application", "Direct KV-Cache Streaming", "8-bit dinamik tensör kuantizasyonu ve streaming (JSON yok, %95 tasarruf)"),
        ("Katman 4", "Transport", "IA-STP", "Shannon entropisi duyarlı seçici ARQ (düşük entropili kayıplar atlanır)"),
        ("Katman 3", "Network", "V-CCR", "Vektör uzayında kosinüs benzerliği tabanlı semantik niyet yönlendirmesi"),
        ("Katman 2", "Data Link", "SP-MAC", "4 seviyeli semantik kritiklik öncelik kuyruğu (Strict Priority MAC)"),
        ("Katman 1", "Physical", "Deep-JSCC", "Nöral Alıcı-Verici; gizil tensörleri doğrudan karmaşık IQ sembollerine eşler"),
    ]

    add_card(s5, Inches(0.8), Inches(1.5), Inches(11.7), Inches(5.3))
    t_box = s5.shapes.add_textbox(Inches(1.0), Inches(1.7), Inches(11.3), Inches(4.9))
    tf_s5 = t_box.text_frame

    for idx, (l_num, name, equiv, innov) in enumerate(layers_data):
        p = tf_s5.paragraphs[0] if idx == 0 else tf_s5.add_paragraph()
        p.text = f"[{l_num}]  {name:<14} |  {equiv:<26}  ➔  {innov}"
        p.font.size = Pt(13)
        p.font.color.rgb = CYAN if "YENİ" in l_num else (WHITE if idx < 3 else LIGHT_GRAY)
        p.font.bold = ("YENİ" in l_num or idx == 1 or idx == 2)

    set_speaker_notes(
        s5,
        """⏱️ [Hedef Süre: 05:00 - 06:30]
🎯 [Temel Mesaj]: Proje gereksiniminde istenen katmanların (a'dan f'ye) tamamının nasıl tasarlandığını ve yeni Katman 6'yı tanıtmak.

🎙️ [Konuşma Metni]:
Sayın Hocam, dersimizin proje yönergesinde belirtilen tüm katman gereksinimlerini harfiyen karşılayacak şekilde 6 katmanlı bir mimari inşa ettik:

En üstte yeni eklediğimiz Katman 6 yer alıyor: AIRL (Agent Intent & Reasoning Layer). Bu katman ajanların niyetlerini ilan etmesini ve mobil uç cihazın yükü arttığında hesaplamayı başka bir ajana devretmesini yönetir.
Katman 5 Uygulama Katmanımızda JSON'u tamamen terk ettik; doğrudan 8-bit kuantize KV-cache akışı yapıyoruz.
Katman 4 Nakil Katmanımız IA-STP, Shannon entropisine bakarak hangi paketin yeniden iletileceğini seçer.
Katman 3 Ağ Katmanımız V-CCR, IP adresi yerine anlamsal kabiliyet vektörleri üzerinden kosinüs benzerliğiyle paket yönlendirir.
Katman 2 Veri Bağı Katmanımız SP-MAC, 4 seviyeli donanımsal öncelik kuyruğuyla kritik çıkarım verilerine sıfır bekleme süresi tanır.
Katman 1 Fiziksel Katmanımız Deep-JSCC ise bit seviyesini atlayıp gizil tensörleri doğrudan sürekli IQ sembollerine eşleyen derin sinir ağı tabanlı bir alıcı-vericidir.

Şimdi bu katmanların detaylarına yakından bakalım."""
    )

    # =========================================================================
    # SLIDE 6: Layer 6 (NEW) — AIRL
    # =========================================================================
    s6 = prs.slides.add_slide(blank_layout)
    add_slide_header(s6, "Katman 6 (YENİ) — Ajan Niyet & Muhakeme Katmanı (AIRL)", "2. Katman Tasarımı")

    add_card(s6, Inches(0.8), Inches(1.6), Inches(5.6), Inches(5.2), title="AIRL Temel Mekanizmaları")
    tb = s6.shapes.add_textbox(Inches(1.0), Inches(2.3), Inches(5.2), Inches(4.3))
    tf = tb.text_frame
    tf.word_wrap = True

    pts = [
        "Dinamik Offload Karar Mekanizması: Mobil ajanın işlemci yükü ve batarya seviyesini izler. Yük >= %75 veya Batarya < %20 ise hesaplamayı uç ağa devreder.",
        "Anlamsal Yetenek Eşleme: Ağdaki uç düğümlerin yetenek vektörlerini (Görsel Muhakeme, Kod Üretimi, Matematiksel Çıkarım) sorgular.",
        "Otonom Sözleşme Müzakeresi (Task Contracting): Görev teklifleri yayınlar, en uygun uç düğümle 1.2 milisaniyede bağlayıcı sözleşme imzalar.",
        "Ortak Bağlam Vektörü Uyumu: Ajanların dahili durum vektörlerini sürekli senkronize eder: c_sync = (1 - α) c_local + α c_remote.",
    ]
    for idx, pt in enumerate(pts):
        p = tf.paragraphs[0] if idx == 0 else tf.add_paragraph()
        p.text = f"• {pt}"
        p.font.size = Pt(12.5)
        p.font.color.rgb = LIGHT_GRAY

    # Right Card: Flow diagram text
    add_card(s6, Inches(6.8), Inches(1.6), Inches(5.7), Inches(5.2), title="AIRL Ajanlar Arası İş Akışı", border_color=CYAN)
    tb_r = s6.shapes.add_textbox(Inches(7.1), Inches(2.4), Inches(5.1), Inches(4.2))
    tf_r = tb_r.text_frame
    workflow_text = (
        "1. Mobil Ajan (Yük = %88, Batarya = %45)\n"
        "   └─ Görev: Görsel Engel Tespiti (Compute-intensive)\n\n"
        "2. AIRL Niyet Yayını (Intent Broadcast)\n"
        "   └─ Hedef: VISUAL_REASONING, Gereken VRAM: 16 GB\n\n"
        "3. Uç Ağ Keşfi & Skorlama\n"
        "   └─ Aday: 'edge_vision_01' (NVIDIA H100, 80GB VRAM)\n"
        "   └─ Semantik Uyum Skoru: 0.94\n\n"
        "4. Bağlayıcı Sözleşme İmzalandı\n"
        "   └─ Durum: [KABUL EDİLDİ] - 1.2 ms içinde\n\n"
        "5. Bağlam Senkronizasyonu Aktif\n"
        "   └─ Paylaşılan Durum Kosinüs Hizalaması = 0.98"
    )
    p = tf_r.paragraphs[0]
    p.text = workflow_text
    p.font.size = Pt(13)
    p.font.color.rgb = WHITE

    set_speaker_notes(
        s6,
        """⏱️ [Hedef Süre: 06:30 - 08:00]
🎯 [Temel Mesaj]: Klasik modelde bulunmayan, SAPS'a özgü Katman 6'nın (AIRL) inovasyonunu açıklamak.

🎙️ [Konuşma Metni]:
Katman 6, SAPS mimarisinin en özgün yeniliğidir. Klasik OSI veya TCP/IP modelinde böyle bir katman bulunmamaktadır.
AIRL, doğrudan yapay zeka ajanlarının çalışma prensiplerine odaklanır. Bir mobil ajan (örneğin kamerasıyla çevre taraması yapan bir drone), işlemci yükü %75'in üzerine çıktığında veya bataryası kritik seviyeye indiğinde görevi yerel olarak sürdüremez.

AIRL bu noktada devreye girer:
Önce ağa bir niyet anonsu (Intent Broadcast) yapar. Bu anonsta görevin tipi, gerekli bellek ve beklenen doğruluk belirtilir.
Ağdaki uç sunucular teklif sunar. Ajanımız kosinüs benzerliği ve donanım uygunluğuna göre en yüksek skoru alan 'edge_vision_01' sunucusunu seçer.
1.2 milisaniye gibi rekor bir sürede aralarında bağlayıcı bir sözleşme imzalanır ve ortak bağlam vektörleri senkronize edilerek işlem alt katmanlara devredilir.
Böylece iletişim başlamadan önce 'kimin, hangi niyetle ne yapacağı' kesinleşmiş olur."""
    )

    # =========================================================================
    # SLIDE 7: Layer 6 Deep Dive — Multi-Agent State Machine
    # =========================================================================
    s7 = prs.slides.add_slide(blank_layout)
    add_slide_header(s7, "Katman 6 Derinlemesine: Çoklu Ajan Müzakere Durum Makinesi", "2. Katman Tasarımı")

    add_card(s7, Inches(0.8), Inches(1.6), Inches(11.7), Inches(5.2), title="AIRL Sonlu Durum Makinesi (Finite State Machine - FSM)")
    tb_s7 = s7.shapes.add_textbox(Inches(1.0), Inches(2.2), Inches(11.3), Inches(4.4))
    tf_s7 = tb_s7.text_frame

    fsm_steps = [
        ("IDLE (Boşta)", "Mobil ajan yerel çıkarım yapar. Sistem yükü L < 0.75 ve Batarya B > 0.20 olduğu sürece iletişim başlatılmaz; enerji tasarrufu sağlanır."),
        ("DISCOVERY (Keşif)", "Tetikleyici: L >= 0.75. Ajan, görev tanımlayıcı gömme vektörünü (Task Embedding Vector e_t) broadcast eder ve uygun uç düğümleri listeler."),
        ("PROPOSAL & SCORING (Teklif & Puanlama)", "Aday düğümler yük, VRAM ve kabiliyet vektörlerini döndürür. Skor fonksiyonu hesaplanır: S = 0.50 * Sim(e_t, e_c) + 0.30 * (1 - L_node) + 0.20 * (VRAM_avail / VRAM_req)."),
        ("BINDING (Sözleşme Bağlama)", "En yüksek skoru alan aday seçilir, kriptografik sözleşme imzalanır ve görev oturumu açılır."),
        ("CONTEXT_SYNC & EXECUTION", "İki ajanın dahili KV durumları sürekli hizalanır: c_t = (1 - α)c_{t-1} + α e_remote. Görev tamamlanınca IDLE durumuna dönülür."),
    ]

    for idx, (step_title, step_desc) in enumerate(fsm_steps):
        p = tf_s7.paragraphs[0] if idx == 0 else tf_s7.add_paragraph()
        p.text = f"• {step_title}: {step_desc}"
        p.font.size = Pt(13)
        p.font.color.rgb = CYAN if idx == 2 else WHITE
        p.font.bold = (idx == 2)

    set_speaker_notes(
        s7,
        """⏱️ [Hedef Süre: 08:00 - 09:15]
🎯 [Temel Mesaj]: AIRL katmanının arkasındaki matematiksel durum makinesini ve çok kriterli karar formülünü açıklamak.

🎙️ [Konuşma Metni]:
Hocam, AIRL katmanımız arka planda kesin bir Sonlu Durum Makinesi (FSM) ile yönetilir.
Ajan normal şartlarda IDLE durumundadır; yani yerel kaynaklar yetiyorsa boş yere telsiz yayını yapıp batarya harcamaz.
Yük eşiği aşıldığında DISCOVERY fazına geçer.
Buradaki en kritik yeniliğimiz 'PROPOSAL & SCORING' aşamasıdır. Ekranda gördüğünüz formülle üç farklı bileşeni ağırlıklandırıyoruz:
1. Semantik kabiliyet benzerliği (%50 ağırlık),
2. Hedef düğümün mevcut boş işlem kapasitesi (%30 ağırlık),
3. VRAM yeterlilik oranı (%20 ağırlık).

Bu sayede sadece en yakın olan düğüm değil, o an görevi en yüksek hız ve hassasiyetle bitirebilecek düğüm seçilmektedir."""
    )

    # =========================================================================
    # SLIDE 8: Layer 5 — Application Layer: Direct KV-Cache Streaming
    # =========================================================================
    s8 = prs.slides.add_slide(blank_layout)
    add_slide_header(s8, "Katman 5 (Uygulama) — Doğrudan KV-Cache & Tensör Akışı", "2. Katman Tasarımı")

    add_card(s8, Inches(0.8), Inches(1.6), Inches(5.6), Inches(5.2), title="KV-Cache Tensör Sıkıştırma")
    tb8 = s8.shapes.add_textbox(Inches(1.0), Inches(2.3), Inches(5.2), Inches(4.3))
    tf8 = tb8.text_frame
    tf8.word_wrap = True
    pts8 = [
        "Metin Serileştirmenin Sonu: JSON ve Protobuf tamamen devreden çıkarılmış, doğrudan bellek içi tensör aktarımı benimsenmiştir.",
        "Rank Truncation (Matris İndirgeme): Dikkat (Attention) matrislerinin en baskın tekil değerleri tutulur, önemsiz boyutlar kırpılır.",
        "8-Bit Dinamik Kuantizasyon: Float32 tensör değerleri, min-scale metaverisi korunarak dinamik şekilde Uint8 tamsayılara ölçeklenir.",
        "Deneysel Sonuç: 65.536 baytlık ham dikkat tensörü, anlam kaybı olmaksızın 3.276 bayta indirilmiştir (%95.0 bant genişliği tasarrufu).",
    ]
    for idx, pt in enumerate(pts8):
        p = tf8.paragraphs[0] if idx == 0 else tf8.add_paragraph()
        p.text = f"• {pt}"
        p.font.size = Pt(13)
        p.font.color.rgb = LIGHT_GRAY

    # Right Card: Mathematical formulation
    add_card(s8, Inches(6.8), Inches(1.6), Inches(5.7), Inches(5.2), title="Kuantizasyon Matematiği & Veri Yapısı", border_color=CYAN)
    tb8_r = s8.shapes.add_textbox(Inches(7.0), Inches(2.3), Inches(5.3), Inches(4.3))
    tf8_r = tb8_r.text_frame
    tf8_r.word_wrap = True
    formula_text = (
        "1. Ölçekleme Faktörü (Scale Factor):\n"
        "   S = (max(X) - min(X)) / 255\n\n"
        "2. Kuantize Tensör Haritalama (Float32 -> Uint8):\n"
        "   q_i = round( (x_i - min(X)) / S )\n\n"
        "3. Ters Kuantizasyon (Dekompresyon):\n"
        "   x_hat_i = (q_i * S) + min(X)\n\n"
        "4. Paket Başlık Yapısı (SAPS Tensor Header):\n"
        "   [TensorID: 16b] | [Shape: 4x16b] | [Scale: 32b] |\n"
        "   [MinVal: 32b] | [Payload: N x 8b]\n\n"
        "✔ Standart HTTP JSON Başlığı: ~800 bayt ek yük\n"
        "✔ SAPS Tensör Başlığı: Yalnızca 18 bayt ek yük!"
    )
    p = tf8_r.paragraphs[0]
    p.text = formula_text
    p.font.size = Pt(12.5)
    p.font.color.rgb = WHITE

    set_speaker_notes(
        s8,
        """⏱️ [Hedef Süre: 09:15 - 10:30]
🎯 [Temel Mesaj]: Katman 5'in JSON serileştirmesini nasıl ortadan kaldırdığını ve %95 veri sıkıştırmasını nasıl başardığını göstermek.

🎙️ [Konuşma Metni]:
Uygulama katmanında günümüz web standartları gRPC, REST ve JSON kullanır. Bir LLM veya görme modelinin katman çıktılarını JSON formatına çevirmek (string serialization), devasa bir hesaplama ve bant genişliği israfıdır.

SAPS Katman 5'te 'Direct KV-Cache Streaming' mimarisi geliştirdik.
Transformatör modellerinin en çok bellek kaplayan kısmı Key-Value dikkat tensörleridir. Biz bu tensörleri Float32'den dinamik 8-bit kuantizasyonla Uint8 formatına indirgiyoruz. Ekranda formülünü gördüğümüz bu dinamik ölçekleme sayesinde, 65 KB'lık bir dikkat tensörü 3.2 KB'a düşüyor.
Üstelik HTTP'nin 800 baytlık devasa başlıkları yerine, yalnızca 18 baytlık ultra hafif SAPS tensör başlığı kullanıyoruz.
Bu sayede sadece uygulama katmanında %95 bant genişliği tasarrufu elde ediyoruz."""
    )

    # =========================================================================
    # SLIDE 9: Layer 4 — Transport Layer: IA-STP
    # =========================================================================
    s9 = prs.slides.add_slide(blank_layout)
    add_slide_header(s9, "Katman 4 (Nakil) — IA-STP: Anlamsal Entropi Duyarlı ARQ", "2. Katman Tasarımı")

    add_card(s9, Inches(0.8), Inches(1.6), Inches(5.6), Inches(5.2), title="IA-STP Çalışma Prensibi")
    tb9 = s9.shapes.add_textbox(Inches(1.0), Inches(2.3), Inches(5.2), Inches(4.3))
    tf9 = tb9.text_frame
    tf9.word_wrap = True
    pts9 = [
        "Kör Yeniden İletim Reddi: TCP veya QUIC gibi düşen her paketi koşulsuz şartsız yeniden iletmez.",
        "Shannon Bilgi Entropisi Hesabı: Her bir token veya tensör bloğunun taşıdığı bilgi miktarı ölçülür.",
        "Seçici İletim Kararı: Bilgi yoğunluğu eşik değerinin üzerindeyse (H >= tau) kayıpta yeniden iletilir.",
        "Bilinçli Paket Atlama: Düşük entropili bağlaçlar ve dolgu tokenları mobil sönümleme anında kasten atlanır.",
        "Kazanım: Baş-sıra tıkanması (Head-of-Line Blocking) ve yeniden iletim patlamaları tamamen engellenir.",
    ]
    for idx, pt in enumerate(pts9):
        p = tf9.paragraphs[0] if idx == 0 else tf9.add_paragraph()
        p.text = f"• {pt}"
        p.font.size = Pt(13)
        p.font.color.rgb = LIGHT_GRAY

    # Right Card: Token Entropy Comparison
    add_card(s9, Inches(6.8), Inches(1.6), Inches(5.7), Inches(5.2), title="IA-STP Seçici Karar Matrisi", border_color=GREEN)
    tb9_r = s9.shapes.add_textbox(Inches(7.0), Inches(2.3), Inches(5.3), Inches(4.3))
    tf9_r = tb9_r.text_frame
    tf9_r.word_wrap = True

    pts9_r = [
        "Yüksek Entropili Token Örneği:\n  'X=41.284, Y=28.712, ACİL_DUR'\n  Entropi: H = 2.85 nats (Eşik = 1.0)\n  Aksiyon: [MUTLAK YENİDEN İLETİM - ARQ]",
        "Düşük Entropili Token Örneği:\n  'bir, ile, ve, bu, [PAD]'\n  Entropi: H = 0.18 nats (Eşik = 1.0)\n  Aksiyon: [BİLİNÇLİ ATLA - NO RETRANSMISSION]",
        "Sistemik Etki:\n  Mobil telsiz kanalında ani sönümleme (deep fade) olduğunda, kuyrukta bekleyen onlarca anlamsız paket hattı kilitlemez.",
    ]
    for idx, pt in enumerate(pts9_r):
        p = tf9_r.paragraphs[0] if idx == 0 else tf9_r.add_paragraph()
        p.text = pt
        p.font.size = Pt(13)
        p.font.color.rgb = WHITE if idx < 2 else LIGHT_GRAY
        p.font.bold = (idx < 2)

    set_speaker_notes(
        s9,
        """⏱️ [Hedef Süre: 10:30 - 11:45]
🎯 [Temel Mesaj]: Katman 4 IA-STP protokolünün mantığını ve neden TCP/QUIC'ten üstün olduğunu anlatmak.

🎙️ [Konuşma Metni]:
Nakil katmanında geliştirdiğimiz protokolün adı IA-STP: Intent-Aware Semantic Transport Protocol.
TCP ve QUIC'in mobil yapay zeka ajanlarındaki en ölümcül kusuru 'kör yeniden iletimdir' (Blind ARQ).
Eğer mobil telsiz kanalında ani bir derin sönümleme (deep fading) yaşanırsa ve bir paket düşerse, TCP hattı durdurur ve o paket gelene kadar sonraki paketlerin teslimatını engeller (Head-of-Line Blocking).

IA-STP bu sorunu Shannon bilgi entropisiyle çözer:
Paket içindeki her token'ın entropisi hesaplanır.
Örneğin bir İHA'nın 'ACİL_DUR' komutu veya 'X=41.284' koordinatı 2.85 nats entropiye sahiptir. Eşiğimiz 1.0 olduğu için bu paket düşerse derhal yeniden iletilir.
Ancak 've', 'bir' gibi dolgu sözcükleri veya padding tokenları 0.18 nats entropiye sahiptir. Bu paket düşerse IA-STP bunu kasten yeniden iletmez, atlar!
Çünkü alıcı ajan dil modeli o dolguyu bağlamdan rahatlıkla tamamlayabilir. Böylece yeniden iletim fırtınaları önlenir."""
    )

    # =========================================================================
    # SLIDE 10: Layer 4 Deep Dive — Entropy Mathematical Formulation
    # =========================================================================
    s10 = prs.slides.add_slide(blank_layout)
    add_slide_header(s10, "Katman 4 Derinlemesine: Shannon Entropisi Matematiksel Modeli", "2. Katman Tasarımı")

    add_card(s10, Inches(0.8), Inches(1.6), Inches(11.7), Inches(5.2), title="IA-STP Entropi Karar Kuralları & Formülasyon")
    tb10 = s10.shapes.add_textbox(Inches(1.0), Inches(2.2), Inches(11.3), Inches(4.4))
    tf10 = tb10.text_frame

    form_pts = [
        "1. Koşullu Olasılık Dağılımı: Dil modeli kelime dağarcığı V üzerinde t_k token'ının olasılık vektörü p(v | t_{<k}) çıkarılır.",
        "2. Shannon Token Entropisi Formülü:\n   H(t_k) = - ∑_{v ∈ V} p(v | t_{<k}) * ln( p(v | t_{<k}) )",
        "3. İkili Karar Mekanizması:\n   ARQ_Decision(t_k) = { RE-TRANSMIT,  eğer H(t_k) >= tau_entropy\n                       { SKIP_LOSS,    eğer H(t_k) <  tau_entropy",
        "4. Dinamik Eşik Uyarlama (SNR-Aware Threshold):\n   tau_entropy(SNR) = tau_base * (1 + beta * exp(-SNR / 10))\n   (Kanal kalitesi düştüğünde eşik otomatik yükseltilerek radyo trafiği sadece en kritik emirlere tahsis edilir).",
    ]
    for idx, pt in enumerate(form_pts):
        p = tf10.paragraphs[0] if idx == 0 else tf10.add_paragraph()
        p.text = pt
        p.font.size = Pt(13.5)
        p.font.color.rgb = CYAN if idx == 1 or idx == 3 else WHITE
        p.font.bold = (idx == 1 or idx == 3)

    set_speaker_notes(
        s10,
        """⏱️ [Hedef Süre: 11:45 - 13:00]
🎯 [Temel Mesaj]: Entropi formülünün ve dinamik eşik mekanizmasının arkasındaki matematiksel kesinliği aktarmak.

🎙️ [Konuşma Metni]:
Sayın Hocam, bu formülasyon IA-STP'nin kalbini oluşturuyor.
Dil modelinin kelime dağarcığı üzerindeki softmax olasılık dağılımından Shannon entropisini hesaplıyoruz:
H(t_k) = - sum p(v) ln p(v).
Eğer model bir sonraki kelimeden %99 eminse (örneğin dil bilgisel bir bağlaç), entropi sıfıra yaklaşır. Ama modelin belirsizliği yüksekse veya beklenmedik kritik bir bilgi geliyorsa entropi zirve yapar.

Ayrıca protokolümüze 'Dinamik Eşik Uyarlama' ekledik:
Ekranda 4. maddede gördüğünüz üzere, mobil telsiz kanalının SNR'ı düştüğünde tau eşiği otomatik olarak yukarı ötelenir.
Böylece kanal kötüleştiğinde sadece ve sadece hayati öneme sahip komutlar telsizden geçer; gereksiz hiçbir trafik kanalı meşgul etmez."""
    )

    # =========================================================================
    # SLIDE 11: Layer 3 — Network Layer: V-CCR
    # =========================================================================
    s11 = prs.slides.add_slide(blank_layout)
    add_slide_header(s11, "Katman 3 (Ağ) — V-CCR: Vektör Uzayında Anlamsal Yönlendirme", "2. Katman Tasarımı")

    add_card(s11, Inches(0.8), Inches(1.6), Inches(5.6), Inches(5.2), title="V-CCR Yönlendirme İlkeleri")
    tb11 = s11.shapes.add_textbox(Inches(1.0), Inches(2.3), Inches(5.2), Inches(4.3))
    tf11 = tb11.text_frame
    tf11.word_wrap = True
    pts11 = [
        "IP Yönlendirme Tablolarının Tasfiyesi: CIDR blokları ve IP adresleri yerine yüksek boyutlu gömme uzayında arama yapılır.",
        "Kosinüs Benzerliği Metriği: Paket başlığındaki görev vektörü ile ağdaki uç düğümlerin yetenek vektörleri karşılaştırılır.",
        "Sıfır DNS Gecikmesi: Alan adı çözme (DNS lookup) ve TCP üçlü el sıkışması bekleme süreleri tamamen elenir.",
        "Otonom Rota Seçimi: Benzerlik skoru eşiği (Sim >= 0.75) geçen ve yükü en az olan düğüme paket tek hamlede yönlendirilir.",
    ]
    for idx, pt in enumerate(pts11):
        p = tf11.paragraphs[0] if idx == 0 else tf11.add_paragraph()
        p.text = f"• {pt}"
        p.font.size = Pt(13)
        p.font.color.rgb = LIGHT_GRAY

    # Right Card: Formula and example
    add_card(s11, Inches(6.8), Inches(1.6), Inches(5.7), Inches(5.2), title="Yönlendirme Metriği & Örnek", border_color=CYAN)
    tb11_r = s11.shapes.add_textbox(Inches(7.0), Inches(2.3), Inches(5.3), Inches(4.3))
    tf11_r = tb11_r.text_frame
    tf11_r.word_wrap = True
    r_text = (
        "1. Kosinüs Benzerlik Formülü:\n"
        "   Sim(v_task, v_node) = (v_task · v_node) / (||v_task|| ||v_node||)\n\n"
        "2. Rota Karar Kuralı:\n"
        "   NextHop = argmax_{i ∈ Nodes} [ Sim(v_task, v_i) - λ * Load_i ]\n\n"
        "3. Karşılaştırma:\n"
        "   Klasik IP: 'Paketi 10.0.4.12 IP adresine gönder.'\n"
        "   (Hedef sunucunun çöküp çökmediğini bilmez).\n\n"
        "   V-CCR: 'Paketi görsel muhakeme benzerliği en yüksek ve boş GPU'su olan en yakın düğüme aktar.'\n"
        "   ✔ Doğrudan amaca yönelik yönlendirme!"
    )
    p = tf11_r.paragraphs[0]
    p.text = r_text
    p.font.size = Pt(12.5)
    p.font.color.rgb = WHITE

    set_speaker_notes(
        s11,
        """⏱️ [Hedef Süre: 13:00 - 14:15]
🎯 [Temel Mesaj]: Katman 3'te IP adreslerinin yerine anlamsal yetenek vektörlerinin nasıl geçtiğini açıklamak.

🎙️ [Konuşma Metni]:
Ağ katmanında geliştirdiğimiz protokol V-CCR: Vector-space Content & Capability Routing.
Klasik IP yönlendirmesi statik topolojiye bakar. Ancak mobil bir ajan için gideceği yerin IP adresi anlamsızdır. Ajan için önemli olan, o paketi alıp işleyebilecek yapay zeka modelinin nerede olduğudur.

V-CCR'da her paketin başlığında d-boyutlu bir semantik niyet vektörü bulunur. Ağdaki uç düğümler de kendi uzmanlıklarını ve boş VRAM durumlarını vektör olarak bildirir.
Yönlendirici (Router), kosinüs benzerliği formülü ile hedef düğümü belirler.
Böylece DNS sorgusu, IP tablosu arama gecikmesi olmadan paket doğrudan en uygun GPU'ya sahip uç düğüme yönlendirilir."""
    )

    # =========================================================================
    # SLIDE 12: Layer 2 — Data Link Layer: SP-MAC
    # =========================================================================
    s12 = prs.slides.add_slide(blank_layout)
    add_slide_header(s12, "Katman 2 (Veri Bağı) — SP-MAC: Semantik Öncelikli MAC", "2. Katman Tasarımı")

    add_card(s12, Inches(0.8), Inches(1.6), Inches(5.6), Inches(5.2), title="4 Seviyeli Öncelik Mimarisi")
    tb12 = s12.shapes.add_textbox(Inches(1.0), Inches(2.3), Inches(5.2), Inches(4.3))
    tf12 = tb12.text_frame
    tf12.word_wrap = True

    queues = [
        ("Öncelik 0 (CRITICAL)", "Güvenlik, acil çarpışma önleme, navigasyon koordinatları. Kesintisiz sıfır kuyruk gecikmesi."),
        ("Öncelik 1 (HIGH)", "Yüksek entropili muhakeme tensörleri, niyet sözleşmeleri."),
        ("Öncelik 2 (MEDIUM)", "Ara durum dikkat ağırlıkları, bağlam senkronizasyonu."),
        ("Öncelik 3 (LOW)", "Telemetri logları, model ağırlık güncelleme parçacıkları."),
    ]
    for idx, (q_name, q_desc) in enumerate(queues):
        p = tf12.paragraphs[0] if idx == 0 else tf12.add_paragraph()
        p.text = f"• {q_name}:\n  {q_desc}\n"
        p.font.size = Pt(12)
        p.font.color.rgb = RED if idx == 0 else (GOLD if idx == 1 else LIGHT_GRAY)
        p.font.bold = (idx == 0 or idx == 1)

    # Right Card: Hardware queuing
    add_card(s12, Inches(6.8), Inches(1.6), Inches(5.7), Inches(5.2), title="SP-MAC Kanal Erişim Mekanizması", border_color=GOLD)
    tb12_r = s12.shapes.add_textbox(Inches(7.0), Inches(2.3), Inches(5.3), Inches(4.3))
    tf12_r = tb12_r.text_frame
    tf12_r.word_wrap = True
    mac_text = (
        "1. Katı Öncelikli Çekme (Strict-Priority Dequeuing):\n"
        "   Kanal boşaldığında CRITICAL kuyruğunda tek bir paket dahi varsa, diğer alt kuyruklar asla kanala erişemez.\n\n"
        "2. Çarpışma Önleme & Dinamik CW:\n"
        "   Klasik 802.11 CSMA/CA'da tüm paketler benzer çekişme penceresine (Contention Window - CW) sahiptir.\n"
        "   SP-MAC'te CRITICAL paketler CW_min = 1 kullanarak anında kanala basılır; düşük öncelikli paketler ise CW_min = 31 ile bekletilir.\n\n"
        "✔ Kritik çıkarım paketleri için 0.00 ms kuyruk gecikmesi!"
    )
    p = tf12_r.paragraphs[0]
    p.text = mac_text
    p.font.size = Pt(12.5)
    p.font.color.rgb = WHITE

    set_speaker_notes(
        s12,
        """⏱️ [Hedef Süre: 14:15 - 15:30]
🎯 [Temel Mesaj]: Katman 2 SP-MAC protokolünün kanal çekişmesini ve kuyruk gecikmesini nasıl ortadan kaldırdığını açıklamak.

🎙️ [Konuşma Metni]:
Veri bağı katmanında geliştirdiğimiz SP-MAC (Semantic-Priority MAC), 4 seviyeli bir donanımsal kuyruk yapısına sahiptir.
Klasik Wi-Fi veya hücresel MAC katmanlarında bir cihaz telemetri logu gönderirken aynı anda gelen kritik bir engel algılama paketi kuyrukta bekleyebilir.
SP-MAC bunu kesin bir strict-priority mekanizmasıyla çözer:
CRITICAL kuyruğundaki acil durum ve navigasyon paketleri Contention Window'u minimum tutarak (CW=1) kanala anında erişir.
Düşük öncelikli arka plan güncellemeleri ise bekletilir.
Böylece kritik kararlarda donanım seviyesinde sıfır kuyruk gecikmesi garanti altına alınır."""
    )

    # =========================================================================
    # SLIDE 13: Layer 1 — Physical Layer: Deep-JSCC
    # =========================================================================
    s13 = prs.slides.add_slide(blank_layout)
    add_slide_header(s13, "Katman 1 (Fiziksel) — Deep-JSCC: Nöral Alıcı-Verici Mimarisi", "2. Katman Tasarımı")

    add_card(s13, Inches(0.8), Inches(1.6), Inches(5.6), Inches(5.2), title="Derin Birleşik Kaynak-Kanal Kodlama")
    tb13 = s13.shapes.add_textbox(Inches(1.0), Inches(2.3), Inches(5.2), Inches(4.3))
    tf13 = tb13.text_frame
    tf13.word_wrap = True
    pts13 = [
        "Ayrı Kodlama Teoreminin Aşılması: Shannon'ın klasik kaynak ve kanal kodlamayı ayıran yaklaşımı, sonlu blok uzunluklarında optimal değildir.",
        "Nöral Verici (Encoder): Çok katmanlı MLP ağı, gizil tensör vektörünü doğrudan sürekli karmaşık IQ sembollerine eşler.",
        "Güç Normalizasyonu: Verici anten gücü kısıtına uymak için sembol enerjisi normalize edilir: E[|s|^2] = 1.",
        "Nöral Alıcı (Decoder): Mobil sönümlemeye ve gürültüye maruz kalan IQ sembollerini doğrudan anlamsal tensöre dönüştürür.",
    ]
    for idx, pt in enumerate(pts13):
        p = tf13.paragraphs[0] if idx == 0 else tf13.add_paragraph()
        p.text = f"• {pt}"
        p.font.size = Pt(13)
        p.font.color.rgb = LIGHT_GRAY

    # Right Card: Architecture
    add_card(s13, Inches(6.8), Inches(1.6), Inches(5.7), Inches(5.2), title="Deep-JSCC Boru Hattı & Fading Kanalı", border_color=CYAN)
    tb13_r = s13.shapes.add_textbox(Inches(7.0), Inches(2.3), Inches(5.3), Inches(4.3))
    tf13_r = tb13_r.text_frame
    tf13_r.word_wrap = True
    jscc_arch = (
        "Girdi: x ∈ R^D (Gizil Temsil Tensörü)\n"
        "   ↓\n"
        "[Nöral Encoder: MLP(D -> 128 -> 2 * K)]\n"
        "   ↓\n"
        "[Güç Normalizasyonu: s = z / sqrt(E[|z|^2])]\n"
        "   ↓ IQ Sembolleri (Karmaşık Kanal)\n"
        "╔═══════════════════════════════════════╗\n"
        "║  Mobil Telsiz Kanalı: y = h * s + n   ║\n"
        "║  (Rayleigh / Rician / Sionna 3GPP)    ║\n"
        "╚═══════════════════════════════════════╝\n"
        "   ↓ Gözlemlenen Semboller: y\n"
        "[Nöral Decoder: MLP(2 * K -> 128 -> D)]\n"
        "   ↓\n"
        "Çıktı: x_hat ∈ R^D (Yeniden Oluşturulan Tensör)"
    )
    p = tf13_r.paragraphs[0]
    p.text = jscc_arch
    p.font.size = Pt(12)
    p.font.color.rgb = WHITE

    set_speaker_notes(
        s13,
        """⏱️ [Hedef Süre: 15:30 - 16:45]
🎯 [Temel Mesaj]: Katman 1 Deep-JSCC nöral mimarisini ve klasik sayısal QAM'dan farkını açıklamak.

🎙️ [Konuşma Metni]:
Fiziksel katmanda Deep-JSCC (Deep Joint Source-Channel Coding) nöral alıcı-verici mimarisini kurduk.
Bildiğiniz üzere Shannon'ın 1948'deki kaynak-kanal ayırma teoremi yalnızca sonsuz blok uzunluğunda geçerlidir. Mobil gecikmeye duyarlı sistemlerde kaynak kodlama (örneğin JPEG/MP3) ve kanal kodlamayı (LDPC/Turbo) ayırmak gecikmeyi artırır.

Deep-JSCC'de bir derin sinir ağı kullanıyoruz:
Ajanın ürettiği gizil tensör vektörü, çok katmanlı bir yapay sinir ağı (MLP Encoder) tarafından doğrudan karmaşık IQ sembollerine dönüştürülür.
Bu sembollerin ortalama gücü 1'e normalize edilerek antene verilir.
Sinyal sönümlemeli kanaldan geçerken üzerine gürültü eklenir.
Alıcı taraftaki Nöral Decoder ise gürültülü IQ sembollerinden doğrudan anlamsal tensörü yeniden inşa eder.
Böylece bit hataları yerine sürekli bir tensör dönüşümü yapılır."""
    )

    # =========================================================================
    # SLIDE 14: Deep-JSCC Physical Layer — Mathematical Loss Formulation
    # =========================================================================
    s14 = prs.slides.add_slide(blank_layout)
    add_slide_header(s14, "Fiziksel Katman Formülasyonu: Kayıp Fonksiyonu & Takımyıldızı", "2. Katman Tasarımı")

    add_card(s14, Inches(0.8), Inches(1.6), Inches(11.7), Inches(5.2), title="Nöral Takımyıldızı (Constellation) Şekillendirme & Uçtan Uca Optimizasyon")
    tb14 = s14.shapes.add_textbox(Inches(1.0), Inches(2.2), Inches(11.3), Inches(4.4))
    tf14 = tb14.text_frame

    j_pts = [
        "1. Uçtan Uca Nöral Kayıp Fonksiyonu (End-to-End MSE Loss):\n   L(θ, φ) = (1 / B) * ∑_{i=1}^B || x_i - x_hat_i(θ, φ; h, σ) ||^2",
        "2. Nöral Takımyıldızı (Neural Constellation Shaping):\n   Klasik 16-QAM veya 64-QAM katı kare ızgaralara kilitlidir. Deep-JSCC ise gürültü dağılımına göre sürekli ve dairesel Gauss benzeri takımyıldızları öğrenir. Bu sayede bit eşleme sınırları ortadan kalkar.",
        "3. Uçurum Etkisinin (Cliff Effect) Önlenmesi:\n   Klasik QAM'de SNR belirli bir eşiğin altına indiğinde sembol kararları tamamen kayar ve paket %100 kaybedilir.\n   Deep-JSCC'de ise SNR düştükçe yeniden oluşturulan tensördeki MSE gürültüsü kademeli olarak artar (Graceful Degradation); iletişim asla aniden kopmaz.",
    ]
    for idx, pt in enumerate(j_pts):
        p = tf14.paragraphs[0] if idx == 0 else tf14.add_paragraph()
        p.text = pt
        p.font.size = Pt(13.5)
        p.font.color.rgb = CYAN if idx == 0 else WHITE
        p.font.bold = (idx == 0 or idx == 2)

    set_speaker_notes(
        s14,
        """⏱️ [Hedef Süre: 16:45 - 18:00]
🎯 [Temel Mesaj]: Nöral takımyıldızının klasik QAM'a göre üstünlüğünü ve uçurum etkisini nasıl ortadan kaldırdığını açıklamak.

🎙️ [Konuşma Metni]:
Sayın Hocam, bu slaytta Deep-JSCC'nin neden klasik QAM modülasyonundan üstün olduğunu matematiksel olarak görüyoruz.
Modelimiz uçtan uca Ortalama Hata Karesi (MSE) kaybıyla eğitilir.
Klasik modülasyonlarda (16-QAM veya 64-QAM gibi) semboller katı bir kare ızgara üzerindedir. Bir sembol gürültü nedeniyle komşu kareye taştığında bitler tamamen ters döner ve tüm paket atılır.

Deep-JSCC ise sürekli bir uzayda çalışır. Sinir ağı kendi optimum takımyıldızını (neural constellation) serbestçe öğrenir.
Sonuç olarak: Kanalda şiddetli bir sönümleme yaşandığında iletişim sıfırlanmaz; tensördeki gürültü biraz artar ama genel anlam korunur.
Bu 'kademeli bozulma' (graceful degradation) özelliği, mobil telsiz kanallarında yapay zeka ajanlarının kesintisiz çalışabilmesinin anahtarıdır."""
    )

    # =========================================================================
    # SLIDE 15: NVIDIA Sionna Integration — 5G/6G Physical Layer
    # =========================================================================
    s15 = prs.slides.add_slide(blank_layout)
    add_slide_header(s15, "NVIDIA Sionna Entegrasyonu: 3GPP TR 38.901 Mobil Kanal Modeli", "3. İleri Seviye Doğrulama")

    add_card(s15, Inches(0.8), Inches(1.6), Inches(5.6), Inches(5.2), title="NVIDIA Sionna Çerçevesi")
    tb15 = s15.shapes.add_textbox(Inches(1.0), Inches(2.3), Inches(5.2), Inches(4.3))
    tf15 = tb15.text_frame
    tf15.word_wrap = True
    pts15 = [
        "Endüstri Standardı 5G/6G Fiziksel Katman Kütüphanesi: NVIDIA tarafından GPU hızlandırmalı geliştirilen Sionna 2.2 entegre edilmiştir.",
        "3GPP TR 38.901 Standardı: Kentsel Mikro Hücre (Urban Micro - UMi) ve Makro Hücre (UMa) senaryoları simüle edilmiştir.",
        "Gerçekçi Telsiz Parametreleri: Taşıyıcı frekansı fc = 3.5 GHz (5G NR Mid-band), araç/İHA hızına karşılık gelen 50 Hz Doppler frekansı.",
        "Çok Yollu Yayılım (Multipath Delay Spread): Gerçekçi kentsel yansımalar ve gölgeleme (shadowing) etkileri birebir modellenmiştir.",
    ]
    for idx, pt in enumerate(pts15):
        p = tf15.paragraphs[0] if idx == 0 else tf15.add_paragraph()
        p.text = f"• {pt}"
        p.font.size = Pt(13)
        p.font.color.rgb = LIGHT_GRAY

    # Right Card: Sionna Integration Code & Result preview
    add_card(s15, Inches(6.8), Inches(1.6), Inches(5.7), Inches(5.2), title="Sionna 3GPP Entegrasyon Mimarisi", border_color=GREEN)
    tb15_r = s15.shapes.add_textbox(Inches(7.0), Inches(2.3), Inches(5.3), Inches(4.3))
    tf15_r = tb15_r.text_frame
    tf15_r.word_wrap = True
    sionna_text = (
        "Entegrasyon Sınıfı: saps/channel/sionna_channel.py\n\n"
        "• SionnaAWGNChannel: Sionna tensör tabanlı gürültü modeli\n"
        "• SionnaFlatFadingChannel: Düz sönümlemeli kanal\n"
        "• Sionna3GPPChannel: 3GPP TR 38.901 UMi/UMa ışın izleme ve çok yollu sönümleme modeli\n\n"
        "PyTorch Uyumluluğu:\n"
        "Sionna 2.2'nin PyTorch desteği sayesinde, Deep-JSCC nöral katmanımız doğrudan Sionna 3GPP kanal nesnesine bağlanmıştır.\n\n"
        "✔ Test Doğrulaması: tests/test_sionna.py (3/3 Geçti)\n"
        "✔ Tam Yığın Testi: 30/30 Birim Test Başarıyla Tamamlandı!"
    )
    p = tf15_r.paragraphs[0]
    p.text = sionna_text
    p.font.size = Pt(12.5)
    p.font.color.rgb = WHITE

    set_speaker_notes(
        s15,
        """⏱️ [Hedef Süre: 18:00 - 19:15]
🎯 [Temel Mesaj]: NVIDIA Sionna entegrasyonunu vurgulayarak projenin ek puan kriterini ve 3GPP 5G/6G uyumunu anlatmak.

🎙️ [Konuşma Metni]:
Sayın Hocam, projemizin değerini ve gerçekçiliğini artırmak adına en güncel 5G/6G endüstri standardı olan NVIDIA Sionna kütüphanesini sistemimize entegre ettik.
NVIDIA Sionna, 3GPP TR 38.901 spesifikasyonuna tam uyumlu ışın izleme (ray tracing) ve kentsel çok yollu sönümleme modelleri sunmaktadır.

Sistemimizde 'saps/channel/sionna_channel.py' modülünü geliştirdik.
Taşıyıcı frekansını 3.5 GHz (5G NR bandı) ve Doppler frekansını 50 Hz (hareketli araç/drone hızı) olarak ayarladık.
Deep-JSCC sinir ağımızın ürettiği IQ sembollerini doğrudan bu Sionna 3GPP kanalından geçirerek test ettik.
Yazdığımız testler 'tests/test_sionna.py' altında %100 başarıyla geçmiş, toplam test sayımız 30'a yükselmiştir.
Böylece SAPS'ın başarısını sadece sentetik kanallarda değil, 3GPP standartlarında da kanıtlamış olduk."""
    )

    # =========================================================================
    # SLIDE 16: Discrete-Event Simulation Testbed Setup
    # =========================================================================
    s16 = prs.slides.add_slide(blank_layout)
    add_slide_header(s16, "Ayrık Olaylı Simülasyon Testbed'i & Değerlendirme Metodolojisi", "3. İmplementasyon")

    add_card(s16, Inches(0.8), Inches(1.6), Inches(5.6), Inches(5.2), title="SimPy + PyTorch Simülasyon Motoru")
    tb16 = s16.shapes.add_textbox(Inches(1.0), Inches(2.3), Inches(5.2), Inches(4.3))
    tf16 = tb16.text_frame
    tf16.word_wrap = True
    pts16 = [
        "Ayrık Olaylı Simülatör (DES): SimPy motoru ile paket kuyrukları, yayılım gecikmeleri ve işlem süreleri mikrosaniye hassasiyetinde modellenmiştir.",
        "Derin Öğrenme Entegrasyonu: PyTorch 2.14 tensör boru hattı SimPy olay döngüsüyle senkronize çalışır.",
        "Kusursuz Karşılaştırma Eşitliği: Hem SAPS hem de Geleneksel HTTP/3+QUIC yığını tıpatıp aynı kanal sönümleme izleri (fading realizations) üzerinde koşturulmuştur.",
        "Test Doğrulaması: 30 kapsamlı birim ve entegrasyon testi ile yazılım güvenilirliği tescillenmiştir.",
    ]
    for idx, pt in enumerate(pts16):
        p = tf16.paragraphs[0] if idx == 0 else tf16.add_paragraph()
        p.text = f"• {pt}"
        p.font.size = Pt(13)
        p.font.color.rgb = LIGHT_GRAY

    # Right Card: Channel parameters
    add_card(s16, Inches(6.8), Inches(1.6), Inches(5.7), Inches(5.2), title="Test Parametreleri & Kanal Özellikleri", border_color=CYAN)
    tb16_r = s16.shapes.add_textbox(Inches(7.0), Inches(2.3), Inches(5.3), Inches(4.3))
    tf16_r = tb16_r.text_frame
    tf16_r.word_wrap = True
    pts16_r = [
        "Rayleigh Sönümleme: Görüş hattı olmayan (NLOS) çok yollu mobil kentsel kanallar.",
        "Rician Sönümleme: Doğrudan görüş hattı (LOS) bileşeni (Rician K-faktörü = 3.0).",
        "NVIDIA Sionna 3GPP UMi: 3GPP TR 38.901 Kentsel Mikro Hücre modeli.",
        "SNR Tarama Aralığı: [0, 5, 10, 15, 20, 25, 30] dB.",
        "Karşılaştırma Temeli (Baseline): HTTP/3 + QUIC, tam ARQ, JSON serileştirme ve 16-QAM modülasyonu.",
    ]
    for idx, pt in enumerate(pts16_r):
        p = tf16_r.paragraphs[0] if idx == 0 else tf16_r.add_paragraph()
        p.text = f"✔ {pt}"
        p.font.size = Pt(13)
        p.font.color.rgb = WHITE if idx == 2 else LIGHT_GRAY
        p.font.bold = (idx == 2)

    set_speaker_notes(
        s16,
        """⏱️ [Hedef Süre: 19:15 - 20:15]
🎯 [Temel Mesaj]: Bilimsel deney metodolojisinin adilliğini ve SimPy + PyTorch altyapısını açıklamak.

🎙️ [Konuşma Metni]:
Simülasyon testbed'imizi Python ortamında SimPy ayrık olaylı simülasyon motoru ile PyTorch derin öğrenme kütüphanesini birleştirerek geliştirdik.
Buradaki en kritik bilimsel prensibimiz 'Adil Karşılaştırma Eşitliği'dir:
Hem SAPS hem de geleneksel HTTP/3 + QUIC protokol yığını, aynı rastgele tohumla (seed) üretilmiş tıpatıp aynı kanal sönümleme koşullarından geçirilmiştir.
SNR aralığı 0 dB ile 30 dB arasında taranmış; gecikme, paket kaybı, bant genişliği ve enerji tüketimi eş zamanlı kaydedilmiştir."""
    )

    # =========================================================================
    # SLIDE 17: Benchmark 1 — Latency vs SNR
    # =========================================================================
    s17 = prs.slides.add_slide(blank_layout)
    add_slide_header(s17, "Deney 1: Uçtan Uca Gecikme vs Mobil Kanal SNR (6.76x Hızlanma)", "4. Deneysel Sonuçlar")

    img_lat = _RESULTS / "latency_vs_snr.png"
    if img_lat.exists():
        s17.shapes.add_picture(str(img_lat), Inches(0.8), Inches(1.6), width=Inches(7.2))

    add_card(s17, Inches(8.3), Inches(1.6), Inches(4.3), Inches(5.2), title="Gecikme Bulguları", border_color=CYAN)
    tb_l17 = s17.shapes.add_textbox(Inches(8.5), Inches(2.3), Inches(3.9), Inches(4.3))
    tf_l17 = tb_l17.text_frame
    tf_l17.word_wrap = True

    pts_l17 = [
        "Ortalama Gecikme:\n  SAPS: 7.79 ms\n  Geleneksel: 52.63 ms\n  ➔ 6.76x Hızlanma!",
        "Düşük SNR Dayanıklılığı:\n  0 dB SNR'da geleneksel QUIC yığını yeniden iletim fırtınalarıyla >300 ms gecikmeye patlarken, SAPS 10.5 ms seviyesinde stabil kalır.",
        "Kritik Çıkarım Eşiği:\n  10 ms otonom karar eşiğini geleneksel yığın hiçbir zaman yakalayamazken, SAPS tüm SNR aralığında bu eşiğin altında kalmayı başarır.",
    ]
    for idx, pt in enumerate(pts_l17):
        p = tf_l17.paragraphs[0] if idx == 0 else tf_l17.add_paragraph()
        p.text = pt
        p.font.size = Pt(12.5)
        p.font.color.rgb = WHITE if "6.76x" in pt else LIGHT_GRAY
        p.font.bold = ("6.76x" in pt)

    set_speaker_notes(
        s17,
        """⏱️ [Hedef Süre: 20:15 - 21:15]
🎯 [Temel Mesaj]: SAPS'ın ortalama 6.76x gecikme hızlanmasını ve düşük SNR'da neden patlama yaşamadığını açıklamak.

🎙️ [Konuşma Metni]:
Grafikte uçtan uca gecikmenin mobil kanal SNR'ına göre değişimini görüyoruz.
Kırmızı çizgi geleneksel HTTP/3 ve QUIC yığınıdır; ortalama 52.6 milisaniye gecikmeye sahiptir. Özellikle 0 dB ve 5 dB gibi zorlu kanal şartlarında yeniden iletim fırtınaları nedeniyle gecikme 300 milisaniyenin üzerine fırlamaktadır.

Mavi çizgi ise geliştirdiğimiz SAPS protokol yığınıdır:
Tüm SNR koşullarında ortalama gecikme 7.79 milisaniyedir! Bu da tam 6.76 kat hızlanma anlamına gelir.
Gördüğünüz gibi otonom sürüş ve drone navigasyonu için kritik olan 10 milisaniye eşiğinin altında kalan tek protokol SAPS olmuştur."""
    )

    # =========================================================================
    # SLIDE 18: Benchmark 2 — Tail Latency & Jitter Analysis
    # =========================================================================
    s18 = prs.slides.add_slide(blank_layout)
    add_slide_header(s18, "Deney 2: Kuyruk Gecikmesi (Tail Latency) & Jitter Analizi (22x İyileşme)", "4. Deneysel Sonuçlar")

    add_card(s18, Inches(0.8), Inches(1.6), Inches(5.6), Inches(5.2), title="Gecikme Dağılımı & Yüzdelik Değerler")
    tb18_l = s18.shapes.add_textbox(Inches(1.0), Inches(2.3), Inches(5.2), Inches(4.3))
    tf18_l = tb18_l.text_frame
    tf18_l.word_wrap = True

    tail_data = [
        ("Ortalama (Mean)", "52.63 ms", "7.79 ms", "6.76x"),
        ("Medyan (50th %)", "44.10 ms", "7.20 ms", "6.12x"),
        ("95. Yüzdelik (p95)", "219.58 ms", "9.78 ms", "22.45x"),
        ("99. Yüzdelik (p99)", "298.40 ms", "10.45 ms", "28.55x"),
        ("Maksimum Gözlenen", "304.25 ms", "10.52 ms", "28.92x"),
    ]
    for idx, (m, b, s, gain) in enumerate(tail_data):
        p = tf18_l.paragraphs[0] if idx == 0 else tf18_l.add_paragraph()
        p.text = f"• {m:<18}: Baz {b:<9} | SAPS {s:<7} ➔ {gain}"
        p.font.size = Pt(12)
        p.font.color.rgb = GREEN if "22." in gain or "28." in gain else WHITE
        p.font.bold = ("p95" in m or "p99" in m)

    # Right Card: Why tail latency matters
    add_card(s18, Inches(6.8), Inches(1.6), Inches(5.7), Inches(5.2), title="Kuyruk Gecikmesinin Önemi", border_color=GOLD)
    tb18_r = s18.shapes.add_textbox(Inches(7.0), Inches(2.3), Inches(5.3), Inches(4.3))
    tf18_r = tb18_r.text_frame
    tf18_r.word_wrap = True
    tail_expl = (
        "Otonom Sistemlerde Ortalama Değil, En Kötü Durum Önemlidir:\n\n"
        "1. TCP/QUIC'in Felaketi:\n"
        "   Ortalama gecikme 50 ms görünse de, paketlerin %5'i (p95) 219 ms'yi aşmaktadır. 200 ms'lik bir gecikme, 50 km/h hızla giden bir aracın 2.8 metre boyunca kararsız ilerlemesi demektir.\n\n"
        "2. SAPS'ın Kesin Kararlılığı:\n"
        "   SAPS'ta 95. yüzdelik gecikme yalnızca 9.78 ms'dir. Maksimum gecikme dahi 10.52 ms'yi asla geçmez.\n\n"
        "✔ Head-of-line blocking elendiği için jitter neredeyse sıfırdır!"
    )
    p = tf18_r.paragraphs[0]
    p.text = tail_expl
    p.font.size = Pt(12.5)
    p.font.color.rgb = WHITE

    set_speaker_notes(
        s18,
        """⏱️ [Hedef Süre: 21:15 - 22:15]
🎯 [Temel Mesaj]: Otonom ajanlar için p95 ve p99 kuyruk gecikmelerinin hayati önemini ve SAPS'ın 22 katlık jitter iyileştirmesini vurgulamak.

🎙️ [Konuşma Metni]:
Hocam, telekomünikasyonda ve özellikle otonom sistemlerde ortalama gecikme aldatıcı olabilir. Esas önemli olan p95 ve p99 dediğimiz kuyruk gecikmeleridir (Tail Latency).
Tabloya baktığımızda çarpıcı bir gerçekle karşılaşıyoruz:
Geleneksel yığında ortalama gecikme 52 ms iken, 95. yüzdelik gecikme 219 ms'ye, 99. yüzdelik ise 298 ms'ye fırlamaktadır!
Bunun sebebi mobil sönümleme anında TCP'nin art arda yaşadığı yeniden iletim tıkanmalarıdır. Saatte 50 km hızla giden bir robot için 300 ms'lik körlük kaza sebebidir.

SAPS'a baktığımızda ise p95 gecikmesi 9.78 ms, en kötü durum maksimum gecikmesi ise 10.52 ms'dir!
Geleneksel yığına göre kuyruk gecikmesinde tam 22 katlık bir iyileşme elde ettik. Ajanlarımız her zaman öngörülebilir ve son derece kararlı bir yanıt süresine sahiptir."""
    )

    # =========================================================================
    # SLIDE 19: Benchmark 3 — BLEU vs Loss Rate
    # =========================================================================
    s19 = prs.slides.add_slide(blank_layout)
    add_slide_header(s19, "Deney 3: Kademeli Bozulma vs Dijital Uçurum Etkisi (BLEU Skoru)", "4. Deneysel Sonuçlar")

    img_bleu = _RESULTS / "bleu_vs_loss_rate.png"
    if img_bleu.exists():
        s19.shapes.add_picture(str(img_bleu), Inches(0.8), Inches(1.6), width=Inches(7.2))

    add_card(s19, Inches(8.3), Inches(1.6), Inches(4.3), Inches(5.2), title="Semantik Doğruluk Analizi", border_color=GREEN)
    tb_b19 = s19.shapes.add_textbox(Inches(8.5), Inches(2.3), Inches(3.9), Inches(4.3))
    tf_b19 = tb_b19.text_frame
    tf_b19.word_wrap = True

    pts_b19 = [
        "Dijital Uçurum Etkisi (Cliff Effect):\n  Geleneksel 16-QAM modülasyonu paket kayıp oranı %20'yi aştığında aniden çöker ve BLEU skoru 0.00'a düşer.",
        "Kademeli Nöral Bozulma (Graceful Degradation):\n  Deep-JSCC nöral alıcı-verici gizil uzay sürekliliğini korur.",
        "Aşırı Kayıpta Dahi Anlam Korunumu:\n  Kanalda %50 paket kaybı yaşandığında dahi SAPS >0.75 BLEU skorunu korur; ajan görevini başarıyla sürdürür.",
    ]
    for idx, pt in enumerate(pts_b19):
        p = tf_b19.paragraphs[0] if idx == 0 else tf_b19.add_paragraph()
        p.text = pt
        p.font.size = Pt(12.5)
        p.font.color.rgb = WHITE if "Graceful" in pt or ">0.75" in pt else LIGHT_GRAY
        p.font.bold = (">0.75" in pt)

    set_speaker_notes(
        s19,
        """⏱️ [Hedef Süre: 22:15 - 23:15]
🎯 [Temel Mesaj]: Fiziksel katmandaki dijital uçurum etkisinin Deep-JSCC ile nasıl aşıldığını BLEU grafiği üzerinden göstermek.

🎙️ [Konuşma Metni]:
Bu grafikte anlamsal doğruluk metriği olan BLEU skorunun paket kayıp oranına göre değişimini inceliyoruz.
Kırmızı eğri klasik QAM tabanlı geleneksel yığındır. Paket kaybı %20'nin üzerine çıktığı an dijital uçurum etkisi (cliff effect) gerçekleşir ve BLEU skoru sıfıra çakılır; yani iletişim tamamen kopar.

Yeşil eğri ise SAPS'ın Deep-JSCC katmanıdır.
Gördüğünüz gibi son derece yumuşak ve kademeli bir bozulma (graceful degradation) sergilemektedir.
Kanalda %50 gibi yıkıcı bir paket kaybı olsa dahi, SAPS 0.75'in üzerinde BLEU doğruluğunu muhafaza eder.
Bu sayede alıcı taraftaki otonom ajan, eksik parçalara rağmen görevi sürdürmeye yetecek anlamı kavramış olur."""
    )

    # =========================================================================
    # SLIDE 20: Benchmark 4 — Bandwidth Savings & Token Entropy
    # =========================================================================
    s20 = prs.slides.add_slide(blank_layout)
    add_slide_header(s20, "Deney 4: Bant Genişliği Tasarrufu (%95.3) & Entropi Dağılımı", "4. Deneysel Sonuçlar")

    img_bw = _RESULTS / "bandwidth_savings.png"
    img_ent = _RESULTS / "token_entropy_distribution.png"

    if img_bw.exists():
        s20.shapes.add_picture(str(img_bw), Inches(0.8), Inches(1.6), width=Inches(5.7))
    if img_ent.exists():
        s20.shapes.add_picture(str(img_ent), Inches(6.8), Inches(1.6), width=Inches(5.7))

    # Bottom summary card
    add_card(s20, Inches(0.8), Inches(5.6), Inches(11.7), Inches(1.4), border_color=GOLD)
    tb_b20 = s20.shapes.add_textbox(Inches(1.0), Inches(5.75), Inches(11.3), Inches(1.1))
    tf_b20 = tb_b20.text_frame
    p20 = tf_b20.paragraphs[0]
    p20.text = "Temel Bulgular: SAPS doğrudan kuantize tensör akışı ve entropi duyarlı filtreleme (Eşik = 1.0 nats) sayesinde taşınan bayt hacmini %95.3 oranında, telsiz verici enerji tüketimini ise %92.1 oranında azaltmıştır!"
    p20.font.size = Pt(13.5)
    p20.font.bold = True
    p20.font.color.rgb = WHITE

    set_speaker_notes(
        s20,
        """⏱️ [Hedef Süre: 23:15 - 24:15]
🎯 [Temel Mesaj]: %95.3 bayt hacmi azalmasını, %92 enerji tasarrufunu ve entropi dağılımını açıklamak.

🎙️ [Konuşma Metni]:
Bu slaytta iki kritik sonucu yan yana görüyoruz:
Sol tarafta bant genişliği ve enerji tasarrufu yer alıyor. Geleneksel HTTP/JSON akışı aynı tensör aktarımı için 68.400 bayt tüketirken, SAPS yalnızca 3.276 bayt ile aynı çıkarımı gerçekleştirmiştir.
Bu tam %95.3'lük bir bant genişliği azalmasıdır! Radyo iletim süresi kısaldığı için mobil ajanın batarya enerji tüketimi de %92.1 oranında düşmektedir.

Sağ taraftaki grafikte ise dil modelinin ürettiği tokenların Shannon entropi dağılımını görüyoruz.
Dağılım açıkça iki tepeye (bimodal) ayrılmıştır:
Sol tepedeki düşük entropili tokenlar dilbilgisel dolgulardır; kaybolsalar da yeniden iletilmezler.
Sağ tepedeki yüksek entropili tokenlar ise hayati komutlar ve koordinatlardır.
IA-STP protokolümüzün 1.0 nats eşiğiyle bu iki grubu mükemmel şekilde ayrıştırdığını deneysel olarak kanıtlamış olduk."""
    )

    # =========================================================================
    # SLIDE 21: Benchmark 5 — NVIDIA Sionna 3GPP TR 38.901 Results
    # =========================================================================
    s21 = prs.slides.add_slide(blank_layout)
    add_slide_header(s21, "Deney 5: NVIDIA Sionna 3GPP TR 38.901 Kentsel Mikro Kanal Sonuçları", "4. Deneysel Sonuçlar")

    img_sionna = _RESULTS / "sionna_3gpp_benchmark.png"
    if img_sionna.exists():
        s21.shapes.add_picture(str(img_sionna), Inches(0.8), Inches(1.6), width=Inches(7.2))

    add_card(s21, Inches(8.3), Inches(1.6), Inches(4.3), Inches(5.2), title="3GPP Doğrulama Çıktıları", border_color=CYAN)
    tb_s21 = s21.shapes.add_textbox(Inches(8.5), Inches(2.3), Inches(3.9), Inches(4.3))
    tf_s21 = tb_s21.text_frame
    tf_s21.word_wrap = True

    pts_s21 = [
        "Sionna 3GPP UMi Kanalında:\n  SAPS Gecikmesi: 7.82 ms\n  Baz Gecikme: 52.06 ms\n  ➔ 6.66x Hızlanma Doğrulandı!",
        "3.5 GHz 5G NR Uyumu:\n  Çok yollu gecikme yayılımı (multipath delay spread) altında dahi Deep-JSCC kararlılığını korumuştur.",
        "Bant Genişliği Tasarrufu:\n  Geleneksel: 71.6 KB\n  SAPS: 3.3 KB\n  ➔ %95.4 Tasarruf!",
        "Endüstriyel Geçerlilik:\n  Sonuçlar sentetik oyuncak modellerde değil, 3GPP onaylı Sionna motorunda teyit edilmiştir.",
    ]
    for idx, pt in enumerate(pts_s21):
        p = tf_s21.paragraphs[0] if idx == 0 else tf_s21.add_paragraph()
        p.text = pt
        p.font.size = Pt(12)
        p.font.color.rgb = WHITE if "6.66x" in pt or "%95.4" in pt else LIGHT_GRAY
        p.font.bold = ("6.66x" in pt or "%95.4" in pt)

    set_speaker_notes(
        s21,
        """⏱️ [Hedef Süre: 24:15 - 25:15]
🎯 [Temel Mesaj]: NVIDIA Sionna 3GPP sonuçlarını sunarak projenin endüstriyel standarttaki başarısını ve ek puan hedefini mühürlemek.

🎙️ [Konuşma Metni]:
Sayın Hocam, bu deney çalışmamızın en iddialı doğrulama adımıdır:
Tüm mimariyi NVIDIA'nın 3GPP TR 38.901 standart kütüphanesi olan Sionna 2.2 üzerinde koşturduk.
3.5 GHz taşıyıcı frekansında, kentsel mikro hücre (UMi) ve 50 Hz Doppler hızında aldığımız sonuçlar sol taraftaki 3 panelli grafikte yer almaktadır:
1. Panelde gecikmenin yine 7.82 ms ile 6.66 kat hızlandığını görüyoruz.
2. Panelde 16-QAM modülasyonunun Sionna kanalında 10 dB SNR altında sıfıra çöktüğünü, Deep-JSCC'nin ise kusursuz devam ettiğini görüyoruz.
3. Panelde ise %95.4 bant genişliği tasarrufunun 3GPP ortamında da aynen korunduğunu kanıtlamış olduk.
Bu sayede SAPS'ın başarısının yapay simülasyon varsayımlarına bağlı olmadığını, 5G/6G standartlarında da birebir geçerli olduğunu ispatladık."""
    )

    # =========================================================================
    # SLIDE 22: Executive 4-Panel Evaluation Dashboard
    # =========================================================================
    s22 = prs.slides.add_slide(blank_layout)
    add_slide_header(s22, "Yönetici Değerlendirme Paneli: 4 Boyutlu Genel Karşılaştırma", "4. Deneysel Sonuçlar")

    img_dash = _RESULTS / "presentation_dashboard.png"
    if img_dash.exists():
        s22.shapes.add_picture(str(img_dash), Inches(1.8), Inches(1.5), height=Inches(5.5))

    set_speaker_notes(
        s22,
        """⏱️ [Hedef Süre: 25:15 - 26:00]
🎯 [Temel Mesaj]: Tüm metrikleri tek bir yönetici gösterge panelinde toplayarak genel tabloyu özetlemek.

🎙️ [Konuşma Metni]:
Bu slaytta projemizin tüm temel kazanımlarını 4 panellik bir yönetici özetinde görüyoruz:
Sol üstte Gecikme (6.76x hızlanma),
Sağ üstte Semantik Kalite (Kademeli bozulma ile kesintisiz iletişim),
Sol altta Bant Genişliği (%95.3 tasarruf),
Sağ altta ise Enerji Tüketimi (%92.1 düşüş).

Bu 4 grafik birlikte gösteriyor ki SAPS, tek bir metriği iyileştirirken diğerlerinden ödün veren bir protokol değildir; tüm metriklerde geleneksel internet yığınını geride bırakmaktadır."""
    )

    # =========================================================================
    # SLIDE 23: Interactive Simulation Dashboard (Web GUI)
    # =========================================================================
    s23 = prs.slides.add_slide(blank_layout)
    add_slide_header(s23, "Canlı İnteraktif Simülatör Web Paneli (scripts/run_simulation_ui.py)", "5. Canlı Simülasyon")

    # Left Card: Web UI Features
    add_card(s23, Inches(0.8), Inches(1.6), Inches(5.6), Inches(5.2), title="İnteraktif Web Kontrol Paneli Özellikleri")
    tb23 = s23.shapes.add_textbox(Inches(1.0), Inches(2.3), Inches(5.2), Inches(4.3))
    tf23 = tb23.text_frame
    tf23.word_wrap = True

    pts23 = [
        "Sıfır Bağımlılıklı Web Mimarisi: Doğrudan Python http.server ve modern HTML5/Canvas ile geliştirilmiştir.",
        "Canlı Parametre Değişimi: Sunum esnasında SNR kaydırıcısı (0-30 dB) ve Entropi Eşiği (0.1-3.0 nats) anlık değiştirilebilir.",
        "Kanal Modeli Seçimi: NVIDIA Sionna 3GPP (UMi), Rayleigh Fading, Rician Fading ve AWGN kanalları arasında anında geçiş.",
        "6 Katmanlı Animasyonlu Traversal: Paketin AIRL'den Deep-JSCC'ye inişi canlı LED'ler ve durum diyagramlarıyla görselleştirilir.",
        "Canlı Takımyıldızı (Constellation) Çizimi: Deep-JSCC'nin ürettiği IQ sembolleri HTML5 Canvas üzerinde gerçek zamanlı çizilir.",
    ]
    for idx, pt in enumerate(pts23):
        p = tf23.paragraphs[0] if idx == 0 else tf23.add_paragraph()
        p.text = f"✔ {pt}"
        p.font.size = Pt(12.5)
        p.font.color.rgb = WHITE if idx == 1 else LIGHT_GRAY
        p.font.bold = (idx == 1)

    # Right Card: How to launch
    add_card(s23, Inches(6.8), Inches(1.6), Inches(5.7), Inches(5.2), title="Canlı Demo Başlatma Komutu", border_color=CYAN)
    tb23_r = s23.shapes.add_textbox(Inches(7.0), Inches(2.3), Inches(5.3), Inches(4.3))
    tf23_r = tb23_r.text_frame
    tf23_r.word_wrap = True

    launch_text = (
        "Nasıl Çalıştırılır? (Terminal):\n\n"
        "  cd saps\n"
        "  py scripts/run_simulation_ui.py --port 8050\n\n"
        "Tarayıcı Otomatik Açılır:\n"
        "  http://localhost:8050\n\n"
        "Sunum Esnasında Canlı Gösterim Senaryosu:\n"
        "1. SNR kaydırıcısını 0 dB'ye çekin: SAPS'ın 8 ms gecikmeyle çalıştığını, geleneksel yığının ise çöktüğünü gösterin.\n"
        "2. Kanalı 'NVIDIA Sionna 3GPP (UMi)' seçin: 3GPP kanal matrisinin çalıştığını gösterin.\n"
        "3. Entropi eşiğini 2.0 yapın: Yalnızca kritik tokenların iletildiğini log ekranında gösterin."
    )
    p = tf23_r.paragraphs[0]
    p.text = launch_text
    p.font.size = Pt(12.5)
    p.font.color.rgb = WHITE

    set_speaker_notes(
        s23,
        """⏱️ [Hedef Süre: 26:00 - 27:00]
🎯 [Temel Mesaj]: Kullanıcının geliştirdiği web arayüzünü tanıtmak ve hocaya canlı test imkanı sunmak.

🎙️ [Konuşma Metni]:
Değerli Hocam, bu çalışmayı yalnızca statik grafiklerle bırakmadık; sunum anında dilediğiniz parametreyi test edebileceğiniz interaktif bir Web Simülatör Gösterge Paneli de geliştirdik.
'py scripts/run_simulation_ui.py' komutuyla çalışan bu arayüzde:
SNR kaydırıcısını hareket ettirerek anlık kanal bozulmalarını simüle edebiliyor,
Kanal modelini NVIDIA Sionna 3GPP olarak seçebiliyor,
Ve sağ taraftaki HTML5 Canvas üzerinde Deep-JSCC'nin karmaşık IQ takımyıldızını gerçek zamanlı izleyebiliyoruz.
Dilerseniz sunum sonundaki soru-cevap kısmında istediğiniz bir parametreyi burada canlı olarak simüle edebiliriz."""
    )

    # =========================================================================
    # SLIDE 24: Live Demonstration & Video Walkthrough
    # =========================================================================
    s24 = prs.slides.add_slide(blank_layout)
    add_slide_header(s24, "Canlı Simülasyon Gösterimi: 6 Katmanlı Uçtan Uca İletim", "5. Gösterim & Video")

    mp4_path = _RESULTS / "saps_demo_video.mp4"
    poster_path = _RESULTS / "saps_demo_poster.png"

    if mp4_path.exists() and poster_path.exists():
        try:
            s24.shapes.add_movie(
                str(mp4_path),
                Inches(0.8), Inches(1.6), Inches(7.5), Inches(4.2),
                poster_frame_image=str(poster_path),
                mime_type="video/mp4"
            )
        except Exception:
            s24.shapes.add_picture(str(poster_path), Inches(0.8), Inches(1.6), width=Inches(7.5))
    elif poster_path.exists():
        s24.shapes.add_picture(str(poster_path), Inches(0.8), Inches(1.6), width=Inches(7.5))

    add_card(s24, Inches(8.6), Inches(1.6), Inches(4.0), Inches(5.2), title="Terminal Demosu", border_color=CYAN)
    tb24 = s24.shapes.add_textbox(Inches(8.8), Inches(2.3), Inches(3.6), Inches(4.3))
    tf24 = tb24.text_frame
    tf24.word_wrap = True

    demo_pts = [
        "Senaryo:\nMobil İHA ajanı %88 işlemci yükü altındayken kritik bir engel koordinatı tespit eder.",
        "Katman İlerlemesi:\nAIRL görevi edge_vision_01'e devreder ➔ App katmanı KV tensörünü kuantize eder ➔ IA-STP entropi kararı verir ➔ SP-MAC öncelik tanır ➔ Deep-JSCC Sionna kanalından iletir.",
        "Terminalden Çalıştırma:\n  cd saps\n  py scripts/demo_presentation.py",
    ]
    for idx, pt in enumerate(demo_pts):
        p = tf24.paragraphs[0] if idx == 0 else tf24.add_paragraph()
        p.text = pt
        p.font.size = Pt(12)
        p.font.color.rgb = WHITE if idx == 2 else LIGHT_GRAY
        p.font.bold = (idx == 2)

    set_speaker_notes(
        s24,
        """⏱️ [Hedef Süre: 27:00 - 28:00]
🎯 [Temel Mesaj]: Simülasyon videosunu ve terminal gösterimini anlatarak sistemin eksiksiz çalıştığını göstermek.

🎙️ [Konuşma Metni]:
Slaytımızda gömülü olarak yer alan demo videosunda, geliştirdiğimiz 6 katmanlı iletimin gerçek bir görev senaryosundaki traversal akışını görüyoruz.
Senaryomuzda mobil bir İHA ajanı, yüksek işlemci yükü altındayken aniden bir engel algılıyor.
Sırasıyla:
1. AIRL Katmanı 1.2 milisaniyede en uygun uç sunucuyla sözleşme imzalıyor.
2. Uygulama Katmanı dikkat tensörünü 8-bite kuantize ediyor.
3. IA-STP yüksek entropili koordinatları koruma altına alıyor.
4. SP-MAC bu pakete en yüksek önceliği vererek kanala sürüyor.
5. Deep-JSCC sembolleri sönümlemeli telsiz kanalından iletiyor ve alıcı ajan görevi 7.8 milisaniyede başarıyla tamamlıyor.
İstendiğinde 'py scripts/demo_presentation.py' komutuyla terminal üzerinden de canlı akışı izleyebiliyoruz."""
    )

    # =========================================================================
    # SLIDE 25: Head-to-Head Comparison Table
    # =========================================================================
    s25 = prs.slides.add_slide(blank_layout)
    add_slide_header(s25, "Kapsamlı Karşılaştırma: Geleneksel HTTP/3 + QUIC vs SAPS", "6. Karşılaştırmalı Özet")

    add_card(s25, Inches(0.8), Inches(1.5), Inches(11.7), Inches(5.3))
    tb25 = s25.shapes.add_textbox(Inches(1.0), Inches(1.7), Inches(11.3), Inches(4.9))
    tf25 = tb25.text_frame

    table_rows = [
        ("Özellik / Metrik", "Geleneksel (HTTP/3 + QUIC + QAM)", "SAPS (Geliştirdiğimiz Protokol)", "Kazanım / Üstünlük"),
        ("Ortalama Gecikme", "52.63 ms", "7.79 ms", "6.76x Daha Hızlı"),
        ("95. Yüzdelik Kuyruk Gecikmesi", "219.58 ms", "9.78 ms", "22x Jitter Azalması"),
        ("Maksimum Gözlenen Gecikme", "304.25 ms", "10.52 ms", "Yeniden İletim Fırtınası Yok"),
        ("Toplam İletilen Bayt", "68.400 bayt", "3.276 bayt", "%95.3 Bant Genişliği Tasarrufu"),
        ("Telsiz Enerji Tüketimi", "Baz Değer (%100)", "%7.9 (Tasarruf: %92.1)", "12 Kat Daha Uzun Batarya Ömrü"),
        ("Kanal Sönümleme Dayanıklılığı", "Uçurum Çöküşü (0 BLEU)", "Kademeli Bozulma (>0.75 BLEU)", "%50 Kayıpta Kesintisiz Anlam"),
        ("NVIDIA Sionna 3GPP Testi", "Uyumsuz / Desteklenmiyor", "3GPP TR 38.901 UMi Doğrulandı", "Endüstri Standardı 5G/6G Uyumu"),
    ]

    for idx, (m, b, s, g) in enumerate(table_rows):
        p = tf25.paragraphs[0] if idx == 0 else tf25.add_paragraph()
        p.text = f"{m:<30} | {b:<28} | {s:<28} | {g}"
        p.font.size = Pt(12)
        p.font.color.rgb = CYAN if idx == 0 else (GREEN if "Hızlı" in g or "Tasarrufu" in g or "Uyumu" in g or "Azalması" in g else WHITE)
        p.font.bold = (idx == 0 or idx == 1 or idx == 4)

    set_speaker_notes(
        s25,
        """⏱️ [Hedef Süre: 28:00 - 29:00]
🎯 [Temel Mesaj]: SAPS'ın geleneksel yığına karşı tüm sayısal üstünlüklerini tablo üzerinden tek bakışta özetlemek.

🎙️ [Konuşma Metni]:
Bu karşılaştırma tablosu, projemizin ulaştığı tüm sayısal başarıların nihai özetidir:
- Ortalama gecikmede 52 ms'den 7.7 ms'ye inerek 6.76 kat hızlanma sağladık.
- Kuyruk gecikmesinde 219 ms'den 9.7 ms'ye inerek 22 katlık bir kararlılık artışı elde ettik.
- İletilen bayt hacmini 68 KB'dan 3.2 KB'a düşürerek %95.3 bant genişliği ve %92.1 enerji tasarrufu sağladık.
- Fiziksel katmandaki uçurum etkisini sıfırlayarak %50 paket kaybında dahi 0.75 BLEU doğruluğunu koruduk.
- Ve tüm bu kazanımları NVIDIA Sionna 3GPP kentsel kanal modelleriyle doğruladık.
Bu metrikler, SAPS'ın otonom yapay zeka ajanları için devrim niteliğinde bir protokol olduğunu açıkça ortaya koymaktadır."""
    )

    # =========================================================================
    # SLIDE 26: Conclusion & Questions
    # =========================================================================
    s26 = prs.slides.add_slide(blank_layout)
    apply_background(s26)

    # Conclusion Card
    add_card(s26, Inches(1.0), Inches(1.0), Inches(11.3), Inches(3.2), title="Sonuç & Temel Akademik Katkılar", border_color=CYAN)
    tb_c = s26.shapes.add_textbox(Inches(1.3), Inches(1.5), Inches(10.7), Inches(2.5))
    tf_c = tb_c.text_frame
    tf_c.word_wrap = True

    c_pts = [
        "1. Yapay Zekaya Özgü İnternet Mimarisi: Ağ protokollerinin bit-seviyesinde kör veri taşımak yerine, anlamsal entropi ve muhakeme yoğunluğuna göre tasarlanması gerektiğini kanıtladık.",
        "2. 6 Katmanlı Eksiksiz Entegrasyon: AIRL, KV-Cache Streaming, IA-STP, V-CCR, SP-MAC ve Deep-JSCC katmanlarını çalışan birleşik bir testbed'de bir araya getirdik.",
        "3. İleri Seviye Doğrulama & Açık Kaynak: NVIDIA Sionna 3GPP desteği, canlı interaktif web simülatörü ve 30/30 geçen test paketi ile eksiksiz bir dönem projesi teslimi sağladık.",
    ]
    for idx, pt in enumerate(c_pts):
        p = tf_c.paragraphs[0] if idx == 0 else tf_c.add_paragraph()
        p.text = pt
        p.font.size = Pt(13)
        p.font.color.rgb = WHITE

    # Q&A Card
    add_card(s26, Inches(1.0), Inches(4.5), Inches(11.3), Inches(2.4), border_color=GREEN)
    tb_q = s26.shapes.add_textbox(Inches(1.3), Inches(4.7), Inches(10.7), Inches(2.0))
    tf_q = tb_q.text_frame

    qp1 = tf_q.paragraphs[0]
    qp1.text = "Teşekkür Ederim! Sorularınız ve Değerlendirmeleriniz"
    qp1.font.size = Pt(23)
    qp1.font.bold = True
    qp1.font.color.rgb = GREEN

    qp2 = tf_q.add_paragraph()
    qp2.text = "Proje Kodu, Simülasyon Logları ve Sionna 3GPP Benchmark Verileri GitHub Deposunda Mevcuttur."
    qp2.font.size = Pt(13)
    qp2.font.color.rgb = LIGHT_GRAY

    qp3 = tf_q.add_paragraph()
    qp3.text = "Prof. Dr. Hasari Çelebi ve değerli meslektaşlarımızın sorularını yanıtlamaktan memnuniyet duyarım."
    qp3.font.size = Pt(13)
    qp3.font.color.rgb = CYAN

    set_speaker_notes(
        s26,
        """⏱️ [Hedef Süre: 29:00 - 30:00+]
🎯 [Temel Mesaj]: Sunumu saygıyla noktalamak ve hocanın gelebilecek teknik sorularına hazır olduğunu göstermek.

🎙️ [Konuşma Metni]:
Özetlemek gerekirse; SAPS ile klasik internet protokollerinin yapay zeka ajanlarındaki yetersizliğini kanıtladık ve 6 katmanın tamamını anlamsal prensiplerle yeniden tasarlayarak çalışan bir prototipe dönüştürdük. 

Dinlediğiniz için çok teşekkür ederim.
Sayın Prof. Dr. Hasari Çelebi Hocam ve değerli arkadaşlarım, sorularınızı ve değerli katkılarınızı almaktan onur duyarım.

💡 [Olası Hoca Soruları ve Cevap İpuçları]:
Soru 1: 'Peki Deep-JSCC kanal SNR'ı aniden değişirse nasıl adapte oluyor?'
Cevap: 'Hocam, Deep-JSCC nöral encoder'ımız SNR geri beslemesini giriş vektörüne ekleyerek güç normalizasyonunu dinamik ölçekler. Ayrıca Sionna kanalında SNR aralığı geniş bir veri kümesiyle eğitilmiştir.'

Soru 2: 'IA-STP'de atlanan düşük entropili tokenlar alıcıda nasıl telafi ediliyor?'
Cevap: 'Alıcı ajan tarafındaki dil modeli (LLM) veya karar mekanizması, gelen bağlam tensörlerini kullanarak eksik dolgu kelimelerini masked language modeling mantığıyla tamamlar. Bu sayede sıfır hata etkisi oluşur.'

Soru 3: 'NVIDIA Sionna'yı entegre etmek ne kazandırdı?'
Cevap: 'Hocam, sentetik sönümleme modelleri kentsel ortamlardaki gerçek gecikme yayılımlarını ve açısal dağılımları yansıtamaz. Sionna 3GPP TR 38.901 kütüphanesi sayesinde sonuçlarımızı 5G/6G endüstriyel test standartlarında kanıtlamış olduk.'"""
    )

    out_pptx = _DOCS / "SAPS_Presentation.pptx"
    prs.save(str(out_pptx))
    print(f"Presentation saved successfully to: {out_pptx}")
    print(f"Total slides built: {len(prs.slides)}")
    return out_pptx


if __name__ == "__main__":
    build_deck()
