"""
Image Utilities for Image Segmentation Studio

This module provides utilities for loading, processing, and saving images
for the Felzenszwalb-Huttenlocher segmentation algorithm.
"""

import numpy as np
import os
from PIL import Image
from skimage import io, data, color
from skimage.transform import resize
import requests
from io import BytesIO


def create_test_image():
    """
    Create a simple test image when no sample images are available.
    
    Returns:
        numpy.ndarray: A simple test image
    """
    # Create a simple test image with some patterns
    image = np.zeros((200, 200, 3), dtype=np.uint8)
    
    # Add some colored rectangles
    image[50:100, 50:100] = [255, 0, 0]    # Red square
    image[50:100, 100:150] = [0, 255, 0]   # Green square
    image[100:150, 50:100] = [0, 0, 255]  # Blue square
    image[100:150, 100:150] = [255, 255, 0] # Yellow square
    
    # Add some text-like pattern
    image[150:200, 50:150] = [128, 128, 128] # Gray rectangle
    
    return image


def load_sample_image(image_name='coffee'):
    """
    Load a sample image from scikit-image data.
    
    Args:
        image_name (str): Name of the sample image ('coffee', 'astronaut', 'camera', etc.)
        
    Returns:
        numpy.ndarray: The loaded image
    """
    # Try to load images safely, handling cases where they might not be available
    image_loaders = {
        'coffee': lambda: data.coffee(),
        'astronaut': lambda: data.astronaut(),
        'camera': lambda: data.camera(),
        'coins': lambda: data.coins(),
        'moon': lambda: data.moon(),
        'rocket': lambda: data.rocket(),
        'text': lambda: data.text(),
        'chelsea': lambda: data.chelsea(),
        'horse': lambda: data.horse(),
        'hubble_deep_field': lambda: data.hubble_deep_field()
    }
    
    # Try to load the requested image
    if image_name in image_loaders:
        try:
            return image_loaders[image_name]()
        except AttributeError:
            # If the image is not available, try coffee as fallback
            pass
    
    # Default fallback - try coffee first, then camera
    try:
        return data.coffee()
    except AttributeError:
        try:
            return data.camera()
        except AttributeError:
            # If even basic images fail, create a simple test image
            return create_test_image()


def load_image_from_file(file_path):
    """
    Load an image from a local file path.
    
    Args:
        file_path (str): Path to the image file
        
    Returns:
        numpy.ndarray: The loaded image
        
    Raises:
        IOError: If the file cannot be loaded
    """
    try:
        image = io.imread(file_path)
        return image
    except Exception as e:
        raise IOError(f"Could not load image from {file_path}: {e}")


def load_image_from_url(url):
    """
    Load an image from a URL.
    
    Args:
        url (str): URL of the image
        
    Returns:
        numpy.ndarray: The loaded image
        
    Raises:
        IOError: If the image cannot be downloaded
    """
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        image = io.imread(BytesIO(response.content))
        return image
    except requests.exceptions.RequestException as e:
        raise IOError(f"Could not download image from URL: {e}")


def preprocess_image(image, max_size=512, convert_to_rgb=True):
    """
    Preprocess an image for segmentation.
    
    Args:
        image (numpy.ndarray): Input image
        max_size (int): Maximum dimension for resizing (maintains aspect ratio)
        convert_to_rgb (bool): Whether to convert to RGB format
        
    Returns:
        numpy.ndarray: Preprocessed image
    """
    # Convert to RGB if needed
    if convert_to_rgb and image.ndim == 3 and image.shape[2] == 4:
        # Remove alpha channel
        image = image[:, :, :3]
    
    # Resize if too large
    height, width = image.shape[:2]
    if max(height, width) > max_size:
        scale = max_size / max(height, width)
        new_height = int(height * scale)
        new_width = int(width * scale)
        image = resize(image, (new_height, new_width), anti_aliasing=True, preserve_range=True)
        image = image.astype(np.uint8)
    
    return image


def save_image(image, file_path, format='PNG'):
    """
    Save an image to a file.
    
    Args:
        image (numpy.ndarray): Image to save
        file_path (str): Output file path
        format (str): Image format ('PNG', 'JPEG', etc.)
    """
    try:
        # Ensure the directory exists
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        
        # Convert numpy array to PIL Image
        if image.ndim == 3:
            pil_image = Image.fromarray(image.astype(np.uint8))
        else:
            pil_image = Image.fromarray(image.astype(np.uint8), mode='L')
        
        # Save the image
        pil_image.save(file_path, format=format)
        
    except Exception as e:
        raise IOError(f"Could not save image to {file_path}: {e}")


def image_to_bytes(image, format='PNG'):
    """
    Convert an image to bytes for download.
    
    Args:
        image (numpy.ndarray): Image to convert
        format (str): Image format
        
    Returns:
        bytes: Image as bytes
    """
    try:
        if image.ndim == 3:
            pil_image = Image.fromarray(image.astype(np.uint8))
        else:
            pil_image = Image.fromarray(image.astype(np.uint8), mode='L')
        
        buffer = BytesIO()
        pil_image.save(buffer, format=format)
        return buffer.getvalue()
        
    except Exception as e:
        raise IOError(f"Could not convert image to bytes: {e}")


def get_image_info(image):
    """
    Get basic information about an image.
    
    Args:
        image (numpy.ndarray): Input image
        
    Returns:
        dict: Image information
    """
    height, width = image.shape[:2]
    is_color = image.ndim == 3
    channels = image.shape[2] if is_color else 1
    
    return {
        'height': height,
        'width': width,
        'channels': channels,
        'is_color': is_color,
        'dtype': str(image.dtype),
        'shape': image.shape,
        'total_pixels': height * width
    }


def create_sample_images():
    """
    Create a collection of sample images for the app.
    
    Returns:
        dict: Dictionary of sample images with names as keys
    """
    samples = {}
    
    # Load various sample images safely
    sample_names = ['coffee', 'astronaut', 'camera', 'coins', 'moon', 'rocket', 'chelsea', 'horse']
    
    for name in sample_names:
        try:
            samples[name] = load_sample_image(name)
        except Exception:
            continue  # Skip if image not available
    
    # If no samples were loaded, create a test image
    if not samples:
        samples['test'] = create_test_image()
    
    return samples

