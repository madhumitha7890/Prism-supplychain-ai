from flask import Flask, jsonify
from neo4j import GraphDatabase

app = Flask(__name__)

# Neo4j connection config
uri = "bolt://localhost:7687"
username = "neo4j"
password = "prism123"
driver = GraphDatabase.driver(uri, auth=(username, password))

@app.route("/")
def welcome():
    return "Welcome to the Causal Graph API 🚀"

@app.route("/nodes", methods=["GET"])
def get_nodes():
    with driver.session() as session:
        result = session.run("MATCH (n:Event) RETURN n.name AS name")
        nodes = [record["name"] for record in result]
        return jsonify(nodes)

@app.route("/edges", methods=["GET"])
def get_edges():
    with driver.session() as session:
        result = session.run("""
            MATCH (a:Event)-[:CAUSES]->(b:Event)
            RETURN a.name AS source, b.name AS target
        """)
        edges = [{"source": r["source"], "target": r["target"]} for r in result]
        return jsonify(edges)

@app.route("/causes/<node>", methods=["GET"])
def get_causes(node):
    with driver.session() as session:
        result = session.run("""
            MATCH (a:Event)-[:CAUSES]->(b:Event {name: $node})
            RETURN a.name AS cause
        """, node=node)
        causes = [r["cause"] for r in result]
        return jsonify(causes)

@app.route("/effects/<node>", methods=["GET"])
def get_effects(node):
    with driver.session() as session:
        result = session.run("""
            MATCH (a:Event {name: $node})-[:CAUSES]->(b:Event)
            RETURN b.name AS effect
        """, node=node)
        effects = [r["effect"] for r in result]
        return jsonify(effects)

if __name__ == "__main__":
    app.run(debug=True)
