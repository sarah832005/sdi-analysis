# 🌍 Sustainable Development Index (SDI) Analysis — 2015–2019

> Analyse du développement durable de 104 pays à partir d'indicateurs économiques, sociaux et environnementaux — basée sur la méthodologie Hickel (2020).

---

## 📌 Contexte

Le **Sustainable Development Index (SDI)** est un indice alternatif au HDI (Human Development Index) qui mesure le développement humain **relatif à l'impact écologique** des pays. Contrairement au HDI, il pénalise les pays qui dépassent les limites planétaires en CO2 et empreinte matérielle.

```
SDI = ID / IIE
```

---

## 📐 Méthodologie — KPIs calculés

| KPI | Nom complet | Formule |
|-----|-------------|---------|
| **IEV** | Indice Espérance de Vie | `(LE - 20) / (85 - 20)` |
| **IE** | Indice Éducation | `(MYS/15 + EYS/18) / 2` |
| **IR** | Indice Revenu (modifié) | `(ln(GNI) - ln(100)) / (ln(75000) - ln(100))` |
| **ID** | Indice de Développement | `(IEV × IE × IR) ^ (1/3)` — moyenne géométrique |
| **IIE** | Impact Écologique | `(CO2/1.74 + MF/6.8) / 2` — dépassement moyen |
| **SDI** | Sustainable Development Index | `ID / IIE` |

**Limites planétaires utilisées :**
- CO2 : **1.74 t/personne/an** (IPCC 2018)
- Empreinte matérielle : **6.8 t/personne/an** (Bringezu et al. 2015)

---

## 📁 Structure du projet

```
sdi-analysis/
├── data/
│   ├── sdi_raw_data.csv          # Données brutes (104 pays × 5 ans)
│   └── sdi_final_dataset.csv     # Dataset avec tous les KPIs calculés
├── notebooks/
│   └── sdi_analysis.ipynb        # Notebook Jupyter complet
├── figures/
│   ├── fig1_eda_distributions.png
│   ├── fig2_top_bottom_sdi.png
│   ├── fig3_scatter_sdi.png
│   ├── fig4_temporal_evolution.png
│   ├── fig5_correlation_breakdown.png
│   ├── fig6_overshoot.png
│   ├── fig7_sdi_rate.png
│   └── fig8_iev_education.png
├── sdi_analysis.py               # Script Python complet
└── README.md
```

---

## 📊 Résultats clés (2019)

- **104 pays** analysés sur **5 ans** (2015–2019)
- **Aucun pays ne dépasse 0.9** → confirme Hickel (2020)
- **94.2%** des pays ont une évolution SDI positive entre 2015 et 2019
- Les pays à fort HDI (USA, Qatar, UAE) sont parmi les **pires SDI** à cause de l'overshoot écologique
- Les meilleurs SDI : pays à développement humain satisfaisant **et** faible impact écologique

| Indicateur | Moyenne mondiale 2019 |
|---|---|
| IEV | 0.844 |
| IE | 0.777 |
| IR | 0.808 |
| ID | 0.803 |
| IIE | 3.376 |
| **SDI** | **0.302** |

---

## 🛠️ Technologies

![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-150458?style=flat&logo=pandas&logoColor=white)
![NumPy](https://img.shields.io/badge/NumPy-013243?style=flat&logo=numpy&logoColor=white)
![Matplotlib](https://img.shields.io/badge/Matplotlib-11557c?style=flat)
![Seaborn](https://img.shields.io/badge/Seaborn-4c72b0?style=flat)
![Jupyter](https://img.shields.io/badge/Jupyter-F37626?style=flat&logo=jupyter&logoColor=white)

---

## 📚 Sources & Références

- Hickel, J. (2020). *The Sustainable Development Index: Measuring the ecological efficiency of human development in the Anthropocene.* Ecological Economics, 167.
- UNDP Human Development Reports — [hdr.undp.org](https://hdr.undp.org)
- UN International Resource Panel — [materialflows.net](https://www.materialflows.net)
- IPCC (2018) — Limites CO2 planétaires

---

*Projet académique — Sarah Mahmoudi*
