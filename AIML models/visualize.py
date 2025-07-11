# visualize.py
import matplotlib.pyplot as plt

def plot_risk_report(risk_dict, start_node):
    nodes = list(risk_dict.keys())
    probs = [risk_dict[n]["probability"] for n in nodes]
    avg_times = [risk_dict[n]["avg_time"] for n in nodes]

    fig, ax1 = plt.subplots(figsize=(12, 6))

    bars = ax1.bar(nodes, avg_times, color='orange', alpha=0.8)
    ax1.set_ylabel("Avg Time to Disruption")
    ax1.set_title(f"Cascade Risk from '{start_node}'")

    for bar, prob in zip(bars, probs):
        ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.05,
                 f"{prob:.2f}", ha='center', va='bottom', fontsize=9, color='red')

    for bar, prob in zip(bars, probs):
        if prob > 0.75:
            bar.set_color("red")
        elif prob > 0.4:
            bar.set_color("orange")
        else:
            bar.set_color("green")

    plt.tight_layout()
    plt.savefig("risk_plot.png")
    plt.show()
