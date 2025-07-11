import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import networkx as nx
from scipy.stats import pearsonr
import warnings
warnings.filterwarnings('ignore')

def create_supply_chain_data(n_samples=3000, seed=42):
    np.random.seed(seed)
    transport_failure = np.random.normal(0, 1, n_samples)
    supplier_delay = 1.5 * transport_failure + np.random.normal(0, 0.5, n_samples)
    inventory_shortage = 1.2 * supplier_delay + np.random.normal(0, 0.5, n_samples)
    production_halt = 1.1 * inventory_shortage + np.random.normal(0, 0.5, n_samples)
    factory_shutdown = 0.9 * production_halt + np.random.normal(0, 0.5, n_samples)
    
    return np.column_stack([
        transport_failure, supplier_delay, inventory_shortage,
        production_halt, factory_shutdown
    ])

def sequential_causal_edges(data, var_names):
    edges = []
    for i in range(len(var_names) - 1):
        r, p = pearsonr(data[:, i], data[:, i + 1])
        edges.append((i, i + 1, r, p))
    return edges

def visualize_graph(edges, var_names, title):
    G = nx.DiGraph()
    for name in var_names:
        G.add_node(name)

    for i, j, r, p in edges:
        G.add_edge(var_names[i], var_names[j], weight=abs(r))

    pos = {
        var_names[0]: (0, 0),
        var_names[1]: (2, 0),
        var_names[2]: (4, 0),
        var_names[3]: (6, 0),
        var_names[4]: (8, 0),
    }

    node_colors = {
        var_names[0]: 'red',
        var_names[4]: 'orange'
    }
    for name in var_names[1:4]:
        node_colors[name] = 'skyblue'

    plt.figure(figsize=(12, 4))
    nx.draw_networkx_nodes(G, pos, node_color=[node_colors[n] for n in G.nodes], node_size=2200)
    nx.draw_networkx_labels(G, pos, font_size=10, font_weight='bold')

    for i, j, r, p in edges:
        style = 'solid'
        width = 2 if abs(r) > 0.7 else 1
        nx.draw_networkx_edges(G, pos, edgelist=[(var_names[i], var_names[j])],
                               style=style, width=width, edge_color='black',
                               arrows=True, arrowsize=20)

    plt.title(f"{title}\n({len(edges)} edges)", fontsize=13, fontweight='bold')
    plt.axis('off')
    plt.tight_layout()
    plt.show()

def main():
    var_names = ['TransportFailure', 'SupplierDelay', 'InventoryShortage', 'ProductionHalt', 'FactoryShutdown']
    data = create_supply_chain_data()
    
    print("📌 Using Sequential Causal Discovery...")
    edges = sequential_causal_edges(data, var_names)

    for i, j, r, p in edges:
        print(f"   {var_names[i]} → {var_names[j]} | r = {r:.3f} | p = {p:.6f}")

    visualize_graph(edges, var_names, "Supply Chain Causal Graph (Sequential)")

if __name__ == "__main__":
    main()
