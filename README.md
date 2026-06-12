# Romanya Vatandaşlık Dosya Durumu Sorgulama

Bu proje, Romanya Adalet Bakanlığı - Ulusal Vatandaşlık Kurumu (ANC) tarafından düzenli olarak yayımlanan **Madde 10 ve Madde 11** kapsamındaki vatandaşlık başvuru dosyalarının durumunu, karmaşık PDF listeleri arasında kaybolmadan, hızlı ve kullanıcı dostu bir arayüzle sorgulamanızı sağlayan web tabanlı bir uygulamadır.

**Streamlit** ve **Pandas** kullanılarak geliştirilmiştir.

---

## ✨ Özellikler

* **Akıllı ve Esnek Arama:** Kullanıcı `1234/2017` araması yaptığında, resmi PDF'lerde araya giren harfleri (Örn: `1234/RD/2017` veya `325/P/2018`) otomatik olarak tolere eder ve tam eşleşmeyi bulur.
* **Tam Eşleşme (Exact Match) Algoritması:** `1234` arandığında `12340` veya `12341` gibi benzer dosyaları eler, sadece tam istenilen dosyayı getirir.
* **Durum Odaklı Renklendirme:** Kullanıcının dosyasında bir karar (SOLUTIE) çıkmışsa sonucu yeşil (olumlu) kutuda, henüz karar çıkmamışsa kırmızı (beklemede) kutuda vurgular.
* **Detaylı Dosya Künyesi:** Başvuru Kayıt Tarihi (DATA ÎNREGISTRĂRII), Sonraki Aşama (TERMEN), Karar (SOLUTIE) ve verinin çekildiği Kaynak Belge ismini tek ekranda sunar.

---

## 🛠️ Kullanılan Teknolojiler

* **Python 3.12+**
* **Streamlit** (Web arayüzü ve sunucu altyapısı)
* **Pandas** (Excel veri manipülasyonu ve regex tabanlı arama)
* **OpenPyXL** (Excel okuma motoru)

---

## 📂 Proje Yapısı

* `ara.py`: Kullanıcıların etkileşime girdiği Streamlit web uygulamasının ana kaynak kodudur.
* `dosyadurumu.xlsx`: ANC'nin yayımladığı resmi PDF'lerden özel bir Python botu (PyMuPDF kullanılarak) ile otomatik çekilip temizlenmiş, filtrelemeye hazır veri tabanı dosyasıdır.
* `requirements.txt`: Uygulamanın çalışması için gereken Python kütüphanelerini listeler.

