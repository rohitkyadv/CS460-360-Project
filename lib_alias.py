alias = {
	"city" : {
		"name"       : ["town", "city"],
		"countrycode" : ["areacode"],
		"district"   : ["locality","region","precint"],
		"population" : ["people","community","natives","peoples","communities","natives"],
	},
	"countrylanguage" : {
		"countrycode" : ["zip code"],
		"language"   : ["accent","style","terminology","tongue"],
		"percentage" : ["percentagetheyspeak", "languagepercentage","languagebarrier"],
	},
	"country" : {
		"name"       : ["nation", "state", "country"],
		"continent"  : ["asia","europe","northamerica","africa", "antarctica","southamerica"],
		"region"     : ["zone","area","territory","sector","place","suburb", "division"],
		"surfacearea" : ["size","dimentions","sqft","squarefeet","spread"],
		"indepyear"  : ["independence","indenpendenceyear"],
		"population" : ["people","community","natives","peoples","communities","natives"],
		"lifeexpectancy" : ["lifeexpectancy","ratiooflife"],
		"gnp"        : ["grossnationalproduct", "marketvalue"],
		"gnpold"     : ["oldgrossnationalproduct", "oldmarketvalue","pastmarketvalue", "pastgrossnationalproduct"],
		"localname"  : ["nickname"],
		"governmentform" : ["monarchy", "constitutionalgovernment","democracy","dictatorship","federalsystems"],
		"headofstate" : ["president", "leader","prince","majesty"],
		"capital"    : ["central","maincity"],
		"code2"      : ["shortname"]
  }
}


# for a given scheme, find a match in alias table and append aliases to the scheme
def alias_lookup(scheme):
  global alias
  
  for t in scheme:      # for every table in schme
    if t in alias:      # test if there is a matching table in alias library
      #print ("aliase table match %s" % t)  # debugger
      for a in scheme[t]:  
        if a in alias[t]:
          #print ("  attri match %s" % a)   # debugger
          # load aliases into scheme
          scheme[t][a].extend(alias[t][a])
        # else does not exist

  return scheme