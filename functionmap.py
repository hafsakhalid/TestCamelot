import rank_din_fix

def contains_new_line(df):
    return df.applymap(lambda x: x.find('\n') > 0)
    # return s.str.contains('\n')
    # # if(s.find('\n') == -1): 
    # #     return False
    # # return True

fxn_map = {
    'contains_new_line' : contains_new_line, 
    'rank_din_fix' : rank_din_fix.rank_din_fix
    
}