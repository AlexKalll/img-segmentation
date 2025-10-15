# Algorithm Details

This application implements the Felzenszwalb–Huttenlocher (FH) graph-based image segmentation algorithm.

## Overview

- Pixels are nodes in a graph
- Edges connect neighboring pixels, weighted by color/intensity difference
- Regions are merged using a threshold that adapts to region size
- A Union–Find data structure ensures near-linear performance

## Key Parameters

- k (Threshold Constant): higher values favor larger merges → fewer segments
- min_size (Minimum Region Size): enforces minimum region size by post-merge cleanup
- sigma (Gaussian Smoothing): pre-smoothing reduces noise and stabilizes edges

## Workflow

1. Optional Gaussian smoothing with `sigma`
2. Graph construction over 4- or 8-neighborhoods
3. Sort edges by weight and process them in ascending order
4. Merge components when intra-component differences are below adaptive threshold
5. Enforce `min_size` via secondary merging of small components

## Complexity

- Union–Find with path compression and union by rank yields near-linear complexity in practice
- Memory usage scales with number of pixels and edges (neighbors per pixel)

## References

- P. Felzenszwalb and D. Huttenlocher, “Efficient Graph-Based Image Segmentation,” IJCV, 2004
