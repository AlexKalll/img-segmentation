# Image Segmentation Studio (FH Edition)
Welcome to  the Image Segmentation Studio.
### Overview

Image Segmentation Studio is a Streamlit application for interactive image segmentation using the Felzenszwalb–Huttenlocher (FH) algorithm with the ease of Union-find data structure. 
It supports multiple image sources, real-time parameter tuning, rich visualization, and downloadable results.
- Core explanatory file: [The Interactive Jupyter Notebook ](https://github.com/AlexKalll/img-segmentation/blob/main/notebooks/fh-impl-final.ipynb) 

### Core Features

- Interactive segmentation with parameter controls (`k`, `min_size`, `sigma`)
- Image sources: samples, file upload, or URL
- Segment analysis and gallery of largest regions
- Side-by-side original vs segmented views
- Download of images and analysis data


### Technologies

- **Streamlit**: Web application framework
- **NumPy**: Numerical computations
- **Matplotlib**: Plotting and visualization
- **scikit-image**: Image processing algorithms
- **Requests**: HTTP requests for URL images

The Felzenszwalb–Huttenlocher (FH) algorithm has been implemented with the ease of Union-find data structure.