import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial import Voronoi, voronoi_plot_2d
import os

# --- AYARLAR ---
genislik = 100
yukseklik = 100
hedef_nokta_sayisi = 100

# --- MANTIK: SOLDA SIKI, SAĞDA GEVŞEK ---
def nokta_kabul_edilsin_mi(x_koordinati):
    # X koordinatını 0-1 arasına çek (Normalize et)
    norm_x = x_koordinati / genislik
    
    # Olasılık formülü: Sol tarafta (x=0) olasılık %100, Sağda (x=100) %0
    olasilik = 1.0 - norm_x
    
    # Bilgisayar 0-1 arası rastgele bir sayı tutsun
    sans = np.random.random()
    
    # Eğer şansımız olasılıktan düşükse kabul et
    if sans < olasilik:
        return True
    else:
        return False

# --- ÜRETİM: NOKTALARI SEÇME ---
kabul_edilen_noktalar = []
deneme_sayisi = 0

# 100 tane nokta bulana kadar döngüye devam et
while len(kabul_edilen_noktalar) < hedef_nokta_sayisi:
    deneme_sayisi += 1
    
    # Rastgele bir konum belirle
    rx = np.random.uniform(0, genislik)
    ry = np.random.uniform(0, yukseklik)
    
    # Mantık fonksiyonuna sor: Bunu alalım mı?
    if nokta_kabul_edilsin_mi(rx):
        kabul_edilen_noktalar.append([rx, ry])

print(f"{deneme_sayisi} kez deneme yapıldı ve {len(kabul_edilen_noktalar)} nokta seçildi.")

# --- ÇİZİM VE KAYIT ---
noktalar = np.array(kabul_edilen_noktalar)
vor = Voronoi(noktalar)

fig, ax = plt.subplots(figsize=(10, 6))

# Voronoi çizgilerini çiz
voronoi_plot_2d(vor, ax=ax, show_vertices=False, line_colors='orange')

# Noktaları da üstüne mavi nokta olarak koy ki görelim
ax.plot(noktalar[:,0], noktalar[:,1], 'b.', markersize=2)

ax.set_xlim(0, genislik)
ax.set_ylim(0, yukseklik)
ax.set_title("Siraç'ın Generative Design Mantığı\n(Sol Taraf: Yoğun Stres Bölgesi | Sağ Taraf: Hafif Bölge)")

# Klasör yoksa hata vermesin diye kontrol et
os.makedirs("data/processed", exist_ok=True)

kayit_yolu = "data/processed/mantikli_voronoi.png"
plt.savefig(kayit_yolu)
print(f"Görsel şuraya kaydedildi: {kayit_yolu}")