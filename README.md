# LPF & HPF Filtering for Graphs

This repository implements spectral graph filtering techniques using Low-Pass Filters (LPF) and High-Pass Filters (HPF) based on graph Fourier transforms.

## Overview

The code demonstrates how to apply signal processing concepts to graph-structured data. By using the spectral decomposition of the graph Laplacian matrix, we can filter out noise and highlight community structures within graphs.

## Features

- Generation of synthetic community-structured graphs with controllable noise
- Implementation of graph Fourier transform for spectral filtering
- Low-pass filtering to preserve community structure and remove noise
- Visual comparison between original and filtered graphs

## How It Works

### Graph Generation

The `create_noisy_community_graph` function generates a graph with:
- Multiple communities with dense internal connections
- Sparse connections between communities
- Random noise (addition/removal of edges)

### Graph Fourier Transform and Filtering

The `graph_fourier_filter` function:
1. Computes the normalized Laplacian matrix of the graph
2. Performs eigendecomposition to get the graph's spectral components
3. Applies a low-pass filter by keeping only eigenvalues below a certain threshold
4. Reconstructs a filtered adjacency matrix
5. Creates a new filtered graph based on this matrix

### Visualization

The `plot_graphs` function displays both the original and filtered graphs side by side for comparison.

## Requirements

- Python 3.x
- NumPy
- NetworkX
- Matplotlib
- SciPy

## Usage

```python
# Generate a noisy graph with community structure
G_original = create_noisy_community_graph(n_nodes=30)

# Apply spectral filtering (low-pass filter with cutoff at 99th percentile)
G_filtered = graph_fourier_filter(G_original, cutoff=0.99)

# Display results
plot_graphs(G_original, G_filtered)
```

## Parameters

- `n_nodes`: Total number of nodes in the graph
- `n_communities`: Number of communities
- `p_in`: Probability of edge creation within communities
- `p_out`: Probability of edge creation between communities
- `noise_level`: Level of random noise
- `cutoff`: Filtering threshold (0-1 scale, where 1 keeps all eigenvalues)

## Applications

- Community detection in social networks
- Noise reduction in biological networks
- Feature extraction from graph-structured data
- Signal processing on irregular domains

## Theory

This implementation is based on spectral graph theory, which extends classical Fourier analysis to graphs. The eigenvalues of the graph Laplacian represent frequencies, with smaller eigenvalues corresponding to low-frequency components (community structure) and larger eigenvalues to high-frequency components (noise).

## License

[MIT License](LICENSE)
