alias = {
	"city" : {
		"Name"       : ["town", "city"],
		"CountryCode" : ["areacode"],
		"District"   : ["locality","region","precint"],
		"Population" : ["people","community","natives","peoples","communities","natives"],
	},
	"countrylanguage" : {
		"CountryCode" : ["zip code"],
		"Language"   : ["accent","style","terminology","tongue"],
		"Percentage" : ["percentagetheyspeak", "languagepercentage","languagebarrier"],
	},
	"country" : {
		"Name"       : ["nation", "state", "country"],
		"Continent"  : ["asia","europe","northamerica","africa", "antarctica","southamerica"],
		"Region"     : ["zone","area","territory","sector","place","suburb", "division"],
		"SurfaceArea" : ["size","dimentions","sqft","squarefeet","spread"],
		"IndepYear"  : ["independence","indenpendenceyear"],
		"Population" : ["people","community","natives","peoples","communities","natives"],
		"LifeExpectancy" : ["lifeexpectancy","ratiooflife"],
		"GNP"        : ["grossnationalproduct", "marketvalue"],
		"GNPOld"     : ["oldgrossnationalproduct", "oldmarketvalue","pastmarketvalue", "pastgrossnationalproduct"],
		"LocalName"  : ["nickname"],
		"GovernmentForm" : ["monarchy", "constitutionalgovernment","democracy","dictatorship","federalsystems"],
		"HeadOfState" : ["president", "leader","prince","majesty"],
		"Capital"    : ["central","maincity"],
		"Code2"      : ["shortname"]
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