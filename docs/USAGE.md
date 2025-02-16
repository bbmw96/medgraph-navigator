# MedGraph Navigator Usage Guide

## Quick Start

### 1. Initialize the System
```python
from src.backend.graph_navigator import MedGraphNavigator

# Create navigator instance
navigator = MedGraphNavigator()

# Load data
success = navigator.load_synthea_data()
```

### 2. Process Queries
```python
# Simple patient query
result = navigator.process_query("Show medical history for patient P123")

# Analyze treatment patterns
patterns = navigator.analyzer.analyze_treatment_patterns("Type 2 Diabetes")

# Find similar patients
similar = navigator.analyzer.find_similar_patients("P123", num_similar=5)
```

### 3. Visualization
```python
# Import visualization component
from src.frontend.MedGraphViz import MedGraphViz

# Create visualization
viz = MedGraphViz(data=result, vizType='timeSeries')
```

## Example Use Cases

1. Patient History Analysis
2. Population Health Insights
3. Risk Factor Prediction
4. Treatment Pattern Analysis

## Best Practices

1. Data Loading
- Verify database connection before loading
- Monitor memory usage during large data loads
- Use batch processing for large datasets

2. Query Optimization
- Use specific query intents for better results
- Leverage GPU acceleration for large graphs
- Cache frequently accessed data

3. Visualization
- Choose appropriate chart types for data
- Consider data volume in visualizations
- Use interactive features for exploration

4. Memory Management
- Monitor GPU memory usage
- Clear cache when needed
- Use batch processing for large operations
