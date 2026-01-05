import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

class ResilienceAnalytics:
    def __init__(self, csv_path: str):
        self.df = pd.read_csv(csv_path)
        # On définit un style "Corporate Tech" pour les graphiques
        sns.set_theme(style="darkgrid")
        plt.rcParams['figure.facecolor'] = '#0B0F19'
        plt.rcParams['axes.facecolor'] = '#0B0F19'
        plt.rcParams['text.color'] = 'white'
        plt.rcParams['axes.labelcolor'] = '#94A3B8'

    def calculate_kpis(self, target_node: str):
        """Calcule les métriques de résilience critiques"""
        node_data = self.df[self.df['node'] == target_node]
        
        # 1. Time-to-Survive (TTS)
        # Temps écoulé entre le début de la panne amont et l'arrêt de l'usine cible
        disruption_start = self.df[self.df['status'] == 'FAILED']['time'].min()
        shutdown_time = node_data[(node_data['time'] >= disruption_start) & 
                                  (node_data['inventory'] <= 0)]['time'].min()
        
        tts = shutdown_time - disruption_start if not pd.isna(shutdown_time) else "Indéfini"

        # 2. Time-to-Recover (TTR)
        # Temps nécessaire pour revenir au niveau de stock nominal après la fin du FAIL
        disruption_end = self.df[self.df['status'] == 'FAILED']['time'].max()
        recovery_data = node_data[node_data['time'] > disruption_end]
        # On considère récupéré quand le stock remonte au niveau initial (ex: 50 unités)
        recovered_time = recovery_data[recovery_data['inventory'] >= 50]['time'].min()
        
        ttr = recovered_time - disruption_end if not pd.isna(recovered_time) else "En cours..."

        return {"TTS": tts, "TTR": ttr}

    def generate_resilience_chart(self, target_node: str):
        """Génère le graphique 'Impact vs Résilience' pour le Portfolio"""
        plt.figure(figsize=(12, 6))
        node_data = self.df[self.df['node'] == target_node]
        
        # Courbe principale
        plt.plot(node_data['time'], node_data['inventory'], color='#00D4FF', linewidth=3, label='Niveau de Stock OEM')
        
        # Zone de Disruption (grisée)
        disruption_times = self.df[self.df['status'] == 'FAILED']['time']
        if not disruption_times.empty:
            plt.axvspan(disruption_times.min(), disruption_times.max(), color='red', alpha=0.1, label='Disruption Tier-2')

        plt.title(f"Analyse de l'Effet Ripple : Stress-Test {target_node}", fontsize=16, fontweight='bold', pad=20)
        plt.xlabel("Temps (Jours)", fontsize=12)
        plt.ylabel("Inventaire (Unités)", fontsize=12)
        plt.legend()
        
        # Sauvegarde optimisée pour le Web
        plt.savefig("data/resilience_chart.png", dpi=300, bbox_inches='tight', transparent=True)
        print("Graphique de haute précision généré : data/resilience_chart.png")