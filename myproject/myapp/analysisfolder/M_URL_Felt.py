import pandas as pd
import numpy as np
from collections import Counter
#Added
import os
from myapp.models import FileData
from django.core.files import File as DjangoFile
import traceback

#Added
def CleanURlAndAddColumn(Data,columnName):
    
    df = Data.formURL.str.split("?", expand = True, n=6).rename(columns={0:"Befor", 1: "Efter"})
    # delete columns
    df = df.drop([ 'Efter'], axis=1)
    df= df.Befor.str.split('/', expand = True, n=10)
    df=df.fillna("") # hvis det er non vil sætte en tom space istedet for
    ll = []
    for i in np.arange(len(df)): # dfnew er en dataframe med alle urler fra formURL, er blevet splittet med "/"
        line= df.iloc[i]# tager en af gang hver splittet url
        http=""
        if line[0].startswith('http'):
            for j in np.arange(len(line)):  # loop rundt i eneste splittet url
                lineSplit= line[j] 

                if lineSplit is None:# hvis den del af splittet url er tomt, så gøres ingen ting
                     http=http       
                elif len(lineSplit)> 0:
                    t2=lineSplit.split("-") # split elementen with(-) for vi ved at der findes noget i urlen der ligner kode og har mange "-" i mellem
                    if (len(t2)==1):
                        try:
                            int(lineSplit) # hvis splitet del ikke kan converts to int kommer i exept del og bliver added
                        except:
                            http=http+lineSplit+"/" 
        else:
            http="NONE"


        ll.append(http) # http er rene url hvor det bliver added til en list
    ll=[w.replace("https:/erst.virk.dk/","") for w in ll] 
    ll=[w.replace("#0","") for w in ll] 
    ll=[w.replace("https://erst.virk.dk/","") for w in ll]
    ll=[w.replace("#","") for w in ll]
    ll=[w.replace("*","") for w in ll]
    Data.insert(13, '{}'.format(columnName), ll, True) # make a new column data and put list ind i
    return Data

def makeUniqe(Data, columnName1,newcolumnName1,newcolumnName2):
    
    Data=pd.DataFrame(Data)
    listOfuniqUrl=pd.DataFrame(Data['{}'.format(columnName1)].unique()).rename(columns={0:'{}'.format(newcolumnName1)})
    listOfuniqUrl['{}'.format(newcolumnName2)] = list(np.arange(len(listOfuniqUrl)))
    return listOfuniqUrl

def makeDictionary(listOfuniqUrl):
    HashlistOfUrl= listOfuniqUrl.to_dict()
    return HashlistOfUrl
def findURLRejser(Data,columnName1,columnName2,columnName3):
    uniqIdGruppeClearUrl =pd.DataFrame( Data.groupby(['{}'.format(columnName1)]).agg({'{}'.format(columnName2): '  #Mellemrum#  '.join}) )
    listOfNotRepeatetURl=[]
    for i in np.arange(len(uniqIdGruppeClearUrl)):
        ClearHttp=[]
        #gruppetClearUrlSplitet= uniqIdGruppeClearUrl.clearURL.str.split("#Mellemrum#")[i] #split de url som vi lagt sammen med Mellemrum
        gruppetClearUrl= uniqIdGruppeClearUrl['clearURL'][i] 
        gruppetClearUrlSplitet=gruppetClearUrl.split('#Mellemrum#')#split de url som vi lagt sammen med #Mellemrum# 
        nloop=len(gruppetClearUrlSplitet)-1 # vi tager et tal mindre fordi ind i loopen kommer vi en data frem
        for j in np.arange(nloop):
            url1 = gruppetClearUrlSplitet[j].strip()
            url2= gruppetClearUrlSplitet[j+1].strip()
            if j != (nloop-1):  #hvis vi er ikke i den sidste loop. 'j' når aldrig til den sisdte tal i loopen                       
                if url1!= url2:
                    ClearHttp.append(url1) # addes ikke noget element indtil de urler er ikke ens, så addes url1 
            else: #hvis vi er i den sidste loop.   
                if url1!= url2: # i det sidste hvis de urler ikke er ens addes begge to
                    ClearHttp.append(url1)
                    ClearHttp.append(url2) 
                else: 
                    ClearHttp.append(url2) #I det sidste element hvis de urler er ens addes en af dem 

        listOfNotRepeatetURl.append(ClearHttp) # addes dem der ikke er gentaget -> rensede urler 

    uniqIdGruppeClearUrl['{}'.format(columnName3)] = listOfNotRepeatetURl # i de ny kolumns addes deres rensede url

    return uniqIdGruppeClearUrl
