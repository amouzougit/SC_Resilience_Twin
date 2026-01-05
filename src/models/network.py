import networkx as nx
from typing import Dict, List, Optional

class AutomotiveNode:
    def __init__(self, node_id: str, node_type: str, capacity: float, initial_inventory: float):
        self.node_id = node_id
        self.node_type = node_type
        self.capacity = capacity
        self.inventory = initial_inventory  # On commence avec un stock défini
        self.status = "OPERATIONAL"

class SCNetworkManager:
    def __init__(self):
        self.graph = nx.DiGraph()
        self.nodes_registry: Dict[str, AutomotiveNode] = {}

    def build_automotive_topology(self):
        # CONFIGURATION LEAN : Production = 100 unités/jour
        # Stock de sécurité = 3 jours (soit 300 unités)
        nodes = [
            AutomotiveNode("AS_Semi_T2", "tier2", 100, 500), # Principal (Asie)
            AutomotiveNode("EU_BackUp_T2", "tier2", 100, 1000),   # SECOURS (Europe)
            AutomotiveNode("EU_Elec_T1", "tier1", 100, 300), # Sous-traitant
            AutomotiveNode("FR_Plant_OEM", "oem", 100, 200)  # Usine France
        ]
        
        for n in nodes:
            self.nodes_registry[n.node_id] = n
            self.graph.add_node(n.node_id, obj=n)

        self.graph.add_edge("AS_Semi_T2", "EU_Elec_T1")
        self.graph.add_edge("EU_Elec_T1", "FR_Plant_OEM")
        self.graph.add_edge("EU_BackUp_T2", "EU_Elec_T1")

    def get_node(self, node_id: str) -> AutomotiveNode:
        return self.nodes_registry[node_id]