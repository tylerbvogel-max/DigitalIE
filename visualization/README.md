# DigitalIE factory campus

Serve this directory over HTTP, then open `index.html`:

```bash
cd visualization
python3 -m http.server 4178
```

The map uses Three.js from a CDN. Buildings represent corpus planes; animated colored payloads trace architectural control, evidence, and learning paths. Click a building to inspect its role and cited DigitalIE source files, drag to orbit, scroll to zoom, and press `R` to reset the view.
