#!/users/bin/env/Python

"""
    @Author: Samson Jacob
    #Purpose: Useful parsing/cleaning functions"
"""

import pandas as pd
import re
import numpy as np

#regex for resection column
rgx1=r'r[0,1,2]'


#important vals

rc = ['Rectal','Colon']
res = ['r0','r1','r2']
ttype=['metastatic','adjuvant','neoadjuvant']
hgrade=['g1','g2','g3','g4']


#Functions
def deus_to_dict(masterdf,val):
    """
    Create a dictonary from the Deus to apply corrections

    :param masterdf: A concated dataframe of raw/clean values (pd.DataFrame)
    :param val: name of a column (str)
    :return: the contents of Raw-col as keys and values as contents of Clean-col (dict)
    """
    outd={}
    sub=masterdf.loc[masterdf['Table']==val].copy()
    for i,v in zip(sub.raw.tolist(),sub.clean.tolist()):
        outd[i]=v
    return outd

def dict_to_df(dic,lis):
    """
    Convert Dictionary to Dataframe

    :param dic: created by deus_to_dict (dict)
    :param lis: names for renaming columns
    :return: dataframe (pd.DataFrame)
    """
    ser = pd.Series(dic)
    df=pd.DataFrame(ser.reset_index())
    df.columns=lis
    return df

def subset_data(df,col,lis):
    """
    Generic Subseting function to keep certain values in DF

    :param df: dataframe to parse (pd.DataFrame)
    :param col: column to parse (str)
    :param lis: list of keep values (list)
    :return:
    """
    return df.loc[df[col].isin(lis)].copy()

def convert_col_todatetime(df,col):
    """
    Convert a specific column to date-time

    :param df: dataframe (pd.DataFrame)
    :param col: column name to convert (str)
    :return: corrected df (pd.DataFrame)
    """
    df[col]= pd.to_datetime(df[col])
    return df

def apply_deus_to_col(df,deus,col,fillvalue):
    """
    Flexible function to correct values based on Deus

    :param df: raw data to be cleaned (pd.DataFrame)
    :param deus: concated deus dataframe (pd.DataFrame)
    :param col:  column to clean via dict (str)
    :param fillvalue: handle non-existent keys (str)
    :return: cleaned dataframe (pd.DataFrame)
    """
    subdic=deus_to_dict(deus,col)
    df[col]=df[col].map(subdic).fillna(fillvalue)
    return df

def splt_join_str(str1,ch):
    """
    Flexible character split function

    :param str1: value to strip (str)
    :param ch: split at this character (str)
    :return: cleaned string (str)
    """
    return str(''.join(char.strip() for char in str1.split(ch)[0]))

def find_val(seq,reg=rgx1):
    """
        find a regex in seq

    :param seq: a sequence to apply a regex (str)
    :param reg: a regular expression; default for rgx1 (regex)
    :return: list of all capture groups, assuming there can be more than 1
    """
    outlis = []
    for match in re.findall(reg,str(seq)):
        outlis.append(match)
    return outlis

def fix_spaces_in_col(df,col,ch):
    """
        remove characters and fix column spacing

    :param df: dataframe to use (pd.DataFrame)
    :param col: column to fix spaces (str)
    :param ch: character to split at (str)
    :return: mutated original df (pd.DataFrame)
    """
    df[col]=df[col].apply(lambda y: splt_join_str(y,ch))
    return df

def convert_col_to_int(df,col):
    """
     coerce a column into int
    :param df: dataframe to use (pd.DataFrame)
    :param col: column to fix (str)
    :return: cleaned/mutated Dataframe (pd.DataFrame)
    """
    outf=[]
    vals = df[col].tolist()
    for x in vals:
        try:
            outf.append(int(x))
        except ValueError:
            outf.append(np.nan)
    df[col]=outf
    return df

def parse_final_df(df):
    """

    :param df: dataframe to parse (pd.DataFrame)
    :return: a lazy return with loc (pd.DataFrame)
    """
    out = df.loc[(df['rectal_or_colon_ca'].isin(rc)) & (df['resection'].isin(res)) & (df['therapy_type'].isin(ttype)) & (df['histological_grade'].isin(hgrade))].copy()
    return out