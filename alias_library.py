alias = {
  "city" : {
    "name" : ['town', 'cities'],
    "countrycode" : ['areacode'],
    "district" : [district,locality,region,precint],
    "population" : [population,people,community,natives,peoples,communities,natives],
  },
  "Countrylanguage" : {
    "Countrycode" : [zipcode],
    "Language" : [language,accent,style,terminology,tongue],
    "percentage" : [percentage they speak, language percentage,language barrier],
  },
  "country" : {
    "name" : [country,nation,town],
    "Continent" : [continent,asia,europe,north america, africa, antarctica, south america],
    "region" : [region,zone,area,territory,sector,place,suburb, division],
    "Surfacearea" : [surface area,size,dimentions,sqft,square feet,spread],
    "indepyear" : [independence,indenpendence year,seld rule],
    "population" : [population,people,community,natives,peoples,communities,natives],
    "lifeExpectancy" : [life expectancy ,ratio of life],
    "GNP" : [gross national product, market value],
    "GNPOld" : [old gross national product, old market value, past market value, past gross national product],
    "localName" : [local name, nick name],
    "GovernmentForm" : [Monarchy, Constitutional Government,Democracy,Dictatorship,Federal Systems],
    "headOFState" : [head of state ,president, leader,prince,majesty],
    "Capital" : [Capital, central,main city],
    "code2" : [short name]
    
  }
}

fun alias_lookup(scheme):
  global alias
  
  for t in scheme:      # for every table in schme
    if t in alias:      # test if there is a matching table in alias library
      for a in scheme[t]:  
        if a in alias[t]
          # load aliases into scheme
          scheme[t][a].exted(alias[t][a])
        # else does not exist

  return scheme