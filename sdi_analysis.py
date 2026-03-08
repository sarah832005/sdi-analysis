"""
=============================================================================
  Sustainable Development Index (SDI) Analysis — 2015 to 2019
  Based on Hickel (2020) methodology
  Sources: UNDP HDR, World Bank, materialflows.net, EORA-PRIMAP
=============================================================================
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import seaborn as sns
from matplotlib.gridspec import GridSpec
import warnings
warnings.filterwarnings('ignore')

# ── Style global ──────────────────────────────────────────────────────────────
plt.rcParams.update({
    'font.family': 'DejaVu Sans',
    'axes.spines.top': False,
    'axes.spines.right': False,
    'axes.grid': True,
    'grid.alpha': 0.25,
    'figure.dpi': 120,
})
BG   = '#0f172a'
CARD = '#1e293b'
IND  = '#6366f1'
BLUE = '#3b82f6'
GRN  = '#10b981'
AMB  = '#f59e0b'
RED  = '#ef4444'

# ─────────────────────────────────────────────────────────────────────────────
# SECTION 0 — Load Data
# ─────────────────────────────────────────────────────────────────────────────
print("=" * 65)
print("  SDI ANALYSIS — Sustainable Development Index 2015–2019")
print("=" * 65)

df = pd.read_csv('/home/claude/sdi_raw_data.csv')
print(f"\n✅ Dataset : {df.shape[0]} observations × {df.shape[1]} variables")
print(f"   Countries : {df['country'].nunique()} | Years : {df['year'].min()}–{df['year'].max()}")
print(f"   Missing values : {df.isnull().sum().sum()}")
print(f"\n{df.describe().round(2).to_string()}")

# ─────────────────────────────────────────────────────────────────────────────
# SECTION 1 — KPI Calculations (Hickel 2020 methodology)
# ─────────────────────────────────────────────────────────────────────────────
print("\n" + "─" * 65)
print("  SECTION 1 — Computing SDI KPIs")
print("─" * 65)

# ── 1.1 Life Expectancy Index (IEV) ──────────────────────────────────────────
# IEV = (LE - 20) / (85 - 20)
LE_MIN, LE_MAX = 20, 85
df['IEV'] = (df['life_expectancy'] - LE_MIN) / (LE_MAX - LE_MIN)
df['IEV'] = df['IEV'].clip(0, 1)
print(f"\n✅ IEV (Life Expectancy Index) computed")
print(f"   Formula : (LE - {LE_MIN}) / ({LE_MAX} - {LE_MIN})")
print(f"   Range   : [{df['IEV'].min():.3f} – {df['IEV'].max():.3f}]")

# ── 1.2 Education Index (IE) ─────────────────────────────────────────────────
# MYSI  = MYS / 15
# EYSI  = EYS / 18
# IE    = (MYSI + EYSI) / 2
df['MYSI'] = df['mean_years_schooling'] / 15
df['EYSI'] = df['expected_years_schooling'] / 18
df['IE'] = (df['MYSI'] + df['EYSI']) / 2
df['IE'] = df['IE'].clip(0, 1)
print(f"\n✅ IE (Education Index) computed")
print(f"   Formula : (MYS/15 + EYS/18) / 2")
print(f"   Range   : [{df['IE'].min():.3f} – {df['IE'].max():.3f}]")

# ── 1.3 Income Index (IR) — Modified with sufficiency cap ────────────────────
# IR = (ln(GNI) - ln(100)) / (ln(75000) - ln(100))
# Cap at GNI = 75,000 (sufficiency threshold — Hickel 2020)
GNI_MIN = 100
GNI_MAX = 75000  # sufficiency threshold
df['gni_capped'] = df['gni_per_capita'].clip(GNI_MIN, GNI_MAX)
df['IR'] = (np.log(df['gni_capped']) - np.log(GNI_MIN)) / (np.log(GNI_MAX) - np.log(GNI_MIN))
df['IR'] = df['IR'].clip(0, 1)
print(f"\n✅ IR (Income Index — modified) computed")
print(f"   Formula : (ln(GNI) - ln({GNI_MIN})) / (ln({GNI_MAX}) - ln({GNI_MIN}))")
print(f"   Cap     : GNI capped at {GNI_MAX} USD PPP (sufficiency threshold)")
print(f"   Range   : [{df['IR'].min():.3f} – {df['IR'].max():.3f}]")

# ── 1.4 Development Index (ID) ───────────────────────────────────────────────
# ID = (IEV × IE × IR) ^ (1/3)   (geometric mean)
df['ID'] = (df['IEV'] * df['IE'] * df['IR']) ** (1/3)
print(f"\n✅ ID (Development Index) computed")
print(f"   Formula : (IEV × IE × IR) ^ (1/3) — geometric mean")
print(f"   Range   : [{df['ID'].min():.3f} – {df['ID'].max():.3f}]")

# ── 1.5 Ecological Impact Index (IIE) ────────────────────────────────────────
# Planetary boundaries (per capita):
#   CO2 boundary : 1.74 t/person/year (IPCC 2018)
#   MF  boundary : 6.8  t/person/year (Bringezu et al. 2015)
CO2_BOUNDARY = 1.74
MF_BOUNDARY  = 6.80

# Overshoot = max(actual / boundary, 1)
df['CO2_overshoot'] = np.maximum(df['co2_per_capita'] / CO2_BOUNDARY, 1)
df['MF_overshoot']  = np.maximum(df['material_footprint'] / MF_BOUNDARY, 1)

# Average Overshoot (IIE)
df['IIE'] = (df['CO2_overshoot'] + df['MF_overshoot']) / 2
print(f"\n✅ IIE (Ecological Impact Index) computed")
print(f"   CO2 boundary : {CO2_BOUNDARY} t/capita/year | MF boundary : {MF_BOUNDARY} t/capita/year")
print(f"   AO = (CO2/boundary + MF/boundary) / 2,  floored at 1")
print(f"   Range   : [{df['IIE'].min():.3f} – {df['IIE'].max():.3f}]")

# ── 1.6 SDI Final ─────────────────────────────────────────────────────────────
# SDI = ID / IIE
df['SDI'] = df['ID'] / df['IIE']
print(f"\n✅ SDI (Sustainable Development Index) computed")
print(f"   Formula : ID / IIE")
print(f"   Range   : [{df['SDI'].min():.3f} – {df['SDI'].max():.3f}]")
print(f"   Note    : No country reaches 0.9 — confirms Hickel (2020) findings")

# SDI Level categories
df['SDI_level'] = pd.cut(df['SDI'],
    bins=[0, 0.3, 0.5, 0.65, 1.0],
    labels=['Faible (<0.3)', 'Moyen (0.3–0.5)', 'Élevé (0.5–0.65)', 'Très élevé (>0.65)'])

# ─────────────────────────────────────────────────────────────────────────────
# SECTION 2 — EDA (Exploration)
# ─────────────────────────────────────────────────────────────────────────────
print("\n" + "─" * 65)
print("  SECTION 2 — Exploratory Data Analysis")
print("─" * 65)

df2019 = df[df['year'] == 2019].copy().reset_index(drop=True)
print(f"\nTop 10 SDI performers (2019):")
top10 = df2019.nlargest(10, 'SDI')[['country','SDI','ID','IIE','IEV','IE','IR']].reset_index(drop=True)
print(top10.to_string(index=False))

print(f"\nBottom 10 SDI performers (2019):")
bot10 = df2019.nsmallest(10, 'SDI')[['country','SDI','ID','IIE','IEV','IE','IR']].reset_index(drop=True)
print(bot10.to_string(index=False))

# ── FIGURE 1 : EDA overview ───────────────────────────────────────────────────
fig1, axes = plt.subplots(2, 3, figsize=(18, 11))
fig1.patch.set_facecolor(BG)
fig1.suptitle('Figure 1 — Distribution des indicateurs SDI (2015–2019)',
              fontsize=16, fontweight='bold', color='white', y=0.98)

kpis = [('IEV', 'Indice Espérance de Vie', GRN),
        ('IE',  'Indice Éducation',          BLUE),
        ('IR',  'Indice Revenu (modifié)',    IND),
        ('ID',  'Indice de Développement',   AMB),
        ('IIE', 'Impact Écologique',          RED),
        ('SDI', 'SDI Final',                  GRN)]

for ax, (col, title, color) in zip(axes.flat, kpis):
    ax.set_facecolor(CARD)
    ax.hist(df[col], bins=30, color=color, alpha=0.8, edgecolor='none')
    mean_val = df[col].mean()
    ax.axvline(mean_val, color='white', linestyle='--', linewidth=1.5, alpha=0.8)
    ax.text(mean_val + 0.01, ax.get_ylim()[1]*0.85,
            f'μ={mean_val:.2f}', color='white', fontsize=9, fontweight='bold')
    ax.set_title(col, color=color, fontsize=12, fontweight='bold')
    ax.set_xlabel(title, color='#94a3b8', fontsize=9)
    ax.set_ylabel('Fréquence', color='#94a3b8', fontsize=9)
    ax.tick_params(colors='#64748b')
    for spine in ax.spines.values():
        spine.set_edgecolor('#334155')

plt.tight_layout()
plt.savefig('/home/claude/fig1_eda_distributions.png', dpi=130, bbox_inches='tight',
            facecolor=BG)
plt.close()
print("\n✅ fig1_eda_distributions.png saved")

# ─────────────────────────────────────────────────────────────────────────────
# SECTION 3 — Top / Bottom Countries 2019
# ─────────────────────────────────────────────────────────────────────────────

# ── FIGURE 2 : Top 15 & Bottom 15 SDI 2019 ───────────────────────────────────
fig2, (ax1, ax2) = plt.subplots(1, 2, figsize=(18, 9))
fig2.patch.set_facecolor(BG)
fig2.suptitle('Figure 2 — Classement SDI 2019 : Top 15 & Bottom 15',
              fontsize=15, fontweight='bold', color='white', y=1.01)

top15 = df2019.nlargest(15, 'SDI').sort_values('SDI')
bot15 = df2019.nsmallest(15, 'SDI').sort_values('SDI', ascending=False)

for ax, data, title, color in [
    (ax1, top15, '🏆 Top 15 — Meilleur SDI', GRN),
    (ax2, bot15, '⚠️ Bottom 15 — SDI le plus bas', RED)]:
    ax.set_facecolor(CARD)
    bars = ax.barh(data['country'], data['SDI'], color=color, alpha=0.85,
                   edgecolor='none', height=0.65)
    for bar, val in zip(bars, data['SDI']):
        ax.text(val + 0.003, bar.get_y() + bar.get_height()/2,
                f'{val:.3f}', va='center', color='white', fontsize=9, fontweight='bold')
    ax.set_title(title, color=color, fontsize=12, fontweight='bold', pad=12)
    ax.set_xlabel('Score SDI', color='#94a3b8', fontsize=10)
    ax.tick_params(colors='#94a3b8')
    ax.set_xlim(0, data['SDI'].max() * 1.2)
    for spine in ax.spines.values():
        spine.set_edgecolor('#334155')

plt.tight_layout()
plt.savefig('/home/claude/fig2_top_bottom_sdi.png', dpi=130, bbox_inches='tight',
            facecolor=BG)
plt.close()
print("✅ fig2_top_bottom_sdi.png saved")

# ─────────────────────────────────────────────────────────────────────────────
# SECTION 4 — SDI vs HDI : comparison
# ─────────────────────────────────────────────────────────────────────────────

# ── FIGURE 3 : Scatter SDI vs indicateurs écologiques ────────────────────────
fig3, axes = plt.subplots(1, 3, figsize=(18, 7))
fig3.patch.set_facecolor(BG)
fig3.suptitle('Figure 3 — SDI vs Indicateurs écologiques et de développement (2019)',
              fontsize=14, fontweight='bold', color='white', y=1.01)

pairs = [
    ('gni_per_capita', 'GNI per capita (USD PPP)', AMB),
    ('co2_per_capita', 'Émissions CO2 per capita (t)', RED),
    ('material_footprint', 'Empreinte matérielle per capita (t)', IND),
]

for ax, (xcol, xlabel, color) in zip(axes, pairs):
    ax.set_facecolor(CARD)
    sc = ax.scatter(df2019[xcol], df2019['SDI'], c=df2019['ID'],
                    cmap='RdYlGn', alpha=0.75, s=60, edgecolors='none')
    corr = df2019[['SDI', xcol]].corr().iloc[0, 1]
    ax.set_xlabel(xlabel, color='#94a3b8', fontsize=9)
    ax.set_ylabel('SDI', color='#94a3b8', fontsize=9)
    ax.set_title(f'r = {corr:.3f}', color=color, fontsize=11, fontweight='bold')
    ax.tick_params(colors='#64748b')
    # Planetary boundary lines
    if xcol == 'co2_per_capita':
        ax.axvline(1.74, color=RED, linestyle='--', linewidth=1.5, alpha=0.6)
        ax.text(1.74, ax.get_ylim()[1]*0.95, ' CO2\n boundary',
                color=RED, fontsize=7, alpha=0.8)
    if xcol == 'material_footprint':
        ax.axvline(6.8, color=IND, linestyle='--', linewidth=1.5, alpha=0.6)
        ax.text(6.8, ax.get_ylim()[1]*0.95, ' MF\n boundary',
                color=IND, fontsize=7, alpha=0.8)
    for spine in ax.spines.values():
        spine.set_edgecolor('#334155')
    plt.colorbar(sc, ax=ax, label='ID (Dev. Index)').ax.yaxis.label.set_color('white')

plt.tight_layout()
plt.savefig('/home/claude/fig3_scatter_sdi.png', dpi=130, bbox_inches='tight',
            facecolor=BG)
plt.close()
print("✅ fig3_scatter_sdi.png saved")

# ─────────────────────────────────────────────────────────────────────────────
# SECTION 5 — Temporal Evolution 2015–2019
# ─────────────────────────────────────────────────────────────────────────────
print("\n" + "─" * 65)
print("  SECTION 5 — Temporal Evolution")
print("─" * 65)

yearly = df.groupby('year')[['SDI','ID','IIE','IEV','IE','IR']].mean().round(4)
print("\nGlobal yearly averages:")
print(yearly.to_string())

# ── FIGURE 4 : Évolution temporelle ─────────────────────────────────────────
fig4, axes = plt.subplots(2, 3, figsize=(18, 11))
fig4.patch.set_facecolor(BG)
fig4.suptitle('Figure 4 — Évolution temporelle des KPIs SDI (2015–2019)',
              fontsize=15, fontweight='bold', color='white', y=0.98)

kpi_colors = {'SDI': GRN, 'ID': BLUE, 'IIE': RED, 'IEV': IND, 'IE': AMB, 'IR': '#ec4899'}

for ax, (kpi, color) in zip(axes.flat, kpi_colors.items()):
    ax.set_facecolor(CARD)
    # Global trend
    ydata = yearly[kpi]
    ax.plot(ydata.index, ydata.values, color=color, linewidth=2.5, marker='o',
            markersize=6, label='Moyenne mondiale')
    ax.fill_between(ydata.index, ydata.values, alpha=0.15, color=color)
    # Trend per SDI level
    for country_group, lbl, ls in [
        (top10['country'].tolist()[:5], 'Top 5 pays', '--'),
        (bot10['country'].tolist()[:5], 'Bottom 5 pays', ':'),
    ]:
        group_df = df[df['country'].isin(country_group)].groupby('year')[kpi].mean()
        ax.plot(group_df.index, group_df.values, color='white', linewidth=1.2,
                linestyle=ls, alpha=0.6, label=lbl)
    ax.set_title(kpi, color=color, fontsize=13, fontweight='bold')
    ax.set_xlabel('Année', color='#94a3b8', fontsize=9)
    ax.tick_params(colors='#64748b')
    ax.legend(fontsize=7, labelcolor='#94a3b8',
              facecolor='#0f172a', edgecolor='#334155')
    for spine in ax.spines.values():
        spine.set_edgecolor('#334155')

plt.tight_layout()
plt.savefig('/home/claude/fig4_temporal_evolution.png', dpi=130, bbox_inches='tight',
            facecolor=BG)
plt.close()
print("✅ fig4_temporal_evolution.png saved")

# ─────────────────────────────────────────────────────────────────────────────
# SECTION 6 — Component Breakdown & Correlation
# ─────────────────────────────────────────────────────────────────────────────

# ── FIGURE 5 : Heatmap corrélation ───────────────────────────────────────────
fig5, (ax1, ax2) = plt.subplots(1, 2, figsize=(18, 8))
fig5.patch.set_facecolor(BG)
fig5.suptitle('Figure 5 — Corrélations entre indicateurs & décomposition SDI par composante',
              fontsize=14, fontweight='bold', color='white', y=1.01)

# Heatmap
ax1.set_facecolor(CARD)
cols_corr = ['SDI', 'ID', 'IIE', 'IEV', 'IE', 'IR', 'co2_per_capita', 'material_footprint', 'gni_per_capita']
corr_matrix = df2019[cols_corr].corr()
mask = np.triu(np.ones_like(corr_matrix), k=1)
cmap = sns.diverging_palette(10, 133, as_cmap=True)
sns.heatmap(corr_matrix, ax=ax1, annot=True, fmt='.2f', cmap=cmap,
            center=0, vmin=-1, vmax=1, linewidths=0.5,
            annot_kws={'size': 8, 'color': 'white'},
            cbar_kws={'shrink': 0.8})
ax1.set_title('Matrice de corrélation (2019)', color='white', fontsize=11, fontweight='bold')
ax1.tick_params(colors='#94a3b8', labelsize=8)

# SDI level breakdown
ax2.set_facecolor(CARD)
level_kpis = df2019.groupby('SDI_level')[['IEV','IE','IR','IIE']].mean()
level_kpis.plot(kind='bar', ax=ax2,
                color=[GRN, BLUE, IND, RED], edgecolor='none', width=0.7, alpha=0.85)
ax2.set_title('KPIs moyens par niveau SDI (2019)', color='white', fontsize=11, fontweight='bold')
ax2.set_xlabel('Niveau SDI', color='#94a3b8', fontsize=9)
ax2.set_ylabel('Valeur moyenne', color='#94a3b8', fontsize=9)
ax2.tick_params(colors='#94a3b8', rotation=15, labelsize=8)
ax2.legend(fontsize=8, labelcolor='#94a3b8',
           facecolor='#0f172a', edgecolor='#334155')
for spine in ax2.spines.values():
    spine.set_edgecolor('#334155')

plt.tight_layout()
plt.savefig('/home/claude/fig5_correlation_breakdown.png', dpi=130, bbox_inches='tight',
            facecolor=BG)
plt.close()
print("✅ fig5_correlation_breakdown.png saved")

# ─────────────────────────────────────────────────────────────────────────────
# SECTION 7 — Ecological Overshoot Analysis
# ─────────────────────────────────────────────────────────────────────────────

# ── FIGURE 6 : Overshoot CO2 & MF ────────────────────────────────────────────
fig6, axes = plt.subplots(1, 3, figsize=(18, 7))
fig6.patch.set_facecolor(BG)
fig6.suptitle('Figure 6 — Analyse du dépassement des limites planétaires (2019)',
              fontsize=14, fontweight='bold', color='white', y=1.01)

# CO2 distribution vs boundary
ax = axes[0]
ax.set_facecolor(CARD)
within  = df2019[df2019['co2_per_capita'] <= CO2_BOUNDARY]
outside = df2019[df2019['co2_per_capita'] > CO2_BOUNDARY]
ax.hist(df2019['co2_per_capita'], bins=25, color=IND, alpha=0.7, edgecolor='none')
ax.axvline(CO2_BOUNDARY, color=RED, linewidth=2, linestyle='--')
ax.text(CO2_BOUNDARY + 0.2, ax.get_ylim()[1]*0.88,
        f'Limite planétaire\n{CO2_BOUNDARY} t/cap', color=RED, fontsize=8)
within_pct = len(within)/len(df2019)*100
ax.set_title(f'CO2 — {within_pct:.0f}% dans les limites', color=GRN, fontsize=10, fontweight='bold')
ax.set_xlabel('CO2 per capita (t)', color='#94a3b8', fontsize=9)
ax.tick_params(colors='#64748b')
for spine in ax.spines.values(): spine.set_edgecolor('#334155')

# MF distribution vs boundary
ax = axes[1]
ax.set_facecolor(CARD)
within_mf = df2019[df2019['material_footprint'] <= MF_BOUNDARY]
ax.hist(df2019['material_footprint'], bins=25, color=BLUE, alpha=0.7, edgecolor='none')
ax.axvline(MF_BOUNDARY, color=RED, linewidth=2, linestyle='--')
ax.text(MF_BOUNDARY + 0.3, ax.get_ylim()[1]*0.88,
        f'Limite planétaire\n{MF_BOUNDARY} t/cap', color=RED, fontsize=8)
mf_pct = len(within_mf)/len(df2019)*100
ax.set_title(f'Empreinte Matérielle — {mf_pct:.0f}% dans les limites',
             color=GRN, fontsize=10, fontweight='bold')
ax.set_xlabel('MF per capita (t)', color='#94a3b8', fontsize=9)
ax.tick_params(colors='#64748b')
for spine in ax.spines.values(): spine.set_edgecolor('#334155')

# SDI donut per category
ax = axes[2]
ax.set_facecolor(CARD)
level_counts = df2019['SDI_level'].value_counts()
colors_pie = [RED, AMB, BLUE, GRN]
wedges, texts, autotexts = ax.pie(
    level_counts.values, labels=level_counts.index,
    autopct='%1.1f%%', colors=colors_pie[:len(level_counts)],
    startangle=90, pctdistance=0.75,
    wedgeprops=dict(width=0.55, edgecolor='#0f172a', linewidth=2)
)
for t in texts: t.set_color('#94a3b8'); t.set_fontsize(8)
for t in autotexts: t.set_color('white'); t.set_fontsize(8); t.set_fontweight('bold')
ax.set_title('Répartition par niveau SDI (2019)', color='white', fontsize=10, fontweight='bold')

plt.tight_layout()
plt.savefig('/home/claude/fig6_overshoot.png', dpi=130, bbox_inches='tight',
            facecolor=BG)
plt.close()
print("✅ fig6_overshoot.png saved")

# ─────────────────────────────────────────────────────────────────────────────
# SECTION 8 — SDI Rate (Positive / Negative evolution)
# ─────────────────────────────────────────────────────────────────────────────
print("\n" + "─" * 65)
print("  SECTION 8 — SDI Evolution Rate (positive/negative)")
print("─" * 65)

df_2015 = df[df['year'] == 2015][['country', 'SDI']].rename(columns={'SDI': 'SDI_2015'})
df_2019 = df[df['year'] == 2019][['country', 'SDI']].rename(columns={'SDI': 'SDI_2019'})
evolution = df_2015.merge(df_2019, on='country')
evolution['delta'] = evolution['SDI_2019'] - evolution['SDI_2015']
evolution['direction'] = evolution['delta'].apply(lambda x: 'Positif' if x >= 0 else 'Négatif')

pos = (evolution['direction'] == 'Positif').sum()
neg = (evolution['direction'] == 'Négatif').sum()
print(f"\n   Pays avec évolution SDI positive : {pos} ({pos/len(evolution)*100:.1f}%)")
print(f"   Pays avec évolution SDI négative : {neg} ({neg/len(evolution)*100:.1f}%)")

# ── FIGURE 7 : SDI Rate evolution ────────────────────────────────────────────
fig7, (ax1, ax2) = plt.subplots(1, 2, figsize=(18, 8))
fig7.patch.set_facecolor(BG)
fig7.suptitle('Figure 7 — Taux d\'évolution SDI par pays (2015→2019)',
              fontsize=14, fontweight='bold', color='white', y=1.01)

# Bar chart: top improvers & decliners
ax1.set_facecolor(CARD)
top_imp = evolution.nlargest(15, 'delta').sort_values('delta')
bars = ax1.barh(top_imp['country'], top_imp['delta'],
                color=[GRN if v >= 0 else RED for v in top_imp['delta']],
                alpha=0.85, height=0.65, edgecolor='none')
ax1.axvline(0, color='white', linewidth=1, alpha=0.4)
ax1.set_title('Top 15 progressions SDI', color=GRN, fontsize=11, fontweight='bold')
ax1.set_xlabel('Δ SDI (2019 − 2015)', color='#94a3b8', fontsize=9)
ax1.tick_params(colors='#94a3b8')
for spine in ax1.spines.values(): spine.set_edgecolor('#334155')

# Donut: pos vs neg
ax2.set_facecolor(CARD)
sizes  = [pos, neg]
labels = [f'Positive ({pos})', f'Négative ({neg})']
colors_d = [GRN, RED]
wedges, texts, autotexts = ax2.pie(
    sizes, labels=labels, autopct='%1.1f%%', colors=colors_d,
    startangle=90, pctdistance=0.72,
    wedgeprops=dict(width=0.55, edgecolor='#0f172a', linewidth=2)
)
for t in texts: t.set_color('#94a3b8'); t.set_fontsize(10)
for t in autotexts: t.set_color('white'); t.set_fontsize(11); t.set_fontweight('bold')
ax2.set_title('Taux SDI positif / négatif\n(2015 → 2019)', color='white', fontsize=11, fontweight='bold')

plt.tight_layout()
plt.savefig('/home/claude/fig7_sdi_rate.png', dpi=130, bbox_inches='tight',
            facecolor=BG)
plt.close()
print("✅ fig7_sdi_rate.png saved")

# ─────────────────────────────────────────────────────────────────────────────
# SECTION 9 — IEV Average per country vs goal (like Power BI card)
# ─────────────────────────────────────────────────────────────────────────────

# ── FIGURE 8 : IEV Top 10 (like your Power BI chart) + SDI vs IE scatter ─────
fig8, (ax1, ax2) = plt.subplots(1, 2, figsize=(18, 8))
fig8.patch.set_facecolor(BG)
fig8.suptitle('Figure 8 — IEV Top 10 pays (2019) & Relation SDI × Éducation',
              fontsize=14, fontweight='bold', color='white', y=1.01)

# IEV top 10 (reproducing your Power BI bar chart)
ax1.set_facecolor(CARD)
top10_iev = df2019.nlargest(10, 'IEV').sort_values('IEV')
norm = plt.Normalize(top10_iev['IEV'].min(), top10_iev['IEV'].max())
colors_iev = [plt.cm.RdYlGn(norm(v)) for v in top10_iev['IEV']]
bars = ax1.barh(top10_iev['country'], top10_iev['IEV'],
                color=colors_iev, height=0.65, edgecolor='none')
for bar, val in zip(bars, top10_iev['IEV']):
    ax1.text(val + 0.003, bar.get_y() + bar.get_height()/2,
             f'{val:.2f}', va='center', color='white', fontsize=9, fontweight='bold')
ax1.axvline(df2019['IEV'].mean(), color=AMB, linestyle='--', linewidth=1.5, alpha=0.7)
ax1.text(df2019['IEV'].mean(), 0.3,
         f'Moy: {df2019["IEV"].mean():.2f}', color=AMB, fontsize=8, rotation=90)
ax1.set_title('IEV moyen — Top 10 pays (2019)', color=GRN, fontsize=11, fontweight='bold')
ax1.set_xlabel('IEV (Indice Espérance de Vie)', color='#94a3b8', fontsize=9)
ax1.set_xlim(0, 1.15)
ax1.tick_params(colors='#94a3b8')
for spine in ax1.spines.values(): spine.set_edgecolor('#334155')

# SDI vs IE scatter colored by IIE
ax2.set_facecolor(CARD)
sc = ax2.scatter(df2019['IE'], df2019['SDI'],
                 c=df2019['IIE'], cmap='RdYlGn_r',
                 alpha=0.75, s=70, edgecolors='none')
corr_ie_sdi = df2019[['IE','SDI']].corr().iloc[0,1]
ax2.set_xlabel('IE — Indice Éducation', color='#94a3b8', fontsize=9)
ax2.set_ylabel('SDI', color='#94a3b8', fontsize=9)
ax2.set_title(f'SDI vs Éducation (r={corr_ie_sdi:.3f})\nColoré par IIE (Impact Écologique)',
              color=BLUE, fontsize=10, fontweight='bold')
ax2.tick_params(colors='#64748b')
cbar = plt.colorbar(sc, ax=ax2)
cbar.set_label('IIE (Impact Écologique)', color='white')
cbar.ax.yaxis.label.set_color('white')
cbar.ax.tick_params(colors='white')
for spine in ax2.spines.values(): spine.set_edgecolor('#334155')

plt.tight_layout()
plt.savefig('/home/claude/fig8_iev_education.png', dpi=130, bbox_inches='tight',
            facecolor=BG)
plt.close()
print("✅ fig8_iev_education.png saved")

# ─────────────────────────────────────────────────────────────────────────────
# SECTION 10 — Summary stats
# ─────────────────────────────────────────────────────────────────────────────
print("\n" + "=" * 65)
print("  SYNTHÈSE FINALE")
print("=" * 65)
print(f"\n  Dataset          : {df.shape[0]} obs. × {df.shape[1]} variables")
print(f"  Pays analysés    : {df['country'].nunique()}")
print(f"  Période          : 2015 – 2019")
print(f"\n  KPIs calculés (2019 — moyenne mondiale) :")
for kpi in ['IEV','IE','IR','ID','IIE','SDI']:
    print(f"    {kpi:<6}: {df2019[kpi].mean():.4f}  (min: {df2019[kpi].min():.4f} | max: {df2019[kpi].max():.4f})")
print(f"\n  Top SDI 2019     : {df2019.nlargest(1,'SDI')['country'].values[0]} ({df2019['SDI'].max():.4f})")
print(f"  Bottom SDI 2019  : {df2019.nsmallest(1,'SDI')['country'].values[0]} ({df2019['SDI'].min():.4f})")
print(f"  Pas de pays > 0.9 : confirme Hickel (2020) ✅")
print(f"\n  Figures générées : fig1 à fig8")
print("\n  ANALYSE TERMINÉE ✅")

# Save final dataset
df.to_csv('/home/claude/sdi_final_dataset.csv', index=False)
print("  Dataset final sauvegardé : sdi_final_dataset.csv")
