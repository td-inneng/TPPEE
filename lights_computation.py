import numpy as np
import pandas as pd
import os

##difine the variables
Ground_floor_power = 31.86
First_floor_power = 33.66
Second_floor_power = 8.68

ground_first_M_T_time = 16 * 4
ground_first_F_time = 6
second_M_T_time = 11 * 4
second_F_time = 5

# compute the power consumption

weekly_Ground_floor_power_consumption = Ground_floor_power * (
    ground_first_M_T_time + ground_first_F_time
)
weekly_First_floor_power_consumption = First_floor_power * (
    ground_first_M_T_time + ground_first_F_time
)
weekly_Second_floor_power_consumption = Second_floor_power * (
    second_M_T_time + second_F_time
)


weekly_Total_power_consumption = round(
    weekly_Ground_floor_power_consumption
    + weekly_First_floor_power_consumption
    + weekly_Second_floor_power_consumption
)
total_power_consumption = round(weekly_Total_power_consumption * 52)
print("Ground floor power consumption: ", weekly_Ground_floor_power_consumption)
print("First floor power cclonsumption: ", weekly_First_floor_power_consumption)
print("Second floor power consumption: ", weekly_Second_floor_power_consumption)
print("Total power consumption: ", weekly_Total_power_consumption)
print("Total power consumption: ", total_power_consumption)
results_df = pd.DataFrame(
    {
        "Floor": [
            "Ground Floor_weekly",
            "First Floor_weekly",
            "Second Floor_weekly",
            "Total_Weekly",
            "Total_yearly",
        ],
        "Power Consumption (kWh)": [
            weekly_Ground_floor_power_consumption,
            weekly_First_floor_power_consumption,
            weekly_Second_floor_power_consumption,
            weekly_Total_power_consumption,
            total_power_consumption,
        ],
    }
)
# Get the directory of the current script
script_dir = os.path.dirname(os.path.abspath(__file__))
output_path = os.path.join(script_dir, "lights_power_consumption.csv")

results_df.to_csv(output_path, index=False)
print(f"\nResults saved to {output_path}")
