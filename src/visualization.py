"""
Visualization Utilities for Image Segmentation Studio

This module provides utilities for visualizing segmentation results,
creating segment galleries, and generating analysis plots.
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.colors import ListedColormap
import json
from typing import List, Dict, Tuple


def create_segment_gallery(original_image, segments, segment_info, grid_size=(3, 3)):
    """
    Create a gallery of the largest segments.
    
    Args:
        original_image (numpy.ndarray): Original input image
        segments (list): List of segment images
        segment_info (list): List of segment information dictionaries
        grid_size (tuple): Size of the gallery grid (rows, cols)
        
    Returns:
        matplotlib.figure.Figure: Figure containing the gallery
    """
    rows, cols = grid_size
    fig, axes = plt.subplots(rows, cols, figsize=(12, 12))
    
    if rows == 1:
        axes = [axes]
    if cols == 1:
        axes = [[ax] for ax in axes]
    
    for i in range(rows):
        for j in range(cols):
            idx = i * cols + j
            
            if idx < len(segments):
                segment = segments[idx]
                info = segment_info[idx]
                
                ax = axes[i][j] if rows > 1 else axes[j]
                
                if segment.ndim == 2:
                    ax.imshow(segment, cmap='gray')
                else:
                    ax.imshow(segment)
                
                ax.set_title(f"Segment {info['id']}\nSize: {info['size']} pixels", 
                           fontsize=10, pad=5)
                ax.axis('off')
            else:
                ax = axes[i][j] if rows > 1 else axes[j]
                ax.axis('off')
    
    plt.tight_layout()
    return fig


def create_segmentation_comparison(original_image, segmented_image, titles=None):
    """
    Create a side-by-side comparison of original and segmented images.
    
    Args:
        original_image (numpy.ndarray): Original input image
        segmented_image (numpy.ndarray): Segmented image
        titles (list): Titles for the images
        
    Returns:
        matplotlib.figure.Figure: Figure containing the comparison
    """
    if titles is None:
        titles = ["Original Image", "Segmented Image"]
    
    fig, axes = plt.subplots(1, 2, figsize=(15, 7))
    
    # Original image
    if original_image.ndim == 2:
        axes[0].imshow(original_image, cmap='gray')
    else:
        axes[0].imshow(original_image)
    axes[0].set_title(titles[0], fontsize=14, pad=10)
    axes[0].axis('off')
    
    # Segmented image
    if segmented_image.ndim == 2:
        axes[1].imshow(segmented_image, cmap='gray')
    else:
        axes[1].imshow(segmented_image)
    axes[1].set_title(titles[1], fontsize=14, pad=10)
    axes[1].axis('off')
    
    plt.tight_layout()
    return fig


def create_segment_size_histogram(component_sizes, bins=20):
    """
    Create a histogram showing the distribution of segment sizes.
    
    Args:
        component_sizes (dict): Dictionary mapping component roots to sizes
        bins (int): Number of bins for the histogram
        
    Returns:
        matplotlib.figure.Figure: Figure containing the histogram
    """
    sizes = list(component_sizes.values())
    
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.hist(sizes, bins=bins, alpha=0.7, color='#F63366', edgecolor='black')
    ax.set_xlabel('Segment Size (pixels)', fontsize=12)
    ax.set_ylabel('Number of Segments', fontsize=12)
    ax.set_title('Distribution of Segment Sizes', fontsize=14, pad=10)
    ax.grid(True, alpha=0.3)
    
    # Add statistics
    mean_size = np.mean(sizes)
    median_size = np.median(sizes)
    ax.axvline(mean_size, color='red', linestyle='--', alpha=0.8, label=f'Mean: {mean_size:.1f}')
    ax.axvline(median_size, color='green', linestyle='--', alpha=0.8, label=f'Median: {median_size:.1f}')
    ax.legend()
    
    plt.tight_layout()
    return fig


def create_segment_overlay(original_image, segment_mask, alpha=0.5, color='red'):
    """
    Create an overlay visualization showing a specific segment on the original image.
    
    Args:
        original_image (numpy.ndarray): Original input image
        segment_mask (numpy.ndarray): Boolean mask for the segment
        alpha (float): Transparency of the overlay
        color (str): Color for the overlay
        
    Returns:
        matplotlib.figure.Figure: Figure containing the overlay
    """
    fig, ax = plt.subplots(figsize=(10, 8))
    
    # Display original image
    if original_image.ndim == 2:
        ax.imshow(original_image, cmap='gray')
    else:
        ax.imshow(original_image)
    
    # Create colored overlay for the segment
    overlay = np.zeros((*original_image.shape[:2], 4))
    overlay[:, :, 0] = segment_mask  # Red channel
    overlay[:, :, 3] = segment_mask * alpha  # Alpha channel
    
    ax.imshow(overlay)
    ax.set_title('Segment Overlay', fontsize=14, pad=10)
    ax.axis('off')
    
    plt.tight_layout()
    return fig


def generate_segmentation_report(analysis_results, parameters):
    """
    Generate a comprehensive segmentation report.
    
    Args:
        analysis_results (dict): Results from analyze_segments function
        parameters (dict): Segmentation parameters used
        
    Returns:
        dict: Report data
    """
    component_sizes = analysis_results['component_sizes']
    sizes = list(component_sizes.values())
    
    report = {
        'parameters': {
            'k': float(parameters['k']),
            'min_size': int(parameters['min_size']),
            'sigma': float(parameters['sigma'])
        },
        'total_segments': int(analysis_results['total_segments']),
        'total_pixels': int(sum(sizes)),
        'statistics': {
            'mean_size': float(np.mean(sizes)),
            'median_size': float(np.median(sizes)),
            'std_size': float(np.std(sizes)),
            'min_size': int(np.min(sizes)),
            'max_size': int(np.max(sizes))
        },
        'largest_segments': [
            {
                'id': int(info['id']),
                'size': int(info['size']),
                'percentage': float((info['size'] / sum(sizes)) * 100)
            }
            for info in analysis_results['segment_info']
        ]
    }
    
    return report


def save_report_to_json(report, file_path):
    """
    Save segmentation report to a JSON file.
    
    Args:
        report (dict): Report data
        file_path (str): Output file path
    """
    try:
        with open(file_path, 'w') as f:
            json.dump(report, f, indent=2)
    except Exception as e:
        raise IOError(f"Could not save report to {file_path}: {e}")


def create_parameter_comparison_plot(results_list, parameter_name):
    """
    Create a plot comparing segmentation results across different parameter values.
    
    Args:
        results_list (list): List of analysis results for different parameters
        parameter_name (str): Name of the parameter being varied
        
    Returns:
        matplotlib.figure.Figure: Figure containing the comparison plot
    """
    param_values = []
    num_segments = []
    mean_sizes = []
    
    for result in results_list:
        param_values.append(result['parameters'][parameter_name])
        num_segments.append(result['total_segments'])
        mean_sizes.append(result['statistics']['mean_size'])
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
    
    # Number of segments vs parameter
    ax1.plot(param_values, num_segments, 'o-', color='#F63366', linewidth=2, markersize=8)
    ax1.set_xlabel(f'{parameter_name}', fontsize=12)
    ax1.set_ylabel('Number of Segments', fontsize=12)
    ax1.set_title(f'Segments vs {parameter_name}', fontsize=14)
    ax1.grid(True, alpha=0.3)
    
    # Mean segment size vs parameter
    ax2.plot(param_values, mean_sizes, 'o-', color='#1f77b4', linewidth=2, markersize=8)
    ax2.set_xlabel(f'{parameter_name}', fontsize=12)
    ax2.set_ylabel('Mean Segment Size', fontsize=12)
    ax2.set_title(f'Mean Size vs {parameter_name}', fontsize=14)
    ax2.grid(True, alpha=0.3)
    
    plt.tight_layout()
    return fig

