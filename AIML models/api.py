from flask import Flask, jsonify
from neo4j import GraphDatabase
from simulate import fetch_graph, monte_carlo_cascade

def create_api_app(uri="bolt://localhost:7687", user="neo4j", pwd="prism123"):
    app = Flask(__name__)
    driver = GraphDatabase.driver(uri, auth=(user, pwd))

    @app.route("/")
    def home():
        return "Welcome to the Causal Graph API 🚀"

    @app.route("/nodes")
    def nodes():
        with driver.session() as s:
            res = s.run("MATCH (n:Event) RETURN n.name AS name")
            return jsonify([r["name"] for r in res])

    @app.route("/edges")
    def edges():
        with driver.session() as s:
            res = s.run("MATCH (a:Event)-[:CAUSES]->(b:Event) RETURN a.name AS src, b.name AS dst")
            return jsonify([{"source": r["src"], "target": r["dst"]} for r in res])

    @app.route("/causes/<node>")
    def causes(node):
        with driver.session() as s:
            res = s.run("MATCH (a:Event)-[:CAUSES]->(b:Event {name: $node}) RETURN a.name AS cause", node=node)
            return jsonify([r["cause"] for r in res])

    @app.route("/effects/<node>")
    def effects(node):
        with driver.session() as s:
            res = s.run("MATCH (a:Event {name: $node})-[:CAUSES]->(b:Event) RETURN b.name AS effect", node=node)
            return jsonify([r["effect"] for r in res])
    

    @app.route("/simulate/<start_node>")
    def simulate_risk(start_node):
        graph = fetch_graph()
        if start_node not in graph.nodes():
            return jsonify({"error": f"{start_node} not found in graph"}), 404
        result = monte_carlo_cascade(graph, start_node)
        return jsonify(result)


    return app