def makecounter(uniqIdGruppeClearUrl,columnName):
    
    dict1 = Counter([tuple(i) for i in uniqIdGruppeClearUrl['{}'.format(columnName)]]) 
    UrlRejserAndCount = pd.DataFrame(data ={'ListOfUrlRejser': list(dict1.keys()), 
                         'count': list(dict1.values())}) 
    UrlRejserAndCount['ListOfUrlRejser']=UrlRejserAndCount['ListOfUrlRejser'].apply(lambda row: list(row))
    return UrlRejserAndCount

def enterNumbersInsteadOfName(uniqIdGruppeClearUrl,HashlistOfUrl,listOfuniqUrl):

    uniqIdGruppeClearUrl=uniqIdGruppeClearUrl['newClearURL'].to_frame()
    for i in np.arange(len(uniqIdGruppeClearUrl)):
        newClearUrlRow=uniqIdGruppeClearUrl['newClearURL'][i]# hives ud hver urlrejse
        for j in np.arange(len(newClearUrlRow)): # hives ud hver url
            for x in np.arange(len(listOfuniqUrl)):
                if (newClearUrlRow[j]==HashlistOfUrl['urlName'][x]): # findes tal der passer til den url gennem det unik url hashlisten
                    newClearUrlRow[j]=listOfuniqUrl.urlNumber[x]                    
        #uniqIdGruppeClearUrl['newClearURL'][i]=newClearUrlRow
    return uniqIdGruppeClearUrl

def saveToCsv_2(UrlRejserAndCount,columnName1,columnName2, path):
    try:
        UrlRejserAndCount[['{}'.format(columnName1),'{}'.format(columnName2)]].to_csv(path ,sep=";", index=False)
        print("CSV file saved!")
    except Exception as e: 
        print(str(e))


def clearFelt(Data, columnName1, columnName2, newColumnName):
    Data = pd.DataFrame(Data)
    gatherFieldidOrFieldName = []
    for i in np.arange(len(Data)):
        feltid = Data['{}'.format(columnName1)][i]

        if ((type(feltid) != type(0.0)) & (feltid != "NONE")):
            # hvis felt id ikke var None eller float type :

            if ((len(feltid.split(" ")) > 15)):
                gatherFieldidOrFieldName.append("NONE")  # hvis den er feltid er for langt så vil addes "NONE"
            elif ("\\n" in feltid):
                feltid = feltid.replace('\\n', "")
                gatherFieldidOrFieldName.append(str(feltid))
            elif (len(feltid.split("-")) > 2):
                gatherFieldidOrFieldName.append('LikeUSERID')
            else:
                gatherFieldidOrFieldName.append(str(feltid))

        else:
            feltNavn = Data['{}'.format(columnName2)][i]
            #print('feltNavn', feltNavn)

            if ((type(feltNavn) == type(0.0)) or (len(feltNavn.split(" ")) > 15) or (feltNavn == "NONE")):
                gatherFieldidOrFieldName.append("NONE")
            else:

                if ("\\n" in feltNavn):
                    feltNavn = feltNavn.replace('\\n', "")  # vil fjerne hvis de er en nylinjetejn '\\n'
                    feltNavn = feltNavn.lstrip()
                    gatherFieldidOrFieldName.append(str(feltNavn))
                elif (len(feltNavn.split("-")) > 2):
                    gatherFieldidOrFieldName.append('LikeUSERID')
                else:
                    gatherFieldidOrFieldName.append(str(feltNavn))
    Data.insert(14, '{}'.format(newColumnName), gatherFieldidOrFieldName, True)
    return Data

