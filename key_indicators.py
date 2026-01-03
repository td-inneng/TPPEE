import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# data definition
sectors_path = Path(__file__).parent / "data" / "sectors.csv"
sectors_df = pd.read_csv(sectors_path, sep=";")

yearly_products = 251184

# calculation
consumption_per_product = sectors_df
consumption_per_product["Consumption [kWh/product]"] = (
    consumption_per_product["Consumption [kWh/year]"] / yearly_products
)

consumption_per_product = consumption_per_product.sort_values(
    by="Consumption [kWh/product]", ascending=False
)

consumption_per_product.to_csv(
    Path(__file__).parent / "data" / "consumption_per_product.csv", index=False
)

# visualization
plt.figure(figsize=(12, 7))
colors = plt.cm.viridis(
    consumption_per_product["Consumption [kWh/product]"]
    / consumption_per_product["Consumption [kWh/product]"].max()
)
plt.bar(
    consumption_per_product["Subsector"],
    consumption_per_product["Consumption [kWh/product]"] * 1000,
    color=colors,
)
plt.xlabel("Subsector")
plt.ylabel("Consumption [Wh/product]")
plt.title("Consumption per Product by Subsector")
plt.xticks(rotation=45, ha="right")
plt.tight_layout()

plt.show()

total_consumption = consumption_per_product["Consumption [kWh/product]"]
print("Total Consumption [kWh/product]:", total_consumption.sum())
