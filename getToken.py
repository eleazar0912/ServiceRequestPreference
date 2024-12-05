import pandas as pd
import json
import requests



def generateToken():
    # Insert File Excel
    excel_file = 'environment.xlsx'
    dataframe = pd.read_excel(excel_file)
    # END

    tokenEndpoint = dataframe['tokenEndpoint'].values[0]
    urlEndpoint = tokenEndpoint.split('/')[2]
    grant_type = dataframe['grant_type'].values[0]
    client_id = dataframe['client_id'].values[0]
    client_secret = dataframe['client_secret'].values[0]
    scope = dataframe['scope'].values[0]

    token = 'Bearer '
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}

    request_body = {
                    "grant_type": str(grant_type),
                    "client_id": str(client_id),
                    "client_secret": str(client_secret),
                    "scope": str(scope)
            }

    response = requests.post(tokenEndpoint, data=request_body,headers=headers)
    token += response.json()['access_token']
   # token += 'eyJhbGciOiJSUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICJQY29mdGQ2YTgyalJXRlhXSlliMF82ajhGTFREQnhmRU1idF9Yd2FHaHBFIn0.eyJleHAiOjE3MzMxNTk2MzIsImlhdCI6MTczMzE1NjAzMiwianRpIjoiYmU5YTc3NDAtMWJiNi00NTI2LWFmMTAtMGQ4NGIwNmEzMjI1IiwiaXNzIjoiaHR0cHM6Ly9yZHItdGVzdC5pZnNjbG91ZC5jb20udHIvYXV0aC9yZWFsbXMvcmRyLXRlc3QiLCJhdWQiOlsicmRyLXRlc3QiLCJhY2NvdW50Il0sInN1YiI6IjQ2ODA2M2FiLTE2ZmMtNDc1NC1hODNlLTI0ZmFmMTc3OGU2NyIsInR5cCI6IkJlYXJlciIsImF6cCI6IlBPU1RNQU4iLCJzZXNzaW9uX3N0YXRlIjoiMzk2ODIwNTMtYTY2MC00OWI5LWFkMmQtNTE1MWZjMjBlOThiIiwicmVhbG1fYWNjZXNzIjp7InJvbGVzIjpbIm9mZmxpbmVfYWNjZXNzIiwiZGVmYXVsdC1yb2xlcy1yZHItdGVzdCIsInVtYV9hdXRob3JpemF0aW9uIl19LCJyZXNvdXJjZV9hY2Nlc3MiOnsiYWNjb3VudCI6eyJyb2xlcyI6WyJtYW5hZ2UtYWNjb3VudCIsIm1hbmFnZS1hY2NvdW50LWxpbmtzIiwidmlldy1wcm9maWxlIl19fSwic2NvcGUiOiJvcGVuaWQgYXVkaWVuY2UgZW1haWwgbWljcm9wcm9maWxlLWp3dCBwcm9maWxlIiwic2lkIjoiMzk2ODIwNTMtYTY2MC00OWI5LWFkMmQtNTE1MWZjMjBlOThiIiwidXBuIjoicG9zdG1hbiIsImNsaWVudEhvc3QiOiIxOTIuMTY4LjEyMi4xIiwiY2xpZW50SWQiOiJQT1NUTUFOIiwiZW1haWxfdmVyaWZpZWQiOmZhbHNlLCJncm91cHMiOlsib2ZmbGluZV9hY2Nlc3MiLCJkZWZhdWx0LXJvbGVzLXJkci10ZXN0IiwidW1hX2F1dGhvcml6YXRpb24iXSwicHJlZmVycmVkX3VzZXJuYW1lIjoicG9zdG1hbiIsImNsaWVudEFkZHJlc3MiOiIxOTIuMTY4LjEyMi4xIn0.vfckKgfNIL_3V6ApSwByAr09zvneXIf910LPdHf2_JPhGMrE_jSFFP_enCPSNAavbt9s-TXWAcKurKeSmraYrLd1Sst_eU2ajEUGfHK2h7KpjP_PScWSP7JYj_oac-8NfjCrw-P_M167O53Ze31lXMdZMzaH6_5Bp6cOow_6Iop7T5yrCooRbtjAlKycrhURKRE3q27uVRFF1ZuAt89aZr5MCjvFs8YJHeXC0FUcK0eUHyosDavpLLzRYhy4zZxaUXPgptDUJAAu31GQTm4ppauKk2ZYrnd2t5M08HkwqSBM5jtNUHzSh4d4Ve3n3ZplbE5Pi_NvHwAA08gG6xrTlA'
    out = {'urlEndpoint':urlEndpoint,"token":token}
    return out

