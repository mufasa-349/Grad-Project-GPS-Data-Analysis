# GNSS Fix visualization (Leaflet + D3)

Interactive browser tools for Android GNSS Logger `Fix` lines: map view, heatmaps, and uncertainty rings. Sample datasets live under `data/`.

## Live demo (GitHub Pages)

Open the main map app directly in the browser (no local clone or server needed for the page itself):

**[https://mufasa-349.github.io/Grad-Project-GPS-Data-Analysis/gnss_tuzla_map_interactive.html](https://mufasa-349.github.io/Grad-Project-GPS-Data-Analysis/gnss_tuzla_map_interactive.html)**

> The bundled `data/*.txt` files are loaded with relative URLs; they work when the site is served from GitHub Pages at that path. For offline development or custom data, use a local server (below).

## Run locally (development)

Opening `gnss_tuzla_map_interactive.html` via `file://` often blocks `fetch()` for data files. Use a simple HTTP server from the **project root**:

```bash
cd /path/to/Grad-Project-GPS-Data-Analysis
python3 -m http.server 8000
```

If port `8000` is already in use, pick another port (e.g. `8001`):

```bash
python3 -m http.server 8001
```

Then open in your browser (adjust host/port if needed):

- **Main map app:** [http://127.0.0.1:8000/gnss_tuzla_map_interactive.html](http://127.0.0.1:8000/gnss_tuzla_map_interactive.html)  
  Example with port `8001`: [http://127.0.0.1:8001/gnss_tuzla_map_interactive.html](http://127.0.0.1:8001/gnss_tuzla_map_interactive.html)

- **Longitude vs altitude scatter (optional):** [http://127.0.0.1:8000/viz/fix_lon_alt_scatter.html](http://127.0.0.1:8000/viz/fix_lon_alt_scatter.html)

Map tiles (OpenStreetMap) need **internet** unless you replace the tile layer.

## Data and helpers

- **`data/`** — GNSS log `.txt` files (including `*_FixOnly.txt`).
- **`helpers/python/extract_fix_only.py`** — Extract lines starting with `Fix,` into a `*_FixOnly.txt` file:

  ```bash
  python3 helpers/python/extract_fix_only.py "data/your_log.txt"
  ```

## How to use (in-app)

The same text appears in the **ⓘ How to use** dialog on `gnss_tuzla_map_interactive.html`. On first visit from `localhost` or `127.0.0.1`, the dialog may open once; use **ⓘ** anytime to reopen it.

- **Data source** — Chooses which FixOnly / combined file to load. Changing it reloads the data automatically.
- **Reload selected file** — Re-reads the currently selected file (refresh).
- **Visualization method**
  - *Original* — Individual points (colored by distance from the first fix).
  - *Heat Map our idea* — Blue grid / density heatmap (stationary datasets) or route + hover preview when the path moves enough.
  - *Heat Map (Blue-Green-Red)* — Soft heatmap-style density with a blue → green → red scale.
  - *GPS Uncertainty (rings + color)* — Semi-transparent circles sized by horizontal accuracy (`AccuracyMeters`), color from good (green) to poor (red); center dot size reflects vertical accuracy (`VerticalAccuracyMeters`).
- **Heatmap cell size** — Grid cell size for the blue **Heat Map our idea** mode (larger = more blocky).
- **Moving routes** — If the distance between the **first and last** fix is **greater than 30 m**, the track is shown as a **dark red line**. Moving the mouse near the line shows a preview for the **i±7** window (circle + heat). **Current preview radius** is that circle’s radius in meters.
- **Local server** — Use `python3 -m http.server` so the browser can load files from `data/`; map tiles still need network access.
