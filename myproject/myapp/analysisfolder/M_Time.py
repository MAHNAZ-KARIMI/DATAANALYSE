import pandas as pd
import numpy as np
import os
import time
import datetime
import matplotlib.pyplot as plt
import matplotlib
from collections import Counter
from myapp.analysisfolder import M_URL_Felt as felt
from myapp.analysisfolder import M_Time as time


def make_ready_new_columns(Data):

    pd.set_option('display.max_columns', None)
    pd.options.display.max_colwidth = 200
    Data = Data.replace(np.nan, 'NONE', regex=True)
    Data['handling'] = Data['handling'].apply(lambda row: 'NONE' if type(row)==type(0.0) else row)
    Data['feltType'] = Data['feltType'].apply(lambda row: 'NONE' if type(row) == type(0.0) else row)
    Data['feltId'] = Data['feltId'].apply(lambda row: 'NONE' if type(row) == type(0.0) else row)
    Data['feltNavn'] = Data['feltNavn'].apply(lambda row: 'NONE' if type(row) == type(0.0) else row)


    Data= felt.CleanURlAndAddColumn(Data,"clearURL")
    listOfuniqUrl= felt.makeUniqe(Data,"clearURL","urlName","urlNumber")
    HashlistOfUrl= felt.makeDictionary(listOfuniqUrl)
    Data= felt.clearFelt(Data,'feltId','feltNavn','clearField')
    listUniqeClearfield= felt.makeUniqe(Data,"clearField","FeildName","numberOfField")
    HashListfeild= felt.makeDictionary(listUniqeClearfield)
    ListOfUniqUserIds= felt.makeUniqe(Data,"id","id","Number")
    return Data,listOfuniqUrl,HashlistOfUrl,listUniqeClearfield,HashListfeild,ListOfUniqUserIds

def findeUrlNum1(listOfuniqUrl, urlRow, HashlistOfUrl):
    for k in np.arange(len(listOfuniqUrl)):# finde tal nummer til uniq url 
        if ((urlRow.clearURL.strip())==(listOfuniqUrl.urlName[k].strip())):
            nummberUniqUrl= HashlistOfUrl['urlNumber'][k]
            break 
    return nummberUniqUrl
def appendMethod(timeList,nummberUniqUrl,listOfTimeList,listOfUrlid):
    listOfTimeList.append(timeList)
    listOfUrlid.append(nummberUniqUrl)
    return listOfTimeList,listOfUrlid;
def findeFeldName(tal,listUniqeClearfield):

    for k in np.arange(len(listUniqeClearfield)):# finde tal nummer til uniq url 
        if (tal==(listUniqeClearfield.numberOfField[k])):
            nameOfFeldt= listUniqeClearfield['FeildName'][k]
            break
    return nameOfFeldt  
def findeHASHFeldName(tal,listUniqeClearfield,HashListfeild):

    for k in np.arange(len(listUniqeClearfield)):# finde tal nummer til uniq url 
        if (tal==(listUniqeClearfield.numberOfField[k])):
            nameOfFeldt= HashListfeild['FeildName'][k]
            break
    return nameOfFeldt 
def findeFeldNum(listUniqeClearfield,row,HashListfeild,numberOfField):

    for k in np.arange(len(listUniqeClearfield)):
        if ((row.clearField.strip())==(listUniqeClearfield.FeildName[k].strip())):
            nummberOfFeldt= HashListfeild.get('{}'.format(numberOfField))[k]
            break
    return nummberOfFeldt

def makeDictionary(listOfuniqUrl):
    HashlistOfUrl= listOfuniqUrl.to_dict()
    return HashlistOfUrl


def calculateTime_URL(listOfurlIdAndServerTimeStamp,listOfUrlid):

    
    datetimeFormat = '%Y-%m-%dT%H:%M:%S.%f'
    ListOfDiffrenceTid=[]

    for i in np.arange(len(listOfurlIdAndServerTimeStamp)):
        listOfDate=listOfurlIdAndServerTimeStamp['List'][i]
        if ((len(listOfDate))==1):
            ListOfDiffrenceTid.append("0")#hvis der er kun en i list så adder vi 0
        #hvis len af data >1, tager vi den sidste og første række serverTimeStamp og beregner tid forsked mellem dem.

        else: 

            date1=datetime.datetime.strptime(listOfDate[0], datetimeFormat)#første række
            date2=datetime.datetime.strptime(listOfDate[len(listOfDate)-1], datetimeFormat)#sidste række
            diff = abs(date2-date1)
            ListOfDiffrenceTid.append(str(diff.total_seconds()))
    listOfurlIdAndDiffrenceTimeStamp= pd.DataFrame(data ={'listOfUrlid': list(listOfUrlid), 
                         'listOfDifferenceTimeStamp': list(ListOfDiffrenceTid)})
    return listOfurlIdAndDiffrenceTimeStamp

