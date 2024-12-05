from ServiceRequestData import ServiceRequestList
from Preferences_SchedTask import PreferencesResourceList
import requests
from getToken import generateToken
import json

#print(ServiceRequestList())

lista = ServiceRequestList()
urlIFS_token = generateToken()
preferResList = PreferencesResourceList()
urlIFS = urlIFS_token['urlEndpoint']
tokenIFS = urlIFS_token['token']
header = {"Authorization":tokenIFS}
with open("ServiceRequests_OK.txt", "a+") as myfile:
    myfile.write('[')
with open("ServiceRequests_NOK.txt", "a+") as myfile:
    myfile.write('[')


for index, elem in enumerate(lista):
    # Get AddressId
    urlLocationSet = "https://"+urlIFS+"/main/ifsapplications/projection/v1/LocationHandling.svc/LocationSet(LocationId='"+str(elem['LocationId'])+"')"
    #print(urlLocationSet)
    #print(header)
    getLocationSet = requests.get(urlLocationSet,headers=header)
    if getLocationSet.status_code == 200:
        print('OK_Location')
        getAddressId = getLocationSet.json()['VisitAddress']
        elem['AddressInfoId'] = getAddressId
        
        #Set Service Request
        urlServiceRequestSet = "https://"+urlIFS+"/main/ifsapplications/projection/v1/RequestHandling.svc/SrvRequestVirtualSet"
        body = json.dumps(elem)
        postServiceRequestSet = requests.post(urlServiceRequestSet, data=body,headers=header)
        #print('postServiceRequest: ',postServiceRequestSet)
        if postServiceRequestSet.status_code == 201:
            getObjkey = postServiceRequestSet.json()['Objkey']
            print('OK_ServiceRequestCreation')
            #Create Service Request
            urlCreateServiceRequestSet = "https://"+urlIFS+"/main/ifsapplications/projection/v1/RequestHandling.svc/SrvRequestVirtualSet(Objkey='"+getObjkey+"')/IfsApp.RequestHandling.SrvRequestVirtual_Finish"
            postServiceRequestSet = requests.post(urlCreateServiceRequestSet,headers=header)
            if postServiceRequestSet.status_code ==201 or postServiceRequestSet.status_code==200:
                elem['NewReqId'] = postServiceRequestSet.json()['NewReqId']
                print('OK_ServiceRequestCreation')
                # START PREFERENCES
                # Get Sequence of the Resource
                resourceId = preferResList[index]['ResourceId']
                urlGetResourceSeq = "https://"+urlIFS+"/main/ifsapplications/projection/v1/ServiceResourceDetailsHandling.svc/Reference_ResourcePersonLov(PersonId='"+resourceId+"')"
                getResourceSeq = requests.get(urlGetResourceSeq,headers=header)
                if getResourceSeq.status_code ==201 or getResourceSeq.status_code==200:
                    resourceSeq = getResourceSeq.json()['ResourceSeq']
                    preferResList[index]['ResourceSeq'] = resourceSeq
                    print('OK_ResourceSequence')
                else:
                    with open("ServiceRequests_NOK.txt", "a+") as myfile:
                        myfile.write(body)
                    print('NOK___')
                
                # Get Tasks of the Service Request
                print(elem['NewReqId'])
                urlGetWorkTasks = "https://"+urlIFS+"/main/ifsapplications/projection/v1/RequestHandling.svc/SrvRequestSet(ReqId='"+elem['NewReqId']+"')/RequestWorkTaskArray"
                #print(urlGetWorkTasks)
                getWorkTaskFromServiceRequest = requests.get(urlGetWorkTasks,headers=header)
                #print(getWorkTaskFromServiceRequest)
                if getWorkTaskFromServiceRequest.status_code ==201 or getWorkTaskFromServiceRequest.status_code==200:
                    print('OK_WorkTasks')
                    workTasks = getWorkTaskFromServiceRequest.json()['value']
                    for elem in workTasks:
                        preferResList[index]['TaskSeq'] = elem['TaskSeq']
                        body = json.dumps(preferResList[index])
                        #print(body)
                        urlCreatePreference = "https://"+urlIFS+"/main/ifsapplications/projection/v1/WorkTaskServiceHandling.svc/JtTaskSet(TaskSeq="+str(elem['TaskSeq'])+")/SvcschTaskPreferenceArray"
                        postCreatePreference = requests.post(urlCreatePreference,data=body,headers=header)
                        #print(urlCreatePreference)
                        if postCreatePreference.status_code ==201 or postCreatePreference.status_code==200:
                            print('OK_ResourcePreference')
                        else:
                            with open("ServiceRequests_NOK.txt", "a+") as myfile:
                                myfile.write(body)
                            print('NOK___ResourcePreference')
                else:
                    with open("ServiceRequests_NOK.txt", "a+") as myfile:
                        myfile.write(body)
                    print('NOK___')


                #END PREFERENCES



                bodyDebug = json.dumps(elem)
                with open("ServiceRequests_OK.txt", "a+") as myfile:
                    myfile.write(bodyDebug+',')
                print(postServiceRequestSet.json()['NewReqId'])
                
                
                
            else:
                with open("ServiceRequests_NOK.txt", "a+") as myfile:
                    myfile.write(body)
                print('NOK___')
        
    else:
        print('NOK: status',getLocationSet.status_code)
        with open("ServiceRequests_NOK.txt", "w") as myfile:
            myfile.write(body+'\n'+getLocationSet.json())

# Set Preferences


with open("ServiceRequests_OK.txt", "a+") as myfile:
    myfile.write(']')
with open("ServiceRequests_NOK.txt", "a+") as myfile:
    myfile.write(']')