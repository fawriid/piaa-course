import matplotlib.pyplot as plt
import networkx as nx
import random

def visualize_tsp_path(n, graph, path, title="TSP Path Visualization"):
   
   
    # Create graph
    G = nx.Graph()
    G.add_nodes_from(range(n))
    
    for i in range(n):
        for j in range(i + 1, n):
            if graph[i][j] > -0.5 and graph[i][j] != 0:
                G.add_edge(i, j, weight=graph[i][j])
    
    pos = nx.circular_layout(G)
    
    # Draw graph
    plt.figure(figsize=(10, 8))
    
    # Draw all nodes
    nx.draw_networkx_nodes(G, pos, node_size=500, node_color='lightblue')
    nx.draw_networkx_labels(G, pos, font_size=12, font_weight='bold')
    
    # Draw all edges (gray)
    nx.draw_networkx_edges(G, pos, width=1, edge_color='gray', alpha=0.5)
    
    # Draw path edges (red, thick)
    path_edges = []
    for i in range(len(path) - 1):
        u = path[i]
        v = path[i + 1]
        if G.has_edge(u, v):
            path_edges.append((u, v))
    
    nx.draw_networkx_edges(G, pos, edgelist=path_edges, width=3, edge_color='red')
    
    # Draw edge labels (weights)
    edge_labels = {(u, v): f"{d['weight']:.1f}" for u, v, d in G.edges(data=True) if d['weight'] > 0}
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=8)
    
    plt.title(title, fontsize=14)
    plt.axis('off')
    plt.tight_layout()
    plt.savefig('tsp_visualization.png', dpi=150, bbox_inches='tight')
    plt.show()
    print("Visualization saved as 'tsp_visualization.png'")

# Example: Generate a small matrix and visualize
def example_visualization():
    # Small example (n=5)
    n = 5
    # Example graph from Stepik
    example_matrix = [
        [-1, 1, 13, 23, 7],
        [12, -1, 15, 18, 28],
        [21, 29, -1, 33, 28],
        [23, 19, 34, -1, 38],
        [5, 40, 7, 39, -1]
    ]
    
    # Found path (0 -> 4 -> 2 -> 3 -> 1 -> 0)
    path = [0, 4, 2, 3, 1, 0]
    
    visualize_tsp_path(n, example_matrix, path, "TSP Optimal Path (Cost: 78)")

if __name__ == "__main__":
    example_visualization()