def calculateTime_total_URL(listOfurlIdAndDiffrenceTimeStamp):

    collectTime = listOfurlIdAndDiffrenceTimeStamp.groupby(['listOfUrlid']).agg({'listOfDifferenceTimeStamp': '  #Mellemrum#  '.join}) 
    collectTime=collectTime.reset_index()
    listofSecoun=[]
    listoflistSecoun=[]
    listOfTotalSec=[]
    lenOfCollection=len(collectTime)# længde af en dataframe gruppet by url id samler tider

    collectTime=pd.DataFrame(collectTime)
    for i in np.arange(lenOfCollection):  # len of url ider
        totalMili =0 
        timeSplitet=collectTime['listOfDifferenceTimeStamp'][i]# et række af gang 
        timeSplitetRow= timeSplitet.split("#Mellemrum#") #split de url som vi havde lagt sammen med #Mellemrum#
        nloop=len(timeSplitetRow)    
        for j in np.arange(nloop): 
            difrenceTime= float(timeSplitetRow[j])# kaster den tal som er tidforskel på SEC
            totalMili += difrenceTime    # lægger dem sammen    
            listofSecoun.append(difrenceTime) # så adder vi den forskel tid fra forskelige brugeren som er på sekunder
        listOfTotalSec.append(("{0:.3f}".format((totalMili))))# bruger kun 3 tal efter decimal
        listoflistSecoun.append(listofSecoun) # addes de forskel tider fra forskellige brugern til en  liste
        listofSecoun=[]  # tømmes i hver loop fordi vi vil gerne tilføje tid under en url
    listOfUrlIdAllTimeStamp= pd.DataFrame(data ={'listOfUrlid':list(collectTime['listOfUrlid']) , 
                         'listOfTimeStamp': list(listOfTotalSec)}) 
    return listOfUrlIdAllTimeStamp,listoflistSecoun


def make_Histogram_For_EveryURl(listoflistSecoun,bruger,csvName):
    #Add
    matplotlib.use('Agg')
    for i in np.arange(len(listoflistSecoun)):
        plt.figure(figsize=(10,5))
        plt.hist(list(listoflistSecoun[i]), density=False, bins=10, rwidth=1)
        plt.xlabel('Time (Sec)')
        plt.ylabel('Amount of Durations')
        plt.xticks(rotation=45)
        #print(i)
        #plt.show()
        plt.savefig('myapp/analysisfolder/Luk_Virksomhed/Histogram/'+bruger+'/URL_Tidsforbrug/'+csvName+'_TimeUsedforUrl_'+str(i)+'.png')
        plt.clf()
        plt.close()
        
