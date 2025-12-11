import numpy as np
import open3d as o3d
import os

class PointCloudGenerator:
    """
    3D Uzayda Generative Design için Yoğunluk Bazlı Nokta Bulutu Oluşturucu.
    Ahmet Bey'in bahsettiği 'Point Cloud Processing'in ilk adımı.
    """
    def __init__(self, size_x=100, size_y=100, size_z=100, target_points=2000):
        self.size_x = size_x
        self.size_y = size_y
        self.size_z = size_z
        self.target_points = target_points
        self.points = []

    def _density_function(self, x):
        """
        2D'deki mantığın aynısı: X ekseni boyunca yoğunluk değişir.
        Sol taraf (x=0) yoğun, sağ taraf (x=size_x) seyrek.
        """
        norm_x = x / self.size_x
        # Olasılık sağa gittikçe azalır
        prob = 1.0 - (norm_x * 0.9) # 0.9 ile çarptım ki en sağda %10 şans kalsın, tamamen bitmesin
        return prob

    def generate(self):
        """Rejection Sampling ile 3D Noktalar üretir."""
        print("3D Nokta Bulutu üretiliyor...")
        count = 0
        while len(self.points) < self.target_points:
            # 3 Boyutlu Rastgele Nokta Adayı
            rx = np.random.uniform(0, self.size_x)
            ry = np.random.uniform(0, self.size_y)
            rz = np.random.uniform(0, self.size_z)
            
            # Sadece X eksenine göre karar veriyoruz (Şimdilik)
            if np.random.random() < self._density_function(rx):
                self.points.append([rx, ry, rz])
            
            count += 1
        
        print(f"-> {count} denemede {len(self.points)} nokta üretildi.")
        return np.array(self.points)

    def visualize(self):
        """Open3D kullanarak etkileşimli pencere açar."""
        if not self.points:
            print("Gösterilecek nokta yok!")
            return

        # Listeyi Open3D formatına çevir
        pcd = o3d.geometry.PointCloud()
        np_points = np.array(self.points)
        pcd.points = o3d.utility.Vector3dVector(np_points)

        # Görsellik: Noktaları renklendir (X eksenine göre renk değişsin)
        # Sol taraf (Yoğun) = Mavi, Sağ taraf (Seyrek) = Kırmızı
        colors = []
        for p in np_points:
            r = p[0] / self.size_x  # X arttıkça Kırmızı artar
            g = 0
            b = 1.0 - r             # X arttıkça Mavi azalır
            colors.append([r, g, b])
        
        pcd.colors = o3d.utility.Vector3dVector(np.array(colors))

        # Koordinat eksenini ekle (Referans için)
        mesh_frame = o3d.geometry.TriangleMesh.create_coordinate_frame(
            size=20, origin=[0, 0, 0])

        print("Pencere açılıyor... (Mouse ile çevirebilirsin)")
        o3d.visualization.draw_geometries([pcd, mesh_frame], window_name="Martur Staj - 3D Gradient Point Cloud")

# --- MAIN (SESSİZ MOD) ---
if __name__ == "__main__":
    print("1. İşlem Başlatılıyor...")
    
    # 1. ÜRET
    generator = PointCloudGenerator(target_points=5000)
    generator.generate()
    
    # 2. KAYDET
    # Klasör yoksa oluştur
    os.makedirs("data/processed", exist_ok=True)
    save_path = "data/processed/gradient_cloud.ply"
    
    print(f"2. Dosya hazırlanıyor: {save_path}")
    
    # Veriyi Open3D formatına çevir
    pcd = o3d.geometry.PointCloud()
    pcd.points = o3d.utility.Vector3dVector(generator.points)
    
    # Renkleri ekle (Mavi -> Kırmızı Gradient)
    colors = []
    for p in generator.points:
        # X koordinatına göre renk değiştir
        r = p[0] / generator.size_x
        colors.append([r, 0, 1.0 - r])
    
    pcd.colors = o3d.utility.Vector3dVector(np.array(colors))
    
    # Dosyayı diske yaz
    o3d.io.write_point_cloud(save_path, pcd)
    
    print("-" * 30)
    print(f"BAŞARILI! Dosya kaydedildi: {save_path}")
    print("Pencere açmaya çalışmadık, o yüzden hata almadın.")
    print("-" * 30)