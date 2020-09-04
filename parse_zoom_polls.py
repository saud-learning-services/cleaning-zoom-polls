import pandas as pd
import math
import sys
import re
import numpy as np
import glob


def get_files():
    filelist = (glob.glob("poll_input/*.csv"))
    
    if len(filelist) == 0:
        print("No files found in poll_input.\nMove your files to the poll_input folder. Then restart run.")
        sys.exit()
    
    else:
        print("Will be transforming data from the following files:\n\t{}\n".format("\n\t".join(filelist)))
        if _confirm("Enter Y to move on to clean these files."):

            print("\nOK. Your output will be in polls_output.\nBeginning data transformation...")

            return(filelist)

        else:
            print("Ending process.")
            sys.exit()
    
    
def _confirm(input_text):
    """ Ask user to enter y or n to continue
    Returns:
        bool
    """
    answer = ""
    while answer not in ["y", "n"]:
        answer = input("{} [Y/N]".format(input_text)).lower()
    return answer == "y"

generic_error = "See requirements for Zoom polls."

def _column_names(ncol):
    """  Zoom poll data starts with a row #, User Name, User Email, Submitted
    Date/Time, and list of question/answers per user per poll. 
    
    Args:
        ncol (int): the number of columns in the file
    
    Returns:
        names (list): a list of column names based on number of columns 
    """
    newcols = list(range(1, int((ncol-1)/2), 1)) * 2
    newcols.sort()
    names = ["row", "username", "email", "datetime"]
    names.extend(["q_text{}".format(str(index)) if i%2==0 else "answer{}".format(str(index)) for i, index in enumerate(newcols)])
    return(names)

    
def read_data(file):
    """  Zoom poll data starts with a row #, User Name, User Email, Submitted
    Date/Time, and list of question/answers per user per poll. 
    
    Args:
        file (string): the name of the poll file to read
    
    Returns:
        DataFrame: a poll dataframe with data for reformatting
    """
    
    delimtype = ","
    
    try:     
        df = pd.read_csv(file, sep=delimtype, encoding="UTF-8")
        
        if df.columns[0].startswith("#\tUser Name\tUser Email\t"):
            delimtype="\t"
            df = pd.read_csv(file, sep=delimtype, encoding="UTF-8")
            
        elif all(df.columns[0:4] == ["#", "User Name", "User Email", "Submitted Date/Time"]): 
            df = pd.read_csv(file, skiprows=1, header=None, sep=delimtype, encoding="UTF-8")
            
        else:
            print("Column error in file. {}".format(generic_error))
            df = None
            sys.exit()
        
        try:
            df = df.dropna(how='all', axis=1)
            ncol = len(df.columns)
            df.columns = _column_names(ncol)
            
        except Exception as e: 
            print("Unknown error. {}".format(generic_error))
            #print(e)
            sys.exit()
            
        return(df)
        
       
                
    except pd.errors.ParserError as e:
        m = re.match(r"Error tokenizing data. C error: Expected (\d*) fields in line 109, saw (\d*)", str(e))
        if bool(m):
            ncol = int(m.group(2)) - 1 
            names = _column_names(ncol)
            df = pd.read_csv(file, sep=delimtype, skiprows=1, usecols=range(0, ncol), names=names, encoding="UTF-8")
            
            df = df.dropna(how='all', axis=1)
            return(df)
        
        else:
            print("Unknown error in file. {}".format(generic_error))
            sys.exit()
            
        
def reformat_long(df):
    
    """ Reformats from wide to long
    
    Args:
        df (DataFrame): the read in version of a zoom poll in dataframe format
    
    Returns:
        DataFrame: a cleaned dataframe with question and answer in long format
    """
    
    polls = df.groupby("q_text1").agg(
        min_poll = pd.NamedAgg("datetime", min),
        max_poll = pd.NamedAgg("datetime", max))\
        .sort_values("min_poll", ascending=True)\
        .reset_index()\
        .rename_axis("poll")\
        .reset_index()\

    polls["poll"] = polls["poll"].apply(lambda x: "poll_{}".format(x + 1))

    df = df.merge(polls, on="q_text1")

    df_long = pd.wide_to_long(df, stubnames=["q_text", "answer"], i=[ "poll", "min_poll", "max_poll", "username", "email", "datetime"], j="question_num")
    # drop any cases where both q_text and answer are NA for any rows of data 
    df_long = df_long[['q_text', 'answer']].dropna(axis=0, how="all").reset_index()
    
    return(df_long)

# working in update-interface

def main():
    
    files = get_files()

    for f in files:
        # expects "poll_input/FILE.csv"
        try:
            f_name = re.search(r"poll_input\/(.*)\.csv", f, re.IGNORECASE).group(1)
            print("Formatting {}".format(f_name))
            df = read_data(f)
            df = reformat_long(df)
            df["file_name"] = f_name
            f_out = "poll_output/{}_cleaned.csv".format(f_name)
            df.to_csv(f_out)
            print("\tOutput created {}".format(f_out))
            print("\n")
        except Exception as e:
            print("\tError: {}\n".format(e))
            pass
        
    print("Done!")
        
    
if __name__ == "__main__":
    main()
