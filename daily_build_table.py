import pandas as pd
import sqlalchemy as sa
import datetime
import calendar
import textwrap
import time
import os

from sqlalchemy import Column, String, Numeric, Integer, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, create_engine, bindparam
from sqlalchemy.orm import Session
import random

Base = declarative_base()

password_file_path = os.path.abspath(os.path.join(os.path.dirname( __file__ )))

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

def get_engine():
    return sa.create_engine(get_connection_string(), echo=False)

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

def command_query(query, engine=None):
    dispose = False
    if not engine:
        # create engine if one wasn't passed
        dispose = True
        engine = sa.create_engine(get_connection_string(), echo=False)
    result = engine.execute(query)
    if dispose:
        # close engine if one wasn't passed
        engine.dispose()
    return result

def maxsmtdate():
    return '''
SELECT max([usage_date]) AS maxdate
FROM [EnchantedRock].[dbo].[CustomerUsage15]
'''

def delete_records_query(tablename):
    return 'DELETE FROM [EnchantedRock].[dbo].[' + tablename + ']'

def generate_SolarGeneration_table_query():
    query = '''
INSERT INTO [EnchantedRock].[dbo].[SolarGeneration]

SELECT
    sa.ESIID AS Account_No
	,t.TDSP
    ,sa.utility
    ,sa.SystemSize AS systemsize
    ,sa.DropDate AS [Drop Date]
    ,sa.Offset
    ,sa.ActualGHISite
    ,sa.ExpectedGHISite
    ,cu15.GenerationCode
    ,Month(cu15.UsageDate) AS FlowMonth
    ,Year(cu15.UsageDate) AS FlowYear
    ,tdsp.premisetype
    ,tdsp.zipcode
	,sum(cu15.Int001+cu15.Int002+cu15.Int003+cu15.Int004) AS HE1
	,sum(cu15.Int005+cu15.Int006+cu15.Int007+cu15.Int008) AS HE2
	,sum(cu15.Int009+cu15.Int010+cu15.Int011+cu15.Int012) AS HE3
	,sum(cu15.Int013+cu15.Int014+cu15.Int015+cu15.Int016) AS HE4
	,sum(cu15.Int017+cu15.Int018+cu15.Int019+cu15.Int020) AS HE5
	,sum(cu15.Int021+cu15.Int022+cu15.Int023+cu15.Int024) AS HE6
	,sum(cu15.Int025+cu15.Int026+cu15.Int027+cu15.Int028) AS HE7
	,sum(cu15.Int029+cu15.Int030+cu15.Int031+cu15.Int032) AS HE8
	,sum(cu15.Int033+cu15.Int034+cu15.Int035+cu15.Int036) AS HE9
	,sum(cu15.Int037+cu15.Int038+cu15.Int039+cu15.Int040) AS HE10
	,sum(cu15.Int041+cu15.Int042+cu15.Int043+cu15.Int044) AS HE11
	,sum(cu15.Int045+cu15.Int046+cu15.Int047+cu15.Int048) AS HE12
	,sum(cu15.Int049+cu15.Int050+cu15.Int051+cu15.Int052) AS HE13
	,sum(cu15.Int053+cu15.Int054+cu15.Int055+cu15.Int056) AS HE14
	,sum(cu15.Int057+cu15.Int058+cu15.Int059+cu15.Int060) AS HE15
	,sum(cu15.Int061+cu15.Int062+cu15.Int063+cu15.Int064) AS HE16
	,sum(cu15.Int065+cu15.Int066+cu15.Int067+cu15.Int068) AS HE17
	,sum(cu15.Int069+cu15.Int070+cu15.Int071+cu15.Int072) AS HE18
	,sum(cu15.Int073+cu15.Int074+cu15.Int075+cu15.Int076) AS HE19
	,sum(cu15.Int077+cu15.Int078+cu15.Int079+cu15.Int080) AS HE20
	,sum(cu15.Int081+cu15.Int082+cu15.Int083+cu15.Int084) AS HE21
	,sum(cu15.Int085+cu15.Int086+cu15.Int087+cu15.Int088) AS HE22
	,sum(cu15.Int089+cu15.Int090+cu15.Int091+cu15.Int092) AS HE23
	,sum(cu15.Int093+cu15.Int094+cu15.Int095+cu15.Int096+isnull(cu15.Int097,0)+isnull(cu15.Int098,0)+isnull(cu15.Int099,0)+isnull(cu15.Int100,0)) AS HE0

	-- matrix multiply real time prices by usage
	,sum((cu15.Int001+cu15.Int002+cu15.Int003+cu15.Int004) * rtm.HE1_rtm/1000) AS HE1_rtm
	,sum((cu15.Int005+cu15.Int006+cu15.Int007+cu15.Int008) * rtm.HE2_rtm/1000) AS HE2_rtm
	,sum((cu15.Int001+cu15.Int002+cu15.Int003+cu15.Int004) * rtm.HE3_rtm/1000) AS HE3_rtm
	,sum((cu15.Int001+cu15.Int002+cu15.Int003+cu15.Int004) * rtm.HE4_rtm/1000) AS HE4_rtm
	,sum((cu15.Int001+cu15.Int002+cu15.Int003+cu15.Int004) * rtm.HE5_rtm/1000) AS HE5_rtm
	,sum((cu15.Int001+cu15.Int002+cu15.Int003+cu15.Int004) * rtm.HE6_rtm/1000) AS HE6_rtm
	,sum((cu15.Int001+cu15.Int002+cu15.Int003+cu15.Int004) * rtm.HE7_rtm/1000) AS HE7_rtm
	,sum((cu15.Int001+cu15.Int002+cu15.Int003+cu15.Int004) * rtm.HE8_rtm/1000) AS HE8_rtm
	,sum((cu15.Int001+cu15.Int002+cu15.Int003+cu15.Int004) * rtm.HE9_rtm/1000) AS HE9_rtm
	,sum((cu15.Int037+cu15.Int038+cu15.Int039+cu15.Int040) * rtm.HE10_rtm/1000) AS HE10_rtm
	,sum((cu15.Int041+cu15.Int042+cu15.Int043+cu15.Int044) * rtm.HE11_rtm/1000) AS HE11_rtm
	,sum((cu15.Int045+cu15.Int046+cu15.Int047+cu15.Int048) * rtm.HE12_rtm/1000) AS HE12_rtm
	,sum((cu15.Int049+cu15.Int050+cu15.Int051+cu15.Int052) * rtm.HE13_rtm/1000) AS HE13_rtm
	,sum((cu15.Int053+cu15.Int054+cu15.Int055+cu15.Int056) * rtm.HE14_rtm/1000) AS HE14_rtm
	,sum((cu15.Int057+cu15.Int058+cu15.Int059+cu15.Int060) * rtm.HE15_rtm/1000) AS HE15_rtm
	,sum((cu15.Int061+cu15.Int062+cu15.Int063+cu15.Int064) * rtm.HE16_rtm/1000) AS HE16_rtm
	,sum((cu15.Int065+cu15.Int066+cu15.Int067+cu15.Int068) * rtm.HE17_rtm/1000) AS HE17_rtm
	,sum((cu15.Int069+cu15.Int070+cu15.Int071+cu15.Int072) * rtm.HE18_rtm/1000) AS HE18_rtm
	,sum((cu15.Int073+cu15.Int074+cu15.Int075+cu15.Int076) * rtm.HE19_rtm/1000) AS HE19_rtm
	,sum((cu15.Int077+cu15.Int078+cu15.Int079+cu15.Int080) * rtm.HE20_rtm/1000) AS HE20_rtm
	,sum((cu15.Int081+cu15.Int082+cu15.Int083+cu15.Int084) * rtm.HE21_rtm/1000) AS HE21_rtm
	,sum((cu15.Int085+cu15.Int086+cu15.Int087+cu15.Int088) * rtm.HE22_rtm/1000) AS HE22_rtm
	,sum((cu15.Int089+cu15.Int090+cu15.Int091+cu15.Int092) * rtm.HE23_rtm/1000) AS HE23_rtm
	,sum((cu15.Int093+cu15.Int094+cu15.Int095+cu15.Int096+ISNULL(cu15.Int097,0)+ISNULL(cu15.Int098,0)+ISNULL(cu15.Int099,0)+ISNULL(cu15.Int100,0)) * rtm.HE0_rtm/1000)  AS HE0_rtm

    ,CAST(DATEADD(month, DATEDIFF(month, 0, cu15.UsageDate), 0) AS date) AS FlowDate

FROM [MP2Energy].[dbo].SolarAccounts sa
INNER JOIN [MP2Energy].[dbo].[CustomerUsage15] cu15
ON cu15.Account_No = sa.ESIID
LEFT JOIN [MP2Energy].[dbo].[TDSP_ESIID_EXTRACT] tdsp
ON sa.ESIID = tdsp.esiid
-- classify which are ONC and CNP based on beginning of ESIID
INNER JOIN
(
	SELECT 'ONC' AS 'TDSP', '1044372' AS 'ESIID_start'
	UNION
	SELECT 'CNP' AS 'TDSP', '1008901' AS 'ESIID_start'
) t
ON LEFT(sa.ESIID,7) = t.ESIID_start
LEFT JOIN
(
	SELECT TDSP
		,FlowDate
		,[1] AS HE1_rtm
		,[2] AS HE2_rtm
		,[3] AS HE3_rtm
		,[4] AS HE4_rtm
		,[5] AS HE5_rtm
		,[6] AS HE6_rtm
		,[7] AS HE7_rtm
		,[8] AS HE8_rtm
		,[9] AS HE9_rtm
		,[10] AS HE10_rtm
		,[11] AS HE11_rtm
		,[12] AS HE12_rtm
		,[13] AS HE13_rtm
		,[14] AS HE14_rtm
		,[15] AS HE15_rtm
		,[16] AS HE16_rtm
		,[17] AS HE17_rtm
		,[18] AS HE18_rtm
		,[19] AS HE19_rtm
		,[20] AS HE20_rtm
		,[21] AS HE21_rtm
		,[22] AS HE22_rtm
		,[23] AS HE23_rtm
		,[24] AS HE0_rtm
	FROM
	(
		SELECT CONVERT(date,[Delivery Date]) AS FlowDate
			,[Delivery Hour]
			,TDSP
			,AVG([Settlement Point Price]) AS avgprice
		FROM [MP2Energy].[dbo].[RTMprice] rtm
		INNER JOIN
		(
			select 'CNP' AS 'TDSP', 'HB_HOUSTON' AS 'Settlement Point Name'
			UNION
			select 'ONC' AS 'TDSP', 'HB_NORTH' AS 'Settlement Point Name'
		) t
		ON t.[Settlement Point Name] = rtm.[Settlement Point Name]
		AND t.TDSP in ('ONC','CNP')
		GROUP BY
			CONVERT(date,[Delivery Date])
			,[Delivery Hour]
			,TDSP
	) src
	PIVOT
	(
		AVG(avgprice)
		FOR [Delivery Hour] in ([1],[2],[3],[4],[5],[6],[7],[8],[9],[10],[11],[12],[13],[14],[15],[16],[17],[18],[19],[20],[21],[22],[23],[24])
	) piv
) rtm
ON rtm.TDSP = t.TDSP
AND  rtm.FlowDate = cu15.UsageDate

GROUP BY sa.ESIID
	,t.TDSP
	,sa.utility
	,sa.SystemSize
	,sa.DropDate
	,sa.Offset
	,sa.ActualGHISite
	,sa.ExpectedGHISite
	,cu15.GenerationCode
	,Month(cu15.UsageDate)
	,Year(cu15.UsageDate)
	,tdsp.premisetype
	,tdsp.zipcode
	,DATEADD(month, DATEDIFF(month, 0, cu15.UsageDate), 0)
'''
    return query

