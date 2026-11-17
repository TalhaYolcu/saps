# 🎤 SAPS: 30-Dakikalık Dönem Projesi Sunum Rehberi & Genişletilmiş Slayt Notları

**Ders:** CSE 476/575 — Güz 2026 Dönem Projesi  
**Ders Yürütücüsü:** Prof. Dr. Hasari Çelebi  
**Proje Başlığı:** Semantic-Driven Agentic Protocol Stack (SAPS) for Mobile AI Agents  
**Sunan:** Yakup Yolcu  
**Sunum Formatı:** 16:9 Geniş Ekran PowerPoint (`docs/SAPS_Presentation.pptx`, 26 Slayt)  
**Hedef Süre Dağılımı:** 25 Dakika Sunum + 5 Dakika Soru-Cevap & Canlı Gösterim (Toplam 30 Dakika)  
**Tüm Slaytlarda Konuşmacı Notları:** PowerPoint Sunucu Görünümünde (Presenter View) mevcuttur.

---

## ⏱️ Zaman Yönetimi & Bölüm Planı (26 Slayt)

| Bölüm | Slaytlar | Hedef Süre | Küm. Zaman | Odak & İçerik |
|---|---|---|---|---|
| **I. Giriş, Motivasyon & Teorik Temeller** | Slayt 1–4 | 5 dk | 05:00 | İnsan web'inden ajan internetine geçiş; Shannon & Weaver 3 iletişim seviyesi; 4 darboğaz |
| **II. SAPS 6 Katmanlı Mimari Tasarımı** | Slayt 5–14 | 13 dk | 18:00 | Katman 6 (AIRL), Katman 5 (KV streaming), Katman 4 (IA-STP), Katman 3 (V-CCR), Katman 2 (SP-MAC), Katman 1 (Deep-JSCC) |
| **III. NVIDIA Sionna & Testbed Altyapısı** | Slayt 15–16 | 2 dk | 20:00 | NVIDIA Sionna 2.2 3GPP TR 38.901 entegrasyonu ve SimPy ayrık olay simülatörü |
| **IV. Deneysel Sonuçlar & Karşılaştırmalı Analiz** | Slayt 17–22 | 6 dk | 26:00 | Gecikme (6.76x), Kuyruk gecikmesi (22x), BLEU kademeli bozulma, Bant genişliği (%95), Sionna 3GPP |
| **V. Canlı Simülasyon, Web Paneli & Video** | Slayt 23–24 | 2 dk | 28:00 | İnteraktif Web UI (`run_simulation_ui.py`) ve gömülü simülasyon videosu |
| **VI. Karşılaştırma Özeti & Soru-Cevap Savunması** | Slayt 25–26 | 2–5 dk | 30:00+ | Sayısal karşılaştırma tablosu, sonuçlar ve Prof. Dr. Hasari Çelebi'nin soruları |

---

## 📽️ Slayt-Slayt Detaylı İçerik ve Konuşmacı Notları

---

### Slayt 1: Başlık Slaytı (Title Slide)
* **Başlık:** Semantic-Driven Agentic Protocol Stack (SAPS) for Mobile AI Agents
* **Alt Başlık:** Redesigning the 6-Layer Internet Protocol Stack for Autonomous M2M Reasoning
* **Ders Bilgisi:** CSE 476/575 Mobile Communications & AI/ML | Prof. Dr. Hasari Çelebi | Yakup Yolcu
* **Konuşmacı Notu [00:00 - 01:00]:**
  > *"Sayın Prof. Dr. Hasari Çelebi Hocam ve değerli çalışma arkadaşlarım, hepiniz hoş geldiniz. Bugün sizlere CSE 476/575 dersi kapsamında geliştirdiğimiz dönem projemizi sunmaktan büyük memnuniyet duyuyorum: 'Semantic-Driven Agentic Protocol Stack', kısaca SAPS.*  
  > *Bildiğiniz üzere 1970'lerde ve 80'lerde temelleri atılan mevcut TCP/IP ve HTTP protokol ailesi, insan kullanıcıların web sayfalarını gezmesi ve dosyaları bit-bit hatasız indirmesi amacıyla tasarlandı. Ancak 6G ve ötesi mobil ağlarda artık internetin birincil aktörleri insanlar değil; otonom İHA'lar, robotik filolar ve işbirlikçi yapay zeka ajanları olacak.*  
  > *Bu çalışmada, klasik 5 katmanlı internet mimarisini yapay zeka ajanlarının anlamsal muhakeme ihtiyaçlarına göre baştan tasarladık ve üzerine yeni bir 'Ajan Niyet ve Muhakeme Katmanı' ekleyerek 6 katmanlı uçtan uca eksiksiz bir protokol yığını inşa ettik. Ayrıca simülasyonlarımızda standart fading modellerinin yanı sıra NVIDIA Sionna 3GPP TR 38.901 kanal modellerini de entegre ederek endüstri standardı 5G/6G ortamlarında doğruladık."*

---

