import simpy
import pandas as pd
from src.models.network import SCNetworkManager
from src.engine.simulation import ResilienceEngine
from src.utils.analytics import ResilienceAnalytics

def execute_stress_test():
    print("--- [INITIALISATION DU JUMEAU NUMÉRIQUE AUTOMOBILE] ---")
    
    # 1. Setup de l'environnement
    env = simpy.Environment()
    nm = SCNetworkManager()
    nm.build_automotive_topology()
    engine = ResilienceEngine(env, nm)

    # 2. Programmation des flux (Modèle Ivanov/Christopher)
    # Flux : Asie (T2) -> Europe (T1) -> France (OEM)
    env.process(engine.production_process("AS_Semi_T2"))
    env.process(engine.production_process("EU_Elec_T1", input_node_id="AS_Semi_T2"))
    env.process(engine.production_process("FR_Plant_OEM", input_node_id="EU_Elec_T1"))

    # 3. Injection du scénario de crise (Ripple Effect)
    # Rupture du fournisseur de semi-conducteurs au Jour 15 pendant 20 jours
    env.process(engine.inject_disruption("AS_Semi_T2", start_time=15, duration=50))

    # 4. Exécution
    print("Simulation en cours sur 100 jours...")
    env.run(until=100)

    # 5. Sauvegarde des données brutes
    df = pd.DataFrame(engine.history)
    df.to_csv("data/simulation_results.csv", index=False)
    print("Données brutes sauvegardées dans data/simulation_results.csv")

    # 6. Analyse de Résilience et Visualisation
    print("\n--- [ANALYSE DES KPI DE RÉSILIENCE] ---")
    analyzer = ResilienceAnalytics("data/simulation_results.csv")
    kpis = analyzer.calculate_kpis("FR_Plant_OEM")
    
    print(f"RESULTAT SCIENTIFIQUE :")
    print(f" > Time-to-Survive (TTS) : {kpis['TTS']} jours")
    print(f" > Time-to-Recover (TTR) : {kpis['TTR']} jours")
    
    analyzer.generate_resilience_chart("FR_Plant_OEM")
    print("\nLe graphique 'resilience_chart.png' a été généré dans le dossier data/.")

if __name__ == "__main__":
    execute_stress_test()