import pandas as pd
import plotly.graph_objects as go

import os

# Get the directory of the current script
script_dir = os.path.dirname(os.path.abspath(__file__))

# Read monthly data
monthly_data = pd.read_csv(os.path.join(script_dir, "montly_data.csv"), sep=";")

# Calculate totals
pv_tot = monthly_data["PV production [kWh]"].sum()
pv_sold = monthly_data["Sold [kWh]"].sum()
pv_consumed = monthly_data["Self-consumed [kWh]"].sum()
grid_bought = monthly_data["Bought [kWh]"].sum()

# Read consumption sectors data
sectors_df = pd.read_csv(os.path.join(script_dir, "sectors.csv"), sep=";")

# 1. Define the Nodes
nodes_labels = ["PV", "GRID", "TOTAL ELECTRICAL CONSUMPTION"]
node_map = {label: i for i, label in enumerate(nodes_labels)}

# Process sectors data to create nodes
total_consumption_value = sectors_df["Consumption [kWh/year]"].sum()

sectors = []
sub_sectors = {}

# Group by Sector to aggregate consumption
grouped = sectors_df.groupby("Sector")

for sector_name, group in grouped:
    sector_consumption = group["Consumption [kWh/year]"].sum()
    percentage = (sector_consumption / total_consumption_value) * 100
    label = f"{sector_name} ({percentage:.1f}%)"

    sectors.append({"name": sector_name, "consumption": sector_consumption})
    sub_sectors[sector_name] = []

    if sector_name not in node_map:
        node_map[sector_name] = len(nodes_labels)
        nodes_labels.append(label)

    for _, row in group.iterrows():
        sub_name = row["Subsector"]
        sub_consumption = row["Consumption [kWh/year]"]
        
        sub_sectors[sector_name].append(
            {"name": sub_name, "consumption": sub_consumption}
        )
        
        if sub_name not in node_map:
            sub_percentage = (sub_consumption / total_consumption_value) * 100
            sub_label = f"{sub_name} ({sub_percentage:.1f}%)"
            node_map[sub_name] = len(nodes_labels)
            nodes_labels.append(sub_label)

# 2. Define the Links
source_links = [0, 0, 1]
target_links = [1, 2, 2]
value_links = [pv_sold, pv_consumed, grid_bought]

total_consumption_node_index = node_map["TOTAL ELECTRICAL CONSUMPTION"]

# Add links from TOTAL ELECTRICAL CONSUMPTION to sectors
for sector in sectors:
    source_links.append(total_consumption_node_index)
    target_links.append(node_map[sector["name"]])
    value_links.append(sector["consumption"])

# Add links from sectors to sub-sectors
for sector_name, sub_sector_list in sub_sectors.items():
    sector_node_index = node_map[sector_name]
    for sub in sub_sector_list:
        source_links.append(sector_node_index)
        target_links.append(node_map[sub["name"]])
        value_links.append(sub["consumption"])

# Create Sankey diagram
data_trace = go.Sankey(
    node=dict(
        pad=15,
        thickness=20,
        line=dict(color="black", width=0.5),
        label=nodes_labels,
    ),
    link=dict(source=source_links, target=target_links, value=value_links),
)

fig = go.Figure(data=[data_trace])

fig.update_layout(title_text="Energy Flow Sankey Diagram", font_size=10)
fig.show()
