from simulate import fetch_graph, monte_carlo_cascade
from visualize import plot_risk_report
import matplotlib.pyplot as plt

graph = fetch_graph()
result = monte_carlo_cascade(graph, start_node="TransportFailure")
plot_risk_report(result, start_node="TransportFailure")
plt.savefig("risk_plot.png")


