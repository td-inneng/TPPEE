import pandas as pd
import plotly.graph_objects as go

import os

# Get the directory of the current script
script_dir = os.path.dirname(os.path.abspath(__file__))

# Read production data
pv = pd.read_csv(os.path.join(script_dir, "pv.csv"))

pv_tot = pv["Electricity produced [kWh]"].iloc[-1]
pv_sold = pv["Electricity sold to the network [kWh]"].iloc[-1]
pv_consumed = pv["Electricity self-consumed [kWh]"].iloc[-1]

# Read grid data
grid = pd.read_csv(os.path.join(script_dir, "grid.csv"))
grid_bought = grid["Energy drawn from the grid POD IT007E00050692 [kWh]"].iloc[-1]

# Read consumption sectors data
sectors_df = pd.read_csv(os.path.join(script_dir, "Sectors_consumption.csv"))

# 1. Define the Nodes
nodes_labels = ["PV", "GRID", "TOTAL ELECTRICAL CONSUMPTION"]
node_map = {label: i for i, label in enumerate(nodes_labels)}

# Process sectors data to create nodes
total_consumption_value = sectors_df.loc[
    sectors_df["Sector"] == "TOTAL", "Consumption [kWh/year]"
].iloc[0]
sectors = []
sub_sectors = {}
current_sector = None

for index, row in sectors_df.iterrows():
    name = row["Sector"].strip()

    if name == "TOTAL":
        continue

    consumption = row["Consumption [kWh/year]"]
    percentage = (consumption / total_consumption_value) * 100
    label = f"{name} ({percentage:.1f}%)"

    if name.isupper():
        current_sector = name
        sectors.append({"name": name, "consumption": consumption})
        sub_sectors[current_sector] = []
        if name not in node_map:
            node_map[name] = len(nodes_labels)
            nodes_labels.append(label)
    else:
        if current_sector:
            sub_sectors[current_sector].append(
                {"name": name, "consumption": consumption}
            )
            if name not in node_map:
                node_map[name] = len(nodes_labels)
                nodes_labels.append(label)

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