def expected_kwh_byhour():
    return textwrap.dedent('''
SELECT [SiteID]
	,[CITY LOC]
	,[DC Sys Size (kW)]
	,[PVW Month]
	,[0] AS HE1
	,[1] AS HE2
	,[2] AS HE3
	,[3] AS HE4
	,[4] AS HE5
	,[5] AS HE6
	,[6] AS HE7
	,[7] AS HE8
	,[8] AS HE9
	,[9] AS HE10
	,[10] AS HE11
	,[11] AS HE12
	,[12] AS HE13
	,[13] AS HE14
	,[14] AS HE15
	,[15] AS HE16
	,[16] AS HE17
	,[17] AS HE18
	,[18] AS HE19
	,[19] AS HE20
	,[20] AS HE21
	,[21] AS HE22
	,[22] AS HE23
	,[23] AS HE0
FROM
(
	SELECT d.SiteID
		,h.[CITY LOC]
		,h.[DC Sys Size (kW)]
		,d.[PVW Month]
		,d.HourBeginning
		,SUM(d.[AC System Output (W)])/1000 AS kwh_expected
	FROM [MP2Energy].[dbo].[PVWSiteData] d
	INNER JOIN [MP2Energy].[dbo].[PVWSiteHeader] h
	ON d.SiteID = h.SiteID
	GROUP BY d.SiteID
		,h.[CITY LOC]
		,h.[DC Sys Size (kW)]
		,d.[PVW Month]
		,d.HourBeginning
) src
PIVOT
(
  sum(kwh_expected)
  for [HOURBeginning] in ([0],[1],[2],[3],[4],[5],[6],[7],[8],[9],[10],[11],[12],[13],[14],[15],[16],[17],[18],[19],[20],[21],[22],[23])
) piv
ORDER BY [SiteID],[PVW Month]
	''')

