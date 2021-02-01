import rank_din_fix

def contains_new_line(df):
    # Every element tested is a string that has a newline that is not at the end.
    condition_map = df.applymap(lambda x: not (isinstance(x, str) and x.find('\n') < (len(x) - 1) and x.find('\n') >= 0))
    print(condition_map)
    return condition_map

fxn_map = {
    'contains_new_line' : contains_new_line, 
    'rank_din_fix' : rank_din_fix.rank_din_fix,
    'no_fix' : (lambda df: df)
}
