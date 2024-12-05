# Read File excel

import pandas as pd
import json


# PLEASE NOTE: the token credentials file must be named: environment.xlsx

def PreferencesResourceList():
    excel_file = 'CIMBALI_POC_Migr.xlsx'
    df = pd.read_excel(excel_file)
    df = df.fillna('')
    df = df.drop('API ROW', axis=1)
    df = df.drop(0)

    dataList =[]

    # set header
    matrixHeader = list(df.columns.values)                      
    headerIntegerList = ['TaskSeq','ResourceSeq']
    headerFloatList = ['Preference']
    #create List
    for index, row in df.iterrows():
        #print(row)
        #print('SPACE')
        data ={}
        for elem in matrixHeader:
            if elem.startswith('SCHTSK_'):
                elemdata = elem.replace('SCHTSK_','')
                if elemdata in headerIntegerList:
                    data[elemdata] = int(row[elem])
                elif elemdata in headerFloatList:
                    val = row[elem].replace(',','.')
                    data[elemdata] = float(val)
                else:
                    #print(row[elem])
                    data[elemdata] = str(row[elem])
        
        dataList.append(data)

        #print(dataList)

    return dataList
