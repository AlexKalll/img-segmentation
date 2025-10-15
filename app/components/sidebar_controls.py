"""
Sidebar Controls Component for Image Segmentation Studio

This module provides interactive sidebar controls for the Streamlit app,
including parameter sliders, image upload, and sample selection.
"""

import streamlit as st
import numpy as np
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'src'))
from image_utils import load_sample_image, load_image_from_file, load_image_from_url, preprocess_image


def create_sidebar_controls():
    """
    Create the sidebar controls for the Streamlit app.
    
    Returns:
        dict: Dictionary containing all control values and uploaded image
    """
    st.sidebar.title("🎛️ Control Panel")
    st.sidebar.markdown(
        """
        <style>
        /* Move sidebar content further up */
        [data-testid="stSidebar"] section[data-testid="stSidebarContent"] { padding-top: 0rem; }
        </style>
        """,
        unsafe_allow_html=True
    )
    st.sidebar.markdown("---")
    
    # Initialize session state for all controls if not exists
    if 'controls_state' not in st.session_state:
        st.session_state.controls_state = {
            'image_source': "Sample Image",
            'sample_choice': "Coffee",
            'max_size': 512,
            'k': 50,
            'min_size': 10,
            'sigma': 0.8
        }
    
    # Image Selection Section (reactive)
    st.sidebar.subheader("📷 Image Selection")

    image_source = st.sidebar.radio(
        "Choose image source:",
        ["Sample Image", "Upload Image", "Image URL"],
        index=["Sample Image", "Upload Image", "Image URL"].index(st.session_state.controls_state['image_source']),
        help="Select whether to use a built-in sample, upload your own image, or load from URL"
    )

    uploaded_image = None
    selected_image = None
    image_key = None

    # Persist choice immediately
    st.session_state.controls_state['image_source'] = image_source

    if image_source == "Sample Image":
        sample_options = {
            "Coffee": "coffee",
            "Astronaut": "astronaut", 
            "Camera": "camera",
            "Coins": "coins",
            "Moon": "moon",
            "Rocket": "rocket"
        }
        
        sample_choice = st.sidebar.selectbox(
            "Select sample image:",
            list(sample_options.keys()),
            index=list(sample_options.keys()).index(st.session_state.controls_state['sample_choice']),
            help="Choose from available sample images"
        )

        st.session_state.controls_state['sample_choice'] = sample_choice
        
        try:
            selected_image = load_sample_image(sample_options[sample_choice])
            st.sidebar.success(f"✅ Loaded {sample_choice} sample")
        except Exception as e:
            st.sidebar.error(f"❌ Error loading sample: {e}")
            selected_image = load_sample_image()  # Fallback to coffee
        image_key = f"sample:{sample_choice}"
    
    elif image_source == "Upload Image":
        uploaded_file = st.sidebar.file_uploader(
            "Upload an image:",
            type=['png', 'jpg', 'jpeg', 'tiff', 'bmp', 'webp'],
            help="Upload an image file for segmentation"
        )
        
        if uploaded_file is not None:
            try:
                # Save uploaded file temporarily
                with open("temp_uploaded_image", "wb") as f:
                    f.write(uploaded_file.getbuffer())
                
                uploaded_image = load_image_from_file("temp_uploaded_image")
                selected_image = uploaded_image
                st.sidebar.success("✅ Image uploaded successfully")
                
            except Exception as e:
                st.sidebar.error(f"❌ Error loading uploaded image: {e}")
                selected_image = load_sample_image()  # Fallback
            # Build a stable-ish key from file metadata
            image_key = f"upload:{uploaded_file.name}:{uploaded_file.size}"
    
    else:  # Image URL
        image_url = st.sidebar.text_input(
            "Enter image URL:",
            placeholder="https://example.com/image.jpg",
            help="Enter a direct URL to an image file"
        )
        
        if image_url:
            try:
                # Validate URL format
                if not (image_url.startswith('http://') or image_url.startswith('https://')):
                    st.sidebar.error("❌ Please enter a valid URL starting with http:// or https://")
                    selected_image = load_sample_image()  # Fallback
                else:
                    # Load image from URL
                    uploaded_image = load_image_from_url(image_url)
                    selected_image = uploaded_image
                    st.sidebar.success("✅ Image loaded from URL successfully")
                    
            except Exception as e:
                st.sidebar.error(f"❌ Error loading image from URL: {e}")
                st.sidebar.info("💡 Make sure the URL points to a valid image file (jpg, png, etc.)")
                selected_image = load_sample_image()  # Fallback
            image_key = f"url:{image_url}"

    # Preprocessing Options
    st.sidebar.markdown("---")
    st.sidebar.subheader("🔧 Preprocessing")
    
    max_size = st.sidebar.slider(
        "Max image size:",
        min_value=256,
        max_value=1024,
        value=st.session_state.controls_state['max_size'],
        step=64,
        help="Resize image if larger than this size (maintains aspect ratio)"
    )
    st.session_state.controls_state['max_size'] = max_size
    
    if selected_image is not None:
        selected_image = preprocess_image(selected_image, max_size=max_size)
    
    # Segmentation Parameters Section
    st.sidebar.markdown("---")
    st.sidebar.subheader("⚙️ Segmentation Parameters")
    
    # Parameter explanations
    with st.sidebar.expander("ℹ️ Parameter Help"):
        st.markdown("""
        **k (Threshold Constant):**
        - Controls the sensitivity of region merging
        - Higher values → fewer, larger segments
        - Lower values → more, smaller segments
        - Range: 10-500
        
        **min_size (Minimum Region Size):**
        - Minimum number of pixels per segment
        - Prevents very small segments
        - Range: 0-200
        
        **sigma (Gaussian Smoothing):**
        - Preprocessing blur to reduce noise
        - Higher values → more smoothing
        - Range: 0.0-2.0
        """)
    
    # Parameter sliders
    k = st.sidebar.slider(
        "k (Threshold Constant):",
        min_value=10,
        max_value=500,
        value=st.session_state.controls_state['k'],
        step=10,
        help="Controls region merging sensitivity"
    )
    st.session_state.controls_state['k'] = k
    
    min_size = st.sidebar.slider(
        "min_size (Minimum Region Size):",
        min_value=0,
        max_value=200,
        value=st.session_state.controls_state['min_size'],
        step=5,
        help="Minimum pixels per segment"
    )
    st.session_state.controls_state['min_size'] = min_size
    
    sigma = st.sidebar.slider(
        "sigma (Gaussian Smoothing):",
        min_value=0.0,
        max_value=2.0,
        value=st.session_state.controls_state['sigma'],
        step=0.1,
        help="Preprocessing blur amount"
    )
    st.session_state.controls_state['sigma'] = sigma
    
    # Action Button
    st.sidebar.markdown("---")
    run_segmentation = st.sidebar.button(
        "🚀 Run Segmentation",
        type="primary",
        help="Execute the Felzenszwalb-Huttenlocher algorithm"
    )
    
    # Removed Current Settings display per request
    
    return {
        'selected_image': selected_image,
        'uploaded_image': uploaded_image,
        'image_key': image_key,
        'parameters': {
            'k': st.session_state.controls_state['k'],
            'min_size': st.session_state.controls_state['min_size'],
            'sigma': st.session_state.controls_state['sigma']
        },
        'run_segmentation': run_segmentation,
        'image_source': st.session_state.controls_state['image_source']
    }


