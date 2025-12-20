import pandas as pd
import plotly.graph_objects as go
from pathlib import Path
from typing import Dict, List, Tuple

# --- Color Palette ---
COLOR_PALETTE = {
    "PV": "rgba(120, 190, 51, 0.8)",         # Distinct Chartreuse Green
    "GRID": "rgba(128, 128, 128, 0.8)",     # Grey
    "TOTAL ELECTRICAL CONSUMPTION": "rgba(31, 119, 180, 0.8)", # Default Blue
    
    # Specific Sector Colors (matching activity_density_plot.py)
    "MAIN ACTIVITIES": "rgba(31, 119, 180, 0.8)",    # Blue
    "AUXILIARY SERVICES": "rgba(255, 127, 14, 0.8)", # Orange
    "GENERAL SERVICES": "rgba(44, 160, 44, 0.8)",    # Standard Green
    
    "SUBSECTOR": "rgba(173, 216, 230, 0.8)",  # Light Blue
}

# --- Helper Functions ---

def load_data(file_path: Path) -> pd.DataFrame:
    """Loads data from a semicolon-separated CSV file."""
    if not file_path.is_file():
        raise FileNotFoundError(f"Data file not found at: {file_path}")
    return pd.read_csv(file_path, sep=";")

def prepare_sankey_data(monthly_df: pd.DataFrame, sectors_df: pd.DataFrame) -> Tuple[Dict, Dict]:
    """
    Prepares the nodes and links for the Sankey diagram. Nodes are ordered for better layout.
    """
    # 1. Calculate total energy flows
    pv_sold = monthly_df["Sold [kWh]"].sum()
    pv_consumed = monthly_df["Self-consumed [kWh]"].sum()
    grid_bought = monthly_df["Bought [kWh]"].sum()
    
    # 2. Define node order and types for a clearer layout
    main_node_names = ["PV", "GRID", "TOTAL ELECTRICAL CONSUMPTION"]
    sector_node_names = sorted(sectors_df['Sector'].unique())
    sub_sector_node_names = sorted(sectors_df['Subsector'].unique())
    
    ordered_node_names = main_node_names + sector_node_names + sub_sector_node_names
    node_map = {name: i for i, name in enumerate(ordered_node_names)}
    
    node_types = (
        ['main'] * len(main_node_names) +
        ['sector'] * len(sector_node_names) +
        ['subsector'] * len(sub_sector_node_names)
    )

    # 3. Create node labels with consumption data
    nodes_with_data = {}
    total_consumption_value = sectors_df["Consumption [kWh/year]"].sum()

    for sector_name in sector_node_names:
        sector_consumption = sectors_df[sectors_df['Sector'] == sector_name]['Consumption [kWh/year]'].sum()
        percentage = (sector_consumption / total_consumption_value) * 100
        nodes_with_data[sector_name] = {"label": f"<b>{sector_name}<br>({percentage:.1f}%)</b>", "consumption": sector_consumption}
        
    for _, row in sectors_df.iterrows():
        sub_name = row["Subsector"]
        sub_consumption = row["Consumption [kWh/year]"]
        sub_percentage = (sub_consumption / total_consumption_value) * 100
        # Included bold formatting for clearer visibility
        nodes_with_data[sub_name] = {"label": f"<b>{sub_name}<br>({sub_percentage:.1f}%)</b>"}

    # 4. Define all links between nodes
    links = {"source": [], "target": [], "value": []}
    
    def add_link(source: str, target: str, value: float):
        if value > 0:
            links["source"].append(node_map[source])
            links["target"].append(node_map[target])
            links["value"].append(value)
            
    add_link("PV", "GRID", pv_sold)
    add_link("PV", "TOTAL ELECTRICAL CONSUMPTION", pv_consumed)
    add_link("GRID", "TOTAL ELECTRICAL CONSUMPTION", grid_bought)
    
    for sector_name in sector_node_names:
        add_link("TOTAL ELECTRICAL CONSUMPTION", sector_name, nodes_with_data[sector_name]["consumption"])
        
    for _, row in sectors_df.iterrows():
        add_link(row['Sector'], row['Subsector'], row['Consumption [kWh/year]'])
        
    # 5. Prepare final node and link dictionaries for Plotly
    
    # Calculate node colors
    subsector_to_sector = dict(zip(sectors_df['Subsector'], sectors_df['Sector']))
    node_colors = []
    
    for name, n_type in zip(ordered_node_names, node_types):
        if name in COLOR_PALETTE:
            node_colors.append(COLOR_PALETTE[name])
        elif n_type == 'subsector' and name in subsector_to_sector:
            parent_sector = subsector_to_sector[name]
            # Use parent sector color (same as arrow)
            node_colors.append(COLOR_PALETTE.get(parent_sector, "rgba(200, 200, 200, 0.8)"))
        else:
            node_colors.append("rgba(200, 200, 200, 0.8)")

    sankey_nodes = {
        "label": [nodes_with_data.get(name, {"label": f"<b>{name}</b>"})["label"] for name in ordered_node_names],
        "name": ordered_node_names,
        "type": node_types,
        "color": node_colors,
    }
    
    return sankey_nodes, links

def create_sankey_figure(nodes: Dict, links: Dict) -> go.Figure:
    """Creates and styles the Sankey diagram figure with custom colors."""
    
    node_colors = nodes["color"]
    link_colors = [node_colors[s].replace("0.8", "0.4") for s in links["source"]]

    trace = go.Sankey(
        node=dict(
            pad=30,  # Increased padding for cleaner separation
            thickness=40, # Thicker nodes for "squared" look
            line=dict(color="black", width=1), # Sharp edges
            label=nodes["label"],
            color=node_colors,
        ),
        link=dict(
            source=links["source"],
            target=links["target"],
            value=links["value"],
            color=link_colors,
        ),
    )
    
    fig = go.Figure(data=[trace])
    fig.update_layout(
        title_text="<b>Energy Flow Sankey Diagram</b>",
        title_font_size=24,
        font=dict(size=14, family="Arial"), # Larger, clearer font
    )
    return fig

def main():
    """Main function to generate and show the Sankey diagram."""
    try:
        script_dir = Path(__file__).parent
        
        monthly_data = load_data(script_dir / "data" / "montly_data.csv")
        sectors_data = load_data(script_dir / "data" / "sectors.csv")
        
        nodes, links = prepare_sankey_data(monthly_data, sectors_data)
        
        fig = create_sankey_figure(nodes, links)
        fig.show()
        
    except FileNotFoundError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()