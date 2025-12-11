# Copilot Instructions for py-generative-design

## Project Overview
This is a **generative design** project for structural optimization using density-based point clouds and Voronoi tessellation. The core concept: generate non-uniform point distributions where density reflects structural stress (dense points = high stress areas, sparse points = low stress areas).

## Architecture & Data Flow

### Two-Stage Generation Pipeline
1. **Point Cloud Generation** (`src/point_cloud_generator.py`): Creates 3D point clouds using rejection sampling
   - `PointCloudGenerator` class handles density-based distribution
   - Output: `.ply` files in `data/processed/`
2. **Voronoi Tessellation** (`src/voronoi_generator.py`): 2D Voronoi diagrams for visualization
   - Script-based (not class-based)
   - Output: `.png` visualizations in `data/processed/`

### Density Function Pattern
Both generators use **rejection sampling** with a left-to-right density gradient:
```python
# Left side (x=0): High density/stress → probability ≈ 1.0
# Right side (x=max): Low density/stress → probability ≈ 0.1
prob = 1.0 - (normalized_x * 0.9)
```

## Key Dependencies
- **Open3D**: 3D point cloud I/O, visualization (`.ply` format)
- **NumPy/SciPy**: Numerical computation, Voronoi algorithms
- **Matplotlib**: 2D visualization only

## Critical Conventions

### Language & Comments
Code uses **Turkish** for variable names and inline comments (e.g., `hedef_nokta_sayisi`, `kabul_edilen_noktalar`). This is intentional - maintain this convention when editing existing code.

### Execution Patterns
- **Headless execution by default**: Scripts save to disk but don't open GUI windows to avoid display errors
- **Main blocks are standalone**: Both generators have `if __name__ == "__main__"` blocks that run end-to-end pipelines
- Run directly: `python src/point_cloud_generator.py` or `python src/voronoi_generator.py`

### File Output
- All generated files go to `data/processed/` (created automatically with `os.makedirs(..., exist_ok=True)`)
- Point clouds: `.ply` format with RGB color gradients (blue→red based on X-coordinate)
- Visualizations: `.png` format

## Development Workflow

### Environment Setup
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Running Generators
```bash
# 3D point cloud generation
python src/point_cloud_generator.py

# 2D Voronoi visualization
python src/voronoi_generator.py
```

### Visualization (Interactive Mode)
To use `PointCloudGenerator.visualize()`, call it explicitly (not included in main block to prevent display errors):
```python
generator = PointCloudGenerator(target_points=5000)
generator.generate()
generator.visualize()  # Opens Open3D GUI window
```

## Code Patterns to Follow

### Color Gradients
Use X-axis normalized color mapping for visual density indication:
```python
colors = []
for p in points:
    r = p[0] / max_x  # Red increases with X
    colors.append([r, 0, 1.0 - r])  # Blue decreases with X
```

### Rejection Sampling Loop
Standard pattern across generators:
```python
while len(accepted_points) < target_count:
    candidate = random_point()
    if random() < density_function(candidate):
        accepted_points.append(candidate)
```

## Project Structure Notes
- `src/models/`: Empty (reserved for future ML models)
- `src/utils/`: Empty (reserved for shared utilities)
- `tests/`: Empty (no test suite yet)
- `notebooks/`: Empty (reserved for Jupyter experiments)

## Future Extension Points
- Extend density functions to consider Y/Z coordinates (currently X-axis only)
- Add stress field input mechanisms (load force vector data)
- Implement 3D Voronoi tessellation using Open3D
- Create parametric density function library for different structural scenarios
