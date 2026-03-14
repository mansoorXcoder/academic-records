"""
Portable CSV Merger - Standalone script for any PC
Just copy this file to any folder with CSV files and run it!

Usage:
1. Copy this file to your folder with CSV files
2. Run: python portable_csv_merger.py
3. Done! Merged file will be in 'merged_output' folder

Features:
- Merges all CSV files in current directory
- Maintains sequential numbering (SNo)
- Sorts by Rating (highest first)
- Creates organized output folder
- Tracks source files
- Works on any PC with Python + pandas
"""

import pandas as pd
import glob
import os
import sys
from datetime import datetime

def install_pandas():
    """Try to install pandas if not available"""
    try:
        import subprocess
        print("📦 Installing pandas...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pandas"])
        print("✅ Pandas installed successfully!")
        return True
    except Exception as e:
        print(f"❌ Could not install pandas automatically: {e}")
        print("💡 Please run: pip install pandas")
        return False

def check_dependencies():
    """Check if required packages are available"""
    try:
        import pandas as pd
        return True
    except ImportError:
        print("pandas not found!")
        choice = input("Install pandas automatically? (y/n): ").lower()
        return install_pandas() if choice == 'y' else False

def merge_csv_files(target_dir=None):
    """Main function to merge CSV files in specified directory"""
    current_dir = target_dir or os.path.dirname(os.path.abspath(__file__))
    output_dir = os.path.join(current_dir, "merged_output")

    print("Portable CSV Merger")
    print("=" * 50)
    print(f"Working directory: {current_dir}")

    os.makedirs(output_dir, exist_ok=True)

    csv_files = glob.glob(os.path.join(current_dir, "*.csv"))
    csv_files = [f for f in csv_files if not f.startswith(output_dir)]

    if not csv_files:
        print("No CSV files found!")
        return False

    print(f"Found {len(csv_files)} CSV files:")
    for i, file in enumerate(csv_files, 1):
        print(f"   {i:2d}. {os.path.basename(file)} ({os.path.getsize(file)/1024:.1f} KB)")

    print("\nValidating file structures...")
    reference_columns = None
    valid_files = []

    for file_path in csv_files:
        try:
            df_header = pd.read_csv(file_path, nrows=0)
            current_columns = list(df_header.columns)

            # Accept all files regardless of structure
            if reference_columns is None:
                reference_columns = current_columns
            valid_files.append(file_path)
            print(f"   [OK] {os.path.basename(file_path)} - Added for merging")
        except Exception as e:
            print(f"   [ERROR] {os.path.basename(file_path)} - Error: {e}")

    if not valid_files:
        print("No compatible CSV files found!")
        return False

    print(f"\nMerging {len(valid_files)} compatible files...")
    all_dataframes = []

    for file_path in valid_files:
        try:
            df = pd.read_csv(file_path)
            df['Source_File'] = os.path.basename(file_path)
            all_dataframes.append(df)
            print(f"   [FILE] {os.path.basename(file_path)}: {len(df):,} rows")
        except Exception as e:
            print(f"   [ERROR] {os.path.basename(file_path)}: Error - {e}")

    if not all_dataframes:
        print("No data could be loaded!")
        return False

    print("\nCombining data...")
    combined_df = pd.concat(all_dataframes, ignore_index=True)

    if 'SNo' in combined_df.columns:
        combined_df['SNo'] = range(1, len(combined_df) + 1)
        print(f"Renumbered SNo: 1 to {len(combined_df):,}")

    if 'Rating' in combined_df.columns:
        print("Sorting by Rating (highest first)...")
        combined_df = combined_df.sort_values('Rating', ascending=False).reset_index(drop=True)
        if 'SNo' in combined_df.columns:
            combined_df['SNo'] = range(1, len(combined_df) + 1)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_filename = f"merged_data_{timestamp}.csv"
    output_path = os.path.join(output_dir, output_filename)

    print("\nSaving merged data...")
    # Remove Source_File column if it exists
    if 'Source_File' in combined_df.columns:
        combined_df = combined_df.drop(columns=['Source_File'])
    combined_df.to_csv(output_path, index=False, encoding='utf-8')

    print("\n" + "=" * 50)
    print("SUCCESS! CSV files merged successfully")
    print("=" * 50)
    print(f"Input files: {len(valid_files)}")
    print(f"Total rows: {len(combined_df):,}")
    print(f"Total columns: {len(combined_df.columns)}")
    print(f"Output file: {output_filename}")
    print(f"Output location: {output_dir}")

    if 'Source_File' in combined_df.columns:
        print("\nRows per source file:")
        for filename, count in combined_df['Source_File'].value_counts().items():
            print(f"   - {filename}: {count:,} rows")

    print("\nDone! Check the 'merged_output' folder.")
    return True

def main():
    # Set console output encoding to UTF-8
    import sys
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    
    print("Starting Portable CSV Merger...")
    if not check_dependencies():
        input("\nPress Enter to exit...")
        return

    target_dir = sys.argv[1] if len(sys.argv) > 1 else None
    success = merge_csv_files(target_dir)

    print("\nProcess completed successfully!" if success else "\nProcess failed!")
    input("\nPress Enter to exit...")

if __name__ == "__main__":
    main()