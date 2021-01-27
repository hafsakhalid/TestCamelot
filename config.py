provider = ["Sun Life"]

string_match = {
      
#   'title_name': "by Number of Claims", 
    'start_page' : '2', #do we need start page? 
#   'match_regex' : "/.*/"
  
   }
  
extracts =  {
    'flavour' : 'stream',
    #'table_extractor': et.extracttable() # isn't this just camelot
}
  
#schema = "somepythonfile"

# schema = {

#       obj : "text"
#   }
  
fixups =  {
     #'SchemaError' : rank_din_fix.rank_din_fix() #this needs to be in the config file but how do you import the method without the args
  }
  
template_map = {
      'src' :"xyz", 
      'dst' : "abc"
  }

