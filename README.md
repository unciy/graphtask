# Graph Generation Project

This project generates a directed graph with specific properties, allowing you to visualize the connections between nodes and control the graph parameters through command-line arguments. The project also includes tests to ensure functionality and correctness. This project requires Python3.

## Clone the Project

To clone the repository to your local machine, open a terminal and run:

````
git clone https://github.com/unciy/graphtask.git
cd graphtask
````
# Create a virtual environment:

```python3 -m venv .venv```


Activate the virtual environment:

Linux/macOS:
```source .venv/bin/activate```

Windows:
```.venv\Scripts\activate```

## Install the required packages:

With the virtual environment active, install the dependencies:

```pip install -r requirements.txt```

# Usage

## Basic usage
For the simplest script execution with default parameters, run:

````python main.py````

This will generate a graph with the default settings (100 nodes, 80% of nodes with multiple connections, and displays the graph without saving).

## Other example
Generate and display a graph with 100 nodes, where 80% of nodes have multiple connections, and save the graph to a file:

````python main.py --num_records 100 --multi_connection_ratio 0.8 --min_connections 2 --max_connections 3 --edge_thickness 1.5 --fig_size 10 --save_to_file````


# Argument Explanation:
The project generates a graph and displays or saves it based on parameters passed through the command line. Here’s how to run the project:

````
python main.py --num_records <number_of_nodes> --multi_connection_ratio <ratio_of_multi_connections> --min_connections <min_connections_per_node> --max_connections <max_connections_per_node> --edge_thickness <thickness_of_edges> --fig_size <size_of_figure> --save_to_file

--num_records: Number of nodes in the graph (must be between 2 and 200).
--multi_connection_ratio: Ratio of nodes with multiple connections (e.g., 0.8 for 80%).
--min_connections: Minimum number of connections for nodes with multiple connections.
--max_connections: Maximum number of connections for nodes with multiple connections.
--edge_thickness: Thickness of edges in the graph display.
--fig_size: Size of the figure for the graph display.
--save_to_file: Optional flag to save the graph as an image instead of displaying it.
````

# Running Tests
To run the tests for this project, make sure you have pytest installed (included in requirements.txt). With the virtual environment active, run:

````
pytest test_graphtask.py -vv
````

# pylint

````pylint ./graphtask.py ./test_graphtask.py````

# mypy

````mypy ./````

# License
This project is licensed under the MIT License. See the LICENSE file for more details.