def expected_ghi_byhour():
    return '''
select [USAF]
	,[monthofyear]
	,[01:00] AS HE1
	,[02:00] AS HE2
	,[03:00] AS HE3
	,[04:00] AS HE4
	,[05:00] AS HE5
	,[06:00] AS HE6
	,[07:00] AS HE7
	,[08:00] AS HE8
	,[09:00] AS HE9
	,[10:00] AS HE10
	,[11:00] AS HE11
	,[12:00] AS HE12
	,[13:00] AS HE13
	,[14:00] AS HE14
	,[15:00] AS HE15
	,[16:00] AS HE16
	,[17:00] AS HE17
	,[18:00] AS HE18
	,[19:00] AS HE19
	,[20:00] AS HE20
	,[21:00] AS HE21
	,[22:00] AS HE22
	,[23:00] AS HE23
	,[24:00] AS HE0
from
(
	SELECT USAF
		,datepart(mm,[Date (MM DD YYYY)]) AS [monthofyear]
		,[Time (HH MM)]
		,sum([GHI (W m^2)]) AS [GHI_Expected]
	FROM [MP2Energy].[dbo].[TMY3_Data]
	WHERE [USAF] = 722506
	GROUP BY USAF, datepart(mm,[Date (MM DD YYYY)]), [Time (HH MM)]
) src
PIVOT
(
  sum([GHI_Expected])
  for [Time (HH MM)] in ([01:00], [02:00], [03:00],[04:00],[05:00],[06:00],[07:00],[08:00],[09:00],[10:00],[11:00],[12:00],[13:00],[14:00],[15:00],[16:00],[17:00],[18:00],[19:00],[20:00],[21:00],[22:00],[23:00],[24:00])
) piv
ORDER BY [USAF],[monthofyear]
    '''