def clearFelt1(Data,columnName1,columnName2,newColumnName):

    Data=pd.DataFrame(Data)
    #print(' feltnavn    ',Data['feltNavn'].unique())
    #print(Data['feltNavn'].unique())
    gatherFieldidOrFieldName=[]
    for i in np.arange(len(Data)):
        feltid = Data['{}'.format(columnName1)][i]

        if(type(feltid)!=type(0.0)):     # hvis felt id ikke var None eller float type :

            if((len(feltid.split(" "))>15)):
                gatherFieldidOrFieldName.append("NONE")# hvis den er feltid er for langt så vil addes "NONE"
            elif("\\n" in feltid):              
                feltid=feltid.replace('\\n',"")            
                gatherFieldidOrFieldName.append(str(feltid))
            elif(len(feltid.split("-"))>2):
                gatherFieldidOrFieldName.append('LikeUSERID') 
            else:
                gatherFieldidOrFieldName.append(str(feltid))

        else:
            feltNavn =Data['{}'.format(columnName2)][i]  
            #print (feltNavn)
            if (type(feltNavn)==type(0.0) or (len(feltNavn.split(" "))>15) ):
                gatherFieldidOrFieldName.append("NONE")
            else:

                if("\\n" in feltNavn):
                    feltNavn=feltNavn.replace('\\n',"")#vil fjerne hvis de er en nylinjetejn '\\n' 
                    feltNavn=feltNavn.lstrip()
                    gatherFieldidOrFieldName.append(str(feltNavn))
                elif(len(feltNavn.split("-"))>2):
                    gatherFieldidOrFieldName.append('LikeUSERID')  
                else:
                    gatherFieldidOrFieldName.append(str(feltNavn))


    Data.insert(14,'{}'.format(newColumnName),gatherFieldidOrFieldName, True)
    print(Data['clearField'].unique())
    return Data

def delete_Handlig_Bluer_And_Reset_Index(Data):
    haandling=''
    iListHandlingHaveBlur=[]
    Data = Data.replace(np.nan, 'NONE', regex=True)
    for i in np.arange(len(Data)):
        try:
            haandling = Data['handling'][i]
        except :
            print(i )

        if (haandling=='blur'):
            iListHandlingHaveBlur.append(i)

    Data.drop(Data.index[iListHandlingHaveBlur], inplace=True)
    Data.reset_index(drop=True ,inplace = True)
    return Data


def appendMethod(feildList,nummberUniqUrl,listOfFeildList,listOfUrlid):
    listOfFeildList.append(feildList)
    listOfUrlid.append(nummberUniqUrl)
    return listOfFeildList,listOfUrlid;  


def findeUrlNum(listOfuniqUrl, HashlistOfUrl,urlRow):
    nummberUniqUrl=5000
    import numpy as np
    for k in np.arange(len(listOfuniqUrl)):# finde tal nummer til uniq url 
        if ((urlRow.clearURL.strip())==(listOfuniqUrl.urlName[k].strip())):
            nummberUniqUrl= HashlistOfUrl['urlNumber'][k]
    if(nummberUniqUrl==5000):
        print("unik url name :"+urlRow.clearURL.strip())
    return nummberUniqUrl


