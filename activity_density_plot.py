import pandas as pd
import matplotlib.pyplot as plt
import os

# --- Constants ---
UNITS_PRODUCED = 251184

# --- Load Data ---
script_dir = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.join(script_dir, "data/sectors.csv")

try:
    df = pd.read_csv(csv_path, sep=';')
except FileNotFoundError:
    print(f"Error: The file {csv_path} was not found.")
    exit()

# --- Calculations ---
# User requested "density of consumption maybe in W/unit".
# Interpreting this as Specific Energy Consumption: Energy (Wh) per Unit produced.
# Formula: (kWh/year * 1000 Wh/kWh) / (Units/year) = Wh/unit
df['Density (Wh/unit)'] = (df['Consumption [kWh/year]'] * 1000) / UNITS_PRODUCED

# Sort by consumption density for better readability
df = df.sort_values(by='Density (Wh/unit)', ascending=False)

# Define colors based on Sector
sector_colors = {
    'MAIN ACTIVITIES': '#1f77b4',      # Blue
    'AUXILIARY SERVICES': '#ff7f0e',   # Orange
    'GENERAL SERVICES': '#2ca02c'      # Green
}
colors = df['Sector'].map(sector_colors)

# --- Plotting ---
plt.figure(figsize=(14, 8))

bars = plt.bar(
    df['Subsector'], 
    df['Density (Wh/unit)'], 
    color=colors,
    edgecolor='black',
    linewidth=0.5
)

# Titles and Labels
plt.title("Energy Consumption Density by Activity", fontsize=18, fontweight='bold')
plt.xlabel("Activity", fontsize=14)
plt.ylabel("Consumption Density (Wh/unit)", fontsize=14)

# Ticks styling
plt.xticks(rotation=45, ha='right', fontsize=12)
plt.yticks(fontsize=12)

# Grid
plt.grid(axis='y', linestyle='--', alpha=0.7)

# Add value labels on top of bars
for bar in bars:
    height = bar.get_height()
    plt.text(
        bar.get_x() + bar.get_width() / 2.0, 
        height + 5, # Offset slightly
        f"{height:.1f}", 
        ha='center', 
        va='bottom', 
        fontsize=10, 
        fontweight='bold'
    )

plt.tight_layout()

# --- Save Plot ---
output_path = os.path.join(script_dir, "activity_density_plot.png")
plt.savefig(output_path)
print(f"Plot saved to {output_path}")

# plt.show()