def rtm_query():
    return '''
SELECT Account_No
	,GenerationCode
	,FlowDate
	,HE1_rtm
	,HE2_rtm
	,HE3_rtm
	,HE4_rtm
	,HE5_rtm
	,HE6_rtm
	,HE7_rtm
	,HE8_rtm
	,HE9_rtm
	,HE10_rtm
	,HE11_rtm
	,HE12_rtm
	,HE13_rtm
	,HE14_rtm
	,HE15_rtm
	,HE16_rtm
	,HE17_rtm
	,HE18_rtm
	,HE19_rtm
	,HE20_rtm
	,HE21_rtm
	,HE22_rtm
	,HE23_rtm
	,HE0_rtm
FROM [MP2Energy].[dbo].[SolarGeneration]
'''

def actual_ghi_byhour():
    return '''
SELECT [USAF]
	,[FlowMonth]
	,[FlowYear]
	,[0] AS HE1
	,[1] AS HE2
	,[2] AS HE3
	,[3] AS HE4
	,[4] AS HE5
	,[5] AS HE6
	,[6] AS HE7
	,[7] AS HE8
	,[8] AS HE9
	,[9] AS HE10
	,[10] AS HE11
	,[11] AS HE12
	,[12] AS HE13
	,[13] AS HE14
	,[14] AS HE15
	,[15] AS HE16
	,[16] AS HE17
	,[17] AS HE18
	,[18] AS HE19
	,[19] AS HE20
	,[20] AS HE21
	,[21] AS HE22
	,[22] AS HE23
	,[23] AS HE0
FROM
(
	SELECT 722506 AS USAF
		,Month([DATE (MM DD YYYY)]) AS FlowMonth
		,Year([DATE (MM DD YYYY)]) AS FlowYear
		,[HOUR-CST] AS FlowHour
		,SUM([Avg Global Horizontal  W m^2 ]) AS ActualGHI
	FROM [MP2Energy].[dbo].[Actualrradiance]
	GROUP BY Month([DATE (MM DD YYYY)])
		,Year([DATE (MM DD YYYY)])
		,[HOUR-CST]
) src
PIVOT
(
  sum([ActualGHI])
  for FlowHour in ([0],[1],[2],[3],[4],[5],[6],[7],[8],[9],[10],[11],[12],[13],[14],[15],[16],[17],[18],[19],[20],[21],[22],[23])
) piv
    '''


