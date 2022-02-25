import requests as r
from urllib import parse as parse

url = parse.urlparse("wss://sbapi.sbtech.com/mooshpt/sportscontent/sportsbook/v1/Websocket?jwt=eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJTZXNzaW9uSVAiOiIxNzYuNzguMjYuMTMwIiwiU2l0ZUlkIjoxNTEsIlZlcnNpb24iOiIyIiwiU2Vzc2lvbklkIjoiMmJmYmJlYTUtNGMyNy00MmQ2LWJhNmMtNmM2OGM5NTVjMTliIiwibmJmIjoxNjQ1Nzg3ODM5LCJleHAiOjE2NDYzOTI2NjksImlhdCI6MTY0NTc4Nzg2OSwiaXNzIjoiQXN5bW1ldHJpY1Rva2VuTWFuYWdlciJ9.gfnaLrk0CZT9JKs4fdvuEFbn6MRgVMRRMe7KCm3Rrpr6Q9piw2V8_Cl2MqxRbTX9IYxyse_xz1JDGA8sHFueVjxggJ98mEKoCX_7rNSjsGjbIx0W7kNdmRmXCG6_U0yq_kUEyow9S03h_MSQLgAeZ6r-Aa9_Ezi1tgd75GzbhoAuuYKl2V15gFf-nxBIMt-M38SlZyzwS0qGvEfd4uvMCvWfG6f9sMiH3pdBjeyINHyK6jyDSUxBrqrmJhZ9lKen5somCUlZPmOzhh66xSDF5tROh3s1cdzyccErrxOKIxU4jaFfN2NPwvsUq9Y1pv_lzZoyefCBFYdGu4xUMibDNQ&locale=pt-pt")


print(str(url) + "\n\n")

string = ""
for c in url[4]:
    if c != "&":
        string += c
    else:
        print(string)
        string = ""
