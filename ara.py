import streamlit as st
import pandas as pd
import re
import os

# Sayfa Ayarları
st.set_page_config(
    page_title="Romanya Vatandaşlık Dosya Durumu Sorgulama",
    page_icon="🔍",
    layout="centered"
)

def dosya_tarihi_getir(dosya_adi):
    if os.path.exists(dosya_adi):
        return os.path.getmtime(dosya_adi)
    return 0

tarih_excel = dosya_tarihi_getir("dosyadurumu.xlsx")

@st.cache_data
def veri_yukle(tarih):
    try:
        df = pd.read_excel("dosyadurumu.xlsx")
        df = df.fillna("")
        df['Dosya No'] = df['Dosya No'].astype(str).str.strip()
        return df
    except Exception as e:
        return pd.DataFrame()

df = veri_yukle(tarih_excel)

# --- ARAYÜZ TASARIMI ---
st.title("Romanya Vatandaşlık Dosya Durumu Sorgulama")
st.markdown("Madde 10/11 kapsamındaki dosyanızın güncel durumunu öğrenmek için dosya numaranızı ve yılını giriniz.")

st.info("💡 **Örnek Arama Formatı:** 1234/2017 veya 1234/RD/2017")
aranan_kelime = st.text_input("Dosya Numaranız (No/Yıl):", placeholder="Örn: 514/2026")

if st.button("🔍 Dosyamı Sorgula"):
    if not aranan_kelime:
        st.warning("Lütfen arama yapmak için bir dosya numarası girin.")
    elif df.empty:
        st.error("Sistemde şu an veri bulunmuyor. Lütfen daha sonra tekrar deneyin.")
    else:
        temiz_arama = aranan_kelime.strip().upper().replace(" ", "")
        
        if "/" in temiz_arama:
            parcalar = temiz_arama.split("/")
            ilk_numara = parcalar[0]
            son_yil = parcalar[-1]
            arama_kriteri = f"^{ilk_numara}/.*{son_yil}$"
            sonuclar = df[df['Dosya No'].str.contains(arama_kriteri, flags=re.IGNORECASE, regex=True)]
        else:
            arama_kriteri = f"^{temiz_arama}/"
            sonuclar = df[df['Dosya No'].str.contains(arama_kriteri, flags=re.IGNORECASE, regex=True)]
        
        # --- SONUÇLARI GÖSTERME KISMI ---
        if not sonuclar.empty:
            st.success(f"✅ Eşleşen {len(sonuclar)} adet kayıt bulundu!")
            
            for index, row in sonuclar.iterrows():
                with st.container():
                    st.markdown("---")
                    
                    # 1. Dosya Numarası: En üstte ve çok büyük (kalın) punto ile
                    st.markdown(f"## 📂 {row['Dosya No']}")
                    
                    # 2. Alt satırlarda diğer detaylar
                    st.markdown(f"**📅 Başvuru Kayıt Tarihi:** {row['Başvuru Tarihi']}")
                    
                    if str(row['TERMEN']).strip() and str(row['TERMEN']).strip() != "-":
                        st.markdown(f"**⏳ Sonraki Aşama (TERMEN):** {row['TERMEN']}")
                        
                    # 3. SOLUTIE (Karar) Renklendirme Mantığı
                    solutie_metni = str(row['SOLUTIE']).strip()
                    
                    if solutie_metni:
                        # İçinde bilgi varsa YEŞİL kutu içinde göster
                        st.success(f"**📝 Karar / Durum (SOLUTIE):** {solutie_metni}")
                    else:
                        # İçi boşsa KIRMIZI kutu içinde beklemede olduğunu belirt
                        st.error("**📝 Karar / Durum (SOLUTIE):** Henüz bir karar/durum bilgisi girilmemiş (Beklemede).")
                        
                    # 4. Kaynak Belge (En altta silik/küçük yazıyla)
                    st.caption(f"📌 Kaynak Belge: {row['Kaynak Belge']}")
                    
            st.markdown("---")
        else:
            st.error("❌ Girdiğiniz kriterlere uygun bir dosya bulunamadı. Lütfen dosya numaranızı ve yılını kontrol edip tekrar deneyin.")

# Alt Bilgi (Geliştirilmiş Kurumsal Açıklama)
footer_metni = """
<br><hr>
<div style='text-align: center; color: gray; font-size: 0.9em; line-height: 1.5;'>
    <i>Bu platform, Romanya Adalet Bakanlığı Ulusal Vatandaşlık Kurumu (ANC) tarafından yayımlanan resmi dosya durumu listelerini (Stadiu Dosar) baz alarak otomatik olarak çalışmaktadır.<br>
    Sistemdeki veriler tamamen bilgilendirme amaçlıdır ve resmi bir belge niteliği taşımaz. Kesin ve nihai teyit için her zaman resmi kurum kaynaklarını referans alınız.</i>
</div>
"""
st.markdown(footer_metni, unsafe_allow_html=True)