def actual_ghi_byhour_old():
    return '''
SELECT [USAF]
	,[monthofyear]
	,[01:00] AS HE1
	,[02:00] AS HE2
	,[03:00] AS HE3
	,[04:00] AS HE4
	,[05:00] AS HE5
	,[06:00] AS HE6
	,[07:00] AS HE7
	,[08:00] AS HE8
	,[09:00] AS HE9
	,[10:00] AS HE10
	,[11:00] AS HE11
	,[12:00] AS HE12
	,[13:00] AS HE13
	,[14:00] AS HE14
	,[15:00] AS HE15
	,[16:00] AS HE16
	,[17:00] AS HE17
	,[18:00] AS HE18
	,[19:00] AS HE19
	,[20:00] AS HE20
	,[21:00] AS HE21
	,[22:00] AS HE22
	,[23:00] AS HE23
	,[24:00] AS HE0
FROM
(
	SELECT USAF
		,datepart(mm,[Date (MM DD YYYY)]) AS [monthofyear]
		,[Time (HH MM)]
		,sum([GHI (W m^2)]*(1-RAND()/10)) AS [GHI_Expected]
	FROM [MP2Energy].[dbo].[TMY3_Data]
	WHERE [USAF] = 722506
	GROUP BY USAF, datepart(mm,[Date (MM DD YYYY)]), [Time (HH MM)]
) src
PIVOT
(
  sum([GHI_Expected])
  for [Time (HH MM)] in ([01:00], [02:00], [03:00],[04:00],[05:00],[06:00],[07:00],[08:00],[09:00],[10:00],[11:00],[12:00],[13:00],[14:00],[15:00],[16:00],[17:00],[18:00],[19:00],[20:00],[21:00],[22:00],[23:00],[24:00])
) piv
ORDER BY [USAF],[monthofyear]
    '''

def actual_rtmcost_byhour():
    return '''
    SELECT [Account_No]
          ,[TDSP]
          ,[utility]
          ,[systemsize]
          ,[Offset]
          ,[ActualGHISite]
          ,[ExpectedGHISite]
          ,[GenerationCode]
          ,[FlowMonth]
          ,[FlowYear]
          ,[FlowDate]
          ,[premisetype]
          ,[zipcode]
          ,[HE1_rtm] AS HE1
          ,[HE2_rtm] AS HE2
          ,[HE3_rtm] AS HE3
          ,[HE4_rtm] AS HE4
          ,[HE5_rtm] AS HE5
          ,[HE6_rtm] AS HE6
          ,[HE7_rtm] AS HE7
          ,[HE8_rtm] AS HE8
          ,[HE9_rtm] AS HE9
          ,[HE10_rtm] AS HE10
          ,[HE11_rtm] AS HE11
          ,[HE12_rtm] AS HE12
          ,[HE13_rtm] AS HE13
          ,[HE14_rtm] AS HE14
          ,[HE15_rtm] AS HE15
          ,[HE16_rtm] AS HE16
          ,[HE17_rtm] AS HE17
          ,[HE18_rtm] AS HE18
          ,[HE19_rtm] AS HE19
          ,[HE20_rtm] AS HE20
          ,[HE21_rtm] AS HE21
          ,[HE22_rtm] AS HE22
          ,[HE23_rtm] AS HE23
          ,[HE0_rtm] AS HE0
    FROM [MP2Energy].[dbo].[SolarGeneration]
        '''

def actual_kwh_byhour():
    return '''
SELECT [Account_No]
      ,[TDSP]
      ,[utility]
      ,[systemsize]
      ,[Offset]
      ,[ActualGHISite]
      ,[ExpectedGHISite]
      ,[GenerationCode]
      ,[FlowMonth]
      ,[FlowYear]
      ,[FlowDate]
      ,[premisetype]
      ,[zipcode]
      ,[HE1]
      ,[HE2]
      ,[HE3]
      ,[HE4]
      ,[HE5]
      ,[HE6]
      ,[HE7]
      ,[HE8]
      ,[HE9]
      ,[HE10]
      ,[HE11]
      ,[HE12]
      ,[HE13]
      ,[HE14]
      ,[HE15]
      ,[HE16]
      ,[HE17]
      ,[HE18]
      ,[HE19]
      ,[HE20]
      ,[HE21]
      ,[HE22]
      ,[HE23]
      ,[HE0]
FROM [MP2Energy].[dbo].[SolarGeneration]
    '''

