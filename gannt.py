import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime, timedelta

# --- Constants ---
START_PROJECT = datetime(2026, 1, 1)

def get_date_from_month(month_offset):
    # Month 1 is Start Date.
    year = START_PROJECT.year + (month_offset - 1) // 12
    month = (START_PROJECT.month + (month_offset - 1) - 1) % 12 + 1
    return datetime(year, month, 1)

def get_end_date_from_month(month_offset):
    # End of the specified month
    start_of_month = get_date_from_month(month_offset)
    # Start of next month
    if start_of_month.month == 12:
        next_month = datetime(start_of_month.year + 1, 1, 1)
    else:
        next_month = datetime(start_of_month.year, start_of_month.month + 1, 1)
    return next_month - timedelta(days=1)

# --- Data Definition ---
# Added M1 and M2 as requested
# Added M1 and M2 as requested
tasks_data = [
    {
        'Task': 'T1: EnM Division & EnMIS',
        'StartMonth': 1, 'EndMonth': 12,
        'Phase': 'Infrastructure',
        'Desc': 'Establish team, InfluxDB, Grafana',
        'Dependency': []
    },
    {
        'Task': 'T2: Compressed Air',
        'StartMonth': 6, 'EndMonth': 18,
        'Phase': 'Optimization',
        'Desc': 'Ultrasonic audits, 4.0 pressure control',
        'Dependency': []
    },
    {
        'Task': 'T3: Movement Efficiency',
        'StartMonth': 12, 'EndMonth': 30,
        'Phase': 'Optimization',
        'Desc': 'Regen drives, Smart Standby',
        'Dependency': []
    },
    {
        'Task': 'T4: Circular Thermal Mgmt',
        'StartMonth': 12, 'EndMonth': 36,
        'Phase': 'Optimization',
        'Desc': 'VFD on pumps/UTAs, Isarco integration',
        'Dependency': []
    },
    {
        'Task': 'T5: PV Load Shifting',
        'StartMonth': 18, 'EndMonth': 30,
        'Phase': 'Advanced',
        'Desc': 'Logic for MES/scheduling',
        'Dependency': ['T1', 'T4']
    },
    {
        'Task': 'M1: ISO 50001 Pre-Audit',
        'StartMonth': 24, 'EndMonth': 27,
        'Phase': 'Certification',
        'Desc': 'Pre-audit checks',
        'Dependency': ['T1', 'T2']
    },
    {
        'Task': 'M2: External Certification',
        'StartMonth': 30, 'EndMonth': 36,
        'Phase': 'Certification',
        'Desc': 'Final Certification',
        'Dependency': ['T3', 'T4', 'T5']
    }
]

# Calculate Dates
for task in tasks_data:
    task['Start'] = get_date_from_month(task['StartMonth'])
    task['End'] = get_end_date_from_month(task['EndMonth'])

df = pd.DataFrame(tasks_data)

# Convert for Matplotlib
df['Start_num'] = df['Start'].apply(mdates.date2num)
df['End_num'] = df['End'].apply(mdates.date2num)
df['Duration'] = df['End_num'] - df['Start_num']

# --- Styling ---
phase_colors = {
    'Infrastructure': '#1f77b4',  # Blue
    'Optimization': '#ff7f0e',    # Orange
    'Advanced': '#2ca02c',        # Green
    'Certification': '#d62728'    # Red
}
df['Color'] = df['Phase'].map(phase_colors)

# Reverse order for Gantt (Top = First item in list)
df = df.iloc[::-1].reset_index(drop=True)

# Helper to look up current index by Task Name substring
def get_idx(task_str):
    # Splits "T1: ..." to match "T1"
    matches = df[df['Task'].str.startswith(task_str)]
    if not matches.empty:
        return matches.index[0]
    return None

# --- Plotting ---
fig, ax = plt.subplots(figsize=(14, 9)) # Increased height for more tasks

# Create bars
bars = ax.barh(
    y=df.index,
    width=df['Duration'],
    left=df['Start_num'],
    color=df['Color'],
    edgecolor='black',
    height=0.6,
    alpha=0.9
)

# Text Labels
for i, row in df.iterrows():
    # Task Name
    ax.text(
        x=row['Start_num'], 
        y=i + 0.35, 
        s=f" {row['Task']}", 
        va='bottom', ha='left', 
        fontweight='bold', fontsize=11
    )
    # Description
    ax.text(
        x=row['Start_num'] + 5, 
        y=i, 
        s=f"{row['Desc']}", 
        va='center', ha='left', 
        color='white', fontsize=9, fontstyle='italic'
    )

# --- Formatting ---
ax.set_title('2026–2029 Strategic Energy Plan', fontsize=16, fontweight='bold', pad=20)
ax.set_xlabel('Timeline', fontsize=12)

# Date Axis
ax.xaxis.set_major_locator(mdates.YearLocator())
ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
ax.xaxis.set_minor_locator(mdates.MonthLocator(interval=3))
plt.xticks(fontsize=11)

# Remove Y Axis ticks
ax.set_yticks([])

# Grid
ax.grid(axis='x', linestyle='--', alpha=0.5)

# Limits
start_lim = mdates.date2num(datetime(2025, 12, 1)) # Start roughly nearby Jan 2026
end_lim = mdates.date2num(datetime(2029, 1, 31)) # End Jan 2029 (36 months after start)
ax.set_xlim(start_lim, end_lim)

# Legend
handles = [plt.Rectangle((0,0),1,1, color=color) for color in phase_colors.values()]
ax.legend(handles, phase_colors.keys(), loc='upper right', title="Phases")

plt.tight_layout()
filename = 'strategic_energy_plan_gantt.png'
plt.savefig(filename, dpi=300)
print(f"Saved {filename}")