import pandas as pd
import os

def print_data_summary(file_path):
    """
    Reads a CSV file and prints a summary of its content.
    """
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return

    try:
        # Read the CSV file
        # Using sep=None to automatically detect separator (common issue with ; vs ,)
        df = pd.read_csv(file_path, sep=None, engine='python')
        
        print(f"\n{'='*40}")
        print(f"File: {os.path.basename(file_path)}")
        print(f"{'='*40}")
        
        print("\n--- First 5 rows ---")
        print(df.head(13))
        
        print("\n--- Totals ---")
        # Select only numeric columns for summation
        numeric_df = df.select_dtypes(include=['number'])
        if not numeric_df.empty:
            totals = numeric_df.sum()
            print(totals)
            
            # Calculate yearly self-consumption if columns exist
            if 'Self-consumed [kWh]' in df.columns and 'Total need [kWh]' in df.columns:
                total_self_consumed = totals['Self-consumed [kWh]']
                total_need = totals['Total need [kWh]']
                if total_need > 0:
                    yearly_self_consumption = (total_self_consumed / total_need) * 100
                    print(f"\nYearly Self-Consumption: {yearly_self_consumption:.2f}%")
        else:
            print("No numeric columns to sum.")
            
        # Check if this is the monthly data file and plot it
        if 'montly_data.csv' in file_path:
             plot_monthly_data(df)
        
    except Exception as e:
        print(f"Error reading {file_path}: {e}")

def main():
    data_dir = os.path.join(os.path.dirname(__file__), 'data')
    
    # List of files to process
    files = [
        'montly_data.csv',
        'sectors.csv',
        'Lights_consumption.csv'
    ]
    
    for filename in files:
        file_path = os.path.join(data_dir, filename)
        print_data_summary(file_path)

if __name__ == "__main__":
    main()
