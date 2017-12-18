
import pymysql

# SQL reference queries
# SELECT TABLE_SCHEMA, TABLE_NAME FROM information_schema.tables where table_schema='drugsdatabase';
# SELECT table_name, column_name FROM `COLUMNS` where table_schema = 'drugsdatabase' and table_name = 'marketingstatus'
# SELECT table_name, column_name FROM `COLUMNS` where table_schema = 'drugsdatabase'


# this runs a database querey and returns a list of what was returned.
def db_run_querey(db, query):
    # https://stackoverflow.com/a/13846183
    config = {
      'user': 'nick',
      'passwd': 'harvey',
      'host': 'database.nkren.net',
      'db': db,
    }
    try:
      conn = pymysql.connect(**config)
    except Exception as e:
        print ("error ", e)
        return 1
    else:
        cur = conn.cursor()
        try:
            cur.execute(query)
        except Exception as e:
            print("An error occured when executing query")
            print("\tThe query: %r " % query)
            print (e)
            return 1
        else:
            rtn_list = []
            #print (cur.fetchall())
            for response in cur:
                #print("Response: %r\tType: %r" % (response, type(response)))   # response is a tuple
                print(response)
                rtn_list.append(response[0])
            #print ("rtn_list: %r" % rtn_list)
        cur.close()
        conn.close()
    return rtn_list


# this function takes a keyword and finds that keyword in the database schema.
# if a hit is found, this function returns a list of tuples for each match [(table, column), (table, column)]
def find_attribute(keyword, schema):
    keyword = keyword.lower()
    # is keyword a table?
    #if keyword in schema:
    #    print("%s is a table name" % keyword)
    
    # is keyword a attribute of a table
    match_found = False
    rtn_list = []
    for t in schema:                            # loop through tables
        #print ("table: %s" % t)                # debugger
        for a in schema[t]:                     # search attributes in table
            #print ("  attribute: %s" % a)      # debugger
            for idx, val in enumerate(schema[t][a]):
                #print ("testing: ", val.lower())   # debugger
                if keyword == val.lower():     # test if keyword exits in the list of aliases for a given attribute
                    #print("Found match for %s in table %s, column: %s" % (keyword, t, a))      # debugger
                    match_found = True
                    rtn_list.append((t,a))          # add result tuple to return list
                    break                           # matched this attribute. break out and continue testing other attributes
    if not match_found:
        print ("No match found for %s" % keyword)
        return 0
    #print("\n>>" + keyword + ": " + str(rtn_list))
    return rtn_list