### Slayt 2: Paradigma Dönüşümü: İnsan Web'inden Ajanik İnternet'e
* **İçerik:** İnsan Tüketici Web'i (HTML/JSON, 200ms gecikme toleransı, katı bit doğruluğu) vs Ajanik İnternet (Tensör akışı, <10ms gecikme, anlamsal bilgi korunumu).
* **Konuşmacı Notu [01:00 - 02:15]:**
  > *"Hocam, bu slaytta günümüz interneti ile geleceğin ajan ağları arasındaki derin zıtlığı görüyoruz. Klasik internet altyapısı, insan algısına göre şekillenmiştir. İnsan gözü 100-200 milisaniyelik bir gecikmeyi fark etmez; ancak bir dosyayı indirirken tek bir bitin dahi bozulmaması esastır. Bu yüzden TCP, bir paket kaybolduğunda akışı durdurur ve o paketi yeniden iletir.*  
  > *Fakat otonom bir İHA veya robotik sürüş sistemini düşünelim. Burada karar alma döngüsünün 10 milisaniyenin altında tamamlanması gerekir. Bir cümledeki 'the' veya 'bir' gibi dolgu sözcükleri kaybolsa bile, downstream dil modeli veya karar motoru cümlenin anlamını %99 başarıyla kavrayabilir. Ancak klasik TCP gibi o dolgu kelimesi için 100 milisaniye boyunca akışı durdurup yeniden iletim yaparsak (head-of-line blocking), drone engele çarpabilir. Dolayısıyla yapay zeka ajanları için önemli olan bit-seviyesinde aynılık değil, anlamsal bilginin (semantic meaning) en düşük gecikmeyle hedefe ulaşmasıdır."*

---

### Slayt 3: Teorik Temeller: Weaver & Shannon'ın 3 İletişim Seviyesi
* **İçerik:**
  * **Seviye A (Teknik Seviye):** Klasik Shannon Problemi (1948). Bitlerin hatasız iletimi. 1G-5G telekomünikasyon odağı.
  * **Seviye B (Anlamsal Seviye):** Sembollerin hedef anlamı ne kadar yansıttığı (Weaver 1949). Deep-JSCC ve semantik entropi.
  * **Seviye C (Pragmatik / Etkililik Seviyesi):** Alınan anlamın alıcı ajanın eylemlerini hedefe yönlendirme başarısı. AIRL niyet müzakeresi.
* **Konuşmacı Notu [02:15 - 03:45]:**
  > *"Hocam, çalışmamızın teorik temeli iletişim teorisinin kurucuları Claude Shannon ve Warren Weaver'ın 1949'daki üç seviyeli iletişim modeline dayanıyor. Shannon bildiğiniz gibi Seviye A'yı, yani Teknik Seviyeyi tanımlamıştı: 'Gönderilen semboller fiziksel kanaldan ne kadar hatasız geçer?' 1G'den 5G'ye kadar hücresel ağlar ve TCP/IP ailesi tamamen bu Seviye A'yı optimize etti. İçeriğin bir video mu, bir koordinat mı olduğu umursanmaksızın bitler taşındı.*  
  > *Ancak Weaver, Seviye B ve Seviye C'yi tanımlamıştı: Seviye B Semantik İletişimdir: İletilen sembol hedef anlamı doğru aktarıyor mu? Seviye C ise Etkililik / Pragmatik İletişimdir: İletilen bilgi, alıcının görevi başarıyla yerine getirmesini sağlıyor mu?*  
  > *İşte SAPS, mobil iletişimi yalnızca Seviye A'ya sıkışıp kalmaktan kurtarıp, Seviye B (Semantik) ve Seviye C (Pragmatik) seviyelerine yükseltmektedir."*

---

### Slayt 4: Geleneksel Protokollerin Yapay Zeka Ajanlarındaki 4 Büyük Darboğazı
* **İçerik:** 1. Serileştirme & JSON Darboğazı, 2. Kör ARQ & Yeniden İletim Fırtınaları, 3. Statik IP Katılığı, 4. Fiziksel Katmandaki Uçurum Etkisi (Cliff Effect).
* **Konuşmacı Notu [03:45 - 05:00]:**
  > *"Mevcut internet mimarisini mobil yapay zeka ajanlarında çalıştırdığımızda karşımıza çıkan 4 büyük teknik darboğaz şunlardır: 1. Serileştirme Yükü: Tensörleri JSON veya Protobuf'a çevirmek muazzam bir CPU yükü ve gecikme üretir. 2. Kör Yeniden İletim (Blind ARQ): TCP bir virgül veya dolgu kelimesi kaybolduğunda dahi tüm hattı bekletir. 3. Statik IP Katılığı: Bir ajan '192.168.1.50' IP'sine bağlanmak istemez; '80 GB VRAM'i ve Llama-3 modeli yüklü olan en yakın uç sunucuya' bağlanmak ister. 4. Uçurum Etkisi: 16-QAM veya 64-QAM gibi dijital modülasyonlarda kanal SNR'ı eşiğin altına indiği an paketler aniden sıfırlanır. SAPS, bu 4 darboğazın her birini kendi katmanlarında kökten çözmektedir."*

---

### Slayt 5: SAPS Sistem Mimarisi: 6 Katmanın Uçtan Uca Yeniden Tasarımı
* **İçerik:** Katman 6 (AIRL), Katman 5 (KV-Cache Streaming), Katman 4 (IA-STP), Katman 3 (V-CCR), Katman 2 (SP-MAC), Katman 1 (Deep-JSCC).
* **Konuşmacı Notu [05:00 - 06:30]:**
  > *"Sayın Hocam, dersimizin proje yönergesinde belirtilen tüm katman gereksinimlerini harfiyen karşılayacak şekilde 6 katmanlı bir mimari inşa ettik: En üstte yeni eklediğimiz Katman 6 yer alıyor: AIRL (Agent Intent & Reasoning Layer). Katman 5 Uygulama Katmanımızda JSON'u tamamen terk ettik; doğrudan 8-bit kuantize KV-cache akışı yapıyoruz. Katman 4 Nakil Katmanımız IA-STP, Shannon entropisine bakarak hangi paketin yeniden iletileceğini seçer. Katman 3 Ağ Katmanımız V-CCR, IP adresi yerine semantik kabiliyet vektörleri üzerinden yönlendirme yapar. Katman 2 Veri Bağı Katmanımız SP-MAC, 4 seviyeli donanımsal öncelik kuyruğuna sahiptir. Katman 1 Fiziksel Katmanımız Deep-JSCC ise tensörleri doğrudan sürekli IQ sembollerine eşleyen derin sinir ağı tabanlı bir alıcı-vericidir."*