def get_tdu(df):
    # https://www.startexpower.com/content/dam/startexpower/Misc%20Docs/Critical%20Care%20Form%20-%20ESP.pdf
    df['TDSP'] = "unknown"
    df.loc[df.Account_No.str.startswith("1020404"), "TDSP"] = "AEPN"
    df.loc[df.Account_No.str.startswith("1003278"), "TDSP"] = "AEPC"
    df.loc[df.Account_No.str.startswith("1008901"), "TDSP"] = "CNP"
    df.loc[df.Account_No.str.startswith("1044372"), "TDSP"] = "ONC"
    df.loc[df.Account_No.str.startswith("1017699"), "TDSP"] = "ONCS"
    df.loc[df.Account_No.str.startswith("1017008"), "TDSP"] = "SHD"
    df.loc[df.Account_No.str.startswith("1013830"), "TDSP"] = "NUE"
    df.loc[df.Account_No.str.startswith("1040051"), "TDSP"] = "TNMP"
    return df

def condition_gen(df):
    df.loc[df['GenerationCode'] == '4','GenerationCode'] = "Import kWh"
    df.loc[df['GenerationCode'] == '1','GenerationCode'] = "Export kWh"
    return df

def condition_rtm(df):
    df.loc[df['GenerationCode'] == '4','GenerationCode'] = "Import Wholesale Dollars"
    df.loc[df['GenerationCode'] == '1','GenerationCode'] = "Export Wholesale Dollars"
    return df


def get_pvwprofile(df, dfpvw):
    # round to the nearest half
    df['systemsize_rounded'] = (df['systemsize']*2).round(0)/2

    # any system not in ONC will be assigned to Houston
    df['pvw_city'] = 'Houston'
    df.loc[df['TDSP'] == 'ONC','pvw_city'] = 'Dallas'

    # find the right PVWatts profile, join on city and size
    dfpvw = dfpvw[(dfpvw['PVW Month'] == 1)]
    dfpvw = dfpvw[['SiteID','CITY LOC','DC Sys Size (kW)']]

    df = pd.merge(df, dfpvw, how='left', left_on=['pvw_city','systemsize_rounded'],right_on=['CITY LOC','DC Sys Size (kW)'])
    # convert non-matches to -1 for SiteID
    df['SiteID'] = df['SiteID'].fillna(-1)
    df['SiteID'] = df['SiteID'].astype(int)
    df = df.drop(['CITY LOC','DC Sys Size (kW)', 'systemsize_rounded','pvw_city'], axis=1)
    df = df.rename(columns={'SiteID': 'PVW_Site'})
    return df

def merge_solar_expectation(df, dfe):
    # isolate solar records
    dfappend = df[df['GenerationCode']=='Export kWh']

    # create a new generation code for solar kwh expectations
    dfappend = dfappend.drop(['GenerationCode'], axis=1)
    dfappend['GenerationCode'] = 'Solar Generation'

    # drop solar records to make way for solar kwh expectations
    dfappend = dfappend.drop(['HE1','HE2','HE3','HE4','HE5','HE6','HE7','HE8','HE9','HE10','HE11','HE12','HE13','HE14','HE15','HE16','HE17','HE18','HE19','HE20','HE21','HE22','HE23','HE0',], axis=1)

    # add solar expectation
    dfe = pd.merge(dfappend,dfe, how="left", left_on=['PVW_Site','FlowMonth'], right_on=['SiteID','PVW Month'])
    dfe = dfe.drop(['CITY LOC','DC Sys Size (kW)','SiteID','PVW Month'], axis=1)
    return(df.append(dfe))

