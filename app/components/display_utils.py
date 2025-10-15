"""
Display Utilities for Image Segmentation Studio

This module provides utilities for displaying results in the Streamlit app,
including image galleries, metrics, and download functionality.
"""

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import json
import os
import sys
from datetime import datetime
import base64
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'src'))
from image_utils import image_to_bytes, save_image
from visualization import (
    create_segmentation_comparison, 
    create_segment_gallery,
    create_segment_size_histogram,
    generate_segmentation_report
)


class NumpyEncoder(json.JSONEncoder):
    """Custom JSON encoder to handle NumPy data types."""
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        return super(NumpyEncoder, self).default(obj)


def display_segmentation_results(original_image, segmented_image, analysis_results, parameters):
    """
    Display the main segmentation results.
    
    Args:
        original_image (numpy.ndarray): Original input image
        segmented_image (numpy.ndarray): Segmented image
        analysis_results (dict): Analysis results from segmentation
        parameters (dict): Parameters used for segmentation
    """
    st.subheader("🎯 Segmentation Results")
    
    # Create comparison plot
    fig = create_segmentation_comparison(
        original_image, 
        segmented_image,
        ["Original Image", f"Segmented (k={parameters['k']}, min_size={parameters['min_size']}, sigma={parameters['sigma']})"]
    )
    
    st.pyplot(fig)
    plt.close(fig)
    
    # Display metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="Total Segments",
            value=analysis_results['total_segments']
        )
    
    with col2:
        total_pixels = sum(analysis_results['component_sizes'].values())
        st.metric(
            label="Total Pixels",
            value=f"{total_pixels:,}"
        )
    
    with col3:
        mean_size = np.mean(list(analysis_results['component_sizes'].values()))
        st.metric(
            label="Mean Segment Size",
            value=f"{mean_size:.1f}"
        )
    
    with col4:
        max_size = max(analysis_results['component_sizes'].values())
        st.metric(
            label="Largest Segment",
            value=f"{max_size:,}"
        )


def display_segment_gallery(analysis_results):
    """
    Display a gallery of the largest segments.
    
    Args:
        analysis_results (dict): Analysis results containing segments
    """
    st.subheader("🖼️ Top Segments Gallery")
    
    segments = analysis_results['largest_segments']
    segment_info = analysis_results['segment_info']
    
    if segments:
        # Create gallery figure
        fig = create_segment_gallery(
            segments[0],  # Use first segment as reference for dimensions
            segments,
            segment_info,
            grid_size=(3, 3)
        )
        
        st.pyplot(fig)
        plt.close(fig)
        
        # Display segment information in a table
        st.subheader("📊 Segment Information")
        
        segment_data = []
        for info in segment_info:
            segment_data.append({
                "Segment ID": info['id'],
                "Size (pixels)": f"{info['size']:,}",
                "Percentage": f"{(info['size'] / sum(analysis_results['component_sizes'].values())) * 100:.2f}%"
            })
        
        st.dataframe(segment_data, use_container_width=True)
    else:
        st.warning("No segments found to display.")


def display_segment_statistics(analysis_results):
    """
    Display detailed statistics about the segmentation.
    
    Args:
        analysis_results (dict): Analysis results from segmentation
    """
    st.subheader("📈 Segmentation Statistics")
    
    component_sizes = analysis_results['component_sizes']
    sizes = list(component_sizes.values())
    
    # Create histogram
    fig = create_segment_size_histogram(component_sizes)
    st.pyplot(fig)
    plt.close(fig)
    
    # Display statistics
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Size Statistics:**")
        st.write(f"• Mean: {np.mean(sizes):.1f} pixels")
        st.write(f"• Median: {np.median(sizes):.1f} pixels")
        st.write(f"• Standard Deviation: {np.std(sizes):.1f} pixels")
        st.write(f"• Minimum: {np.min(sizes):,} pixels")
        st.write(f"• Maximum: {np.max(sizes):,} pixels")
    
    with col2:
        st.markdown("**Distribution:**")
        st.write(f"• Total Segments: {len(sizes)}")
        st.write(f"• Single-pixel Segments: {sum(1 for s in sizes if s == 1)}")
        st.write(f"• Large Segments (>1000px): {sum(1 for s in sizes if s > 1000)}")
        st.write(f"• Very Large Segments (>5000px): {sum(1 for s in sizes if s > 5000)}")