def feldtTimeCalculate( Data,ListOfUniqUserIds,listOfuniqUrl,HashlistOfUrl,listUniqeClearfield,HashListfeild):
    
    handlinDataWithOutNone=Data[Data['handling'].notnull()]
    handlinAndClearFieldDataWithOutNone=handlinDataWithOutNone[handlinDataWithOutNone['clearField']!="NONE"]

    listOfUserId=[]
    listOfFeldName=[]
    listOftime=[]
    listIOfurlId=[]
    listOfFeltNr=[]
    collectUrlAndFelt=[]
    #først finder vi data hvor deres handling er ikke none og bage efter grupper vi data til hver bruger id . så 
    # en liste af user ider og en med felt navn, liste af tider, liste af url, list af felt nr, en blanding af urlog felt

    lenOfListOfUniqIds=len(ListOfUniqUserIds)
    for k in np.arange(lenOfListOfUniqIds):

        userId=ListOfUniqUserIds['id'][k]
        DataForHverUser= handlinAndClearFieldDataWithOutNone[handlinAndClearFieldDataWithOutNone['id']==userId]
        if(len(DataForHverUser)>1):

            datetimeFormat = '%Y-%m-%dT%H:%M:%S.%f'# date format 
                    #DataForHverUser er de data for hver bruger som vi finder de unike urler og unike felter ud af de data
            listUniqClearUrl= pd.DataFrame(DataForHverUser['clearURL'].unique()).rename(columns={0:"urlName"})
            listUniqClearFeldt= pd.DataFrame(DataForHverUser['clearField'].unique()).rename(columns={0:"FeildName"})

        

            #Med 2 for loop så vil vi tjeke hvis En bruger har vært det samme url og samme felt
            for x in np.arange(len(listUniqClearUrl)): 

                clearUrl=listUniqClearUrl['urlName'][x]  # url navn henholdsvis 

                for y in np.arange(len(listUniqClearFeldt)): 

                    ClearFeldt=listUniqClearFeldt['FeildName'][y] #felt navn henholdsvis            

                    userData= DataForHverUser[(DataForHverUser['clearURL']==clearUrl) 
                                            &  (DataForHverUser['clearField']==ClearFeldt)]#hiver data ud hvor
                                                #brugeren har vært i en url og en felt
                    lenDataUserOneLess=len(userData)-1 #lenOfdata hvor data er en liste af en bruger og en url og en felt
                    if((len(userData))>1):#Hvis vi har minimum to række af data og 
                                                                     #feltet er ikke "LikeUSERID"
                        for j in np.arange(lenDataUserOneLess):

                            row1=userData.iloc[j]                        
                            if (row1.handling=="focus"):# tjekker hvis første rækkes handling er focus

                                for u in (np.arange(lenDataUserOneLess-j)+j+1): # vil springe 2 række fram af
                                    # så tjekke nr 1 og 2 næste bliver 3 og 4               
                                    row2=userData.iloc[u] 

                                    if(row2.handling=="blur"): #hvis næste data rækkes handlingen er "blur"

                                        if (row1.virkStartForloebsId == row2.virkStartForloebsId):# tjekes hvis både række af 
                                                         #data har ens forløbsid
                                            date1=datetime.datetime.strptime(row1.serverTimeStamp, datetimeFormat)#første rowstid
                                            date2=datetime.datetime.strptime(row2.serverTimeStamp, datetimeFormat)#næste rows tid            
                                            diff = abs(date2-date1)# beregnes tiden når handling starter med focus og næste er blur
                                            timeForHandlig = "{0:.3f}".format(diff.total_seconds())
                                            nummberUniqUrl= felt.findeUrlNum(listOfuniqUrl, HashlistOfUrl, row1)# beregner tal for en url
                                            nummberOfFeldtt=findeFeldNum(listUniqeClearfield,row1,HashListfeild,"numberOfField")
                                            # finder nummer til felt

                                            listOfUserId.append(row1['id']) # addes user id 
                                            listOfFeldName.append(row1.clearField)# addes feltnavn
                                            listOftime.append(timeForHandlig)# tiden som er blevet beregnet
                                            listIOfurlId.append(nummberUniqUrl) # addes url id
                                            listOfFeltNr.append(nummberOfFeldtt)# addes felt id
                                            collectUrlAndFelt.append(str(nummberUniqUrl)+"-"+str(nummberOfFeldtt))
                                            # lægges sammen url id med felt id med et streg i mellem
                                            break   
                    # en dataframe med de liste af urler, feltnavn og feltider samt de tider som er brugt til hver felt 
    listOfurlAndfeildHandling = pd.DataFrame(data ={'listOfUserId': list(listOfUserId), 
                                                        'listOfFeldName':list(listOfFeldName),
                                                        'listOftime':list(listOftime),
                                                        'listIOfurlId':list(listIOfurlId), 
                                                        'listOfFeltNr':list(listOfFeltNr), 
                                                        'collectUrlAndFelt': list(collectUrlAndFelt)})       

    #listOfurlAndfeildHandling=listOfurlAndfeildHandling.sort_values(by='listIOfurlId', ascending=False)                                
    CounterUrl_Felt = Counter([(i) for i in listOfurlAndfeildHandling["collectUrlAndFelt"]]) 
    Url_Felt_Count = pd.DataFrame(data ={'url-felt': list(CounterUrl_Felt.keys()), 
                                     'count': list(CounterUrl_Felt.values())})    
    listOfurlAndfeildHandling=listOfurlAndfeildHandling.sort_values(by='listIOfurlId', ascending=False)

    return listOfurlAndfeildHandling,Url_Felt_Count; 

def saveToCsv_3(UrlRejserAndCount,columnName1,columnName2,columnName3, path):
    try:
        UrlRejserAndCount[['{}'.format(columnName1),'{}'.format(columnName2),'{}'.format(columnName3)]].to_csv(path ,sep=";", index=False)
        print("CSV file saved!")
    except Exception as e: 
        print(str(e))
        
