# DigitalIE 3D map

Serve this directory over HTTP, then open `index.html`:

```bash
cd visualization
python3 -m http.server 4178
```

The map uses Three.js from a CDN. Colored districts represent corpus planes; smaller nodes represent documents. Click a district or document to focus it, drag to orbit, scroll to zoom, and press `R` to reset the view.
