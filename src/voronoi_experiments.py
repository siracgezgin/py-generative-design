import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial import Voronoi, voronoi_plot_2d
import os

"""
HAFTA 1 - GÜN 1: Density Function Experiments
Hedef: Farklı stress pattern'ları simüle eden density function'ları test et
"""

# --- AYARLAR ---
genislik = 100
yukseklik = 100
hedef_nokta_sayisi = 150

# --- DENSİTY FUNCTION VERSİYONLARI ---

def density_left_heavy(x, y):
    """
    VERSİYON 1: Sol Yoğun (Orijinal)
    Use Case: Sol tarafta sabitlenmiş, sağdan yük uygulanan bracket
    """
    norm_x = x / genislik
    olasilik = 1.0 - norm_x * 0.9  # Sol %100, sağ %10
    return olasilik

def density_center_heavy(x, y):
    """
    VERSİYON 2: Merkez Yoğun
    Use Case: Ortadan dağılan kuvvet (headrest gibi)
    """
    # Merkeze olan uzaklığı hesapla
    center_x, center_y = genislik / 2, yukseklik / 2
    distance = np.sqrt((x - center_x)**2 + (y - center_y)**2)
    max_distance = np.sqrt((genislik/2)**2 + (yukseklik/2)**2)
    norm_distance = distance / max_distance
    
    olasilik = 1.0 - norm_distance * 0.85  # Merkez %100, kenar %15
    return max(0.1, olasilik)  # Minimum %10 şans

def density_diagonal_stress(x, y):
    """
    VERSİYON 3: Çapraz Stres
    Use Case: Köşeden köşeye yük aktarımı
    """
    # Sol üstten sağ alta doğru stress azalır
    norm_diagonal = (x + y) / (genislik + yukseklik)
    olasilik = 1.0 - norm_diagonal * 0.9
    return max(0.1, olasilik)

def density_four_point_load(x, y):
    """
    VERSİYON 4: 4 Nokta Yük
    Use Case: Dört köşeden gelen kuvvetler
    """
    corners = [
        (genislik * 0.2, yukseklik * 0.2),
        (genislik * 0.8, yukseklik * 0.2),
        (genislik * 0.2, yukseklik * 0.8),
        (genislik * 0.8, yukseklik * 0.8),
    ]
    
    # En yakın köşeye olan uzaklık
    distances = [np.sqrt((x - cx)**2 + (y - cy)**2) for cx, cy in corners]
    min_distance = min(distances)
    max_possible = np.sqrt(genislik**2 + yukseklik**2) / 2
    
    norm_distance = min_distance / max_possible
    olasilik = 1.0 - norm_distance * 0.8
    return max(0.1, olasilik)

# --- NOKTA ÜRETİMİ ---
def generate_points(density_function, target_count, name=""):
    """Verilen density function ile nokta üret"""
    kabul_edilen = []
    deneme = 0
    max_deneme = target_count * 100  # Sonsuz döngü önleme
    
    print(f"\n{name} üretiliyor...")
    while len(kabul_edilen) < target_count and deneme < max_deneme:
        deneme += 1
        rx = np.random.uniform(0, genislik)
        ry = np.random.uniform(0, yukseklik)
        
        if np.random.random() < density_function(rx, ry):
            kabul_edilen.append([rx, ry])
    
    print(f"-> {deneme} denemede {len(kabul_edilen)} nokta")
    return np.array(kabul_edilen)

# --- VİZÜALİZASYON ---
def visualize_voronoi(points, title, filename):
    """Voronoi diagram oluştur ve kaydet"""
    vor = Voronoi(points)
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 7))
    
    # Sol: Sadece noktalar (density map)
    ax1.scatter(points[:, 0], points[:, 1], c='blue', s=10, alpha=0.6)
    ax1.set_xlim(0, genislik)
    ax1.set_ylim(0, yukseklik)
    ax1.set_title(f'{title}\n(Point Density Map)', fontsize=12, weight='bold')
    ax1.set_xlabel('X')
    ax1.set_ylabel('Y')
    ax1.grid(True, alpha=0.3)
    
    # Sağ: Voronoi diagram
    voronoi_plot_2d(vor, ax=ax2, show_vertices=False, line_colors='orange', line_width=1.5)
    ax2.plot(points[:, 0], points[:, 1], 'b.', markersize=3)
    ax2.set_xlim(0, genislik)
    ax2.set_ylim(0, yukseklik)
    ax2.set_title(f'{title}\n(Voronoi Tessellation)', fontsize=12, weight='bold')
    ax2.set_xlabel('X')
    ax2.set_ylabel('Y')
    
    plt.tight_layout()
    
    os.makedirs("data/processed/experiments", exist_ok=True)
    save_path = f"data/processed/experiments/{filename}"
    plt.savefig(save_path, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"Kaydedildi: {save_path}")

# --- ANA PROGRAM ---
if __name__ == "__main__":
    print("=" * 60)
    print("HAFTA 1 - Density Function Experiments")
    print("=" * 60)
    
    experiments = [
        (density_left_heavy, "V1: Sol Yoğun (Left Heavy)", "v1_left_heavy.png"),
        (density_center_heavy, "V2: Merkez Yoğun (Center Heavy)", "v2_center_heavy.png"),
        (density_diagonal_stress, "V3: Çapraz Stres (Diagonal)", "v3_diagonal.png"),
        (density_four_point_load, "V4: 4 Nokta Yük (Four Point)", "v4_four_point.png"),
    ]
    
    for density_func, title, filename in experiments:
        points = generate_points(density_func, hedef_nokta_sayisi, title)
        visualize_voronoi(points, title, filename)
    
    print("\n" + "=" * 60)
    print("TÜM DENEMELER TAMAMLANDI!")
    print("Dosyalar: data/processed/experiments/")
    print("=" * 60)
