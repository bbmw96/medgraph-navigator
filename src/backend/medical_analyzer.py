import networkx as nx

class MedicalAnalyzer:
    def __init__(self, graph):
        self.graph = graph
        
    def analyze_treatment_patterns(self, condition):
        """
        Analyze common treatment patterns for a specific condition
        """
        treatment_patterns = {}
        
        # Find all encounters with this condition
        condition_encounters = [n for n, attr in self.graph.nodes(data=True)
                             if attr.get('type') == 'condition' and 
                             attr.get('data', {}).get('description') == condition]
        
        for c_id in condition_encounters:
            # Get associated medications through encounters
            medications = []
            for path in nx.all_simple_paths(self.graph, c_id, weight='date', cutoff=2):
                end_node = path[-1]
                if self.graph.nodes[end_node].get('type') == 'medication':
                    medications.append(self.graph.nodes[end_node]['data']['description'])
            
            # Record the treatment pattern
            pattern = tuple(sorted(medications))
            treatment_patterns[pattern] = treatment_patterns.get(pattern, 0) + 1
        
        return treatment_patterns
        
    def find_similar_patients(self, patient_id, num_similar=5):
        """
        Find similar patients based on condition and treatment patterns
        """
        # Get patient's conditions and medications
        patient_conditions = set()
        patient_medications = set()
        
        for neighbor in self.graph.neighbors(patient_id):
            node_type = self.graph.nodes[neighbor]['type']
            if node_type == 'condition':
                patient_conditions.add(self.graph.nodes[neighbor]['data']['description'])
            elif node_type == 'medication':
                patient_medications.add(self.graph.nodes[neighbor]['data']['description'])
        
        # Calculate similarity scores for other patients
        similarity_scores = {}
        for node, attr in self.graph.nodes(data=True):
            if attr.get('type') == 'patient' and node != patient_id:
                other_conditions = set()
                other_medications = set()
                
                for neighbor in self.graph.neighbors(node):
                    node_type = self.graph.nodes[neighbor]['type']
                    if node_type == 'condition':
                        other_conditions.add(self.graph.nodes[neighbor]['data']['description'])
                    elif node_type == 'medication':
                        other_medications.add(self.graph.nodes[neighbor]['data']['description'])
                
                # Calculate Jaccard similarity
                condition_similarity = len(patient_conditions & other_conditions) / len(patient_conditions | other_conditions)
                medication_similarity = len(patient_medications & other_medications) / len(patient_medications | other_medications)
                
                # Combined similarity score
                similarity_scores[node] = (condition_similarity + medication_similarity) / 2
        
        # Return top similar patients
        similar_patients = sorted(similarity_scores.items(), key=lambda x: x[1], reverse=True)[:num_similar]
        return similar_patients
        
    def predict_risk_factors(self, condition):
        """
        Identify potential risk factors for a specific condition
        """
        risk_factors = {}
        
        # Find all patients with the condition
        condition_patients = set()
        for node, attr in self.graph.nodes(data=True):
            if attr.get('type') == 'condition' and attr.get('data', {}).get('description') == condition:
                # Get the patient through the encounter
                for path in nx.all_simple_paths(self.graph, node, cutoff=2):
                    end_node = path[-1]
                    if self.graph.nodes[end_node].get('type') == 'patient':
                        condition_patients.add(end_node)
        
        # Analyze prior conditions for these patients
        for patient_id in condition_patients:
            prior_conditions = []
            for neighbor in self.graph.neighbors(patient_id):
                if self.graph.nodes[neighbor]['type'] == 'condition':
                    condition_data = self.graph.nodes[neighbor]['data']
                    if condition_data['description'] != condition:
                        prior_conditions.append(condition_data['description'])
            
            # Count frequency of prior conditions
            for prior in prior_conditions:
                risk_factors[prior] = risk_factors.get(prior, 0) + 1
        
        # Calculate risk ratios
        total_patients = len([n for n, attr in self.graph.nodes(data=True) 
                            if attr.get('type') == 'patient'])
        
        risk_ratios = {}
        for factor, count in risk_factors.items():
            risk_ratio = (count / len(condition_patients)) / (count / total_patients)
            risk_ratios[factor] = risk_ratio
        
        return risk_ratios
