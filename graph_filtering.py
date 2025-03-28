import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from scipy import sparse
from scipy.sparse.linalg import eigsh

def create_noisy_community_graph(n_nodes=30, n_communities=3, p_in=0.5, p_out=0.1, noise_level=0.15):
    nodes_per_community = n_nodes // n_communities
    G = nx.Graph()
    G.add_nodes_from(range(n_nodes))
    
    # 커뮤니티 내부 연결
    for comm in range(n_communities):
        nodes = range(comm * nodes_per_community, (comm + 1) * nodes_per_community)
        for i in nodes:
            for j in nodes:
                if i < j and np.random.random() < p_in:
                    G.add_edge(i, j)
    
    # 커뮤니티 간 연결 (노이즈)
    for i in range(n_nodes):
        for j in range(i + 1, n_nodes):
            if i // nodes_per_community != j // nodes_per_community:
                if np.random.random() < p_out:
                    G.add_edge(i, j)
    
    # 추가 랜덤 노이즈
    for i in range(n_nodes):
        for j in range(i + 1, n_nodes):
            if np.random.random() < noise_level:
                if G.has_edge(i, j):
                    G.remove_edge(i, j)
                else:
                    G.add_edge(i, j)
    
    return G

def graph_fourier_filter(G, cutoff=0.5):
    L = nx.normalized_laplacian_matrix(G)
    eigenvals, eigenvecs = eigsh(L, k=15, which='SM')  # k값 감소
    
    mask = eigenvals < np.percentile(eigenvals, cutoff * 100)
    filtered_eigenvecs = eigenvecs[:, mask]
    filtered_eigenvals = eigenvals[mask]
    
    n = G.number_of_nodes()
    A_filtered = np.zeros((n, n))
    
    for i in range(len(filtered_eigenvals)):
        v = filtered_eigenvecs[:, i]
        A_filtered += np.outer(v, v) * filtered_eigenvals[i]
    
    A_filtered = np.abs(A_filtered)
    A_filtered = (A_filtered + A_filtered.T) / 2
    
    G_filtered = nx.Graph()
    G_filtered.add_nodes_from(range(n))
    
    threshold = np.mean(A_filtered) + 0.5 * np.std(A_filtered)
    for i in range(n):
        for j in range(i+1, n):
            if A_filtered[i,j] > threshold:
                G_filtered.add_edge(i, j)
    
    return G_filtered

def plot_graphs(G_original, G_filtered):
    plt.figure(figsize=(15, 6))
    
    plt.subplot(121)
    pos = nx.spring_layout(G_original, seed=42)
    nx.draw(G_original, pos, node_size=200, node_color='blue', 
            alpha=0.6, with_labels=True, font_size=8)
    plt.title("Original Graph")
    
    plt.subplot(122)
    nx.draw(G_filtered, pos, node_size=200, node_color='red', 
            alpha=0.6, with_labels=True, font_size=8)
    plt.title("Filtered Graph")
    
    plt.tight_layout()
    plt.show()

# 메인 실행
if __name__ == "__main__":
    G_original = create_noisy_community_graph(n_nodes=30)
    G_filtered = graph_fourier_filter(G_original, cutoff=0.99)

    print(f"Original Graph - Nodes: {G_original.number_of_nodes()}, Edges: {G_original.number_of_edges()}")
    print(f"Filtered Graph - Nodes: {G_filtered.number_of_nodes()}, Edges: {G_filtered.number_of_edges()}")

    plot_graphs(G_original, G_filtered)