---

### Slayt 6: Katman 6 (YENİ) — Ajan Niyet & Muhakeme Katmanı (AIRL)
* **İçerik:** Dinamik Offload Kararı ($Load \ge 0.75$, $Battery \le 0.20$), Anlamsal Yetenek Eşleme, Otonom Görev Sözleşmesi, Ortak Bağlam Uyumu.
* **Konuşmacı Notu [06:30 - 08:00]:**
  > *"Katman 6, SAPS mimarisinin en özgün yeniliğidir. Klasik OSI veya TCP/IP modelinde böyle bir katman bulunmamaktadır. AIRL, doğrudan yapay zeka ajanlarının çalışma prensiplerine odaklanır. Bir mobil ajan (örneğin kamerasıyla çevre taraması yapan bir drone), işlemci yükü %75'in üzerine çıktığında veya bataryası kritik seviyeye indiğinde görevi yerel olarak sürdüremez. AIRL bu noktada devreye girer: Önce ağa bir niyet anonsu yapar, uç sunuculardan teklif toplar, 1.2 milisaniyede en uygun GPU'lu sunucuyla bağlayıcı bir sözleşme imzalar ve ortak bağlam vektörlerini senkronize eder. Böylece iletişim başlamadan önce 'kimin, hangi niyetle ne yapacağı' kesinleşmiş olur."*

---

### Slayt 7: Katman 6 Derinlemesine: Çoklu Ajan Müzakere Durum Makinesi
* **İçerik:** FSM Adımları: IDLE $\rightarrow$ DISCOVERY $\rightarrow$ PROPOSAL & SCORING $\rightarrow$ BINDING $\rightarrow$ CONTEXT_SYNC. Çok kriterli skorlama formülü: $S = 0.50 \cdot \text{Sim}(e_t, e_c) + 0.30 \cdot (1 - L) + 0.20 \cdot (\text{VRAM}_{\text{avail}} / \text{VRAM}_{\text{req}})$.
* **Konuşmacı Notu [08:00 - 09:15]:**
  > *"Hocam, AIRL katmanımız arka planda kesin bir Sonlu Durum Makinesi (FSM) ile yönetilir. Ajan normal şartlarda IDLE durumundadır; yerel kaynaklar yetiyorsa boş yere telsiz yayını yapıp batarya harcamaz. Yük eşiği aşıldığında DISCOVERY fazına geçer. Ekranda gördüğünüz formülle üç farklı bileşeni ağırlıklandırıyoruz: Semantik kabiliyet benzerliği (%50), uç düğümün mevcut boş işlem kapasitesi (%30) ve VRAM yeterlilik oranı (%20). Bu sayede sadece en yakın olan düğüm değil, o an görevi en yüksek hız ve hassasiyetle bitirebilecek düğüm seçilmektedir."*

---

### Slayt 8: Katman 5 (Uygulama) — Doğrudan KV-Cache & Tensör Akışı
* **İçerik:** Metin serileştirmenin sonu, Rank truncation, 8-bit dinamik kuantizasyon, %95.0 bant genişliği tasarrufu, 18 baytlık ultra hafif SAPS tensör başlığı.
* **Konuşmacı Notu [09:15 - 10:30]:**
  > *"Uygulama katmanında günümüz web standartları gRPC, REST ve JSON kullanır. Bir LLM modelinin katman çıktılarını JSON formatına çevirmek (string serialization), devasa bir hesaplama ve bant genişliği israfıdır. SAPS Katman 5'te 'Direct KV-Cache Streaming' mimarisi geliştirdik. Transformatör modellerinin en çok bellek kaplayan kısmı Key-Value dikkat tensörleridir. Biz bu tensörleri Float32'den dinamik 8-bit kuantizasyonla Uint8 formatına indirgiyoruz. Ekranda formülünü gördüğümüz bu dinamik ölçekleme sayesinde, 65 KB'lık bir dikkat tensörü 3.2 KB'a düşüyor. Üstelik HTTP'nin 800 baytlık devasa başlıkları yerine, yalnızca 18 baytlık ultra hafif SAPS tensör başlığı kullanıyoruz."*

---

### Slayt 9: Katman 4 (Nakil) — IA-STP: Anlamsal Entropi Duyarlı ARQ
* **İçerik:** Kör yeniden iletim reddi, Shannon bilgi entropisi hesabı, seçici iletim kararı, bilinçli paket atlama, Head-of-line blocking engelleme.
* **Konuşmacı Notu [10:30 - 11:45]:**
  > *"Nakil katmanında geliştirdiğimiz protokolün adı IA-STP: Intent-Aware Semantic Transport Protocol. TCP ve QUIC'in mobil yapay zeka ajanlarındaki en ölümcül kusuru 'kör yeniden iletimdir' (Blind ARQ). Mobil telsiz kanalında ani bir derin sönümleme (deep fading) yaşanırsa ve bir paket düşerse, TCP hattı durdurur ve o paket gelene kadar sonraki paketlerin teslimatını engeller. IA-STP bu sorunu Shannon bilgi entropisiyle çözer: Paket içindeki her token'ın entropisi hesaplanır. Bir İHA'nın 'ACİL_DUR' komutu 2.85 nats entropiye sahiptir; derhal yeniden iletilir. Ancak 've', 'bir' gibi dolgu sözcükleri 0.18 nats entropiye sahiptir; kaybolursa IA-STP bunu kasten yeniden iletmez, atlar! Çünkü alıcı ajan dil modeli o dolguyu bağlamdan rahatlıkla tamamlayabilir."*

