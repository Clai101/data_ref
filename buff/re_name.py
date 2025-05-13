import os
import pandas as pd

def rename_column_in_csv(folder_path):
    """Renames the column 'cos_theta_Lc' to 'cos_theta_L' in all CSV files in the given folder."""
    for file_name in os.listdir(folder_path):
        if file_name.endswith('.csv'):
            file_path = os.path.join(folder_path, file_name)
            try:
                # Read the CSV file
                df = pd.read_csv(file_path)

                # Check if the column exists and rename it
                if 'cos_theta_Lc' in df.columns:
                    df.rename(columns={'cos_theta_Lc': 'cos_theta_L'}, inplace=True)

                    # Save the updated CSV file back
                    df.to_csv(file_path, index=False)
                    print(f"Renamed column in: {file_name}")
                else:
                    print(f"No column to rename in: {file_name}")
            except Exception as e:
                print(f"Error processing {file_name}: {e}")

# Example usage
folder_path = "."  # Replace with your folder path
rename_column_in_csv(folder_path)
