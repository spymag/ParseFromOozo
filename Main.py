import json
import urllib2
import lxml.etree as ET

def returnElements(root):
    FooList=[]
    for elements in root.findall('Table'):
        gemeenteurl = elements.find('gemeenteurl').text 
        wijkurl = elements.find('wijkurl').text
        buurturl = elements.find('buurturl').text
        statusurl = elements.find('statusurl').text
        objectid = elements.find('objectid').text
        paginaurl = elements.find('paginaurl').text
        #print(gemeenteurl, wijkurl, buurturl, statusurl, objectid, paginaurl)
        foo = ('http://www.oozo.nl/woningen/'+gemeenteurl+'/'+wijkurl+'/'+buurturl+'/'+statusurl+'/'+objectid+'/'+paginaurl+' ')
        FooList.append(foo)
    return(FooList)

def returnRoot(pageIndex,straatnaam):
    data = {'pageIndex': pageIndex, 'dataTypeId': 7, 'provincieId': 0, 'meldingsoortId': 0, 'gemeentecode': 599, 'wijkcode': 59901, 'buurtcode': 5990110, 'straatnaam': straatnaam, 'sbiCode': ""}
    url='http://www.oozo.nl/woningen/rotterdam/rotterdam-centrum/stadsdriehoek/wijnkade'
    req = urllib2.Request('http://www.oozo.nl/Zoeken.aspx/GetDataItems')
    req.add_header('Content-Type', 'application/json')
    req.add_header('Referer',url )
    response = urllib2.urlopen(req, json.dumps(data))
    jsonString = response.read()
    jsonA = json.loads(jsonString)
    xmlResult = jsonA['d']
    #print xmlResult
    root = ET.fromstring(xmlResult)
    return(root)     
            
            
                
        
    
    

def WriteLinkFiles(address):    
    pageIndex=1
    resultsFile=address+'.txt'
    with open(resultsFile, 'w') as file_:
        while pageIndex<100:    
            root=returnRoot(pageIndex,address)
            foo=returnElements(root)
            if not foo==[]:
                pageIndex+=1
                foo.append(str(foo))              
            else:    
                pageIndex=1000
            foos=str(foo)
            print foos
            file_.write(str(foos))

#addresses = ["Wijnkade","Jufferkade","Scheepmakerskade","Jufferstraat","Bierstraat","Wijnhaven","Wijnbrugstraat","Wijnstraat"]
addresses = ["Wijnstraat"]
for address in addresses:
    WriteLinkFiles(address)    

