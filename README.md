# Image Segmentation Studio (FH Edition)

A professional Streamlit application for interactive image segmentation using the Felzenszwalb-Huttenlocher algorithm.

## 🚀 Features

- **Interactive Image Segmentation**: Upload images or use built-in samples
- **Real-time Parameter Adjustment**: Adjust `k`, `min_size`, and `sigma` parameters
- **Visual Results**: Side-by-side comparison of original and segmented images
- **Segment Analysis**: Detailed statistics and top 9 largest segments gallery
- **Download Capabilities**: Export segmented images and analysis reports
- **Modern UI**: Dark theme with professional design
- **Parameter Comparison**: Compare results across different parameter values

## 🧩 Algorithm

The **Felzenszwalb-Huttenlocher algorithm** is a graph-based image segmentation method that:

- Treats pixels as nodes in a graph
- Creates edges based on color similarity between adjacent pixels
- Uses Union-Find data structure for efficient region merging
- Applies adaptive thresholding based on region size
- Includes optional Gaussian smoothing for noise reduction

## 📦 Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd img-segmentation
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**:
   ```bash
   streamlit run app/main.py
   ```

## 🎯 Usage

### Basic Usage

1. **Select Image Source**:
   - Choose from built-in sample images (Coffee, Astronaut, Camera, etc.)
   - Upload your own image file (PNG, JPG, JPEG, TIFF, BMP, WEBP)

2. **Adjust Parameters**:
   - **k (Threshold Constant)**: Controls region merging sensitivity
     - Higher values → fewer, larger segments
     - Lower values → more, smaller segments
     - Range: 10-500
   
   - **min_size (Minimum Region Size)**: Minimum pixels per segment
     - Prevents very small segments
     - Range: 0-200
   
   - **sigma (Gaussian Smoothing)**: Preprocessing blur amount
     - Reduces noise before segmentation
     - Range: 0.0-2.0

3. **Run Segmentation**: Click "🚀 Run Segmentation" button

4. **View Results**:
   - Original vs Segmented image comparison
   - Total segments count and statistics
   - Top 9 largest segments gallery
   - Detailed segment size distribution

5. **Download Results**:
   - Segmented image as PNG
   - Analysis report as JSON

### Quick Presets

- **Fine**: Many small segments (k=20, min_size=5, sigma=0.5)
- **Coarse**: Few large segments (k=200, min_size=50, sigma=1.2)

### Parameter Comparison

Enable comparison mode to test multiple parameter values and visualize the differences in segmentation results.

## 🏗️ Project Structure

```
img-segmentation/
├── app/                          # Streamlit application
│   ├── main.py                  # Main app entry point
│   └── components/              # UI components
│       ├── sidebar_controls.py # Parameter controls
│       └── display_utils.py    # Display utilities
├── src/                         # Core algorithm implementation
│   ├── fh_segmentation.py      # FH algorithm
│   ├── union_find.py           # Union-Find data structure
│   ├── image_utils.py          # Image processing utilities
│   └── visualization.py        # Visualization utilities
├── outputs/                     # Generated outputs
│   ├── segmented/              # Segmented images
│   ├── segments/               # Individual segments
│   └── metrics/               # Analysis reports
├── .streamlit/                 # Streamlit configuration
│   └── config.toml            # Theme and settings
├── requirements.txt            # Python dependencies
└── README.md                  # This file
```

## 🔧 Configuration

### Theme Customization

Edit `.streamlit/config.toml` to customize the app theme:

```toml
[theme]
base = "dark"
primaryColor = "#F63366"
backgroundColor = "#0E1117"
secondaryBackgroundColor = "#262730"
textColor = "#FAFAFA"
font = "monospace"
```

### Server Settings

Configure server settings in `.streamlit/config.toml`:

```toml
[server]
headless = true
port = 8501
enableCORS = false
```

## 🚀 Deployment

### Local Development

```bash
streamlit run app/main.py
```

### Streamlit Cloud

1. **Push to GitHub**:
   ```bash
   git init
   git add .
   git commit -m "Initial commit - FH Streamlit segmentation app"
   git branch -M main
   git remote add origin https://github.com/yourusername/img-segmentation.git
   git push -u origin main
   ```

2. **Deploy on Streamlit Cloud**:
   - Go to [streamlit.io/cloud](https://streamlit.io/cloud)
   - Click "Deploy"
   - Select your repository
   - Set entry point to `app/main.py`
   - Click "Deploy"

### Docker Deployment

Create a `Dockerfile`:

```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8501

CMD ["streamlit", "run", "app/main.py", "--server.address", "0.0.0.0"]
```

Build and run:

```bash
docker build -t img-segmentation .
docker run -p 8501:8501 img-segmentation
```

## 📊 Algorithm Parameters

| Parameter | Description | Range | Effect |
|-----------|-------------|-------|--------|
| `k` | Threshold constant | 10-500 | Higher = fewer segments |
| `min_size` | Minimum region size | 0-200 | Prevents tiny segments |
| `sigma` | Gaussian smoothing | 0.0-2.0 | Higher = more smoothing |

## 🎨 UI Features

- **Dark Theme**: Professional dark mode with accent color
- **Responsive Layout**: Adapts to different screen sizes
- **Progress Indicators**: Real-time processing feedback
- **Interactive Controls**: Sliders, buttons, and file uploads
- **Data Tables**: Structured display of segment information
- **Download Buttons**: Easy export of results

## 🔬 Technical Details

### Dependencies

- **Streamlit**: Web application framework
- **NumPy**: Numerical computations
- **Matplotlib**: Plotting and visualization
- **scikit-image**: Image processing algorithms
- **Pillow**: Image I/O operations
- **Requests**: HTTP requests for URL images

### Performance

- Optimized Union-Find with path compression
- Efficient graph construction for pixel adjacency
- Memory-efficient segment analysis
- Cached results for improved responsiveness

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- **Felzenszwalb & Huttenlocher**: Original algorithm authors
- **Streamlit Team**: For the amazing web framework
- **scikit-image**: For image processing utilities
- **Matplotlib**: For visualization capabilities

## 📞 Support

For questions, issues, or contributions, please:

1. Check the [Issues](https://github.com/yourusername/img-segmentation/issues) page
2. Create a new issue with detailed description
3. Contact the development team

---

**Image Segmentation Studio (FH Edition)** - Professional image segmentation made simple! 🧩✨