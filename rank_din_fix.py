def rank_din_fix(df): 
    df[['Rank', 'DIN', 'Drug Name']] = df['0'].str.split('\n',expand=True)
    df = df.drop(df.columns[0], axis=1)
    #can remove the headers in the csv
    df = df.dropna()
    cols = df.columns.tolist() 
    #preappending the sepearted values
    for j in range(3):
        i = 1
        cols = [cols[-i]]+cols[:-i]
     #print(cols)
        df = df.reindex(columns=cols)

    #dropping values    
    df = df.drop(df.index[[0]])
    df = df.rename(columns={"Rank": "0"})
    
    return df


    