def histogram_For_EveryFelt_in_EveryURl_Save_Quatiler11(listOfurlAndfeildHandling, collectUrlAndFelt,listUniqeClearfield,HashListfeild,path,quatiler,csvName):

    #lave histogram for hver de unikke urler and felt og tider som brugt per url og felt
    t50_arr=[]
    t90_arr=[]
    Count=[]
    #listOfurlAndfeildHandling=listOfurlAndfeildHandling.sort_values(by='collectUrlAndFelt', ascending=False)
    uniqcollectUrlAndFelt= listOfurlAndfeildHandling['{}'.format(collectUrlAndFelt)]
    #uniqcollectUrlAndFelt=uniqcollectUrlAndFelt.sort_index()
    uniqUrlFElt=""
    lessOf5Url_felt_index=[]

    for d in np.arange(len(uniqcollectUrlAndFelt)):# list of unikke url o felt
        if uniqcollectUrlAndFelt is not None:
            uniqUrlFElt=uniqcollectUrlAndFelt[d] 
        else:
            print("uniqcollectUrlAndFelt[d]:  "+uniqcollectUrlAndFelt[d])
        DataEvryFeild= (listOfurlAndfeildHandling[listOfurlAndfeildHandling['collectUrlAndFelt']==uniqUrlFElt])
        feldtName =str(findeHASHFeldName(int(uniqUrlFElt.split('-')[1]),listUniqeClearfield,HashListfeild))
       
        urlNumber=uniqUrlFElt.split('-')[0]        
        
        feldtName = format_filename(feldtName)
 
        #print(feldtName)
        t50=-1
        t90=-1

        if (len(DataEvryFeild.listOftime) > 5): # hvis der er mere end 5 hits så bliver der oprettes histogram af den
            t50=pd.to_numeric(DataEvryFeild.listOftime).quantile(q=.5)
            t90=pd.to_numeric(DataEvryFeild.listOftime).quantile(q=.9)

            plt.figure(figsize=(10,5))
            plt.hist(pd.to_numeric(DataEvryFeild['listOftime']),range=[0,60],bins=31) # list af tider i hver uniq
            try :
                #plt.title( feldtName.decode('utf8')+"\n"+" url - felt: "+ uniqUrlFElt +"\n" +
                plt.title( feldtName+"\n"+" url - felt: "+ uniqUrlFElt +"\n" +
                          ". fraktil 50-90 :  "+ str("{0:.3f}".format(t50))+" -"+str("{0:.3f}".format(t90)))
            except:
                #plt.title( feldtName.decode('latin1')+"\n"+" url - felt: "+ uniqUrlFElt +"\n" +
                plt.title( feldtName+"\n"+" url - felt: "+ uniqUrlFElt +"\n" +
                          ". fraktil 50-90 :  "+ str("{0:.3f}".format(t50))+" -"+str("{0:.3f}".format(t90)))

            plt.axvline(t50, color='red')
            plt.axvline(t90, color='yellow')
            plt.xlabel('Time (Min)')
            plt.ylabel('Amount ')
            plt.xticks(rotation=45)
            #oprattes hver histogram png med felt navn og tider og gemmes i nedstående sti 
            plt.savefig(path+csvName+'_'+feldtName+"_FeltNumber_"+str(uniqUrlFElt.split('-')[1])+"_UrlNumber_"+ str(urlNumber)+'.png')
            # det feltnavn som er valgt 

                                          
            
            t50_arr.append(t50)
            t90_arr.append(t90)
            #print('ff',d)

            #plt.show()
            plt.clf()
            plt.close()# Close a figure window
            Count.append(len(DataEvryFeild.listOftime))
        else:
            lessOf5Url_felt_index.append(d)
            #print('d',d)

    uniqcollectUrlAndFelt=uniqcollectUrlAndFelt.drop(lessOf5Url_felt_index)
    #print(uniqcollectUrlAndFelt.sort_index())
    if uniqcollectUrlAndFelt is not None:
        t_quatil=pd.DataFrame({"URl-Felt": uniqcollectUrlAndFelt, "t50":t50_arr, "t90":t90_arr, "Count":Count})
        t_quatil.to_csv("myapp/analysisfolder/Luk_Virksomhed/Quatiler/"+str('{}'.format(quatiler))+'.csv',sep=";", index=False)
    else:
        print('uniqcollectUrlAndFelt is empty')
    
            
    return uniqcollectUrlAndFelt,t_quatil

