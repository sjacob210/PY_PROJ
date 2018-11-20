#!/users/bin/env/Python

"""
    @Author: Samson Jacob
    #Purpose: Standardize the deus aka "aux_dataset.xlsx"
"""

import pandas as pd

def read_sheets_tolis(file):
    """
    Find out the names of the sheets in an excel file
    
    :param file: An Excel File with multiple sheets  (str)
    :return: a list of the names of the sheets (list)
    """
    xls = pd.ExcelFile(file) # assumption of xlrd install
    return xls.sheet_names

def read_excel_sheet(filepth,sheetname):
    """
    Standardize the read-in of an excel sheet

    :param filepth: The path to the excel file (str)
    :param sheetname: Name of the Sheet (str)
    :return: Pandas Dataframe (pd.DataFrame)
    """
    df = pd.read_excel(filepth,sheet_name=sheetname,dtype={'raw':str,'clean':str})
    df['clean']=df['clean'].str.replace('_','').map(lambda x: x.strip())
    df['Table']=sheetname
    return df

def concat_excel_samples(filepth):
    """
    Merge all the sheets of an excel file into one dataframe

    :param filepth: path to the excel file (str)
    :return: a pandas dataframe with all of the sheets concated (pd.DataFrame)
    """
    sheets =read_sheets_tolis(filepth)
    mergedf=pd.concat([read_excel_sheet(filepth,i) for i in sheets])
    return mergedf
