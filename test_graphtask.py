"""
Main testes
"""

import os
from datetime import datetime
from glob import glob
import pytest
from graphtask import generate_random_data, main


# Test for data generation and graph creation conditions
def test_generate_random_data_structure():
    """Test that generated data is in the correct format and follows structure."""
    data = generate_random_data(num_records=100, multi_connection_ratio=0.8)

    # Check that the data has exactly 100 nodes
    assert len(data) == 100, "Data should contain 100 records"

    # Check that exactly 80% of nodes have more than one connection
    multi_connection_nodes = sum(1 for connections in data.values() if len(connections) > 1)
    assert multi_connection_nodes == 80, "80% of nodes should have more than one connection"

    # Check that each node's connections are unique and do not contain itself
    for node, connections in data.items():
        assert node not in connections, f"Node {node} should not connect to itself"
        assert len(connections) == len(set(connections)), \
            f"Connections of node {node} should be unique"


def test_generate_random_data_small_values():
    """Test data generation for edge cases of num_records (2 and 3 nodes)."""
    # Edge case: 2 nodes
    data_two_nodes = generate_random_data(num_records=2)
    assert len(data_two_nodes) == 2
    assert data_two_nodes == {0: [1], 1: [0]}, "Graph with 2 nodes should connect each to the other"

    # Edge case: 3 nodes
    data_three_nodes = generate_random_data(num_records=3, multi_connection_ratio=0.8)
    assert len(data_three_nodes) == 3, "Graph with 3 nodes should contain exactly 3 nodes"


def test_generate_random_data_large_values():
    """Test data generation with num_records set to the maximum allowed value of 200."""
    data_large = generate_random_data(num_records=200, multi_connection_ratio=0.8)
    assert len(data_large) == 200, "Graph with max nodes should contain exactly 200 nodes"


def test_generate_random_data_invalid_values():
    """Test that invalid values for num_records raise exceptions."""
    with pytest.raises(ValueError, match="num_records must be between 2 and 200"):
        generate_random_data(num_records=1)

    with pytest.raises(ValueError, match="num_records must be between 2 and 200"):
        generate_random_data(num_records=201)


# Test for graph visualization - main function call with timestamped filename
def test_main_graph_structure():
    """Test main function's graph structure and output for valid input with timestamped filename."""
    # Run the main function with save_to_file option
    main(num_records=100, multi_connection_ratio=0.8, min_connections=2, max_connections=3,
         edge_thickness=1.5, fig_size=10, save_to_file=True)

    # Look for the latest file with timestamp pattern in the name
    timestamp = datetime.now().strftime("%Y%m%d_%H")
    matching_files = glob(f"generated_graph_{timestamp}*.png")

    # Assert that at least one file matching the pattern exists
    assert len(matching_files) > 0, \
        "Expected a file with a timestamped filename, but none was found."

    # Clean up created files
    for file in matching_files:
        os.remove(file)


# Tests for input arguments and validation
@pytest.mark.parametrize("num_records, expected_exception, expected_message", [
    (1, ValueError, "num_records must be between 2 and 200"),
    (201, ValueError, "num_records must be between 2 and 200"),
    (-10, ValueError, "num_records must be between 2 and 200"),
])
def test_num_records_boundary(num_records, expected_exception, expected_message):
    """Test boundaries and validation of num_records argument."""
    with pytest.raises(expected_exception, match=expected_message):
        generate_random_data(num_records=num_records)


@pytest.mark.parametrize("multi_connection_ratio, min_connections, max_connections", [
    (0.8, 2, 3),
    (0.8, 1, 5),
    (0.8, 2, 4),
])
def test_random_data_properties(multi_connection_ratio, min_connections, max_connections):
    """Test generation properties for valid input combinations with 80% multi-connection ratio."""
    data = generate_random_data(num_records=100, multi_connection_ratio=multi_connection_ratio,
                                min_connections=min_connections, max_connections=max_connections)

    # Verify number of nodes
    assert len(data) == 100, "Data should contain exactly 100 records"

    # Check that multi_connection_ratio is exactly 80%
    multi_connection_nodes = sum(1 for connections in data.values() if len(connections) > 1)
    assert multi_connection_nodes == int(
        100 * multi_connection_ratio), (f"Graph should have exactly "
                                        f"{multi_connection_ratio * 100}% "
                                        f"nodes with multiple connections")


@pytest.mark.parametrize("fig_size, edge_thickness", [
    (5, 0.5),
    (10, 1.5),
    (15, 2.0),
])
def test_visual_parameters(fig_size, edge_thickness):
    """Test different visual parameters for the graph to ensure no errors."""
    # Run the main function with save_to_file option
    main(num_records=100, multi_connection_ratio=0.8, min_connections=2, max_connections=3,
         edge_thickness=edge_thickness, fig_size=fig_size, save_to_file=True)

    # Look for the latest file with timestamp pattern in the name
    timestamp = datetime.now().strftime("%Y%m%d_%H")
    matching_files = glob(f"generated_graph_{timestamp}*.png")

    # Assert that at least one file matching the pattern exists
    assert len(matching_files) > 0, \
        "Expected a file with a timestamped filename, but none was found."

    # Clean up created files
    for file in matching_files:
        os.remove(file)