def histogram_For_EveryFelt_in_EveryURl_Save_Quatiler(listOfurlAndfeildHandling, collectUrlAndFelt,listUniqeClearfield,HashListfeild,path,quatiler,csvName):
    #lave histogram for hver de unikke urler and felt og tider som brugt per url og felt
    t50_arr=[]
    t90_arr=[]
    Count=[]
    #listOfurlAndfeildHandling=listOfurlAndfeildHandling.sort_values(by='collectUrlAndFelt', ascending=False)
    uniqcollectUrlAndFelt=listOfurlAndfeildHandling['{}'.format(collectUrlAndFelt)]
    #uniqcollectUrlAndFelt=uniqcollectUrlAndFelt.sort_index()
    uniqUrlFElt=""
    lessOf5Url_felt_index=[]
    if uniqcollectUrlAndFelt is not None:
        for d in np.arange(len(uniqcollectUrlAndFelt)):# list of unikke url o felt
            uniqUrlFElt=uniqcollectUrlAndFelt[d]

            DataEvryFeild= (listOfurlAndfeildHandling[listOfurlAndfeildHandling['collectUrlAndFelt']==uniqUrlFElt])
            urlNumber=uniqUrlFElt.split('-')[0]
            feldtName = format_filename(str(findeHASHFeldName(int(uniqUrlFElt.split('-')[1]),listUniqeClearfield,HashListfeild)))
            t50=-1
            t90=-1
            if (len(DataEvryFeild.listOftime) > 5): # hvis der er mere end 5 hits så bliver der oprettes histogram af den
                t50=pd.to_numeric(DataEvryFeild.listOftime).quantile(q=.5)
                t90=pd.to_numeric(DataEvryFeild.listOftime).quantile(q=.9)
                plt.figure(figsize=(10,5))
                plt.hist(pd.to_numeric(DataEvryFeild['listOftime']),range=[0,60],bins=31) # list af tider i hver uniq
                try :
                    plt.title( feldtName+"\n"+" url - felt: "+ uniqUrlFElt +"\n" +
                              ". fraktil 50-90 :  "+ str("{0:.3f}".format(t50))+" -"+str("{0:.3f}".format(t90)))
                except:
                    plt.title( feldtName+"\n"+" url - felt: "+ uniqUrlFElt +"\n" +
                              ". fraktil 50-90 :  "+ str("{0:.3f}".format(t50))+" -"+str("{0:.3f}".format(t90)))
                plt.axvline(t50, color='red')
                plt.axvline(t90, color='yellow')
                plt.xlabel('Time (Min)')
                plt.ylabel('Amount ')
                plt.xticks(rotation=45)
                #oprattes hver histogram png med felt navn og tider og gemmes i nedstående sti
                plt.savefig(path+csvName+'_'+feldtName+"_FeltNumber_"+str(uniqUrlFElt.split('-')[1])+"_UrlNumber_"+ str(urlNumber)+'.png')
                t50_arr.append(t50)
                t90_arr.append(t90)
                plt.clf()
                plt.close()# Close a figure window
                Count.append(len(DataEvryFeild.listOftime))
            else:
                lessOf5Url_felt_index.append(d)
        uniqcollectUrlAndFelt=uniqcollectUrlAndFelt.drop(lessOf5Url_felt_index)
        if uniqcollectUrlAndFelt is not None:
            t_quatil = pd.DataFrame({"URl-Felt": uniqcollectUrlAndFelt, "t50": t50_arr, "t90": t90_arr, "Count": Count})
            t_quatil.to_csv(
                "myapp/analysisfolder/Luk_Virksomhed/Quatiler/" + str('{}'.format(quatiler)) + '.csv',
                sep=";", index=False)
        else:
            print('uniqcollectUrlAndFelt after delete som of index is empty')
    else:
        print('uniqcollectUrlAndFelt is empty')

    return uniqcollectUrlAndFelt,t_quatil


def format_filename(s):
    import string
    """Take a string and return a valid filename constructed from the string.
Uses a whitelist approach: any characters not present in valid_chars are
removed. Also spaces are replaced with underscores.
 
Note: this method may produce invalid filenames such as ``, `.` or `..`
When I use this method I prepend a date string like '2009_01_15_19_46_32_'
and append a file extension like '.txt', so I avoid the potential of using
an invalid filename.
 
"""
    valid_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)
    filename = ''.join(c for c in s if c in valid_chars)
    filename = filename.replace(' ','_') # I don't like spaces in filenames.
    return filename

