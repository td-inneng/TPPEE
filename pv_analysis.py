import pandas as pd
import matplotlib.pyplot as plt

# --- Plotting Function (modified to accept column names) ---
def plot_energy_data(df, self_consumed_col, bought_col, title):
    """
    Plots a stacked bar chart for monthly energy data.
    """
    try:
        months = df['Month']
        self_consumed = df[self_consumed_col]
        bought = df[bought_col]

        plt.figure(figsize=(10, 6))
        
        p1 = plt.bar(months, self_consumed, label='Self-consumed')
        p2 = plt.bar(months, bought, bottom=self_consumed, label='Bought from Grid')
        
        for i, (sc, b) in enumerate(zip(self_consumed, bought)):
            total = sc + b
            if total > 0:
                percentage = (sc / total) * 100
                plt.text(i, sc/2, f'{percentage:.1f}%', ha='center', va='center', color='white', fontsize=8)
        
        plt.xlabel('Month')
        plt.ylabel('Energy (kWh)')
        plt.title(title)
        plt.xticks(rotation=45)
        plt.legend()
        plt.tight_layout()
        plt.show()
        
    except KeyError as e:
        print(f"Missing columns for plotting: {e}")
    except Exception as e:
        print(f"Error plotting data: {e}")

# Load data
monthly_data = pd.read_csv('data/montly_data.csv', sep=';')

# --- Base Scenario ---
print("--- Base Scenario ---")
original_self_consumption_sum = monthly_data['Self-consumed [kWh]'].sum()
original_total_need_sum = monthly_data['Total need [kWh]'].sum()
original_self_consumption_percentage = original_self_consumption_sum / original_total_need_sum
print(f"Original Self-consumption: {original_self_consumption_percentage*100:.2f}%")

original_energy_sold_to_grid = monthly_data['Sold [kWh]'].sum()
print(f"Original Energy Sold to Grid: {original_energy_sold_to_grid:.2f} kWh")

plot_energy_data(monthly_data, 'Self-consumed [kWh]', 'Bought [kWh]', 'Original Monthly Energy Consumption')


# --- Increased PV Scenario ---
print("\n--- Increased PV Scenario ---")
capacity_pv = 938.80
incresed_pv = capacity_pv + 200.00
increase_factor = incresed_pv / capacity_pv

monthly_data['New PV production [kWh]'] = monthly_data['PV production [kWh]'] * increase_factor
monthly_data['New Self-consumed [kWh]'] = monthly_data['Self-consumed [kWh]'] * increase_factor
monthly_data['New Bought [kWh]'] = monthly_data['Total need [kWh]'] - monthly_data['New Self-consumed [kWh]']
monthly_data['New Bought [kWh]'] = monthly_data['New Bought [kWh]'].apply(lambda x: max(0, x))
monthly_data['New Sold [kWh]'] = monthly_data['New PV production [kWh]'] - monthly_data['New Self-consumed [kWh]']
monthly_data['New Sold [kWh]'] = monthly_data['New Sold [kWh]'].apply(lambda x: max(0, x))

new_self_consumption_sum = monthly_data['New Self-consumed [kWh]'].sum()
new_self_consumption_percentage = new_self_consumption_sum / original_total_need_sum
print(f"New Self-consumption with increased PV: {new_self_consumption_percentage*100:.2f}%")

new_energy_sold_to_grid = monthly_data['New Sold [kWh]'].sum()
print(f"New Energy Sold to Grid: {new_energy_sold_to_grid:.2f} kWh")

plot_energy_data(monthly_data, 'New Self-consumed [kWh]', 'New Bought [kWh]', 'Increased PV Scenario Monthly Energy Consumption')
