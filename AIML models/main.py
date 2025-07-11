from discovery import create_supply_chain_data, get_causal_edges
from export import export_to_neo4j
from api import create_api_app
from simulate import fetch_graph, monte_carlo_cascade
from visualize import plot_risk_report

if __name__ == "__main__":
    var_names = ['TransportFailure', 'SupplierDelay', 'InventoryShortage', 'ProductionHalt', 'FactoryShutdown']
    
    print("📦 Step 1: Generating causal data...")
    data = create_supply_chain_data()
    
    print("📈 Step 2: Extracting causal edges...")
    edges = get_causal_edges(data, var_names)
    
    print("🧠 Step 3: Exporting to Neo4j...")
    export_to_neo4j(var_names, edges)
    
    print("🎲 Step 4: Running Monte Carlo simulation from 'TransportFailure'...")
    graph = fetch_graph()
    start_node = "TransportFailure"
    result = monte_carlo_cascade(graph, start_node)

    print("📊 Step 5: Plotting disruption risk heatmap...")
    plot_risk_report(result, start_node)

    print("🚀 Step 6: Launching API...")
    app = create_api_app()
    app.run(debug=True)
