# simulate.py
from neo4j import GraphDatabase
import networkx as nx

driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "prism123"))

def fetch_graph():
    G = nx.DiGraph()
    with driver.session() as session:
        result = session.run("MATCH (a)-[r:CAUSES]->(b) RETURN a.name AS src, b.name AS tgt")
        for record in result:
            src, tgt = record["src"], record["tgt"]
            G.add_edge(src, tgt, weight=0.8)  # default weight if none set
    return G

import numpy as np

def monte_carlo_cascade(graph, start_node, steps=10, simulations=10000):
    impact_count = {node: [] for node in graph.nodes()}
    
    for _ in range(simulations):
        active = {start_node}
        visited = set()
        time_to_hit = {node: None for node in graph.nodes()}
        
        for t in range(steps):
            next_active = set()
            for node in active:
                for neighbor in graph.successors(node):
                    if neighbor not in visited:
                        p = graph[node][neighbor].get('weight', 0.5)
                        if np.random.rand() < p:
                            next_active.add(neighbor)
                            if time_to_hit[neighbor] is None:
                                time_to_hit[neighbor] = t
                visited.add(node)
            active = next_active
        
        for node, t in time_to_hit.items():
            if t is not None:
                impact_count[node].append(t)
    
    result = {}
    for node, hits in impact_count.items():
        if hits:
            result[node] = {
                "probability": round(len(hits) / simulations, 3),
                "avg_time": round(np.mean(hits), 2),
                "min_time": int(min(hits)),
                "max_time": int(max(hits))
            }
    return result
