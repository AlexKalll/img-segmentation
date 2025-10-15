"""
Image Segmentation Studio (FH Edition) - Main Streamlit App

This is the main entry point for the Streamlit application that provides
an interactive interface for the Felzenszwalb-Huttenlocher image segmentation algorithm.
"""

import streamlit as st
import numpy as np
import os
import sys
from datetime import datetime

# Add src directory to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

# Import our custom modules
from fh_segmentation import felzenszwalb_huttenlocher, analyze_segments
from components.sidebar_controls import create_sidebar_controls, display_image_info
from components.display_utils import (
    display_app_header, 
    display_algorithm_info,
    display_segmentation_results,
    display_segment_gallery,
    display_segment_statistics,
    create_download_section,
    display_parameter_comparison,
    display_processing_progress,
    update_progress,
    create_sidebar_footer
)


def main():
    """
    Main function to run the Streamlit app.
    """
    # Configure page
    st.set_page_config(
        page_title="Image Segmentation Studio",
        page_icon="🧩",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Display header
    display_app_header()
    
    # Create sidebar controls
    controls = create_sidebar_controls()
    current_image_key = controls.get('image_key')
    
    # Display image information
    if controls['selected_image'] is not None:
        display_image_info(controls['selected_image'])
    
    # Create sidebar footer
    create_sidebar_footer()
    
    # Main content area
    if controls['selected_image'] is None:
        st.warning("⚠️ Please select, upload or enter an image URL to begin segmentation.")
        display_algorithm_info()
        return
    
    # Display algorithm info
    display_algorithm_info()
    
    # Determine whether cached results match current image
    cached_ok = False
    if 'segmentation_results' in st.session_state and current_image_key:
        cached_ok = st.session_state['segmentation_results'].get('image_key') == current_image_key

    # If user changed/added a new image source, prompt to run instead of showing old results
    if not cached_ok:
        prompt_placeholder = st.empty()
        with prompt_placeholder.container():
            if  not controls['run_segmentation']:
                st.info("A new image is selected. Run segmentation to generate fresh results.")
            body_run = st.button("🚀 Run Segmentation", type="primary", use_container_width=True)
        if body_run or controls['run_segmentation']:
            # Clear the prompt so the button/text are removed when results render
            prompt_placeholder.empty()
            run_segmentation_analysis(controls)
        return
    
    # If cached results are valid and no new run requested, show them
    if controls['run_segmentation']:
        run_segmentation_analysis(controls)
    else:
        display_cached_results()


def run_segmentation_analysis(controls):
    """
    Run the segmentation analysis with progress indication.
    
    Args:
        controls (dict): Control values from sidebar
    """
    selected_image = controls['selected_image']
    parameters = controls['parameters']
    image_key = controls.get('image_key')
    
    # Create progress indicators
    progress_bar, status_text = display_processing_progress()
    
    try:
        # Step 1: Preprocessing
        update_progress(progress_bar, status_text, 0.2, "🔄 Preprocessing image...")
        
        # Step 2: Segmentation
        update_progress(progress_bar, status_text, 0.5, "🧩 Running Felzenszwalb-Huttenlocher algorithm...")
        
        segmented_image, num_segments, union_find_obj = felzenszwalb_huttenlocher(
            selected_image,
            k=parameters['k'],
            min_size=parameters['min_size'],
            sigma=parameters['sigma']
        )
        
        # Step 3: Analysis
        update_progress(progress_bar, status_text, 0.8, "📊 Analyzing segments...")
        
        analysis_results = analyze_segments(selected_image, union_find_obj, top_n=9)
        
        # Step 4: Complete
        update_progress(progress_bar, status_text, 1.0, "✅ Segmentation complete!")
        
        # Store results in session state
        st.session_state['segmentation_results'] = {
            'original_image': selected_image,
            'segmented_image': segmented_image,
            'analysis_results': analysis_results,
            'parameters': parameters,
            'timestamp': datetime.now(),
            'image_key': image_key
        }
        
        # Clear progress indicators
        progress_bar.empty()
        status_text.empty()
        
        # Display results
        display_segmentation_results(
            selected_image,
            segmented_image,
            analysis_results,
            parameters
        )
        
        display_segment_gallery(analysis_results)
        
        display_segment_statistics(analysis_results)
        
        create_download_section(
            segmented_image,
            analysis_results,
            parameters
        )
        
    except Exception as e:
        progress_bar.empty()
        status_text.empty()
        st.error(f"❌ Error during segmentation: {str(e)}")
        st.exception(e)


def display_cached_results():
    """
    Display cached segmentation results from session state.
    """
    results = st.session_state['segmentation_results']
    
    # Check if results are recent (within last hour)
    time_diff = datetime.now() - results['timestamp']
    if time_diff.total_seconds() > 3600:  # 1 hour
        st.warning("⚠️ Results are older than 1 hour. Consider re-running segmentation.")
    
    st.info(f"📅 Results from: {results['timestamp'].strftime('%Y-%m-%d %H:%M:%S')}")
    
    display_segmentation_results(
        results['original_image'],
        results['segmented_image'],
        results['analysis_results'],
        results['parameters']
    )
    
    display_segment_gallery(results['analysis_results'])
    
    display_segment_statistics(results['analysis_results'])
    
    create_download_section(
        results['segmented_image'],
        results['analysis_results'],
        results['parameters']
    )


def run_parameter_comparison(controls, comparison_controls):
    """
    Run parameter comparison analysis.
    
    Args:
        controls (dict): Main control values
        comparison_controls (dict): Comparison control values
    """
    if not comparison_controls['enable_comparison']:
        return
    
    selected_image = controls['selected_image']
    base_parameters = controls['parameters']
    param_to_vary = comparison_controls['param_to_vary']
    values = comparison_controls['values']
    
    if not values:
        st.warning("Please select values for parameter comparison.")
        return
    
    st.subheader("🔬 Parameter Comparison Analysis")
    
    comparison_results = []
    progress_bar, status_text = display_processing_progress()
    
    try:
        for i, value in enumerate(values):
            # Update parameters
            test_parameters = base_parameters.copy()
            test_parameters[param_to_vary] = value
            
            # Update progress
            progress = (i + 1) / len(values)
            update_progress(
                progress_bar, 
                status_text, 
                progress, 
                f"🔄 Testing {param_to_vary}={value}..."
            )
            
            # Run segmentation
            segmented_image, num_segments, union_find_obj = felzenszwalb_huttenlocher(
                selected_image,
                k=test_parameters['k'],
                min_size=test_parameters['min_size'],
                sigma=test_parameters['sigma']
            )
            
            # Analyze results
            analysis_results = analyze_segments(selected_image, union_find_obj)
            
            # Generate report
            from visualization import generate_segmentation_report
            report = generate_segmentation_report(analysis_results, test_parameters)
            
            comparison_results.append(report)
        
        # Clear progress
        progress_bar.empty()
        status_text.empty()
        
        # Display comparison results
        display_parameter_comparison(comparison_results)
        
    except Exception as e:
        progress_bar.empty()
        status_text.empty()
        st.error(f"❌ Error during parameter comparison: {str(e)}")


if __name__ == "__main__":
    main()

