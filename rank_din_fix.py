import pdb
import pandas as pd
pd.set_option('display.max_columns', None)

def rank_din_fix(df):
    """
    Fixup for a specific column conflation error.

    # TODO: This tests works but there is a strange problem
    # >>> rank_din_fix(pd.read_csv('rank_din_fix_test.csv')) # doctest: +NORMALIZE_WHITESPACE
        0         1                               2              3  \
    0  14  02377233            ELIQUIS 2.5MG TABLET  Single Source
    1  14  02409100           INTUNIV XR 1MG TABLET  Single Source
    2  15  02372746  APO-MYCOPHENOLIC ACID 360MG EC        Generic
    3  15  02417170        CONSTELLA 290MCG CAPSULE  Single Source
    4  16  02351064  VICTOZA MULTIDOSE PEN INJECTOR  Single Source
    5  17  02425629  LUCENTIS 10MG/ML OPH PRE-FILLE  Single Source
    <BLANKLINE>
                                                 4  5      6         7      8
    0  Blood Formation, Coagulation and Thrombosis  5  0.36%  1,049.50  1.03%
    1                         Cardiovascular Drugs  5  0.36%  1,083.70  1.06%
    2              Unclassified Therapeutic Agents  4  0.29%  7,139.54  7.01%
    3                       Gastrointestinal Drugs  4  0.29%  1,686.83  1.66%
    4           Hormones and Synthetic Substitutes  3  0.21%  3,147.90  3.09%
    5             Eye, Ear, Nose and Throat (EENT)  2  0.14%  3,636.34  3.57%
    """
    # #split the first column into 3 rows because rank, din and drug name need to be seperated
    #df[['Rank', 'DIN', 'Drug Name']] = df['0'].str.split('\n',expand=True)
    df[['temp', 'temp1', 'temp2']] = df['0'].str.split('\n',expand=True)

    #drop that column
    #df = df.drop(df.columns[0], axis=1);
    #df = df.dropna()

    cols = df.columns.tolist()

    #preappending the sepearted values
    for j in range(3):
        i = 1
        cols = [cols[-i]]+cols[:-i]
        df = df.reindex(columns=cols)

    #dropping values    
    df = df.drop(['0'], axis=1)

    #renaming columns so that it can pass the schema
    column_map = {c: c for c in df.columns}
    column_map['temp'] = '0'
    column_map['temp1'] = '1'
    column_map['temp2'] = '2'
    for i in range(1, 7):
        column_map[str(i)] = str(i + 2)
    df = df.rename(columns=column_map)
    return df

    
if __name__ == "__main__":
    import sys
    import doctest

    # Return the number of doctests that fail. This gives calling scripts
    # a non-zero exit code if there are failing tests.
    sys.exit(doctest.testmod(verbose=True)[0])
