from neo4j import GraphDatabase

# Neo4j credentials
uri = "bolt://localhost:7687"
username = "neo4j"
password = "prism123"

driver = GraphDatabase.driver(uri, auth=(username, password))

# Causal graph nodes (same as your sequential model)
nodes = [
    "TransportFailure",
    "SupplierDelay",
    "InventoryShortage",
    "ProductionHalt",
    "FactoryShutdown"
]

# Directed edges (cause → effect)
edges = [
    ("TransportFailure", "SupplierDelay"),
    ("SupplierDelay", "InventoryShortage"),
    ("InventoryShortage", "ProductionHalt"),
    ("ProductionHalt", "FactoryShutdown")
]

def push_to_neo4j():
    with driver.session() as session:
        # Step 1: Clear existing data
        session.run("MATCH (n) DETACH DELETE n")
        print("✅ Cleared existing graph")

        # Step 2: Create nodes
        for name in nodes:
            session.run("MERGE (:Event {name: $name})", name=name)
        print("✅ Nodes created")

        # Step 3: Create relationships
        for src, dst in edges:
            session.run("""
                MATCH (a:Event {name: $src}), (b:Event {name: $dst})
                MERGE (a)-[:CAUSES]->(b)
            """, src=src, dst=dst)
        print("✅ Relationships created")

if __name__ == "__main__":
    push_to_neo4j()
    print("🎉 Done! Open http://localhost:7474 to view your causal graph.")