def findeFeildOrServerTime(Data, listOfuniqUrl, HashlistOfUrl, columnsName):
    listOfUrlid = []
    List = []
    listOfList = []
    #print(columnsName)
    #print(len(Data))
    if (columnsName=='clearField'):
        Data= Data[Data['clearField']!="NONE"]

    #print(len(Data))
    if(len(Data)>1):
        aNumberLessOfDataLength = (len(Data) - 1)  # hvor vi i methoden kalder vi en value frem af, for at undgå få exeption
        toNumberLessOfDataLength = aNumberLessOfDataLength - 1  # når i en for loop ikke vi at i rammer sidste element

        for i in np.arange(aNumberLessOfDataLength):  # loop for at finde hver linje i Data

            row1 = Data.iloc[i]
            row2 = Data.iloc[i + 1]

            nummberUniqUrl = findeUrlNum(listOfuniqUrl, HashlistOfUrl, row1)  # beregner tal for en url

            if (i != (toNumberLessOfDataLength)):  # når vi er er en til sidste data row
                if ((row1.id == row2.id) and (row1.clearURL.strip() == row2.clearURL.strip())):  # når en brugeren er ens og brugeren er på en url.

                    List.append(row1.get(key=columnsName))  # så tager vi den første rækkes servertimeStamp og sætter# i en list.

                else:  # Hvis brugeren eller urlen ikke er ens så addes den første række til servertime list og bruge
                    List.append(row1.get(key=columnsName))  # en method for at adde de servertime list og url id
                    listOfList, listOfUrlid = appendMethod(List, nummberUniqUrl, listOfList, listOfUrlid)
                    List = []  # tommes servertime list når brugern eller url er ikke ens

            else:  # når er den sidste række af data
                if ((row1.id == row2.id) and (
                        row1.clearURL.strip() == row2.clearURL.strip())):  # hvis brugeren og url er ens
                    List.append(row1.get(key=columnsName))  # addes begge serverTimeStamp og url id addes til
                    List.append(row2.get(key=columnsName))
                    listOfList, listOfUrlid = appendMethod(List, nummberUniqUrl, listOfList, listOfUrlid)
                else:  # hvis brugern eller url ikke er ens i den sidste 2 række
                    List.append(row1.get(key=columnsName))  # Først addes den første række serverTimeStamp og dens url
                    listOfList, listOfUrlid = appendMethod(List, nummberUniqUrl, listOfList, listOfUrlid)
                    List = []  # så tommes time liste
                    List.append(row2.get(key=columnsName))  # addes næste serverTimeStamp
                    nummberUniqUrl = findeUrlNum(listOfuniqUrl, HashlistOfUrl,
                                                 row2)  # finde url nr og kalder den 'appendMethod'
                    listOfList, listOfUrlid = appendMethod(List, nummberUniqUrl, listOfList, listOfUrlid)

        listOfUrlIdAndFeltRejse = pd.DataFrame(data={'Urlid': list(listOfUrlid),
                                                     'List': list(listOfList)})
    return listOfUrlIdAndFeltRejse


def enters_Numbers_Instead_Of_Felt_Name(listOfUrlIdAndFeltRejse,HashListfeild):
    listOfAllNumOFFeildList=[]
    for i in np.arange(len(listOfUrlIdAndFeltRejse)):# list of feltlister sammen med urlider
        listFieldRow=listOfUrlIdAndFeltRejse['List'][i]    #row fra felt lister
        listOfFeilt=[]
        for j in np.arange(len(listFieldRow)): # looper i hver row, hver row har måsker list af urler
            field=listFieldRow[j] # første element
            if (type(field) == list): #hvis første element er også en liste, har vi bruge for kun den første element
                field = field[0]
            for x in np.arange(len(HashListfeild["FeildName"])): #her finder vi tal nummer til hver felter
                if field==HashListfeild["FeildName"][x] or ((type(field)==type(0.0)) & (type(HashListfeild["FeildName"][x])==type(0.0))):
                    # Non element giver besværligheder for at undgå det checker vi det at element er non(Float) eller ej
                    listOfFeilt.append(x)
                    break
        listOfAllNumOFFeildList.append(listOfFeilt)

    listOfUrlIdAndFeltRejse["listOfNumberOFFelt"]=listOfAllNumOFFeildList                   
    return listOfUrlIdAndFeltRejse 