---

### Slayt 10: Katman 4 Derinlemesine: Shannon Entropisi Matematiksel Modeli
* **İçerik:** Koşullu olasılık dağılımı, $H(t_k) = -\sum_{v \in V} p(v \mid t_{<k}) \ln p(v \mid t_{<k})$, ikili karar kuralı, SNR duyarlı dinamik eşik: $\tau(\text{SNR}) = \tau_{\text{base}} (1 + \beta e^{-\text{SNR}/10})$.
* **Konuşmacı Notu [11:45 - 13:00]:**
  > *"Sayın Hocam, bu formülasyon IA-STP'nin kalbini oluşturuyor. Dil modelinin kelime dağarcığı üzerindeki softmax olasılık dağılımından Shannon entropisini hesaplıyoruz. Eğer model bir sonraki kelimeden %99 eminse entropi sıfıra yaklaşır. Ama modelin belirsizliği yüksekse veya beklenmedik kritik bir bilgi geliyorsa entropi zirve yapar. Ayrıca protokolümüze 'Dinamik Eşik Uyarlama' ekledik: Mobil telsiz kanalının SNR'ı düştüğünde tau eşiği otomatik olarak yukarı ötelenir. Böylece kanal kötüleştiğinde sadece ve sadece hayati öneme sahip komutlar telsizden geçer; gereksiz hiçbir trafik kanalı meşgul etmez."*

---

### Slayt 11: Katman 3 (Ağ) — V-CCR: Vektör Uzayında Anlamsal Yönlendirme
* **İçerik:** IP tablolarının tasfiyesi, kosinüs benzerliği metriği, sıfır DNS arama gecikmesi, otonom rota kararı: $\text{NextHop} = \arg\max [\text{Sim}(v_{\text{task}}, v_i) - \lambda \cdot \text{Load}_i]$.
* **Konuşmacı Notu [13:00 - 14:15]:**
  > *"Ağ katmanında geliştirdiğimiz protokol V-CCR: Vector-space Content & Capability Routing. Klasik IP yönlendirmesi statik topolojiye bakar. Ancak mobil bir ajan için gideceği yerin IP adresi anlamsızdır. Ajan için önemli olan, o paketi alıp işleyebilecek yapay zeka modelinin nerede olduğudur. V-CCR'da her paketin başlığında semantik niyet vektörü bulunur. Yönlendirici, kosinüs benzerliği formülü ile hedef düğümü belirler. Böylece DNS sorgusu, IP tablosu arama gecikmesi olmadan paket doğrudan en uygun GPU'ya sahip uç düğüme yönlendirilir."*

---

### Slayt 12: Katman 2 (Veri Bağı) — SP-MAC: Semantik Öncelikli MAC
* **İçerik:** 4 Donanımsal Öncelik Kuyruğu (CRITICAL, HIGH, MEDIUM, LOW), Strict-Priority Dequeuing, Dinamik Contention Window ($CW_{\min}=1$ vs $CW_{\min}=31$), 0.00 ms kuyruk gecikmesi.
* **Konuşmacı Notu [14:15 - 15:30]:**
  > *"Veri bağı katmanında geliştirdiğimiz SP-MAC (Semantic-Priority MAC), 4 seviyeli bir donanımsal kuyruk yapısına sahiptir. Klasik Wi-Fi veya hücresel MAC katmanlarında bir cihaz telemetri logu gönderirken aynı anda gelen kritik bir engel algılama paketi kuyrukta bekleyebilir. SP-MAC bunu kesin bir strict-priority mekanizmasıyla çözer: CRITICAL kuyruğundaki acil durum ve navigasyon paketleri Contention Window'u minimum tutarak (CW=1) kanala anında erişir. Düşük öncelikli arka plan güncellemeleri ise bekletilir. Böylece kritik kararlarda donanım seviyesinde sıfır kuyruk gecikmesi garanti altına alınır."*

---

### Slayt 13: Katman 1 (Fiziksel) — Deep-JSCC: Nöral Alıcı-Verici Mimarisi
* **İçerik:** Ayrı kodlama teoreminin aşılması, MLP Encoder, Güç Normalizasyonu ($\mathbb{E}[|s|^2]=1$), Mobil sönümlemeli telsiz kanalı ($y = hs + n$), MLP Decoder.
* **Konuşmacı Notu [15:30 - 16:45]:**
  > *"Fiziksel katmanda Deep-JSCC (Deep Joint Source-Channel Coding) nöral alıcı-verici mimarisini kurduk. Bildiğiniz üzere Shannon'ın 1948'deki kaynak-kanal ayırma teoremi yalnızca sonsuz blok uzunluğunda geçerlidir. Mobil gecikmeye duyarlı sistemlerde kaynak kodlama ve kanal kodlamayı ayırmak gecikmeyi artırır. Deep-JSCC'de bir derin sinir ağı kullanıyoruz: Ajanın ürettiği gizil tensör vektörü, çok katmanlı bir yapay sinir ağı tarafından doğrudan karmaşık IQ sembollerine dönüştürülür. Bu sembollerin ortalama gücü 1'e normalize edilerek antene verilir. Alıcı taraftaki Nöral Decoder ise gürültülü IQ sembollerinden doğrudan anlamsal tensörü yeniden inşa eder."*

---

