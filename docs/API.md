# MedGraph Navigator API Documentation

## Core Classes

### MedGraphNavigator

Main class for graph operations and query processing.

#### Methods

`load_synthea_data()`
- Loads medical data into the graph
- Returns: bool (success/failure)

`process_query(query: str)`
- Processes natural language queries
- Parameters:
  - query: str - Natural language query
- Returns: Query results

`run_graph_analytics(analysis_type: str, params: dict = None)`
- Runs GPU-accelerated graph analytics
- Parameters:
  - analysis_type: str - Type of analysis
  - params: dict - Additional parameters
- Returns: Analysis results

### MedicalAnalyzer

Class for medical data analysis and pattern recognition.

#### Methods

`analyze_treatment_patterns(condition: str)`
- Analyzes common treatment patterns
- Parameters:
  - condition: str - Medical condition
- Returns: dict of patterns

`find_similar_patients(patient_id: str, num_similar: int = 5)`
- Finds similar patients
- Parameters:
  - patient_id: str - Patient identifier
  - num_similar: int - Number of similar patients
- Returns: list of similar patients

`predict_risk_factors(condition: str)`
- Predicts risk factors for conditions
- Parameters:
  - condition: str - Target condition
- Returns: dict of risk factors

## Utility Functions

### GPU Utilities

`check_gpu_availability()`
- Checks GPU availability
- Returns: (bool, device, properties)

`optimize_memory_usage()`
- Optimizes GPU memory
- Returns: bool (success/failure)

### Data Generation

`generate_demo_data()`
- Generates sample medical data
- Returns: dict of generated data