def create_download_section(segmented_image, analysis_results, parameters):
    """
    Create download section for results.
    
    Args:
        segmented_image (numpy.ndarray): Segmented image
        analysis_results (dict): Analysis results
        parameters (dict): Parameters used
    """
    st.subheader("💾 Download Results")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Download segmented image
        if segmented_image is not None:
            image_bytes = image_to_bytes(segmented_image, format='PNG')
            file_name = f"segmented_image_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
            b64_image = base64.b64encode(image_bytes).decode()
            href_image = f"data:image/png;base64,{b64_image}"
            st.markdown(
                f"<a href=\"{href_image}\" download=\"{file_name}\"><button style='width:100%'>📥 Download Segmented Image</button></a>",
                unsafe_allow_html=True
            )
    
    with col2:
        # Download JSON report
        report = generate_segmentation_report(analysis_results, parameters)
        report_json = json.dumps(report, indent=2, cls=NumpyEncoder)
        
        report_file_name = f"segmentation_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        report_bytes = report_json.encode('utf-8')
        b64_report = base64.b64encode(report_bytes).decode()
        href_report = f"data:application/json;base64,{b64_report}"
        st.markdown(
            f"<a href=\"{href_report}\" download=\"{report_file_name}\"><button style='width:100%'>📊 Download Analysis Report</button></a>",
            unsafe_allow_html=True
        )


def display_parameter_comparison(comparison_results):
    """
    Display results from parameter comparison.
    
    Args:
        comparison_results (list): List of analysis results for different parameters
    """
    st.subheader("🔬 Parameter Comparison Results")
    
    if not comparison_results:
        st.warning("No comparison results available.")
        return
    
    # Create comparison table
    comparison_data = []
    for result in comparison_results:
        params = result['parameters']
        stats = result['statistics']
        
        comparison_data.append({
            "k": params['k'],
            "min_size": params['min_size'],
            "sigma": params['sigma'],
            "Total Segments": result['total_segments'],
            "Mean Size": f"{stats['mean_size']:.1f}",
            "Std Size": f"{stats['std_size']:.1f}",
            "Min Size": stats['min_size'],
            "Max Size": stats['max_size']
        })
    
    st.dataframe(comparison_data, use_container_width=True)
    
    # Create comparison plots
    from visualization import create_parameter_comparison_plot
    
    # Determine which parameter was varied
    param_names = ['k', 'min_size', 'sigma']
    varied_param = None
    
    for param in param_names:
        values = [r['parameters'][param] for r in comparison_results]
        if len(set(values)) > 1:
            varied_param = param
            break
    
    if varied_param:
        fig = create_parameter_comparison_plot(comparison_results, varied_param)
        st.pyplot(fig)
        plt.close(fig)


def display_processing_progress():
    """
    Display a progress indicator during processing.
    """
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    return progress_bar, status_text


def update_progress(progress_bar, status_text, progress, message):
    """
    Update the progress indicator.
    
    Args:
        progress_bar: Streamlit progress bar
        status_text: Streamlit empty container for status
        progress (float): Progress value (0-1)
        message (str): Status message
    """
    progress_bar.progress(progress)
    status_text.text(message)


def display_app_header():
    """
    Display the main app header and description.
    """
    st.title("🧩 Image Segmentation Studio (FH Edition)")
    st.markdown("""
    **Professional image segmentation using the Felzenszwalb-Huttenlocher algorithm**
    
    Upload an image or choose a sample, adjust parameters interactively, and visualize 
    segmentation results with detailed analysis and downloadable outputs.
    """)
    
    st.markdown("---")


def display_algorithm_info():
    """
    Display information about the Felzenszwalb-Huttenlocher algorithm.
    """
    with st.expander("ℹ️ About the Felzenszwalb-Huttenlocher Algorithm"):
        st.markdown("""
        The **Felzenszwalb-Huttenlocher algorithm** is a graph-based image segmentation 
        method that efficiently segments images by treating pixels as nodes in a graph 
        and merging regions based on similarity criteria.
        
        **Key Features:**
        - **Graph-based approach**: Treats pixels as nodes with edges based on color similarity
        - **Efficient merging**: Uses Union-Find data structure for fast region merging
        - **Adaptive thresholding**: Dynamic threshold based on region size
        - **Noise reduction**: Optional Gaussian smoothing preprocessing
        
        **Parameters:**
        - **k**: Controls the sensitivity of region merging
        - **min_size**: Minimum number of pixels per segment
        - **sigma**: Gaussian smoothing parameter for noise reduction
        
        **Applications:**
        - Object detection preprocessing
        - Image analysis and computer vision
        - Medical image segmentation
        - Satellite image analysis
        """)


def create_sidebar_footer():
    """
    Create a footer for the sidebar with app information.
    """
    st.sidebar.markdown("---")
    st.sidebar.markdown("""
    **Image Segmentation Studio**  
    *FH Edition v1.0*
    
    Built with ❤️ using Streamlit
    """)