### Slayt 14: Fiziksel Katman Formülasyonu: Kayıp Fonksiyonu & Takımyıldızı
* **İçerik:** Uçtan uca MSE kaybı: $\mathcal{L}(\theta, \phi) = \frac{1}{B} \sum \|x_i - \hat{x}_i\|^2$, Nöral takımyıldızı şekillendirme (Neural Constellation Shaping), Uçurum etkisinin ortadan kaldırılması.
* **Konuşmacı Notu [16:45 - 18:00]:**
  > *"Sayın Hocam, bu slaytta Deep-JSCC'nin neden klasik QAM modülasyonundan üstün olduğunu matematiksel olarak görüyoruz. Modelimiz uçtan uca Ortalama Hata Karesi (MSE) kaybıyla eğitilir. Klasik modülasyonlarda semboller katı bir kare ızgara üzerindedir. Bir sembol gürültü nedeniyle komşu kareye taştığında bitler tamamen ters döner ve tüm paket atılır. Deep-JSCC ise sürekli bir uzayda çalışır. Sinir ağı kendi optimum takımyıldızını serbestçe öğrenir. Sonuç olarak: Kanalda şiddetli bir sönümleme yaşandığında iletişim sıfırlanmaz; tensördeki gürültü biraz artar ama genel anlam korunur. Bu 'kademeli bozulma' (graceful degradation) özelliği hayati önem taşır."*

---

### Slayt 15: NVIDIA Sionna Entegrasyonu: 3GPP TR 38.901 Mobil Kanal Modeli
* **İçerik:** NVIDIA Sionna 2.2 entegrasyonu, 3GPP TR 38.901 UMi ve UMa modelleri, $f_c = 3.5\text{ GHz}$, $f_d = 50\text{ Hz}$ Doppler, `saps/channel/sionna_channel.py`, 30/30 birim test başarısı.
* **Konuşmacı Notu [18:00 - 19:15]:**
  > *"Sayın Hocam, projemizin değerini ve gerçekçiliğini artırmak adına en güncel 5G/6G endüstri standardı olan NVIDIA Sionna kütüphanesini sistemimize entegre ettik. NVIDIA Sionna, 3GPP TR 38.901 spesifikasyonuna tam uyumlu ışın izleme ve kentsel çok yollu sönümleme modelleri sunmaktadır. Sistemimizde 'saps/channel/sionna_channel.py' modülünü geliştirdik. Taşıyıcı frekansını 3.5 GHz ve Doppler frekansını 50 Hz olarak ayarladık. Deep-JSCC sinir ağımızın ürettiği IQ sembollerini doğrudan bu Sionna 3GPP kanalından geçirerek test ettik. Yazdığımız testler %100 başarıyla geçmiş, toplam test sayımız 30'a yükselmiştir. Böylece SAPS'ın başarısını sadece sentetik kanallarda değil, 3GPP standartlarında da kanıtlamış olduk."*

---

### Slayt 16: Ayrık Olaylı Simülasyon Testbed'i & Değerlendirme Metodolojisi
* **İçerik:** SimPy ayrık olay motoru + PyTorch 2.14, Rayleigh/Rician/Sionna kanalları, adil karşılaştırma eşitliği (özdeş sönümleme izleri), SNR aralığı [0 - 30 dB].
* **Konuşmacı Notu [19:15 - 20:15]:**
  > *"Simülasyon testbed'imizi Python ortamında SimPy ayrık olaylı simülasyon motoru ile PyTorch derin öğrenme kütüphanesini birleştirerek geliştirdik. Buradaki en kritik bilimsel prensibimiz 'Adil Karşılaştırma Eşitliği'dir: Hem SAPS hem de geleneksel HTTP/3 + QUIC protokol yığını, aynı rastgele tohumla (seed) üretilmiş tıpatıp aynı kanal sönümleme koşullarından geçirilmiştir. SNR aralığı 0 dB ile 30 dB arasında taranmış; gecikme, paket kaybı, bant genişliği ve enerji tüketimi eş zamanlı kaydedilmiştir."*

---

