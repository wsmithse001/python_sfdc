from zeep import Client
from zeep.helpers import serialize_object

username = 'xxxxx'
password = 'xxxxx'
wsdl = './sfdc_partner.wsdl'

def login():
    client = Client(wsdl)
    serviceBinding = '{urn:partner.soap.sforce.com}SoapBinding'
    loginResult = client.service.login(username, password)
    client._default_soapheaders ={'SessionHeader':{'sessionId' : loginResult.sessionId}}
    clientService = client.create_service(serviceBinding, loginResult.serverUrl)
    return clientService

def processsObjects(clientService):
    sobjects = serialize_object(clientService.describeGlobal()).get('body', {}).get('result', {}).get('sobjects', {})
    for sobject in sobjects:
        sObjectName = sobject['name']
        describesObjectFields = serialize_object(clientService.describeSObject(sObjectName)).get('body', {}).get('result', {}).get('fields', {})
        processsDescribesObjectFields(clientService, sobject, describesObjectFields)

def processsDescribesObjectFields(clientService, sobject, describesObjectFields):
    for describesObjectField in describesObjectFields:
        fieldType = describesObjectField['type']
        if (
            (fieldType == 'picklist') or
            (fieldType == 'multipicklist')
            ):
            processPicklistField(clientService, sobject, describesObjectField)

def processPicklistField(clientService, sobject, describesObjectField):
    picklistValues = describesObjectField['picklistValues']
    for picklistValues in picklistValues:
        sobjectname = sobject['name']
        fieldname = describesObjectField['name']
        label = picklistValues['label']
        value = picklistValues['value']
        txt = f'"{sobjectname}","{fieldname}","{label}","{value}"'
        print(txt)

clientService = login()
print('"sobjectname","fieldname","label","value"')
processsObjects(clientService)
clientService.logout()
