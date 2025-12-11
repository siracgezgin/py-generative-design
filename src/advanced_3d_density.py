import numpy as np
import open3d as o3d
import os

"""
HAFTA 1 - GÜN 2 (İLERİ): Multi-Axis Density Functions
Hedef: Y ve Z eksenlerini de kullanarak daha gerçekçi stress pattern'ları
"""

class AdvancedPointCloudGenerator:
    """3D Nokta Bulutu - Çok Eksenli Density Function'lar"""
    
    def __init__(self, size_x=100, size_y=100, size_z=100, target_points=3000):
        self.size_x = size_x
        self.size_y = size_y
        self.size_z = size_z
        self.target_points = target_points
        self.points = []
    
    def density_cantilever_beam(self, x, y, z):
        """
        CANTILEVER BEAM (Konsol Kiriş)
        Sol taraf sabit, sağ uçtan yük
        Stress: Sol tarafta yüksek, sağa doğru azalır
        Ayrıca üst/alt yüzeylerde daha yüksek (bending stress)
        """
        # X ekseni: Sol yoğun
        x_factor = 1.0 - (x / self.size_x) * 0.7
        
        # Y ekseni: Üst ve alt yüzeylerde yoğun (bending)
        y_center = self.size_y / 2
        y_distance = abs(y - y_center) / (self.size_y / 2)
        y_factor = 0.5 + y_distance * 0.5  # Merkez 0.5, kenarlar 1.0
        
        # Z ekseni: Uniform (veya hafif varyasyon)
        z_factor = 1.0
        
        prob = x_factor * y_factor * z_factor
        return max(0.1, prob)
    
    def density_compression_load(self, x, y, z):
        """
        COMPRESSION (Basma Yükü)
        Üstten basma kuvveti, alt sabit
        Z ekseni boyunca gradient, X-Y düzleminde merkez yoğun
        """
        # Z ekseni: Üstte yoğun (yükün geldiği yer)
        z_factor = 1.0 - (z / self.size_z) * 0.6
        
        # XY düzlemi: Merkeze yakın bölgeler yoğun
        center_x = self.size_x / 2
        center_y = self.size_y / 2
        xy_distance = np.sqrt((x - center_x)**2 + (y - center_y)**2)
        max_xy_dist = np.sqrt((self.size_x/2)**2 + (self.size_y/2)**2)
        xy_norm = xy_distance / max_xy_dist
        xy_factor = 1.0 - xy_norm * 0.5
        
        prob = z_factor * xy_factor
        return max(0.1, prob)
    
    def density_torsion(self, x, y, z):
        """
        TORSION (Burulma)
        Z ekseni etrafında dönme, dış yüzeylerde stress yüksek
        """
        # Merkez eksenden radyal uzaklık (XY düzlemi)
        center_x = self.size_x / 2
        center_y = self.size_y / 2
        radial_dist = np.sqrt((x - center_x)**2 + (y - center_y)**2)
        max_radial = np.sqrt((self.size_x/2)**2 + (self.size_y/2)**2)
        
        # Dışa doğru artan stress
        radial_norm = radial_dist / max_radial
        radial_factor = 0.3 + radial_norm * 0.7  # Merkez 0.3, kenar 1.0
        
        # Z ekseni: Uniform
        z_factor = 1.0
        
        prob = radial_factor * z_factor
        return max(0.1, prob)
    
    def density_bracket_realistic(self, x, y, z):
        """
        REALİSTİK BRACKET
        Sol alt köşe sabit, sağ üst köşeden yük
        Çapraz yük yolu boyunca yoğun
        """
        # Sol alt köşe (0, 0, 0) sabit
        # Sağ üst köşe (max_x, max_y, max_z) yük noktası
        
        # Çapraz mesafe hesapla
        load_point_x = self.size_x * 0.9
        load_point_y = self.size_y * 0.9
        load_point_z = self.size_z * 0.9
        
        # Sabit noktaya uzaklık
        dist_to_fixed = np.sqrt(x**2 + y**2 + z**2)
        
        # Yük noktasına uzaklık
        dist_to_load = np.sqrt(
            (x - load_point_x)**2 + 
            (y - load_point_y)**2 + 
            (z - load_point_z)**2
        )
        
        max_dist = np.sqrt(
            self.size_x**2 + self.size_y**2 + self.size_z**2
        )
        
        # Her iki noktaya da yakın bölgeler yoğun
        combined_factor = 1.0 - (
            (dist_to_fixed / max_dist + dist_to_load / max_dist) / 2
        ) * 0.7
        
        prob = max(0.1, combined_factor)
        return prob
    
    def density_multi_load_paths(self, x, y, z):
        """
        ÇOK YOLLU YÜK AKTARIMI
        3 farklı noktadan gelen kuvvetler
        """
        load_points = [
            (self.size_x * 0.2, self.size_y * 0.8, self.size_z * 0.8),
            (self.size_x * 0.8, self.size_y * 0.2, self.size_z * 0.8),
            (self.size_x * 0.5, self.size_y * 0.5, self.size_z * 0.1),
        ]
        
        # Her load point'e olan mesafe
        distances = [
            np.sqrt((x - lx)**2 + (y - ly)**2 + (z - lz)**2)
            for lx, ly, lz in load_points
        ]
        
        # En yakın load point'e olan mesafe kullan
        min_distance = min(distances)
        max_possible = np.sqrt(
            self.size_x**2 + self.size_y**2 + self.size_z**2
        )
        
        norm_dist = min_distance / max_possible
        prob = 1.0 - norm_dist * 0.8
        
        return max(0.15, prob)
    
    def generate(self, density_function_name):
        """Belirtilen density function ile nokta üret"""
        density_func = getattr(self, f"density_{density_function_name}")
        
        print(f"\n3D Advanced: {density_function_name}")
        print(f"Hedef: {self.target_points} nokta")
        
        self.points = []
        count = 0
        max_attempts = self.target_points * 150
        
        while len(self.points) < self.target_points and count < max_attempts:
            count += 1
            rx = np.random.uniform(0, self.size_x)
            ry = np.random.uniform(0, self.size_y)
            rz = np.random.uniform(0, self.size_z)
            
            if np.random.random() < density_func(rx, ry, rz):
                self.points.append([rx, ry, rz])
        
        print(f"-> {count} denemede {len(self.points)} nokta")
        return np.array(self.points)
    
    def save_ply(self, filename):
        """PLY formatında kaydet - Stress-based coloring"""
        if not self.points:
            return
        
        pcd = o3d.geometry.PointCloud()
        pcd.points = o3d.utility.Vector3dVector(self.points)
        
        # 3D konuma göre renklendirme (XYZ bileşenleri)
        colors = []
        for p in self.points:
            r = p[0] / self.size_x  # X -> Red
            g = p[1] / self.size_y  # Y -> Green
            b = p[2] / self.size_z  # Z -> Blue
            colors.append([r, g, b])
        
        pcd.colors = o3d.utility.Vector3dVector(np.array(colors))
        
        os.makedirs("data/processed/advanced_3d", exist_ok=True)
        save_path = f"data/processed/advanced_3d/{filename}"
        o3d.io.write_point_cloud(save_path, pcd)
        print(f"Kaydedildi: {save_path}")

# --- ANA PROGRAM ---
if __name__ == "__main__":
    print("=" * 70)
    print("HAFTA 1 - GÜN 2 (İLERİ): Multi-Axis Density Functions")
    print("=" * 70)
    
    experiments = [
        ("cantilever_beam", "adv_cantilever_beam.ply"),
        ("compression_load", "adv_compression.ply"),
        ("torsion", "adv_torsion.ply"),
        ("bracket_realistic", "adv_bracket_realistic.ply"),
        ("multi_load_paths", "adv_multi_load.ply"),
    ]
    
    for func_name, filename in experiments:
        gen = AdvancedPointCloudGenerator(target_points=3000)
        gen.generate(func_name)
        gen.save_ply(filename)
    
    print("\n" + "=" * 70)
    print("İLERİ SEVİYE DENEMELER TAMAMLANDI!")
    print("Dosyalar: data/processed/advanced_3d/")
    print("=" * 70)