def display_image_info(image):
    """
    Display information about the selected image in the sidebar.
    
    Args:
        image (numpy.ndarray): The image to analyze
    """
    if image is not None:
        st.sidebar.markdown("---")
        st.sidebar.subheader("📋 Image Info")
        
        height, width = image.shape[:2]
        is_color = image.ndim == 3
        channels = image.shape[2] if is_color else 1
        
        st.sidebar.write(f"**Dimensions:** {width} × {height}")
        st.sidebar.write(f"**Channels:** {channels}")
        st.sidebar.write(f"**Type:** {'Color' if is_color else 'Grayscale'}")
        st.sidebar.write(f"**Total Pixels:** {width * height:,}")


def create_parameter_comparison_controls():
    """
    Create controls for parameter comparison mode.
    
    Returns:
        dict: Comparison control values
    """
    st.sidebar.markdown("---")
    st.sidebar.subheader("🔬 Parameter Comparison")
    
    enable_comparison = st.sidebar.checkbox(
        "Enable comparison mode",
        help="Compare results across different parameter values"
    )
    
    if enable_comparison:
        param_to_vary = st.sidebar.selectbox(
            "Parameter to vary:",
            ["k", "min_size", "sigma"],
            help="Which parameter to vary for comparison"
        )
        
        if param_to_vary == "k":
            values = st.sidebar.multiselect(
                "k values:",
                [10, 25, 50, 100, 200, 300],
                default=[25, 50, 100],
                help="Select multiple k values to compare"
            )
        elif param_to_vary == "min_size":
            values = st.sidebar.multiselect(
                "min_size values:",
                [0, 5, 10, 25, 50, 100],
                default=[5, 10, 25],
                help="Select multiple min_size values to compare"
            )
        else:  # sigma
            values = st.sidebar.multiselect(
                "sigma values:",
                [0.0, 0.5, 0.8, 1.0, 1.5, 2.0],
                default=[0.5, 0.8, 1.0],
                help="Select multiple sigma values to compare"
            )
        
        return {
            'enable_comparison': enable_comparison,
            'param_to_vary': param_to_vary,
            'values': values
        }
    
    return {'enable_comparison': False}

