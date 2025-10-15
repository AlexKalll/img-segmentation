"""
Union-Find (Disjoint Set Union) Data Structure

This module implements the Union-Find data structure with path compression
and union by rank optimizations for efficient image segmentation.
"""

import numpy as np


class UnionFind:
    """
    A class to represent the Disjoint Set Union (DSU) data structure
    with Path Compression and Union by Rank optimizations.
    
    This implementation is optimized for image segmentation tasks where
    we need to efficiently merge pixel regions based on similarity criteria.
    """
    
    def __init__(self, size):
        """
        Initializes the Union-Find data structure.

        Args:
            size (int): The number of elements in the set (typically number of pixels).
        """
        self.parent = np.arange(size)
        self.rank = np.zeros(size)
        self.num_sets = size

    def find(self, i):
        """
        Finds the representative (root) of the set containing element i
        with path compression optimization.

        Args:
            i (int): The element to find.

        Returns:
            int: The representative of the set containing element i.
        """
        if self.parent[i] != i:
            self.parent[i] = self.find(self.parent[i])
        return self.parent[i]

    def union(self, i, j):
        """
        Merges the sets containing elements i and j using union by rank.

        Args:
            i (int): An element in the first set.
            j (int): An element in the second set.
        """
        root_i = self.find(i)
        root_j = self.find(j)
        
        if root_i != root_j:
            if self.rank[root_i] < self.rank[root_j]:
                self.parent[root_i] = root_j
            elif self.rank[root_i] > self.rank[root_j]:
                self.parent[root_j] = root_i
            else:
                self.parent[root_j] = root_i
                self.rank[root_i] += 1
            self.num_sets -= 1

    def get_component_sizes(self):
        """
        Returns the size of each component in the Union-Find structure.
        
        Returns:
            dict: A dictionary mapping component root to its size.
        """
        roots = np.array([self.find(i) for i in range(len(self.parent))])
        unique_roots, counts = np.unique(roots, return_counts=True)
        return dict(zip(unique_roots, counts))

    def get_largest_components(self, n=9):
        """
        Returns the n largest components sorted by size.
        
        Args:
            n (int): Number of largest components to return.
            
        Returns:
            tuple: (component_roots, sizes) sorted by size in descending order.
        """
        component_sizes = self.get_component_sizes()
        sorted_components = sorted(component_sizes.items(), key=lambda x: x[1], reverse=True)
        
        if len(sorted_components) >= n:
            roots, sizes = zip(*sorted_components[:n])
            return list(roots), list(sizes)
        else:
            roots, sizes = zip(*sorted_components)
            return list(roots), list(sizes)

