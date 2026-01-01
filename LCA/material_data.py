import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# Set the aesthetics
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['Arial', 'Helvetica', 'DejaVu Sans']
plt.rcParams['axes.titleweight'] = 'bold'

# Data
data = {
    "Tempered glass": 46.693,
    "Aluminium": 7.371,
    "Stainless steel": 0.132,
    "ZAMa (Zinc alloy)": 0.482,
    "Brass (alloy of copper and zinc)": 0.03,
    "PA (polyamide)": 0.023,
    "PA+GF": 0.02,
    "PC (polycarbonate)": 0.007,
    "ABS (thermoplastic)": 0.025,
    "PVC (Polyvinyl Chloride)": 0.59,
    "Neodymium Magnet": 0.055,
    "General materials": 1,
    "Corrugated cardboard": 11.072,
    "Polystyrène": 1.744,
    "Hot melt adhesive": 0.05,
    "Transparent PVC film": 0.004
}

total_input = 69.298

# Group definitions
groups = {
    "Glass": ["Tempered glass"],
    "Cardboard & Paper": ["Corrugated cardboard"],
    "Aluminium": ["Aluminium"],
    "Polymers": ["Polystyrène", "PVC (Polyvinyl Chloride)", "PA (polyamide)", "PA+GF", "PC (polycarbonate)", "ABS (thermoplastic)", "Transparent PVC film"],
    "Other Metals": ["ZAMa (Zinc alloy)", "Stainless steel", "Neodymium Magnet", "Brass (alloy of copper and zinc)"],
    "Others": ["General materials", "Hot melt adhesive"]
}

# Aggregate data
grouped_data = {}
for group, items in groups.items():
    grouped_data[group] = sum(data[item] for item in items)

# Verify sum
calculated_sum = sum(grouped_data.values())
print(f"Calculated Sum: {calculated_sum:.3f}")
print(f"Target Sum: {total_input}")

# Calculate percentages
# The user asked to calculate on Total Material Input (69.298)
percentages = {k: (v / total_input) * 100 for k, v in grouped_data.items()}

# Prepare for plotting
df = pd.DataFrame(list(percentages.items()), columns=['Material', 'Percentage'])
df = df.sort_values('Percentage', ascending=True)

# Plotting
fig, ax = plt.subplots(figsize=(10, 6))

# Colors (Premium Palette)
colors = ['#E0E0E0', '#B0BEC5', '#90CAF9', '#64B5F6', '#42A5F5', '#1E88E5']
# Or map specific colors to materials for better semantics
color_map = {
    "Glass": "#4DB6AC",         # Teal
    "Cardboard & Paper": "#D4E157", # Lime/Yellowish
    "Aluminium": "#90A4AE",     # Blue Grey
    "Polymers": "#FF8A65",      # Deep Orange
    "Other Metals": "#A1887F",  # Brown
    "Others": "#E0E0E0"         # Grey
}
bar_colors = [color_map.get(m, '#E0E0E0') for m in df['Material']]

bars = ax.barh(df['Material'], df['Percentage'], color=bar_colors, edgecolor='white', height=0.6)

# Labels and Title
ax.set_xlabel('Percentage by Weight (%)', fontsize=12, labelpad=10)
# ax.set_ylabel('Material Group', fontsize=12) # Labels are on Y axis
ax.set_title('Material Input Distribution (Weight %)', fontsize=16, pad=20)

# Add value labels
for bar in bars:
    width = bar.get_width()
    ax.text(width + 0.5, bar.get_y() + bar.get_height()/2, 
            f'{width:.1f}%', va='center', fontsize=11, fontweight='bold', color='#333333')

# Clean up axes
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_visible(False)
ax.spines['bottom'].set_color('#DDDDDD')
ax.tick_params(axis='y', length=0)
ax.grid(axis='x', linestyle='--', alpha=0.5, color='#CCCCCC')

# Add the note
note_text = "Note: Calculated on Total Material Input to account for manufacturing scraps and process efficiency"
fig.text(0.5, 0.02, note_text, ha='center', fontsize=9, style='italic', color='#666666')

plt.tight_layout()
plt.subplots_adjust(bottom=0.15) # Make room for the note

# Save Bar Chart
output_path_bar = 'LCA/material_distribution_bar.png'
plt.savefig(output_path_bar, dpi=300, bbox_inches='tight')
print(f"Bar chart saved to {output_path_bar}")

# --- Donut Chart ---
fig2, ax2 = plt.subplots(figsize=(10, 8))

# Prepare data for donut (ensure sorted for consistency)
# Use same colors
colors_mapped = [color_map.get(m, '#E0E0E0') for m in df['Material']]

