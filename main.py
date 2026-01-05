import simpy
from src.models.network import SCNetworkManager
from src.engine.simulation import ResilienceEngine
import pandas as pd

# 1. Initialisation
env = simpy.Environment()
nm = SCNetworkManager()
nm.build_automotive_topology()

engine = ResilienceEngine(env, nm)

# 2. Programmation des processus
# L'OEM consomme ce que le Tier-1 produit
env.process(engine.production_process("AS_Semi_T2"))
env.process(engine.production_process("EU_Elec_T1", input_node_id="AS_Semi_T2"))
env.process(engine.production_process("FR_Plant_OEM", input_node_id="EU_Elec_T1"))

# 3. Injection du Risque (Basé sur Ivanov : Scénario de crise)
# On coupe le fournisseur de puces asiatique au jour 20 pendant 15 jours
env.process(engine.inject_disruption("AS_Semi_T2", start_time=20, duration=15))

# 4. Lancement
env.run(until=100)

# 5. Export des résultats pour le Portfolio
df = pd.DataFrame(engine.history)
df.to_csv("data/simulation_results.csv", index=False)
print("Simulation terminée. Données prêtes pour analyse.")