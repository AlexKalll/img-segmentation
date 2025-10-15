"""
Felzenszwalb-Huttenlocher Image Segmentation Algorithm

This module implements the core Felzenszwalb-Huttenlocher algorithm for
efficient graph-based image segmentation.
"""

import numpy as np
from skimage.filters import gaussian
from union_find import UnionFind


def create_graph(image):
    """
    Creates a graph from an image where each pixel is a node and
    edges connect adjacent pixels with weights based on color difference.

    Args:
        image (numpy.ndarray): The input image (grayscale or color).

    Returns:
        list: A list of edges, where each edge is a tuple
              (weight, pixel1_index, pixel2_index).
    """
    height, width = image.shape[:2]
    is_color = image.ndim == 3
    edges = []
    
    for y in range(height):
        for x in range(width):
            u = y * width + x
            
            # Horizontal edge (right neighbor)
            if x < width - 1:
                v = y * width + (x + 1)
                if is_color:
                    diff = np.sum((image[y, x] - image[y, x + 1])**2)
                else:
                    diff = (image[y, x] - image[y, x + 1])**2
                edges.append((diff, u, v))
            
            # Vertical edge (bottom neighbor)
            if y < height - 1:
                v = (y + 1) * width + x
                if is_color:
                    diff = np.sum((image[y, x] - image[y + 1, x])**2)
                else:
                    diff = (image[y, x] - image[y + 1, x])**2
                edges.append((diff, u, v))
    
    return sorted(edges)


def felzenszwalb_huttenlocher(image, k=50, min_size=10, sigma=0.8):
    """
    Implements the Felzenszwalb-Huttenlocher image segmentation algorithm.

    Args:
        image (numpy.ndarray): The input image (grayscale or color).
        k (float): A constant to control the threshold for merging regions.
                  Higher values lead to fewer, larger segments.
        min_size (int): The minimum size of a segment in pixels.
        sigma (float): The standard deviation for the Gaussian filter.
                       Set to 0 to disable smoothing.

    Returns:
        tuple: (segmented_image, num_segments, union_find_object)
            - segmented_image: The segmented image with random colors for each region
            - num_segments: Total number of segments found
            - union_find_object: The UnionFind object for further analysis
    """
    height, width = image.shape[:2]
    num_pixels = height * width
    is_color = image.ndim == 3

    # Pre-process the image with Gaussian smoothing
    if sigma > 0:
        if is_color:
            smoothed_image = gaussian(image, sigma=sigma, channel_axis=-1, preserve_range=True)
        else:
            smoothed_image = gaussian(image, sigma=sigma, preserve_range=True)
    else:
        smoothed_image = image.copy()

    # Create the graph and initialize Union-Find
    edges = create_graph(smoothed_image)
    uf = UnionFind(num_pixels)
    threshold = np.full(num_pixels, float(k), dtype=float)

    # Process edges in order of increasing weight
    for weight, u, v in edges:
        root_u = uf.find(u)
        root_v = uf.find(v)
        
        if root_u != root_v:
            MInt = min(threshold[root_u], threshold[root_v])
            if weight <= MInt:
                uf.union(root_u, root_v)
                new_root = uf.find(root_u)
                threshold[new_root] = weight + float(k)

    # Merge small components
    if min_size > 0:
        for weight, u, v in edges:
            root_u = uf.find(u)
            root_v = uf.find(v)
            
            if root_u != root_v:
                size_u = np.sum(uf.parent == root_u)
                size_v = np.sum(uf.parent == root_v)
                
                if size_u < min_size or size_v < min_size:
                    uf.union(root_u, root_v)

    # Create the segmented image with random colors
    segmented_image = np.zeros_like(image)
    component_colors = {}
    
    for y in range(height):
        for x in range(width):
            root = uf.find(y * width + x)
            
            if root not in component_colors:
                if is_color:
                    component_colors[root] = np.random.randint(0, 255, 3)
                else:
                    component_colors[root] = np.random.randint(0, 255)
            
            if is_color:
                segmented_image[y, x] = component_colors[root]
            else:
                segmented_image[y, x] = component_colors[root]

    return segmented_image, uf.num_sets, uf


def analyze_segments(original_image, union_find_obj, top_n=9):
    """
    Analyzes the segmentation results and extracts information about segments.

    Args:
        original_image (numpy.ndarray): The original input image.
        union_find_obj (UnionFind): The UnionFind object after segmentation.
        top_n (int): Number of largest segments to analyze.

    Returns:
        dict: Analysis results containing segment information.
    """
    height, width = original_image.shape[:2]
    num_pixels = height * width
    
    # Get largest components
    largest_roots, largest_sizes = union_find_obj.get_largest_components(top_n)
    
    # Create segment masks and extract segments
    segments = []
    segment_info = []
    
    for i, (root, size) in enumerate(zip(largest_roots, largest_sizes)):
        mask = np.array([union_find_obj.find(j) == root for j in range(num_pixels)]).reshape(height, width)
        
        # Extract segment from original image
        segment = np.zeros_like(original_image)
        segment[mask] = original_image[mask]
        
        segments.append(segment)
        segment_info.append({
            'id': i + 1,
            'root': root,
            'size': size,
            'mask': mask
        })
    
    return {
        'total_segments': union_find_obj.num_sets,
        'largest_segments': segments,
        'segment_info': segment_info,
        'component_sizes': union_find_obj.get_component_sizes()
    }

