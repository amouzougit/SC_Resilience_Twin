import simpy
import random # IMPORT
from typing import Optional
from src.models.network import SCNetworkManager

class ResilienceEngine:
    """
    Moteur de simulation de Jumeau Numérique (Digital Twin).
    Intègre la stochasticité pour le réalisme et des stratégies de 
    Contingency Planning (Dmitry Ivanov).
    """
    def __init__(self, env: simpy.Environment, network_manager: SCNetworkManager):
        self.env = env
        self.nm = network_manager
        self.history = []

    def production_process(self, node_id: str, input_node_id: Optional[str] = None):
        node = self.nm.get_node(node_id)
        
        while True:
            # 1. ÉTAT DE PANNE DU NŒUD
            if node.status == "FAILED":
                self._record_state(node_id, node.inventory)
                yield self.env.timeout(1)
                continue

            # Demande moyenne de 100 unités avec un écart-type de 5 (Loi Normale)
            daily_demand = max(0, random.normalvariate(100, 5))

            # 3. LOGIQUE DE RÉSILIENCE (Dual Sourcing & Ramp-up)
            if node_id == "EU_Elec_T1":
                main_supplier = self.nm.get_node("AS_Semi_T2")
                backup_supplier = self.nm.get_node("EU_BackUp_T2")
                
                if main_supplier.status == "FAILED":
                    # Modélisation d'une montée en charge (Ramp-up)
                    # On ne récupère que 50% au début, puis 100% après 2 jours de crise
                    capacity_available = 100 if self.env.now > 17 else 50
                    if backup_supplier.inventory >= capacity_available:
                        backup_supplier.inventory -= capacity_available
                        node.inventory += capacity_available
                        print(f"[STOCHASTIC] T={self.env.now}: Secours activé ({capacity_available} u.)")

            # 4. FLUX DE MATIÈRES
            if input_node_id:
                input_node = self.nm.get_node(input_node_id)
                # Consommation basée sur la demande stochastique
                if input_node.inventory >= daily_demand:
                    input_node.inventory -= daily_demand
                    node.inventory += daily_demand
            else:
                # Nœud Source : Production avec aléas techniques (95% à 105%)
                node.inventory += node.capacity * random.uniform(0.95, 1.05)

            # 5. EXPÉDITION OEM (Sortie de stock)
            if node.node_type == "oem":
                node.inventory = max(0, node.inventory - daily_demand)

            self._record_state(node_id, node.inventory)
            yield self.env.timeout(1)

    def _record_state(self, node_id: str, level: float):
        self.history.append({
            'time': self.env.now,
            'node': node_id,
            'inventory': round(level, 2),
            'status': self.nm.get_node(node_id).status
        })

    def inject_disruption(self, node_id: str, start_time: int, duration: int):
        yield self.env.timeout(start_time)
        node = self.nm.get_node(node_id)
        node.status = "FAILED"
        print(f"\n[ALERTE ROUGE] T={start_time}: Disruption majeure sur {node_id}")
        
        yield self.env.timeout(duration)
        node.status = "OPERATIONAL"
        print(f"[RETOUR] T={start_time + duration}: Rétablissement de {node_id}")