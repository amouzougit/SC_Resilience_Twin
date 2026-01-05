import simpy
from typing import Optional
from src.models.network import SCNetworkManager

class ResilienceEngine:
    """
    Moteur de simulation de Jumeau Numérique (Digital Twin).
    Intègre les concepts de 'Contingency Planning' (Ivanov) et 
    'Agile Supply Chain' (Martin Christopher).
    """
    def __init__(self, env: simpy.Environment, network_manager: SCNetworkManager):
        self.env = env
        self.nm = network_manager
        self.history = []

    def production_process(self, node_id: str, input_node_id: Optional[str] = None):
        node = self.nm.get_node(node_id)
        
        while True:
            # 1. ÉTAT DE PANNE (Node Failure)
            # Si le nœud lui-même subit une disruption (ex: grève interne)
            if node.status == "FAILED":
                self._record_state(node_id, node.inventory)
                yield self.env.timeout(1)
                continue

            # 2. STRATÉGIE DE RÉSILIENCE : DUAL SOURCING RÉACTIF
            # On active le secours si le fournisseur principal (Asie) tombe
            demand = 100 
            
            if node_id == "EU_Elec_T1":
                main_supplier = self.nm.get_node("AS_Semi_T2")
                backup_supplier = self.nm.get_node("EU_BackUp_T2")
                
                if main_supplier.status == "FAILED":
                    # OPTIMISATION : On achète 100% de la demande au secours
                    # pour garantir un TTS indéfini (Zéro rupture)
                    if backup_supplier.inventory >= demand:
                        backup_supplier.inventory -= demand
                        node.inventory += demand 
                        print(f"[RESILIENCE] T={self.env.now}: Basculement total sur Backup Europe")

            # 3. FLUX NOMINAL (Just-in-Time)
            if input_node_id:
                input_node = self.nm.get_node(input_node_id)
                # Si le fournisseur amont est opérationnel et a du stock
                if input_node.status == "OPERATIONAL" and input_node.inventory >= demand:
                    input_node.inventory -= demand
                    node.inventory += demand
                else:
                    # Rupture de stock amont : propagation de l'effet Ripple
                    pass
            else:
                # Source primaire (Tier-2) : Production selon capacité
                node.inventory += node.capacity

            # 4. CONSOMMATION FINALE (Expédition OEM)
            # Simule la sortie des véhicules finis de l'usine française
            if node.node_type == "oem":
                node.inventory = max(0, node.inventory - demand)

            # 5. ENREGISTREMENT DES DONNÉES
            self._record_state(node_id, node.inventory)
            yield self.env.timeout(1)

    def _record_state(self, node_id: str, level: float):
        """Enregistrement pour analyse des KPIs (TTS/TTR)"""
        self.history.append({
            'time': self.env.now,
            'node': node_id,
            'inventory': level,
            'status': self.nm.get_node(node_id).status
        })

    def inject_disruption(self, node_id: str, start_time: int, duration: int):
        """Simule un choc externe sur la chaîne logistique"""
        yield self.env.timeout(start_time)
        node = self.nm.get_node(node_id)
        node.status = "FAILED"
        print(f"\n[ALERTE ROUGE] T={start_time}: Disruption majeure sur {node_id}")
        
        yield self.env.timeout(duration)
        node.status = "OPERATIONAL"
        print(f"[RETOUR] T={start_time + duration}: Rétablissement de {node_id}")