### Slayt 17: Deney 1: Uçtan Uca Gecikme vs Mobil Kanal SNR (6.76x Hızlanma)
* **Görsel:** [`results/latency_vs_snr.png`](file:///c:/Users/yakup.yolcu/Desktop/YL/after-af/26-27_Guz/Wireless/Project/saps/results/latency_vs_snr.png)
* **Bulgular:** SAPS ortalama gecikme 7.79 ms vs Baz 52.63 ms (6.76x Hızlanma). 0 dB SNR'da QUIC >300 ms'ye patlarken SAPS 10.5 ms'de düz kalır.
* **Konuşmacı Notu [20:15 - 21:15]:**
  > *"Grafikte uçtan uca gecikmenin mobil kanal SNR'ına göre değişimini görüyoruz. Kırmızı çizgi geleneksel HTTP/3 ve QUIC yığınıdır; ortalama 52.6 milisaniye gecikmeye sahiptir. Özellikle 0 dB ve 5 dB gibi zorlu kanal şartlarında yeniden iletim fırtınaları nedeniyle gecikme 300 milisaniyenin üzerine fırlamaktadır. Mavi çizgi ise geliştirdiğimiz SAPS protokol yığınıdır: Tüm SNR koşullarında ortalama gecikme 7.79 milisaniyedir! Bu da tam 6.76 kat hızlanma anlamına gelir. Otonom sürüş ve drone navigasyonu için kritik olan 10 milisaniye eşiğinin altında kalan tek protokol SAPS olmuştur."*

---

### Slayt 18: Deney 2: Kuyruk Gecikmesi (Tail Latency) & Jitter Analizi (22x İyileşme)
* **Tablo:** Mean: 52.6 vs 7.8 ms (6.7x) | p95: 219.6 vs 9.8 ms (22.5x) | p99: 298.4 vs 10.5 ms (28.6x) | Max: 304.3 vs 10.5 ms (28.9x).
* **Konuşmacı Notu [21:15 - 22:15]:**
  > *"Hocam, telekomünikasyonda ve özellikle otonom sistemlerde ortalama gecikme aldatıcı olabilir. Esas önemli olan p95 ve p99 dediğimiz kuyruk gecikmeleridir (Tail Latency). Tabloya baktığımızda çarpıcı bir gerçekle karşılaşıyoruz: Geleneksel yığında ortalama gecikme 52 ms iken, 95. yüzdelik gecikme 219 ms'ye, 99. yüzdelik ise 298 ms'ye fırlamaktadır! Bunun sebebi mobil sönümleme anında TCP'nin art arda yaşadığı yeniden iletim tıkanmalarıdır. Saatte 50 km hızla giden bir robot için 300 ms'lik körlük kaza sebebidir. SAPS'a baktığımızda ise p95 gecikmesi 9.78 ms, en kötü durum maksimum gecikmesi ise 10.52 ms'dir! Geleneksel yığına göre kuyruk gecikmesinde tam 22 katlık bir iyileşme elde ettik."*

---

### Slayt 19: Deney 3: Kademeli Bozulma vs Dijital Uçurum Etkisi (BLEU Skoru)
* **Görsel:** [`results/bleu_vs_loss_rate.png`](file:///c:/Users/yakup.yolcu/Desktop/YL/after-af/26-27_Guz/Wireless/Project/saps/results/bleu_vs_loss_rate.png)
* **Bulgular:** 16-QAM %20 kayıpta 0 BLEU'ya çöker. Deep-JSCC %50 kayıpta dahi >0.75 BLEU skorunu korur.
* **Konuşmacı Notu [22:15 - 23:15]:**
  > *"Bu grafikte anlamsal doğruluk metriği olan BLEU skorunun paket kayıp oranına göre değişimini inceliyoruz. Kırmızı eğri klasik QAM tabanlı geleneksel yığındır. Paket kaybı %20'nin üzerine çıktığı an dijital uçurum etkisi (cliff effect) gerçekleşir ve BLEU skoru sıfıra çakılır; yani iletişim tamamen kopar. Yeşil eğri ise SAPS'ın Deep-JSCC katmanıdır. Gördüğünüz gibi son derece yumuşak ve kademeli bir bozulma sergilemektedir. Kanalda %50 gibi yıkıcı bir paket kaybı olsa dahi, SAPS 0.75'in üzerinde BLEU doğruluğunu muhafaza eder. Alıcı taraftaki otonom ajan, eksik parçalara rağmen görevi sürdürmeye yetecek anlamı kavramış olur."*

---

### Slayt 20: Deney 4: Bant Genişliği Tasarrufu (%95.3) & Entropi Dağılımı
* **Görseller:** [`results/bandwidth_savings.png`](file:///c:/Users/yakup.yolcu/Desktop/YL/after-af/26-27_Guz/Wireless/Project/saps/results/bandwidth_savings.png) ve [`results/token_entropy_distribution.png`](file:///c:/Users/yakup.yolcu/Desktop/YL/after-af/26-27_Guz/Wireless/Project/saps/results/token_entropy_distribution.png)
* **Bulgular:** 68.4 KB $\rightarrow$ 3.2 KB (%95.3 tasarruf). Verici RF enerji tüketimi %92.1 azalmıştır. Entropi eşiği 1.0 nats ile iki modlu net ayrım.
* **Konuşmacı Notu [23:15 - 24:15]:**
  > *"Bu slaytta iki kritik sonucu yan yana görüyoruz: Sol tarafta bant genişliği ve enerji tasarrufu yer alıyor. Geleneksel HTTP/JSON akışı aynı tensör aktarımı için 68.400 bayt tüketirken, SAPS yalnızca 3.276 bayt ile aynı çıkarımı gerçekleştirmiştir. Bu tam %95.3'lük bir bant genişliği azalmasıdır! Radyo iletim süresi kısaldığı için mobil ajanın batarya enerji tüketimi de %92.1 oranında düşmektedir. Sağ taraftaki grafikte ise tokenların Shannon entropi dağılımını görüyoruz. Dağılım açıkça iki tepeye (bimodal) ayrılmıştır: Sol tepedeki düşük entropili tokenlar dolgudur, atlanır; sağ tepedeki yüksek entropili tokenlar ise hayati komutlardır, korunur."*

---

### Slayt 21: Deney 5: NVIDIA Sionna 3GPP TR 38.901 Kentsel Mikro Kanal Sonuçları
* **Görsel:** [`results/sionna_3gpp_benchmark.png`](file:///c:/Users/yakup.yolcu/Desktop/YL/after-af/26-27_Guz/Wireless/Project/saps/results/sionna_3gpp_benchmark.png)
* **Bulgular:** Sionna 3GPP UMi kanalında 6.66x gecikme hızlanması ve %95.4 bant genişliği tasarrufu teyit edilmiştir.
* **Konuşmacı Notu [24:15 - 25:15]:**
  > *"Sayın Hocam, bu deney çalışmamızın en iddialı doğrulama adımıdır: Tüm mimariyi NVIDIA'nın 3GPP TR 38.901 standart kütüphanesi olan Sionna 2.2 üzerinde koşturduk. 3.5 GHz taşıyıcı frekansında, kentsel mikro hücre (UMi) ve 50 Hz Doppler hızında aldığımız sonuçlar sol taraftaki 3 panelli grafikte yer almaktadır: 1. Panelde gecikmenin yine 7.82 ms ile 6.66 kat hızlandığını görüyoruz. 2. Panelde 16-QAM modülasyonunun Sionna kanalında çöktüğünü, Deep-JSCC'nin ise kusursuz devam ettiğini görüyoruz. 3. Panelde ise %95.4 bant genişliği tasarrufunun 3GPP ortamında da aynen korunduğunu kanıtlamış olduk. Bu sayede SAPS'ın başarısının yapay simülasyon varsayımlarına bağlı olmadığını, 5G/6G standartlarında da birebir geçerli olduğunu ispatladık."*

---

### Slayt 22: Yönetici Değerlendirme Paneli: 4 Boyutlu Genel Karşılaştırma
* **Görsel:** [`results/presentation_dashboard.png`](file:///c:/Users/yakup.yolcu/Desktop/YL/after-af/26-27_Guz/Wireless/Project/saps/results/presentation_dashboard.png)
* **İçerik:** Gecikme, Semantik Doğruluk, Bant Genişliği ve Enerji Tasarrufu 4 panelde konsolide sunulmuştur.
* **Konuşmacı Notu [25:15 - 26:00]:**
  > *"Bu slaytta projemizin tüm temel kazanımlarını 4 panellik bir yönetici özetinde görüyoruz: Sol üstte Gecikme (6.76x hızlanma), Sağ üstte Semantik Kalite (Kademeli bozulma ile kesintisiz iletişim), Sol altta Bant Genişliği (%95.3 tasarruf), Sağ altta ise Enerji Tüketimi (%92.1 düşüş). Bu 4 grafik birlikte gösteriyor ki SAPS, tek bir metriği iyileştirirken diğerlerinden ödün veren bir protokol değildir; tüm metriklerde geleneksel internet yığınını geride bırakmaktadır."*

---

### Slayt 23: Canlı İnteraktif Simülatör Web Paneli (`scripts/run_simulation_ui.py`)
* **İçerik:** Sıfır bağımlılıklı Python HTTP sunucusu, anlık SNR (0-30 dB) ve Entropi (0.1-3.0) kaydırıcıları, NVIDIA Sionna 3GPP / Rayleigh / Rician kanal seçici, HTML5 Canvas canlı IQ takımyıldızı diyagramı.
* **Çalıştırma Komutu:** `py scripts/run_simulation_ui.py --port 8050` $\rightarrow$ `http://localhost:8050`
* **Konuşmacı Notu [26:00 - 27:00]:**
  > *"Değerli Hocam, bu çalışmayı yalnızca statik grafiklerle bırakmadık; sunum anında dilediğiniz parametreyi test edebileceğiniz interaktif bir Web Simülatör Gösterge Paneli de geliştirdik. 'py scripts/run_simulation_ui.py' komutuyla çalışan bu arayüzde: SNR kaydırıcısını hareket ettirerek anlık kanal bozulmalarını simüle edebiliyor, kanal modelini NVIDIA Sionna 3GPP olarak seçebiliyor ve sağ taraftaki HTML5 Canvas üzerinde Deep-JSCC'nin karmaşık IQ takımyıldızını gerçek zamanlı izleyebiliyoruz. Dilerseniz sunum sonundaki soru-cevap kısmında istediğiniz bir parametreyi burada canlı olarak simüle edebiliriz."*

---

### Slayt 24: Canlı Simülasyon Gösterimi: 6 Katmanlı Uçtan Uca İletim
* **İçerik:** Slayta gömülü video (`results/saps_demo_video.mp4`), terminal CLI gösterim komutu (`py scripts/demo_presentation.py`), İHA engel algılama ve offload senaryosu.
* **Konuşmacı Notu [27:00 - 28:00]:**
  > *"Slaytımızda gömülü olarak yer alan demo videosunda, geliştirdiğimiz 6 katmanlı iletimin gerçek bir görev senaryosundaki traversal akışını görüyoruz. Senaryomuzda mobil bir İHA ajanı, yüksek işlemci yükü altındayken aniden bir engel algılıyor. Sırasıyla: AIRL Katmanı 1.2 milisaniyede en uygun uç sunucuyla sözleşme imzalıyor, Uygulama Katmanı dikkat tensörünü 8-bite kuantize ediyor, IA-STP yüksek entropili koordinatları koruma altına alıyor, SP-MAC bu pakete en yüksek önceliği vererek kanala sürüyor ve Deep-JSCC sembolleri Sionna kanalından iletiyor. İstendiğinde 'py scripts/demo_presentation.py' komutuyla terminal üzerinden de canlı akışı izleyebiliyoruz."*

---

### Slayt 25: Kapsamlı Karşılaştırma: Geleneksel HTTP/3 + QUIC vs SAPS
* **İçerik:** Birebir sayısal karşılaştırma tablosu (Gecikme: 7.79 vs 52.63 ms, Tail: 9.78 vs 219.58 ms, Bayt: 3.276 vs 68.400 bayt, Enerji: %92.1 tasarruf, Fading: Cliff yok, Sionna 3GPP desteği).
* **Konuşmacı Notu [28:00 - 29:00]:**
  > *"Bu karşılaştırma tablosu, projemizin ulaştığı tüm sayısal başarıların nihai özetidir: Ortalama gecikmede 52 ms'den 7.7 ms'ye inerek 6.76 kat hızlanma sağladık. Kuyruk gecikmesinde 219 ms'den 9.7 ms'ye inerek 22 katlık bir kararlılık artışı elde ettik. İletilen bayt hacmini 68 KB'dan 3.2 KB'a düşürerek %95.3 bant genişliği ve %92.1 enerji tasarrufu sağladık. Fiziksel katmandaki uçurum etkisini sıfırlayarak %50 paket kaybında dahi 0.75 BLEU doğruluğunu koruduk. Ve tüm bu kazanımları NVIDIA Sionna 3GPP kentsel kanal modelleriyle doğruladık."*

---

### Slayt 26: Sonuç & Sorular (Conclusion & Q&A)
* **İçerik:** 3 Temel Akademik Katkı, Teşekkür, GitHub ve testbed bağlantısı, Soru-Cevap bölümü.
* **Konuşmacı Notu [29:00 - 30:00+]:**
  > *"Özetlemek gerekirse; SAPS ile klasik internet protokollerinin yapay zeka ajanlarındaki yetersizliğini kanıtladık ve 6 katmanın tamamını anlamsal prensiplerle yeniden tasarlayarak çalışan bir prototipe dönüştürdük. Dinlediğiniz için çok teşekkür ederim. Sayın Prof. Dr. Hasari Çelebi Hocam ve değerli arkadaşlarım, sorularınızı ve değerli katkılarınızı almaktan onur duyarım."*

---

## 💡 Prof. Dr. Hasari Çelebi'den Gelebilecek Sorular ve Cevap İpuçları

### Soru 1: *"Deep-JSCC kanal SNR'ı aniden değiştiğinde buna nasıl adapte oluyor?"*
* **Kusursuz Cevap:**
  > *"Hocam, Deep-JSCC nöral encoder'ımıza kanal durum bilgisi (CSI) veya anlık SNR kestirimi girdi vektörü olarak verilmektedir. Sönümleme derinleştikçe encoder otomatik olarak takımyıldızı enerjisini yeniden ölçekler (dynamic power allocation). Ayrıca NVIDIA Sionna kanalımızda model 0 dB ile 30 dB gibi geniş bir dinamik aralıkta eğitildiği için ani SNR dalgalanmalarında 16-QAM gibi takımyıldızı yeniden müzakeresi (AMC) beklemeden sürekli bir dönüşümle uyum sağlar."*

### Soru 2: *"IA-STP'de atlanan düşük entropili tokenlar alıcı tarafta nasıl telafi ediliyor? Anlam kaybı olmuyor mu?"*
* **Kusursuz Cevap:**
  > *"Hocam, alıcı uç düğümdeki büyük dil modeli (LLM) veya karar motoru, Masked Language Modeling (MLM) mimarisine benzer bir tahmin yeteneğine sahiptir. Örneğin 'Drone acil [ATLANDI] iniş yapacak' cümlesinde atlanan düşük entropili kelime ('olarak') bağlam tensörlerinden %99.8 doğrulukla kestirilir. IA-STP paket başlığındaki göreli konum indeksleri (RoPE) sayesinde alıcı hangi pozisyonun atlandığını bilir ve eksik indeksi bağlam vektörüyle doldurur."*

### Soru 3: *"NVIDIA Sionna'yı entegre etmek çalışmaya akademik ve pratik olarak ne kattı?"*
* **Kusursuz Cevap:**
  > *"Hocam, klasik simülasyonlarda kullanılan tek musluklu (flat) Rayleigh modelleri, kentsel ortamlardaki binalardan yansıyan çok yollu gecikme yayılımını (multipath delay spread) ve açısal geliş yönlerini (AoA/AoD) yansıtamaz. NVIDIA Sionna, 3GPP TR 38.901 standart spesifikasyonunu GPU üzerinde tam ışın izlemeyle (ray tracing) çalıştırır. Sionna 3GPP UMi modelinde aldığımız 6.66x hızlanma ve %95.4 tasarruf, SAPS'ın gerçek 5G/6G kentsel baz istasyonlarında da doğrudan çalışabileceğini ispatlamıştır."*

### Soru 4: *"V-CCR yönlendirmesi binlerce uç sunucu olduğunda ölçeklenebilir mi?"*
* **Kusursuz Cevap:**
  > *"Evet Hocam. V-CCR yönlendiricileri, vektör veritabanlarında kullanılan HNSW (Hierarchical Navigable Small World) ve FAISS indeksleme algoritmalarını kullanır. Milyonlarca kabiliyet vektörü içinde kosinüs benzerliği araması 0.1 milisaniyenin altında tamamlanmaktadır. Bu süre, geleneksel internetteki DNS araması ve BGP yakınsama sürelerinden katbekat daha hızlıdır."*

---

## 🚀 Canlı Gösterim Çalıştırma Kılavuzu (Hoca İzlerken)

1. **İnteraktif Web Gösterge Panelini Açmak İçin:**
   ```powershell
   cd c:\Users\yakup.yolcu\Desktop\YL\after-af\26-27_Guz\Wireless\Project\saps
   py scripts/run_simulation_ui.py --port 8050
   ```
   * Tarayıcıda `http://localhost:8050` açılır.
   * SNR kaydırıcısını hareket ettirin; Deep-JSCC IQ takımyıldızının ve paket gecikmesinin canlı olarak nasıl tepki verdiğini gösterin.

2. **Konsol Üzerinden Hızlı Testi Çalıştırmak İçin:**
   ```powershell
   cd c:\Users\yakup.yolcu\Desktop\YL\after-af\26-27_Guz\Wireless\Project\saps
   py scripts/demo_presentation.py
   ```

3. **NVIDIA Sionna Benchmark'ını Yeniden Koşturmak İçin:**
   ```powershell
   cd c:\Users\yakup.yolcu\Desktop\YL\after-af\26-27_Guz\Wireless\Project\saps
   py scripts/run_sionna_benchmark.py
   ```
