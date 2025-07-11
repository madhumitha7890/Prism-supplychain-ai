from neo4j import GraphDatabase

def export_to_neo4j(nodes, edges, uri="bolt://localhost:7687", user="neo4j", pwd="prism123"):
    driver = GraphDatabase.driver(uri, auth=(user, pwd))
    with driver.session() as session:
        session.run("MATCH (n) DETACH DELETE n")
        
        # Create all nodes
        for node in nodes:
            session.run("MERGE (:Event {name: $name})", name=node)
        
        # Create all relationships
        for src, dst, r in edges:
            result = session.run("""
                MATCH (a:Event {name: $src}), (b:Event {name: $dst})
                RETURN a, b
            """, src=src, dst=dst)

            records = list(result)
            if records:  # Only create edge if both nodes found
                session.run("""
                    MATCH (a:Event {name: $src}), (b:Event {name: $dst})
                    MERGE (a)-[:CAUSES]->(b)
                """, src=src, dst=dst)
            else:
                print(f"⚠️ Nodes not found for edge: {src} → {dst}")

    driver.close()
