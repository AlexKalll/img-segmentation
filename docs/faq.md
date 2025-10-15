# FAQ

## Can I use the app without installing anything?
Yes. Use the live app at https://img-seg.streamlit.app/

## What image formats are supported?
PNG, JPG, JPEG, TIFF, BMP, and WEBP.

## Why don’t results update when I change the image source?
After selecting a new image (sample, upload, or URL), the main page shows a Run Segmentation button to generate fresh results.

## How do I download the results?
Use the download buttons under the results to save the segmented image (PNG) and a JSON analysis report.

## What do the parameters mean?
- k: controls merge sensitivity (higher → fewer segments)
- min_size: enforces minimum segment size
- sigma: pre-segmentation smoothing

## Is there a dark mode?
Yes. The app ships with a dark theme configured in `.streamlit/config.toml`.
