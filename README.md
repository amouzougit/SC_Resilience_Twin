# 🚀 Automotive Supply Chain Digital Twin: Resilience Analysis

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)
[![UTBM](https://img.shields.io/badge/Institution-UTBM-red.svg)](https://www.utbm.fr/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## 📌 Présentation du Projet
Ce projet est un **Jumeau Numérique (Digital Twin)** conçu pour stress-tester la résilience d'une chaîne logistique automobile face à des chocs externes (Effet Ripple). 

Basé sur les travaux de **Dmitry Ivanov** (*Introduction to Supply Chain Analytics*) et **Martin Christopher**, ce simulateur utilise la **Simulation à Événements Discrets (DES)** pour calculer l'impact réel d'une rupture de flux sur une ligne d'assemblage OEM en France.

## 🔬 Fondements Scientifiques & KPIs
Le moteur de simulation modélise la propagation des perturbations et calcule deux indicateurs critiques :

1. **Time-to-Survive (TTS) :** Durée maximale pendant laquelle l'usine peut maintenir sa production après une rupture fournisseur.
   $$TTS = \max \{t \mid Inventory_{OEM}(t) > 0\}$$

2. **Time-to-Recover (TTR) :** Temps nécessaire pour restaurer un niveau de stock nominal post-crise.

## 🛠️ Architecture Technique
- **Moteur :** Python & `SimPy` (Asynchronous event simulation)
- **Modélisation :** `NetworkX` (Topologie de graphe dirigé)
- **Analyse :** `Pandas` & `Matplotlib` / `Seaborn`

## 📊 Résultats de la Simulation
L'analyse a permis de comparer deux scénarios :
* **Baseline (Fragile) :** TTS de 9 jours.
* **Optimisé (Dual Sourcing) :** TTS de 14 jours (+55% de résilience) grâce à un basculement réactif sur un fournisseur de secours européen.

![Resilience Chart](data/resilience_chart.png)

## 🚀 Installation & Usage
```bash
# Cloner le projet
git clone [https://github.com/amouzougit/SC_Resilience_Twin.git](https://github.com/amouzougit/SC_Resilience_Twin.git)

# Installer les dépendances
pip install -r requirements.txt

# Lancer la simulation
python run_full_analysis.py

✍️ Auteur
Kevo Amouzou - Étudiant à l'UTBM (Master Affaires Industrielles & Master Informatique).
