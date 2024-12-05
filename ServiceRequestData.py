# Read File excel

import pandas as pd
import json


# PLEASE NOTE: the token credentials file must be named: environment.xlsx

def ServiceRequestList():
    excel_file = 'CIMBALI_POC_Migr.xlsx'
    df = pd.read_excel(excel_file)
    df = df.fillna('')
    df = df.drop('API ROW', axis=1)
    df = df.drop(0)

    dataList =[]

    # set header
    matrixHeader = list(df.columns.values)
    headerIntegerList = []
                            

    #create JSON
    for index, row in df.iterrows():
        #print(row)
        #print('SPACE')
        data ={}
        for elem in matrixHeader:
            if elem.startswith('SR_'):
                elemdata = elem.replace('SR_','')
                #print(elem)
                if elem in headerIntegerList:
                    data[elemdata] = int(row[elem])
                else:
                    #print(row[elem])
                    data[elemdata] = str(row[elem])
                # static params
                data['QuotationNeededDb']= False
                data['NewLocation']= False
                data['NewContact'] = False
                data['UrgencyBased'] = False
                data['UrgencyBasedService']= True
                data['UrgencyBasedContract']= False
                data['RequestRelease']= False
                data['QuotationNeededDbStatus']= "Request"
                data['Revision']= "1"
        #
        dataList.append(data)

        #print(dataList)

    return dataList