import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime, timedelta

# 1. Definition of Tasks and Duration
# We use a 'Task', 'Start Date', 'End Date' format
# Fictitious start date: 2026-01-01

tasks_data = [
    {'Task': 'T1: Team & EnMIS Setup', 'Start': '2026-01-01', 'End': '2026-06-30', 'Phase': 'Foundation'},
    {'Task': 'T2: Compressed Air Opt.', 'Start': '2026-03-01', 'End': '2027-03-01', 'Phase': 'Execution'},
    {'Task': 'T4: PV Expansion Install.', 'Start': '2026-06-01', 'End': '2027-01-31', 'Phase': 'Execution'},
    {'Task': 'T3: Milling Center Logic', 'Start': '2026-08-01', 'End': '2027-05-01', 'Phase': 'Execution'},
    {'Task': 'Operative Checks (T5)', 'Start': '2026-09-01', 'End': '2027-03-30', 'Phase': 'Execution'},
    {'Task': 'Internal Audit & Check', 'Start': '2027-01-01', 'End': '2028-01-31', 'Phase': 'Maturity'},
    {'Task': 'Certification Objective', 'Start': '2028-01-01', 'End': '2028-01-31', 'Phase': 'Maturity'}
]

df = pd.DataFrame(tasks_data)

# Converti le date in formato numerico (necessario per matplotlib)
df['Start_date'] = pd.to_datetime(df['Start'])
df['End_date'] = pd.to_datetime(df['End'])
df['Duration'] = df['End_date'] - df['Start_date']
df['Start_num'] = df['Start_date'].apply(mdates.date2num)

# Assegna un colore in base alla fase
phase_colors = {
    'Foundation': '#1f77b4',  # Blu
    'Execution': '#ff7f0e',   # Arancione
    'Maturity': '#2ca02c'     # Verde
}
df['Color'] = df['Phase'].map(phase_colors)

# 2. Creazione del Grafico

fig, ax = plt.subplots(figsize=(12, 6))

# Crea le barre orizzontali
ax.barh(
    y=df['Task'],
    width=df['Duration'].dt.days,
    left=df['Start_num'],
    color=df['Color']
)

# Aggiungi etichette ai nomi delle barre
for i, row in df.iterrows():
    # Posiziona il testo all'inizio della barra con un piccolo offset
    ax.text(
        x=row['Start_num'] + 5,  # Aggiungi un piccolo offset per non sovrapporre il bordo
        y=i,
        s=row['Task'],
        va='center',
        ha='left',
        color='black',
        fontsize=10 # Aumenta la dimensione del font per maggiore leggibilità
    )

# 3. Formattazione dell'Asse X (Date)

# Converti i numeri di matplotlib in date leggibili
formatter = mdates.DateFormatter('%b %Y')
ax.xaxis.set_major_formatter(formatter)

# Imposta l'intervallo dell'asse X (Major ticks)
ax.xaxis.set_major_locator(mdates.MonthLocator(interval=6))
ax.xaxis.set_minor_locator(mdates.MonthLocator(interval=3))

# Rotazione delle etichette per leggibilità
plt.xticks(rotation=45, ha='right')

# 4. Aggiunta Dettagli Grafici

ax.set_title('Energy Audit Action Plan: Implementation Gantt (24 Months)', fontsize=14)
ax.set_xlabel('Timeline')
ax.grid(axis='x', linestyle='--', alpha=0.7)

# Invert the Y axis to have the most important tasks at the top
ax.invert_yaxis()

# Create legend for the phases
handles = [plt.Rectangle((0,0),1,1, color=phase_colors[label]) for label in phase_colors]
ax.legend(handles, phase_colors.keys(), title="Phases", loc='upper right')

plt.tight_layout()
plt.savefig('gantt_chart_energy_audit.png')
print("Gantt chart saved as 'gantt_chart_energy_audit.png'")