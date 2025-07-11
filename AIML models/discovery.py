import numpy as np
from scipy.stats import pearsonr

def create_supply_chain_data(n_samples=3000, seed=42):
    np.random.seed(seed)
    tf = np.random.normal(0, 1, n_samples)
    sd = 1.5 * tf + np.random.normal(0, 0.5, n_samples)
    ishort = 1.2 * sd + np.random.normal(0, 0.5, n_samples)
    ph = 1.1 * ishort + np.random.normal(0, 0.5, n_samples)
    fs = 0.9 * ph + np.random.normal(0, 0.5, n_samples)
    return np.column_stack([tf, sd, ishort, ph, fs])

def get_causal_edges(data, var_names):
    edges = []
    for i in range(len(var_names) - 1):
        r, p = pearsonr(data[:, i], data[:, i+1])
        edges.append((var_names[i], var_names[i+1], r))
    return edges
