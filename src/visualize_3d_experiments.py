import numpy as np
import open3d as o3d
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import os

"""
3D Point Cloud'ları matplotlib ile görselleştir (headless mode için)
"""

def visualize_point_cloud(ply_path, title):
    """PLY dosyasını oku ve 3D scatter plot oluştur"""
    # Open3D ile oku
    pcd = o3d.io.read_point_cloud(ply_path)
    points = np.asarray(pcd.points)
    colors = np.asarray(pcd.colors)
    
    # 3 farklı açıdan görsel oluştur
    fig = plt.figure(figsize=(18, 6))
    
    views = [
        (30, 45, 'Isometric View'),
        (0, 0, 'Front View (XY)'),
        (0, 90, 'Side View (XZ)'),
    ]
    
    for idx, (elev, azim, view_name) in enumerate(views, 1):
        ax = fig.add_subplot(1, 3, idx, projection='3d')
        
        # Scatter plot
        ax.scatter(points[:, 0], points[:, 1], points[:, 2], 
                  c=colors, s=1, alpha=0.6)
        
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')
        ax.set_title(f'{view_name}', fontsize=10)
        ax.view_init(elev=elev, azim=azim)
        
        # Aspect ratio
        max_range = 100
        ax.set_xlim([0, max_range])
        ax.set_ylim([0, max_range])
        ax.set_zlim([0, max_range])
    
    fig.suptitle(f'{title}\n(Total points: {len(points)})', 
                 fontsize=14, weight='bold')
    plt.tight_layout()
    
    # Kaydet
    output_name = os.path.basename(ply_path).replace('.ply', '_viz.png')
    output_path = f'data/processed/3d_experiments/{output_name}'
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    plt.close()
    
    print(f"✓ {output_name}")
    return output_path

if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("3D Point Cloud Görselleştirme")
    print("=" * 60 + "\n")
    
    experiments = [
        ('v1_3d_left_heavy.ply', 'V1: Left Heavy (Sol Yoğun)'),
        ('v2_3d_center_heavy.ply', 'V2: Center Heavy (Merkez Yoğun)'),
        ('v3_3d_xy_plane.ply', 'V3: XY Plane Stress (Düzlemsel)'),
        ('v4_3d_bottom_fixed.ply', 'V4: Bottom Fixed (Alt Sabit)'),
        ('v5_3d_four_corners.ply', 'V5: Four Corners (4 Köşe)'),
    ]
    
    for filename, title in experiments:
        ply_path = f'data/processed/3d_experiments/{filename}'
        if os.path.exists(ply_path):
            visualize_point_cloud(ply_path, title)
        else:
            print(f"✗ Dosya bulunamadı: {filename}")
    
    print("\n" + "=" * 60)
    print("Görselleştirmeler tamamlandı!")
    print("Konum: data/processed/3d_experiments/*_viz.png")
    print("=" * 60 + "\n")