# Wedgeprops for separation
wedges, texts, autotexts = ax2.pie(df['Percentage'], labels=None, autopct='', startangle=90, 
                                   pctdistance=0.85, colors=colors_mapped, wedgeprops=dict(width=0.4, edgecolor='w'))

# Add legend nicely
ax2.legend(wedges, df['Material'], title="Materials", loc="center left", bbox_to_anchor=(1, 0, 0.5, 1))

# Add percentages manually to look cleaner or just rely on the legend/table?
# Let's put labels with lines if possible, or just the main ones inside.
# Given small slices, standard pie labels might overlap.
# Let's use a list on the side or just the legend.
# We'll calculate labels for the legend: "Name (X.X%)"
legend_labels = [f"{m} ({p:.1f}%)" for m, p in zip(df['Material'], df['Percentage'])]
ax2.legend(wedges, legend_labels, title="Materials", loc="center left", bbox_to_anchor=(1, 0, 0.5, 1))


ax2.set_title('Material Input Composition', fontsize=16, fontweight='bold')

# Center text
ax2.text(0, 0, f'Total\n{total_input:,.1f} kg', ha='center', va='center', fontsize=14, fontweight='bold', color='#555555')

# Add the note
fig2.text(0.5, 0.05, note_text, ha='center', fontsize=9, style='italic', color='#666666')

# Save Donut Chart
output_path_donut = 'LCA/material_distribution_donut.png'
plt.tight_layout()
plt.subplots_adjust(bottom=0.15)
plt.savefig(output_path_donut, dpi=300, bbox_inches='tight')
print(f"Donut chart saved to {output_path_donut}")

# --- Detailed Bar Charts per Category ---
import re

for group_name, items in groups.items():
    if len(items) <= 1:
        continue # Skip categories with single item (redundant)
        
    # Extract sub-data
    sub_data = {item: data[item] for item in items}
    sub_total = sum(sub_data.values())
    
    # Sort for visual appeal
    sub_df = pd.DataFrame(list(sub_data.items()), columns=['Material', 'Weight'])
    sub_df['RelativePercentage'] = (sub_df['Weight'] / sub_total) * 100 # For the chart slices
    sub_df['TotalPercentage'] = (sub_df['Weight'] / total_input) * 100  # For the labels
    sub_df = sub_df.sort_values('Weight', ascending=True) # Ascending for BarH
    
     # Plot - Horizontal Bar Chart
    fig3, ax3 = plt.subplots(figsize=(10, 6))
    
    # Colors
    base_color_hex = color_map.get(group_name, '#9E9E9E')
    # Create valid color list
    bar_colors = [base_color_hex] * len(sub_df)
    
    bars = ax3.barh(sub_df['Material'], sub_df['TotalPercentage'], color=bar_colors, edgecolor='white', height=0.6)
    
    # Add values
    for i, bar in enumerate(bars):
        width = bar.get_width()
        weight = sub_df.iloc[i]['Weight']
        label_text = f"{weight:.3f} kg ({width:.3f}%)"
        ax3.text(width + (0.005 if width < 0.05 else 0.05), bar.get_y() + bar.get_height()/2, 
                 label_text, va='center', fontsize=10, fontweight='bold', color='#333333')

    # Add 1% Threshold Line
    ax3.axvline(x=1.0, color='red', linestyle='--', linewidth=1.5, alpha=0.7)
    # Add text for threshold
    ax3.text(1.0, ax3.get_ylim()[1], ' 1% Threshold', color='red', va='bottom', ha='center', fontsize=9, fontweight='bold')

    # Formatting
    ax3.set_xlabel('Percentage of Total Input (%)', fontsize=12)
    ax3.set_title(f'{group_name} Detailed Breakdown', fontsize=14, fontweight='bold', pad=20)
    
    # Clean up axes
    ax3.spines['top'].set_visible(False)
    ax3.spines['right'].set_visible(False)
    ax3.spines['left'].set_visible(False)
    ax3.spines['bottom'].set_color('#DDDDDD')
    ax3.grid(axis='x', linestyle='--', alpha=0.5, color='#CCCCCC')
    
    # Add Note
    fig3.text(0.5, 0.02, note_text, ha='center', fontsize=8, style='italic', color='#666666')
    
    plt.tight_layout()
    plt.subplots_adjust(bottom=0.15)
    
    # Save
    safe_name = re.sub(r'[^a-zA-Z0-9]', '_', group_name).lower()
    output_path_sub = f'LCA/material_distribution_detail_{safe_name}_bar.png'
    plt.savefig(output_path_sub, dpi=300, bbox_inches='tight')
    print(f"Detailed chart for {group_name} saved to {output_path_sub}")
    plt.close(fig3) # Close to free memory
