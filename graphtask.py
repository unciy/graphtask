"""
This project generates a directed graph with specific properties,
allowing you to visualize the connections between nodes and control the graph parameters
through command-line arguments. The project also includes tests
to ensure functionality and correctness. This project requires Python3.
"""

import random
from datetime import datetime
import argparse
from math import sqrt
import textwrap
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib import colors as mcolors
from matplotlib import gridspec


def generate_random_data(num_records=100, multi_connection_ratio=0.8, min_connections=2,
                         max_connections=3):
    """
    Generate random graph data
    """
    # Validate the number of nodes
    if num_records < 2 or num_records > 200:
        raise ValueError("num_records must be between 2 and 200")
    if num_records == 2:
        print("Only two nodes; creating single connection.")
        return {0: [1], 1: [0]}

    # Create a list of unique nodes
    nodes = random.sample(range(num_records), num_records)
    connections = {}

    # Calculate the number of nodes that should have multiple connections
    multi_connection_nodes_count = int(num_records * multi_connection_ratio)
    single_connection_nodes_count = num_records - multi_connection_nodes_count

    # Select nodes for single and multiple connections
    single_connection_nodes = set(random.sample(nodes, single_connection_nodes_count))
    multi_connection_nodes = set(nodes) - single_connection_nodes

    # Create single connections for nodes with only one connection
    for node in single_connection_nodes:
        target = random.choice([n for n in nodes if n != node])
        connections[node] = [target]

    # Create multiple connections for nodes with multiple connections
    for node in multi_connection_nodes:
        # Ensure the number of connections is within specified min and max
        num_connections = max(min(random.randint(min_connections, max_connections),
                                  len(nodes) - 1), 2)
        targets = random.sample([n for n in nodes if n != node], num_connections)
        connections[node] = targets

    return connections


def main(num_records, multi_connection_ratio, min_connections, max_connections, edge_thickness,
         fig_size, save_to_file):
    # pylint: disable=R0913
    # pylint: disable=R0917
    # pylint: disable=R0914
    """
    Generate nodes and draw
    """
    data = generate_random_data(num_records, multi_connection_ratio,
                                min_connections, max_connections)

    fig = plt.figure(figsize=(fig_size, fig_size))
    gs = gridspec.GridSpec(2, 1, height_ratios=[4, 1])
    ax_graph = fig.add_subplot(gs[0])
    ax_text = fig.add_subplot(gs[1])
    ax_text.axis("off")

    # Create graph
    digraph = nx.DiGraph()
    for key, values in data.items():
        for value in values:
            digraph.add_edge(key, value)

    # Position nodes
    if len(digraph.nodes) < 5:
        pos = {i: (i * 0.5, 0) for i in digraph.nodes}
    else:
        k = 1 / sqrt(len(digraph.nodes))
        pos = nx.spring_layout(digraph, k=k, iterations=100)

    # Draw nodes and edges
    all_colors = list(mcolors.CSS4_COLORS.keys())
    nx.draw_networkx_nodes(digraph, pos, ax=ax_graph, node_size=300, node_color="lightblue",
                           edgecolors="black", linewidths=edge_thickness)
    for edge in digraph.edges():
        color = random.choice(all_colors)
        nx.draw_networkx_edges(digraph, pos, ax=ax_graph, edgelist=[edge],
                               edge_color=color, arrows=True)
    nx.draw_networkx_labels(digraph, pos, ax=ax_graph, font_size=8, font_weight="bold")

    ax_graph.set_title("Randomly Generated Graph with Colored Edges and Node Borders")

    # Format connections for text area (list of nodes and connections)
    connections_text = "\n".join(
        f"• {node} -> {sorted(connections)}" for node, connections in sorted(data.items())
    )
    wrapped_text = "\n".join(textwrap.wrap(connections_text, width=80))
    ax_text.text(0, 1, wrapped_text, ha="left", va="top", fontsize=6, wrap=True)

    # Save or display graph
    if save_to_file:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"generated_graph_{timestamp}.png"
        plt.savefig(filename, bbox_inches="tight")
        print(f"Graph saved to '{filename}'")
    else:
        plt.show()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate and display a random "
                                                 "graph with customizable parameters.")
    parser.add_argument("--num_records", type=int, default=100,
                        help="Number of nodes in the graph (minimum: 2, maximum: 200)")
    parser.add_argument("--multi_connection_ratio", type=float, default=0.8,
                        help="Ratio of nodes with multiple connections (default: 0.8)")
    parser.add_argument("--min_connections", type=int, default=2,
                        help="Minimum number of connections per multi-connection node (default: 2)")
    parser.add_argument("--max_connections", type=int, default=3,
                        help="Maximum number of connections per multi-connection node (default: 3)")
    parser.add_argument("--edge_thickness", type=float, default=1,
                        help="Thickness of node borders (default: 1)")
    parser.add_argument("--fig_size", type=int, default=10,
                        help="Size of the figure for the graph (default: 10)")
    parser.add_argument("--save_to_file", action="store_true",
                        help="Save the graph as an image instead of displaying it")

    args = parser.parse_args()
    main(args.num_records, args.multi_connection_ratio, args.min_connections, args.max_connections,
         args.edge_thickness, args.fig_size, args.save_to_file)
