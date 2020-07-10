# -*- coding: utf-8 -*-
"""
Created on Tue Jul  7 20:30:42 2020

@author: marcw
"""

import requests
import json
import pandas as pd 
import math

baseAPIHead = "https://api.census.gov/data/2018/acs/acs1/profile?get=NAME,"
baseAPITail = "&for=state:*&key=e6e686c049dba8c5672e13edb673ee357d9d7295"
baseAPITailUS = "&for=us:*&key=e6e686c049dba8c5672e13edb673ee357d9d7295"
#DP02_0002PE,DP02_0003PE,DP02_0004PE,DP02_0005PE,DP02_0006PE,DP02_0007PE,DP02_0008PE,DP02_0009PE,DP02_0010PE,DP02_0011PE,DP02_0012PE,DP02_0013PE,DP02_0014PE,DP02_0015E,DP02_0016E,DP02_0025PE,DP02_0026PE,DP02_0027PE,DP02_0028PE,DP02_0029PE,DP02_0031PE,DP02_0032PE,DP02_0033PE,DP02_0034PE,DP02_0035PE,DP02_0036PE,DP02_0052PE,DP02_0059PE,DP02_0060PE,DP02_0061PE,DP02_0062PE,DP02_0063PE,DP02_0064PE,DP02_0065PE,DP02_0066PE,DP02_0067PE,DP02_0068PE,DP02_0069PE,DP02_0071PE,DP02_0084PE,DP02_0090PE,DP02_0092PE,DP02_0094PE,DP02_0103PE,DP02_0111PE,DP02_0112PE,DP02_0123PE,DP02_0124PE

dfVariables = pd.read_csv("acsVariables.csv")

selectedRows = dfVariables.loc[dfVariables['Include'] == "X"][["Name","Label"]]
selectedRows = selectedRows.reset_index()
nSelected = selectedRows.count()[0]
nGroups = math.ceil(nSelected/48)#1 + (nSelected - nSelected % 48)/48




for i in range(nGroups):
    if i == (nGroups - 1):
        endNum = nSelected
    else:
        endNum = (i+1)*48
        
    groupRows = selectedRows.loc[range(i*48,endNum)]["Name"]
    #getString = str(groupRows[0])
    #groupRows = groupRows.reset_index()
    #for j in range(1,groupRows.count()[0]):
    getParameters =",".join(groupRows)
    
    apiCall = baseAPIHead + getParameters + baseAPITail
    apiCallUS = baseAPIHead + getParameters + baseAPITailUS
    response = requests.get(apiCall)
    responseUS = requests.get(apiCallUS)
    data = response.json()
    dataUS = responseUS.json()
    dfTemp = pd.DataFrame(data[1::])
    dfTemp.columns = data[0]
    dfTempUS = pd.DataFrame(dataUS[1::])
    dfTempUS.columns = dataUS[0]
    dfTempUS = dfTempUS.drop(["us"],axis=1)
    dfTempUS['state']="0"
    
    dfTemp = pd.concat([dfTemp, dfTempUS], axis=0,sort = True)
    
    dfTemp = dfTemp.sort_values(by=["NAME"])
    dfTemp = dfTemp.reset_index()
    if i == 0:
        dfTemp = dfTemp.drop(["index"],axis=1)
        df = dfTemp
    else:
        dfTemp = dfTemp.drop(["state","NAME","index"],axis=1)
        df = pd.concat([df, dfTemp], axis=1) #Temp.join(df,on="NAME",how="outer")#
    
df = df[df.NAME != "Puerto Rico"]
df = df.set_index('NAME')
#this next line makes me cry
dfExport = df.rename(columns=lambda x: (selectedRows['Label'][selectedRows['Name'] == x]).item()  if x in list(selectedRows['Name']) else x)
dfExport = dfExport.transpose()
dfExport.to_csv("CompiledACDData.csv")