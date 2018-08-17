import textwrap
import pandas as pd
import sqlalchemy as sa
import os

password_file_path = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '../..'))

def get_pw(pathname=password_file_path, filename='dbpw.txt'):
    path_and_file = os.path.join(pathname, filename)
    with open(path_and_file, 'r') as f:
        userid = f.readline().strip()
        pw = f.readline().strip()
        dbpath = f.readline().strip()
        dbname = f.readline().strip()
    return userid, pw, dbpath, dbname

def get_connection_string():
    userid, pw, dbpath, dbname = get_pw()
    cstring = 'mssql+pyodbc://' + userid + ':' + pw + '@' + dbpath + '/' + dbname

    # http://docs.sqlalchemy.org/en/latest/dialects/mssql.html#hostname-connections
    cstring = cstring + '?driver=ODBC+Driver+13+for+SQL+Server'
    return cstring

def data_query(query, engine=None):
    dispose = False
    if not engine:
        # create engine if one wasn't passed
        dispose = True
        engine = sa.create_engine(get_connection_string(), echo=False)
    df = pd.read_sql(query, engine)
    if dispose:
        # close engine if one wasn't passed
        engine.dispose()
    return df


def realtimesettlement():
    return '''
    SELECT *
    FROM [Public-UtilityReporting].[dbo].[ERCOT_RealTimeSettlementPointPrices]
    '''

def ptc():
    return '''
    SELECT * FROM [JustEnergy-UtilityReporting].[dbo].[PowerToChoose]
    '''






def site_metadata(sites=None):
    query =  '''
    SELECT DISTINCT
    	a.ESIID as Account_No
        ,a.SystemSize
    FROM [EnchantedRock].[dbo].[Utility_810_Transactions] a
    '''
    if sites:
        query = query + "WHERE a.ESIID in ("
        for s in sites:
            query = query + "'" + str(s) + "',"
        query = query[:-1] + ")"
    return textwrap.dedent(query)

def alltsdps():
	return '''
	SELECT DISTINCT
	CASE [Utility_DUNS]
    	WHEN '007924772' THEN 'AEPC'
    	WHEN '007923311' THEN 'AEPN'
    	WHEN '957877905' THEN 'CNP'
    	WHEN '1039940674000' THEN 'ONC'
    	WHEN '007929441' THEN 'TNMP'
    	ELSE 'Unknown TDSP'
	END AS [TDSP]
	FROM [EnchantedRock].[dbo].[Utility_810_Transactions]'''

def maxmindate(artmin=None,artmax=None):
    '''
    param artmin: the artificial minimum date you would like to choose from (probably not used)
    param artmax: the artificial maximum date you would like to choose from (probably not used)
    '''
	query = '''
	SELECT
	MAX([Payment_Due_Date]) as [maxdate],
	MIN([Payment_Due_Date]) as [mindate],
	FROM [EnchantedRock].[dbo].[Utility_810_Transactions]'''

    if artmin or artmax:
        query = query + '''WHERE '''
        if artmin:
            query = query + '''[Payment_Due_Date] > \'''' + artmin + '''' '''
        if artmin and artmax:
            query = query + '''AND '''
        if artmax:
            query = query + '''[Payment_Due_Date] < \'''' + artmax + '''''''
    return query

def numsystems(dates=[],TDSP=[],accounts=[]):
	query = '''
	SELECT COUNT(DISTINCT Account_No) as numsystems
	FROM [EnchantedRock].[dbo].[Utility_810_Transactions]
	'''
	for date in dates:

def query_transactions(flowdates=[], TDSP=[], ESIID=[], compact=False):
    query = '''
    SELECT * FROM
    (SELECT [Document_Tracking_Number]
    	,[Original_Document_ID]
    	,[Marketer_DUNS]
        ,CASE [Utility_DUNS]
        	WHEN '007924772' THEN 'AEPC'
            WHEN '007923311' THEN 'AEPN'
            WHEN '957877905' THEN 'CNP'
            WHEN '1039940674000' THEN 'ONC'
            WHEN '007929441' THEN 'TNMP'
            ELSE 'Unknown TDSP'
        END AS [TDSP]
        ,[Payment_Due_Date]
        ,[ESI_ID]
        ,[Invoice_Total_Amount]
        ,NULL [Processed]
        '''

    query = query + ' FROM [EnchantedRock].[dbo].[Utility_810_Transactions] '

    if flowdates:
        query = query + " WHERE [Payment_Due_Date] in ("
        for f in flowdates:
            query = query + "'" + str(f) + "',"
        query = query[0: -1]  # strip last comma
        query = query + ')'
    else:
        query = query + " WHERE [Payment_Due_Date] in ('') "

    if TDSP:
        query = query + " AND TDSP in ("
        for t in TDSP:
            query = query + "'" + t + "',"
        query = query[0: -1] # strip last comma
        query = query + ')'
    else:
        query = query + " AND TDSP in ('') "

    if ESIID:
        query = query + ''' AND [ESI_ID] in ('''
        for e in ESIID:
            query = query + "'" + str(e) + "',"
        query = query[0: -1] # strip last comma
        query = query + ')'

    query = query + '''
	GROUP BY [ESI_ID]
    ,[Payment_Due_Date]
'''
    if not compact:
        query = query + '''
    ,[TDSP]
    ,[Marketer_DUNS]
'''
    query = query + '''
)SRC
PIVOT
(
  sum(Amount)
) piv
ORDER BY [Payment_Due_Date],[Invoice_Total_Amount]
'''
    return query
