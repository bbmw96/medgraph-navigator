import networkx as nx
from arango import ArangoClient
import json
from langchain.agents import Tool, AgentExecutor
from langchain.chains import LLMChain
from langchain.agents import ZeroShotAgent
from langchain.chat_models import ChatOpenAI
import os

# Initialize ArangoDB client
client = ArangoClient(hosts='http://localhost:8529')
db = client.db('medgraph', username='root', password='')

# Initialize graph structure
class MedGraphNavigator:
    def __init__(self):
        self.graph = nx.Graph()
        self.db = db
        
    def load_synthea_data(self):
        """
        Load Synthea dataset from ArangoDB into NetworkX with validation
        """
        try:
            # Connect to ArangoDB collections
            collections = {
                'patients': self.db.collection('patients'),
                'encounters': self.db.collection('encounters'),
                'conditions': self.db.collection('conditions'),
                'medications': self.db.collection('medications'),
                'procedures': self.db.collection('procedures')
            }
            
            # Validate collections exist
            for name, collection in collections.items():
                if not collection.properties()['status']:
                    raise ValueError(f"Collection {name} not found or not active")
            
            # Load nodes with progress tracking
            node_types = {
                'patients': {'id_field': '_key', 'type': 'patient'},
                'encounters': {'id_field': '_key', 'type': 'encounter'},
                'conditions': {'id_field': '_key', 'type': 'condition'},
                'medications': {'id_field': '_key', 'type': 'medication'},
                'procedures': {'id_field': '_key', 'type': 'procedure'}
            }
            
            for col_name, props in node_types.items():
                print(f"Loading {col_name}...")
                for doc in collections[col_name].all():
                    self.graph.add_node(
                        doc[props['id_field']], 
                        type=props['type'],
                        data=doc
                    )
                print(f"Loaded {self.graph.number_of_nodes()} total nodes")
            
            # Add relationships
            print("Building relationships...")
            
            # Patient-Encounter relationships
            for encounter in collections['encounters'].all():
                self.graph.add_edge(
                    encounter['patient_id'],
                    encounter['_key'],
                    type='HAD_ENCOUNTER',
                    date=encounter.get('date', '')
                )
            
            # Encounter-Condition relationships
            for condition in collections['conditions'].all():
                if 'encounter_id' in condition:
                    self.graph.add_edge(
                        condition['encounter_id'],
                        condition['_key'],
                        type='DIAGNOSED_WITH',
                        date=condition.get('date', '')
                    )
            
            # Encounter-Medication relationships
            for medication in collections['medications'].all():
                if 'encounter_id' in medication:
                    self.graph.add_edge(
                        medication['encounter_id'],
                        medication['_key'],
                        type='PRESCRIBED',
                        date=medication.get('date', '')
                    )
            
            print(f"Built {self.graph.number_of_edges()} relationships")
            
            return True
            
        except Exception as e:
            print(f"Error loading data: {str(e)}")
            return False
                              
    def setup_agent_tools(self):
        """
        Initialize LangChain tools for the agent
        """
        tools = [
            Tool(
                name="AQL_Query",
                func=self.execute_aql_query,
                description="Execute AQL queries on the medical graph"
            ),
            Tool(
                name="Graph_Analytics",
                func=self.run_graph_analytics,
                description="Run advanced graph analytics using GPU acceleration"
            )
        ]
        return tools
        
    def execute_aql_query(self, query_intent):
        """
        Execute AQL query based on natural language intent
        """
        try:
            # Map common query intents to AQL templates
            aql_templates = {
                "patient_history": """
                    FOR patient IN patients
                    FILTER patient._key == @patient_id
                    LET encounters = (
                        FOR e IN OUTBOUND patient._id patient_encounters
                        SORT e.date DESC
                        RETURN e
                    )
                    RETURN { patient, encounters }
                """,
                "condition_frequency": """
                    FOR c IN conditions
                    COLLECT condition = c.description WITH COUNT INTO freq
                    SORT freq DESC
                    LIMIT 10
                    RETURN { condition, frequency: freq }
                """
            }
            
            # Execute query and return results
            if query_intent in aql_templates:
                cursor = self.db.aql.execute(aql_templates[query_intent])
                return list(cursor)
            else:
                return {"error": "Unsupported query intent"}
                
        except Exception as e:
            return {"error": str(e)}
            
    def run_graph_analytics(self, analysis_type, params=None):
        """
        Run GPU-accelerated graph analytics using cuGraph
        """
        try:
            import cugraph
            import cudf
            
            # Convert NetworkX graph to cuGraph
            G_cu = cugraph.from_networkx(self.graph)
            
            analytics_functions = {
                "pagerank": lambda: cugraph.pagerank(G_cu),
                "community_detection": lambda: cugraph.louvain(G_cu),
                "centrality": lambda: cugraph.betweenness_centrality(G_cu),
                "shortest_path": lambda: cugraph.shortest_path(
                    G_cu, 
                    source=params.get('source'),
                    target=params.get('target')
                )
            }
            
            if analysis_type in analytics_functions:
                result = analytics_functions[analysis_type]()
                # Convert result back to CPU for processing
                return result.to_pandas()
            else:
                return {"error": "Unsupported analysis type"}
                
        except ImportError:
            print("GPU acceleration not available, falling back to CPU...")
            # Implement CPU fallback using NetworkX
            analytics_functions_cpu = {
                "pagerank": lambda: nx.pagerank(self.graph),
                "community_detection": lambda: nx.community.louvain_communities(self.graph),
                "centrality": lambda: nx.betweenness_centrality(self.graph),
                "shortest_path": lambda: nx.shortest_path(
                    self.graph,
                    source=params.get('source'),
                    target=params.get('target')
                )
            }
            
            if analysis_type in analytics_functions_cpu:
                return analytics_functions_cpu[analysis_type]()
            else:
                return {"error": "Unsupported analysis type"}

    def setup_agent(self):
        """
        Initialize the LangChain agent with tools and prompts
        """
        # Define the tools available to the agent
        tools = self.setup_agent_tools()
        
        # Define the agent's prompt template
        prefix = """You are a medical data analysis assistant that helps healthcare professionals analyze patient data and medical relationships.
        You have access to the following tools:"""
        
        suffix = """When analyzing medical data, always consider patient privacy and data sensitivity.
        
        Question: {input}
        {agent_scratchpad}"""
        
        prompt = ZeroShotAgent.create_prompt(
            tools,
            prefix=prefix,
            suffix=suffix,
            input_variables=["input", "agent_scratchpad"]
        )
        
        # Initialize the LLM
        llm = ChatOpenAI(temperature=0)
        
        # Create the agent
        llm_chain = LLMChain(llm=llm, prompt=prompt)
        agent = ZeroShotAgent(llm_chain=llm_chain, tools=tools, verbose=True)
        
        # Create the agent executor
        agent_executor = AgentExecutor.from_agent_and_tools(
            agent=agent,
            tools=tools,
            verbose=True,
            max_iterations=3
        )
        
        return agent_executor
        
    def process_query(self, query):
        """
        Process natural language query and return appropriate response
        """
        try:
            # Initialize agent if not already done
            if not hasattr(self, 'agent_executor'):
                self.agent_executor = self.setup_agent()
            
            # Execute the query
            response = self.agent_executor.run(query)
            return response
            
        except Exception as e:
            return f"Error processing query: {str(e)}"

# Initialize the navigator
navigator = MedGraphNavigator()

# Example usage
if __name__ == "__main__":
    # Load the data
    success = navigator.load_synthea_data()
    if success:
        # Process a sample query
        query = "What are the most common conditions diagnosed in patients over 60?"
        result = navigator.process_query(query)
        print(result)
