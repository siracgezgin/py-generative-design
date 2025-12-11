import numpy as np
import open3d as o3d
import os

"""
HAFTA 1 - GÜN 2: 3D Point Cloud Density Experiments
Hedef: 2D density function'ları 3D'ye genişlet
"""

class PointCloud3DGenerator:
    """3D Nokta Bulutu Üretici - Farklı Density Function'larla"""
    
    def __init__(self, size_x=100, size_y=100, size_z=100, target_points=2000):
        self.size_x = size_x
        self.size_y = size_y
        self.size_z = size_z
        self.target_points = target_points
        self.points = []
    
    # --- DENSITY FUNCTIONS (3D) ---
    
    def density_left_heavy(self, x, y, z):
        """Sadece X eksenine göre (orijinal)"""
        norm_x = x / self.size_x
        return 1.0 - (norm_x * 0.9)
    
    def density_center_heavy(self, x, y, z):
        """Merkeze olan 3D uzaklığa göre"""
        center_x = self.size_x / 2
        center_y = self.size_y / 2
        center_z = self.size_z / 2
        
        distance = np.sqrt(
            (x - center_x)**2 + 
            (y - center_y)**2 + 
            (z - center_z)**2
        )
        max_distance = np.sqrt(
            (self.size_x/2)**2 + 
            (self.size_y/2)**2 + 
            (self.size_z/2)**2
        )
        norm_distance = distance / max_distance
        
        prob = 1.0 - norm_distance * 0.85
        return max(0.1, prob)
    
    def density_xy_plane_stress(self, x, y, z):
        """
        Z yönünde uniform, XY düzleminde çapraz
        Use case: Düzlemsel kuvvet
        """
        norm_diagonal = (x + y) / (self.size_x + self.size_y)
        prob = 1.0 - norm_diagonal * 0.9
        return max(0.1, prob)
    
    def density_bottom_fixed(self, x, y, z):
        """
        Alt kısım sabit (z=0), yukarı çıktıkça azalan yoğunluk
        Use case: Yerden sabitlenen dikey yapı
        """
        norm_z = z / self.size_z
        prob = 1.0 - norm_z * 0.85
        return max(0.1, prob)
    
    def density_four_corners(self, x, y, z):
        """
        4 köşeye yakın bölgeler yoğun
        Use case: Çoklu sabitleme
        """
        corners = [
            (self.size_x * 0.2, self.size_y * 0.2, self.size_z * 0.5),
            (self.size_x * 0.8, self.size_y * 0.2, self.size_z * 0.5),
            (self.size_x * 0.2, self.size_y * 0.8, self.size_z * 0.5),
            (self.size_x * 0.8, self.size_y * 0.8, self.size_z * 0.5),
        ]
        
        distances = [
            np.sqrt((x - cx)**2 + (y - cy)**2 + (z - cz)**2) 
            for cx, cy, cz in corners
        ]
        min_distance = min(distances)
        max_possible = np.sqrt(
            self.size_x**2 + self.size_y**2 + self.size_z**2
        ) / 2
        
        norm_distance = min_distance / max_possible
        prob = 1.0 - norm_distance * 0.8
        return max(0.1, prob)
    
    # --- GENERATION ---
    
    def generate(self, density_function_name="left_heavy"):
        """Belirtilen density function ile nokta üret"""
        density_func = getattr(self, f"density_{density_function_name}")
        
        print(f"\n3D Point Cloud üretiliyor: {density_function_name}")
        print(f"Hedef: {self.target_points} nokta")
        
        self.points = []
        count = 0
        max_attempts = self.target_points * 100
        
        while len(self.points) < self.target_points and count < max_attempts:
            count += 1
            rx = np.random.uniform(0, self.size_x)
            ry = np.random.uniform(0, self.size_y)
            rz = np.random.uniform(0, self.size_z)
            
            if np.random.random() < density_func(rx, ry, rz):
                self.points.append([rx, ry, rz])
        
        print(f"-> {count} denemede {len(self.points)} nokta üretildi")
        return np.array(self.points)
    
    def save_ply(self, filename):
        """PLY formatında kaydet"""
        if not self.points:
            print("Kaydedilecek nokta yok!")
            return
        
        pcd = o3d.geometry.PointCloud()
        pcd.points = o3d.utility.Vector3dVector(self.points)
        
        # X eksenine göre renklendirme (mavi -> kırmızı)
        colors = []
        for p in self.points:
            r = p[0] / self.size_x
            colors.append([r, 0, 1.0 - r])
        
        pcd.colors = o3d.utility.Vector3dVector(np.array(colors))
        
        os.makedirs("data/processed/3d_experiments", exist_ok=True)
        save_path = f"data/processed/3d_experiments/{filename}"
        o3d.io.write_point_cloud(save_path, pcd)
        print(f"Kaydedildi: {save_path}")
        
        return save_path

# --- ANA PROGRAM ---
if __name__ == "__main__":
    print("=" * 70)
    print("HAFTA 1 - GÜN 2: 3D Point Cloud Density Experiments")
    print("=" * 70)
    
    experiments = [
        ("left_heavy", "v1_3d_left_heavy.ply"),
        ("center_heavy", "v2_3d_center_heavy.ply"),
        ("xy_plane_stress", "v3_3d_xy_plane.ply"),
        ("bottom_fixed", "v4_3d_bottom_fixed.ply"),
        ("four_corners", "v5_3d_four_corners.ply"),
    ]
    
    for func_name, filename in experiments:
        generator = PointCloud3DGenerator(target_points=3000)
        generator.generate(func_name)
        generator.save_ply(filename)
    
    print("\n" + "=" * 70)
    print("TÜM 3D DENEMELER TAMAMLANDI!")
    print("Dosyalar: data/processed/3d_experiments/")
    print("\nOpen3D ile görüntüle:")
    print("  python -c \"import open3d as o3d; o3d.visualization.draw_geometries([o3d.io.read_point_cloud('data/processed/3d_experiments/v1_3d_left_heavy.ply')])\"")
    print("=" * 70)
