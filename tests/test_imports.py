import importlib

def test_imports():
    import streamlit
    import numpy
    import matplotlib

def test_project_modules_import():
    for mod in [
        "src.fh_segmentation",
        "src.union_find",
        "src.image_utils",
    ]:
        importlib.import_module(mod)
