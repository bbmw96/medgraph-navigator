import pytest
from src.backend.graph_navigator import MedGraphNavigator
from src.utils.data_generation import generate_demo_data

@pytest.fixture
def navigator():
    """Create a test navigator instance with sample data"""
    nav = MedGraphNavigator()
    nav.load_synthea_data()
    return nav

def test_data_loading(navigator):
    """Test if data is loaded correctly"""
    assert navigator.graph is not None
    assert len(navigator.graph.nodes) > 0
    assert len(navigator.graph.edges) > 0

def test_query_processing(navigator):
    """Test natural language query processing"""
    query = "Show medical history for patient P123"
    result = navigator.process_query(query)
    assert result is not None

def test_graph_analytics(navigator):
    """Test GPU-accelerated analytics"""
    result = navigator.run_graph_analytics("pagerank")
    assert result is not None
    assert isinstance(result, dict)

def test_error_handling(navigator):
    """Test error handling for invalid queries"""
    result = navigator.process_query("invalid query")
    assert "error" in str(result).lower()
