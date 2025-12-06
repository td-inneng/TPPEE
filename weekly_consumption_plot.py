import pandas as pd
import matplotlib.pyplot as plt
import os

# Get the directory of the current script
script_dir = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.join(script_dir, "lights_power_consumption.csv")

# Load the data
try:
    df = pd.read_csv(csv_path)
except FileNotFoundError:
    print(f"Error: The file {csv_path} was not found.")
    exit()

# Filter for the weekly data of the specific floors
floors_of_interest = [
    "Ground Floor_weekly",
    "First Floor_weekly",
    "Second Floor_weekly",
]
df_filtered = df[df["Floor"].isin(floors_of_interest)]

# Create the bar plot
plt.figure(figsize=(10, 6))
bars = plt.bar(
    df_filtered["Floor"],
    df_filtered["Power Consumption (kWh)"],
    color=["#1f77b4", "#ff7f0e", "#2ca02c"],
)

# Add title and labels
plt.title("Weekly Power Consumption by Floor", fontsize=16)
plt.xlabel("Floor", fontsize=12)
plt.ylabel("Power Consumption (kWh)", fontsize=12)

# Add value labels on top of the bars
for bar in bars:
    height = bar.get_height()
    plt.text(
        bar.get_x() + bar.get_width() / 2.0,
        height,
        f"{height}",
        ha="center",
        va="bottom",
    )

# Save the plot
output_path = os.path.join(script_dir, "weekly_consumption_plot.png")
plt.savefig(output_path)
print(f"Plot saved to {output_path}")

# Show the plot (optional, but good for local debugging if run interactively, though we are in headless mostly)
# plt.show()