def merge_ghi(df, dfe, dfa):
    # convert data type for for merge
    dfe['USAF'] = dfe['USAF'].astype(str)
    dfa['USAF'] = dfa['USAF'].astype(str)

    # isolate solar records
    dfappend = df[df['GenerationCode']=='Export kWh']
    # create a new generation code for ghi expectations
    dfappend = dfappend.drop(['GenerationCode'], axis=1)
    dfappend['GenerationCode'] = 'Expected GHI'
    # drop solar records to make way for ghi
    dfappend = dfappend.drop(['HE1','HE2','HE3','HE4','HE5','HE6','HE7','HE8','HE9','HE10','HE11','HE12','HE13','HE14','HE15','HE16','HE17','HE18','HE19','HE20','HE21','HE22','HE23','HE0',], axis=1)
    # add ghi
    dfe = pd.merge(dfappend,dfe, how="left", left_on=['ExpectedGHISite','FlowMonth'], right_on=['USAF','monthofyear'])
    dfe = dfe.drop(['monthofyear','USAF'], axis=1)

    # do it again for actual ghi
    dfappend = df[df['GenerationCode']=='Export kWh']
    dfappend = dfappend.drop(['GenerationCode'], axis=1)
    dfappend['GenerationCode'] = 'Actual GHI'    # ghi actual
    dfappend = dfappend.drop(['HE1','HE2','HE3','HE4','HE5','HE6','HE7','HE8','HE9','HE10','HE11','HE12','HE13','HE14','HE15','HE16','HE17','HE18','HE19','HE20','HE21','HE22','HE23','HE0',], axis=1)
    dfa = pd.merge(dfappend,dfa, how="left", left_on=['ActualGHISite','FlowMonth','FlowYear'], right_on=['USAF','FlowMonth','FlowYear'])
    dfa = dfa.drop(['USAF'], axis=1)

    # add actual ghi and expected ghi records back to original generation records
    return df.append(dfa.append(dfe))

def get_current_month_scalar():
    maxdate = data_query(maxsmtdate())['maxdate'].iloc[0]
    scalar =  maxdate.day / calendar.monthrange(maxdate.year, maxdate.month)[1]
    return scalar, maxdate

def scale_current_month(df):
    # Purpose is to scale back current month's expected irradiance and solar production since the assumption is currently
    # a full month's worth of generation even if only 4 days have passed
    scalar, maxdate = get_current_month_scalar()
    scalecols = ['HE1','HE2','HE3','HE4','HE5','HE6','HE7','HE8','HE9','HE10','HE11','HE12','HE13','HE14','HE15','HE16','HE17','HE18','HE19','HE20','HE21','HE22','HE23','HE0']
    e_ghi_filter = (df['FlowMonth'] == maxdate.month) & (df['FlowYear'] == maxdate.year) & (df['GenerationCode'] == 'Expected GHI')
    df.loc[e_ghi_filter, scalecols] = df.loc[e_ghi_filter, scalecols] * scalar
    e_expectedgen_filter = (df['FlowMonth'] == maxdate.month) & (df['FlowYear'] == maxdate.year) & (df['GenerationCode'] == 'Solar Generation')
    df.loc[e_expectedgen_filter, scalecols] = df.loc[e_expectedgen_filter, scalecols] * scalar
    return df

def merge_rtm(df, dfr):
    dfr.loc[:, dfr.columns.str.startswith('HE')] = dfr.loc[:, dfr.columns.str.startswith('HE')].mul(.001)
    dfr['TDSP'] = dfr['Settlement Point Name'].map({'HB_HOUSTON': 'CNP', 'HB_NORTH': 'ONC'})
    dfr = dfr.drop(['Settlement Point Name'], axis = 1)
    dfr['GenerationCode'] = 'RTM'
    dfappend = df.drop(['HE1','HE2','HE3','HE4','HE5','HE6','HE7','HE8','HE9','HE10','HE11','HE12','HE13','HE14','HE15','HE16','HE17','HE18','HE19','HE20','HE21','HE22','HE23','HE0','GenerationCode'], axis=1)
    dfappend = dfappend.drop_duplicates(keep='first')
    dfr['FlowDate'] = pd.to_datetime(dfr['FlowDate'])
    dfappend = pd.merge(dfappend,dfr, how="left", left_on=['FlowDate','TDSP'], right_on=['FlowDate','TDSP'])
    dfcost= df.loc[(df['GenerationCode'] == 'Export kWh')]
    dfcost = dfcost.append(dfappend)
    p1 = dfcost.groupby(['Account_No', 'ActualGHISite', 'ExpectedGHISite','FlowMonth','FlowYear','PVW_Site','TDSP','premisetype','utility','zipcode','FlowDate','systemsize'], as_index=False).prod().assign(GenerationCode='Export Wholesale Dollars')
    dfcost = df.loc[(df['GenerationCode'] == 'Import kWh')]
    dfcost = dfcost.append(dfappend)
    p2 = dfcost.groupby(['Account_No', 'ActualGHISite','ExpectedGHISite','FlowMonth','FlowYear','PVW_Site','TDSP','premisetype','utility','zipcode','FlowDate','systemsize'], as_index=False).prod().assign(GenerationCode='Import Wholesale Dollars')
    return df.append(p1.append(p2))

