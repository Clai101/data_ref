import os
import uproot
import pandas as pd
from concurrent.futures import ThreadPoolExecutor, as_completed

# Function to process each file and save as CSV
def process_file(filename):
        try:
            with uproot.open(filename) as file:
                tupl2 = file['LcXc_2_wf']
                print(f"Processing {filename} with keys: {tupl2.keys()}")
                inc = tupl2.arrays(library='pd')
                inc['source_file'] = filename
                csv_path = f"{os.path.splitext(filename)[0]}.csv"
                inc.to_csv(csv_path, index=False)  # Save as CSV
                print(f"Saved {csv_path}")
                return csv_path
        except Exception as e:
            print(f"Failed to process {filename}: {e}")

# Main function to execute parallel processing
def main():
    with ThreadPoolExecutor() as executor:
        futures = [executor.submit(process_file, filename) for filename in os.listdir() if filename.endswith('.root')]
        # Collect results as they are completed
        for future in as_completed(futures):
            csv_path = future.result()
            if csv_path:
                print(f"Completed and saved: {csv_path}")

if __name__ == "__main__":
    main()