def make_Csv_For_FeldList_for_every_URL(listOfuniqUrl,listOfUrlIdAndFeltRejse, path):
    # try:
        for i in np.arange(len(listOfuniqUrl)):# I in en størelse af unike url liste efter delete data med ''
            csvname= path+'FeltBrugerRejser_Under_URL{}.csv'.format(i)
            # opretter 
            #dynamic navn for csv file som vil indeholde felt brugerrejser og antal af dem

            listQuery=listOfUrlIdAndFeltRejse.query('Urlid==@i')[['List']]#hiver data ud fra
            # hver unike url id og bruger dens felterrejser 
            countfeltamount = Counter([tuple(i) for i in listQuery['List']])# beregner antal af de uniq felter

            FeltRejserAndCount = pd.DataFrame(data ={'feltLis': [list(t) for t in countfeltamount.keys()],
                                 'count': list(countfeltamount.values())}) # opretter en DF med unike felt brugerrejse og antal af dem
            csv_file = FeltRejserAndCount.to_csv(csvname,sep=";", index=False)# kaster den DF to csv med den dynamic navn fra ovnpå  

        print("CSV file saved!")
    # except Exception as e: 
    #     print(str(e))


def makeDependency():
    import pandas as pd
    import numpy as np
    import os
    import time
    from collections import Counter
    from datetime import timedelta
    import matplotlib.pyplot as plt
    import random
    from myapp.analysisfolder import M_URL_Felt as felt
    from myapp.analysisfolder import M_Time as time
    from myapp.analysisfolder import M_PID_RID as PID_RID
    return pd,np,os,time,Counter,timedelta,plt,random,felt,time,PID_RID


def find_Felt_Under_Url_for_every_User1(Data,listOfuniqUrl,HashlistOfUrl):

    listOfUrlid=[]
    feildList=[]
    listOfFeildList=[]

    aNumberLessOfDataLength= (len(Data)-1) # hvor vi i methoden kalder vi en value frem af, for at undgå få exeption
    toNumberLessOfDataLength=(len(Data)-2) # når i en for loop "i" skal ramme størrelse eller sidste element


    for i in np.arange(aNumberLessOfDataLength): #loop for at finde hver linje i Data
        #finde 2 rows af data af gang
        row1=Data.iloc[i]
        row2=Data.iloc[i+1]
        nummberUniqUrl=0

        nummberUniqUrl= findeUrlNum(listOfuniqUrl,HashlistOfUrl,row1)# finde id eller den tal for hver url, for
        # vi vil adde url id til de felter vi samler fra

        if (i!=(toNumberLessOfDataLength)): # hvis datarow er ikke den ene som er tilbage til den sidste.
            if((row1.id==row2.id) and (row1.clearURL.strip()==row2.clearURL.strip())):#hvis 2 row af data er fra
                #en bruger som er i en url addes clearField to en list og venter til den næste hvis den er stadig ens
                #Derfor tommes den liste ikke indtil brugeren eller url er ikke ens!
                feildList.append(row1.clearField)

            else:  # hvor der ikke er en bruger eller brugeren ikke er under en url så addes den først felt navn og
                #den list addes til den anden liste som gemmes urler i og derefter tommes feltList
                feildList.append(row1.clearField)
                listOfFeildList,listOfUrlid=appendMethod(feildList,nummberUniqUrl,listOfFeildList,listOfUrlid)
                feildList=[]

        else:  # når vi er en tilbage af sidste row

            if((row1.id==row2.id) and (row1.clearURL.strip()==row2.clearURL.strip())):#hvis brugeren og url er ens
                feildList.append(row1.clearField) # addes de to sidste felt navner
                feildList.append(row2.clearField)
                listOfFeildList,listOfUrlid=appendMethod(feildList,nummberUniqUrl,listOfFeildList,listOfUrlid)
            else:
                feildList.append(row1.clearField) # hvis brugeren og url er ikke ens, først addes den første clearField
                #addes den liste to den stor liste og så tommes
                listOfFeildList,listOfUrlid=appendMethod(feildList,nummberUniqUrl,listOfFeildList,listOfUrlid)
                feildList=[]
                feildList.append(row2.clearField) #så addes den sidste clearField to
                nummberUniqUrl= findeUrlNum(listOfuniqUrl,HashlistOfUrl,row2)
                listOfFeildList,listOfUrlid=appendMethod(feildList,nummberUniqUrl,listOfFeildList,listOfUrlid)


    listOfUrlIdAndFeltRejse = pd.DataFrame(data ={'Urlid': list(listOfUrlid),
                         'FeildList': list(listOfFeildList)})
    return listOfUrlIdAndFeltRejse