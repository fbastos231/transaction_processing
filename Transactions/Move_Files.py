import pandas as pd
import os
import glob
import fnmatch

def move_files():
    # Step 1: Define the directory where the files are located
    from_directory = '/Users/felipebastos/Downloads'  # Replace with your directory path
    to_directory = '/Users/felipebastos/Desktop/Transactions'    
    
    if fnmatch.fnmatch(os.path.basename(from_directory), 'SIMPLII.csv'):
        os.rename(os.path.join(from_directory, "SIMPLII.csv"),os.path.join(to_directory, "SIMPLII.csv"))
    
    # Step 3: Use glob to find all files starting with "trans" and ending with ".csv"
    files = glob.glob(os.path.join(from_directory, "trans*.csv"))
    
    files.extend(glob.glob(os.path.join(from_directory, "cibc*.csv")))

    # Step 4: Loop through each file
    for file_path in files:
           
        # Read the CSV file
        df = pd.read_csv(file_path)

        if fnmatch.fnmatch(os.path.basename(file_path), 'trans*.csv'):
            # Extract the desired value (assuming the value is in the first row and a specific column)
            account_type = df.loc[0, 'Account Type']  # Replace 'desired_column' with your actual column name
            
            if account_type == 'MONEYMRKT':
                os.rename(file_path,os.path.join(to_directory, "RBCChecking.csv"))

            if account_type == 'CREDITCARD':
                os.rename(file_path,os.path.join(to_directory, "RBC.csv"))
        
        if fnmatch.fnmatch(os.path.basename(file_path), 'cibc*.csv'):
            # Extract the desired value (assuming the value is in the first row and a specific column)
            account_number = int(df.iloc[0][4][12:])  # Replace 'desired_column' with your actual column name
            
            if (account_number == 1817 or account_number == 2053):
                os.rename(file_path,os.path.join(to_directory, "cibcM.csv"))

            if (account_number == 9547 or account_number ==  9929):
                os.rename(file_path,os.path.join(to_directory, "cibcV.csv"))

    return