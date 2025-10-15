"""
Quick test script to verify the Image Segmentation Studio components work correctly.
"""

import sys
import os
import numpy as np

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
SRC_DIR = os.path.join(PROJECT_ROOT, 'src')
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)
if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)

def test_imports():
    """Test that all modules can be imported correctly."""
    try:
        from src.union_find import UnionFind
        from src.fh_segmentation import felzenszwalb_huttenlocher, analyze_segments
        from src.image_utils import load_sample_image, preprocess_image
        from src.visualization import create_segmentation_comparison
        print("✅ All imports successful!")
        return True
    except ImportError as e:
        print(f"Import error: {e}")
        return False

def test_union_find():
    """Test the UnionFind data structure."""
    try:
        from src.union_find import UnionFind
        
        uf = UnionFind(10)
        assert uf.num_sets == 10
        
        uf.union(0, 1)
        assert uf.num_sets == 9
        
        assert uf.find(0) == uf.find(1)
        print("✅ UnionFind test passed!")
        return True
    except Exception as e:
        print(f"UnionFind test failed: {e}")
        return False

def test_segmentation():
    """Test the segmentation algorithm with a small sample."""
    try:
        from src.fh_segmentation import felzenszwalb_huttenlocher
        from src.image_utils import load_sample_image
        
        # Load a small sample image
        image = load_sample_image('coffee')
        
        # Resize to small size for quick test
        from skimage.transform import resize
        small_image = resize(image, (50, 50), anti_aliasing=True, preserve_range=True).astype(np.uint8)
        
        # Run segmentation
        segmented_image, num_segments, uf = felzenszwalb_huttenlocher(
            small_image, k=50, min_size=5, sigma=0.5
        )
        
        assert segmented_image.shape == small_image.shape
        assert num_segments > 0
        print(f"✅ Segmentation test passed! Found {num_segments} segments.")
        return True
    except Exception as e:
        print(f"Segmentation test failed: {e}")
        return False

def main():
    """Run all tests."""
    print("Testing Image Segmentation Studio components...")
    print("=" * 50)
    
    tests = [
        ("Import Test", test_imports),
        ("UnionFind Test", test_union_find),
        ("Segmentation Test", test_segmentation)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\nRunning {test_name}...")
        if test_func():
            passed += 1
    
    print("\n" + "=" * 50)
    print(f"Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("All tests passed! The application is ready to use.")
    else:
        print("Some tests failed. Please check the errors above.")

if __name__ == "__main__":
    main()
