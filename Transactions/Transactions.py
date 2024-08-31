# Import packages needed
import numpy as np
import pandas as pd

def transactions():
    # Read the given CSV file
    amex = pd.read_csv("AMEX.csv")
    rbc = pd.read_csv("RBC.csv")
    simplii = pd.read_csv("SIMPLII.csv")
    rbcchecking = pd.read_csv("RBCChecking.csv")
    cibcV = pd.read_csv("cibcV.csv")
    cibcM = pd.read_csv("cibcM.csv")

    # Dataframe for capturing all transactions
    results = pd.DataFrame()

    #Simplii
    simplii.columns = simplii.columns.str.strip()
    simplii.columns = simplii.columns.str.replace(" ","_")
    simplii.columns = simplii.columns.str.replace("Transaction_Details","Description")
    simplii.columns = simplii.columns.str.replace("Funds_Out","Amount")
    simplii['Amount'] = simplii['Amount'].fillna(simplii['Funds_In'])
    simplii = simplii[['Date','Description','Amount']]
    #simplii = simplii.dropna()
    simplii['Account'] = 'Simplii CAD Checking'
    results = simplii

    #AMEX
    amex.columns = amex.columns.str.strip()
    amex = amex[['Date','Description','Amount']]
    #amex = amex[amex['Description'].str.contains("PAYMENT")==False]
    amex['Account'] = 'Amex US Credit'
    results = pd.concat([results, amex])

    #RBCCredit
    rbc.columns = rbc.columns.str.strip()
    rbc.columns = rbc.columns.str.replace(" ","_")
    rbc.columns = rbc.columns.str.replace("Transaction_Posted_Date","Date")
    rbc = rbc[['Date','Description','Amount']]
    #rbc = rbc[rbc['Description'].str.contains("PAYMENT")==False]
    rbc['Amount'] = rbc['Amount']*-1
    rbc['Account'] = 'RBC US Credit'
    results = pd.concat([results, rbc])

    #RBCChecking
    rbcchecking.columns = rbcchecking.columns.str.strip()
    rbcchecking.columns = rbcchecking.columns.str.replace(" ","_")
    rbcchecking.columns = rbcchecking.columns.str.replace("Transaction_Posted_Date","Date")
    rbcchecking = rbcchecking[['Date','Description','Amount']]
    rbcchecking['Account'] = 'RBC US Checking'
    results = pd.concat([results, rbcchecking])

    #CIBCVisa
    cibcV = cibcV.T.reset_index().T.reset_index(drop=True)
    cibcV = cibcV.rename(columns={0:"Date", 1:"Description", 2:"Amount"})
    cibcV.loc[cibcV['Amount'].str.contains('Unnamed', na=False), 'Amount'] = np.nan
    cibcV['Amount'] = cibcV['Amount'].fillna(cibcV[3])
    cibcV = cibcV.drop([3, 4], axis=1)
    cibcV['Account'] = 'CIBC Visa'
    results = pd.concat([results, cibcV])

    #CIBCMaster
    cibcM = cibcM.T.reset_index().T.reset_index(drop=True)
    cibcM = cibcM.rename(columns={0:"Date", 1:"Description", 2:"Amount"})
    cibcM.loc[cibcM['Amount'].str.contains('Unnamed', na=False), 'Amount'] = np.nan
    cibcM['Amount'] = cibcM['Amount'].fillna(-1*cibcM[3])
    cibcM = cibcM.drop([3, 4], axis=1)
    cibcM['Account'] = 'CIBC Master'
    results = pd.concat([results, cibcM])

    #Rename Date column -> Timestamp
    results.columns = results.columns.str.replace("Date","Timestamp")

    #Sort by Timestamp and reset index
    results = results.sort_values(by='Timestamp')
    results = results.reset_index(drop=True)

    #Add rest of the columns for upload
    results['Timestamp'] = results['Timestamp'].astype(str) + ' 12:00:00'
    results.insert(3,"Category","")
    results.insert(4,"Which Benzinho?","")
    results.insert(5,"Did this expense happen today?","Yes")
    results.insert(6,"Enter Date","")
    results.insert(7,"Which Currency?","")

    #Add Currency based on account
    currency_dict = {
        'Simplii CAD Checking': 'CAD', 
        'CIBC Master': 'CAD',
        'CIBC Visa': 'CAD', 
        'RBC US Credit': 'USD',
        'RBC US Checking': 'USD',
        'Amex US Credit':'USD'
    }

    results['Which Currency?'] = results['Account'].map(currency_dict)

    #Process Amount format
    results['Amount'] = results['Amount'].astype(str)
    results['Amount'] = results['Amount'].str.replace(",","")
    results['Amount'] = results['Amount'].astype(float)

    #Export for upload
    results.to_csv(r'Export.csv', index=False, header=True)
    return