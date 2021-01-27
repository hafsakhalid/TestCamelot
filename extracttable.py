import camelot

def extracttable(pdf, pagelist, flavour): 
    tables = camelot.read_pdf(pdf, pages=pagelist, flavor=flavour)
    df = tables[0].df
    return df