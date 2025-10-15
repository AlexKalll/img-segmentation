# User Guide

## Quick Start

- Open the live app: https://img-seg.streamlit.app/
- In the sidebar, pick an image source under "📷 Image Selection":
  - Sample Image: choose one of the built-in images
  - Upload Image: select a file (PNG, JPG, JPEG, TIFF, BMP, WEBP)
  - Image URL: paste a direct link to an image
- The main page will prompt you to run segmentation after choosing a new image.
- Click "Run Segmentation" to process and view results.

## Image Sources

- Sample Image: pick from curated examples (Coffee, Astronaut, Camera, etc.)
- Upload Image: files are processed locally in the session; large images will be resized to the configured max size
- Image URL: ensure the link points directly to an image (http/https)

## Parameters

- k (Threshold Constant): controls region merging sensitivity; higher → fewer, larger segments
- min_size (Minimum Region Size): enforces minimum segment size (in pixels)
- sigma (Gaussian Smoothing): pre-segmentation blur; higher reduces noise more

Use the sidebar "⚙️ Segmentation Parameters" section and submit to apply new values. Re-run segmentation to update results.

## Results

- Original vs Segmented Views: compare input and output
- Segment Analytics: count, distribution, and top-9 largest segments gallery
- Downloads: export segmented image (PNG) and analysis report (JSON)

## Tips

- Start with defaults (k≈50, min_size≈10, sigma≈0.8)
- Increase k for coarser segmentation; reduce for finer details
- Slightly increase sigma for noisy images