def generate_hourly_table(verbose=False, starttime=None, writeCSV=False, writePickle=False):
    if starttime:
        s1 = starttime
    else:
        s1 = datetime.datetime.now()
    s = datetime.datetime.now()
    if verbose:
        print("getting db engine")
    engine = get_engine()
    f = datetime.datetime.now()
    if verbose:
        print(f-s)

    if verbose:
        print("starting pvw query")
    s = datetime.datetime.now()
    df_expected_kwh = data_query(expected_kwh_byhour(), engine)
    f = datetime.datetime.now()
    if verbose:
        print(f-s)

    if verbose:
        print("starting expected ghi query.")
    s = datetime.datetime.now()
    df_expected_ghi = data_query(expected_ghi_byhour(), engine)
    f = datetime.datetime.now()
    if verbose:
        print(str(f-s))

    if verbose:
        print("starting actual ghi query.")
    s = datetime.datetime.now()
    df_actual_ghi = data_query(actual_ghi_byhour(), engine)
    f = datetime.datetime.now()
    if verbose:
        print(str(f-s))

    if verbose:
        print("starting actual generation (smt) query.")
    s = datetime.datetime.now()
    df_actual_generation = data_query(actual_kwh_byhour(), engine)
    f = datetime.datetime.now()
    if verbose:
        print(str(f-s))

    if verbose:
        print("starting real time market prices query.")
    s = datetime.datetime.now()
    df_rtm = data_query(actual_rtmcost_byhour(), engine)
    f = datetime.datetime.now()
    if verbose:
        print(str(f-s))

    if verbose:
        print("manipulating data")
    s = datetime.datetime.now()
    df_actual_generation = condition_gen(df_actual_generation)
    df_rtm = condition_rtm(df_rtm)
    df_actual_generation = df_actual_generation.append(df_rtm)
    df_actual_generation = get_pvwprofile(df_actual_generation, df_expected_kwh)
    df_actual_generation = merge_solar_expectation(df_actual_generation, df_expected_kwh)
    df_actual_generation = merge_ghi(df_actual_generation, df_expected_ghi, df_actual_ghi)
    df_actual_generation = scale_current_month(df_actual_generation)
    f = datetime.datetime.now()
    if verbose:
        print(str(f-s))

    if verbose:
        print("deleting records in hourly table")
    s = datetime.datetime.now()
    command_query(delete_records_query('hourly'))
    f = datetime.datetime.now()
    if verbose:
        print(str(f-s))

    if verbose:
        print("writing data to hourly table")
    s = datetime.datetime.now()
    df_actual_generation.to_sql(name='hourly',
                             con=engine,
                             if_exists='append',
                             index=False,
                             chunksize=100000
                             )
    f = datetime.datetime.now()
    if verbose:
        print(str(f-s))

    if writeCSV:
        if verbose:
            print("writing data to hourly.csv")
        s = datetime.datetime.now()
        df_actual_generation.to_csv("hourly.csv", index=False)
        f = datetime.datetime.now()
        if verbose:
            print(str(f-s))
    if writePickle:
        if verbose:
            print("writing data to hourly.pickle")
        s = datetime.datetime.now()
        df_actual_generation.to_pickle("hourly.pickle")
        f = datetime.datetime.now()
        if verbose:
            print(str(f-s))
    if verbose:
        print("total time:")
        print(str(f-s1))

    engine.dispose()


    return df_actual_generation


def generate_SolarGeneration_table(verbose=False):
    # delete old records and create new records in solar generation table

    s1 = datetime.datetime.now()
    if verbose:
        print("deleting old records in SolarGeneration table.")
    command_query(delete_records_query('SolarGeneration'))
    f = datetime.datetime.now()
    if verbose:
        print(str(f - s1))

    s = datetime.datetime.now()
    if verbose:
        print("re-populating SolarGeneration table.")
    command_query(generate_SolarGeneration_table_query())
    f = datetime.datetime.now()
    if verbose:
        print(str(f-s))
        print("total time recreating SolarGeneration table:")
        print(str(f-s1))

def daily(verbose=False):
    starttime = datetime.datetime.now()

    generate_SolarGeneration_table(verbose)

    # generate records for hourly table
    df = generate_hourly_table(verbose=verbose, starttime=starttime, writeCSV=True, writePickle=True)


if __name__ == "__main__":
    daily(verbose=True)
