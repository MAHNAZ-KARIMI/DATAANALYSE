import pandas as pd
from myapp.analysisfolder import M_URL_Felt as felt
from myapp.analysisfolder import M_Time as time
import os
import time
from collections import Counter
from datetime import timedelta
import matplotlib.pyplot as plt
import random
from myapp.analysisfolder import M_URL_Felt as felt
from myapp.analysisfolder import M_Time as time
from myapp.analysisfolder import M_PID_RID as PID_RID
import pandas as pd
import numpy as np


def makeDataAndCsv(Data,i):
    data_slut=[]
    csvname=""
    if i==0:
        csvname='gennem_RID__enscvr.csv'
        completedDuration= Data[Data['forloebVarighed'].notnull()]
        ridCompletedDuration=completedDuration[completedDuration['RID'].astype(str).str.isdigit()]#hvor i rid columns er tal
        try:
            
            data_slut= ridCompletedDuration.query('cvr==cvrIndberet')  
        except :
            print(i)
        return data_slut, csvname
     
    elif i==1:
        csvname='gennem_RID_ikke_enscvr.csv'
        completedDuration= Data[Data['forloebVarighed'].notnull()]
        ridCompletedDuration=completedDuration[completedDuration['RID'].astype(str).str.isdigit()]
        try:            
            data_slut= ridCompletedDuration.query('cvr!=cvrIndberet')
        except :    
            print(i)
        return data_slut, csvname
    
    elif i==2:
        csvname='gennem_RID_PID_enscvr.csv'
        try:
            completedDuration= Data[Data['forloebVarighed'].notnull()]
            pidCompletedDuration=completedDuration[completedDuration['RID'].astype(str).str.contains("-")]#hvor vi har personid med("_") i
            data_slut= pidCompletedDuration.query('cvr==cvrIndberet')
        except:
            print(i)
            
        return data_slut, csvname
        
    elif i==3:
        csvname='gennem_RID_PID_ikke_enscvr.csv'
        completedDuration= Data[Data['forloebVarighed'].notnull()]
        pidCompletedDuration=completedDuration[completedDuration['RID'].astype(str).str.contains("-")]
        try:
            data_slut= pidCompletedDuration.query('cvr!=cvrIndberet') 
        except:
            print(i)
        return data_slut, csvname
            
    elif i==4:
        csvname='gennem_PID_enscvr.csv'
        completedDuration= Data[Data['forloebVarighed'].notnull()]
        pidCompletedDuration=completedDuration[completedDuration['PID'].notnull()]
        try:
            data_slut= pidCompletedDuration.query('cvr==cvrIndberet')
        except:
            print(i)
        return data_slut, csvname
        
    elif i==5:
        csvname='gennem_PID_ikke_enscvr.csv'
        completedDuration= Data[Data['forloebVarighed'].notnull()]
        pidCompletedDuration=completedDuration[completedDuration['PID'].notnull()]
        try:
            data_slut= pidCompletedDuration.query('cvr!=cvrIndberet')
        except:
            print(i)
        return data_slut, csvname
        
    elif i==6:
        csvname='ikke_gennem_RID_enscvr.csv'
        notCompletedDuration= Data[Data['forloebVarighed'].isnull()]
        ridCompletedDuration=notCompletedDuration[notCompletedDuration['RID'].astype(str).str.isdigit()]#hvor i rid columns er tal  
        try:
            data_slut= ridCompletedDuration.query('cvr==cvrIndberet') 
        except:
            print(i)
        return data_slut, csvname
        
    elif i==7:
        csvname='ikke_gennem_RID_ikke_enscvr.csv'
        notCompletedDuration= Data[Data['forloebVarighed'].isnull()]
        ridCompletedDuration=notCompletedDuration[notCompletedDuration['RID'].astype(str).str.isdigit()]#hvor i rid columns er tal
        try:
            data_slut= ridCompletedDuration.query('cvr!=cvrIndberet')
        except:
            print(i)
        return data_slut, csvname
        
    elif i==8:
        csvname='ikke_gennem_RID_PID_enscvr.csv'
        notCompletedDuration= Data[Data['forloebVarighed'].isnull()]
        ridCompletedDuration=notCompletedDuration[notCompletedDuration['RID'].astype(str).str.contains("-")]#hvor i rid columns er tal
        try:
            data_slut= ridCompletedDuration.query('cvr==cvrIndberet')
        except:
            print(i)    
        return data_slut, csvname
    elif i==9:
        csvname='ikke_gennem_RID_PID_ikke_enscvr.csv'
        notCompletedDuration= Data[Data['forloebVarighed'].isnull()]
        ridCompletedDuration=notCompletedDuration[notCompletedDuration['RID'].astype(str).str.contains("-")]#hvor i rid columns er tal
        try:
            data_slut= ridCompletedDuration.query('cvr!=cvrIndberet')
        except:
            print(i)
        return data_slut, csvname
        
    elif i==10:
        csvname='ikke_gennem_PID_enscvr.csv'
        notCompletedDuration= Data[Data['forloebVarighed'].isnull()]
        pidCompletedDuration=notCompletedDuration[notCompletedDuration['PID'].notnull()]#hvor i rid columns er tal
        data_slut= pidCompletedDuration.query('cvr==cvrIndberet')
        return data_slut, csvname
        
    elif i==11:
        csvname='ikke_gennem_PID_ikke_enscvr.csv'
        notCompletedDuration= Data[Data['forloebVarighed'].isnull()]
        pidCompletedDuration=notCompletedDuration[notCompletedDuration['PID'].notnull()]#hvor i rid columns er tal
        try:
            data_slut= pidCompletedDuration.query('cvr!=cvrIndberet')
        except:
            print(i)
        return data_slut, csvname
        
    elif i==12:
        csvname='hele_Data_gennem.csv'
        data_slut= Data[Data['forloebVarighed'].notnull()]
        return data_slut, csvname
        
    elif i==13:
        csvname='hele_Data_ikke_gennem.csv'
        data_slut= Data[Data['forloebVarighed'].isnull()]
        return data_slut, csvname
    #-------- finde urlrejser hver uniq id i data_slut. den del er kopi fra AnalyseData

        
def make_Analyse_For_PId_RID(Data, tal, quatiler_PID_RID, Bruger):

    Data,listOfuniqUrl,HashlistOfUrl,listUniqeClearfield,HashListfeild,ListOfUniqUserIds=time.make_ready_new_columns(Data)


    for i in np.arange(tal):

        data_slut, csvname=makeDataAndCsv(Data,i)
        c = csvname.split('.')[0]
        data_slut = Data.replace(np.nan, 'NONE', regex=True)
        mainData =data_slut


        if (len(data_slut)!=0):
            uniqIdGruppeClearUrl = felt.findURLRejser(data_slut, "id", "clearURL", "newClearURL")
            UrlRejserAndCount = felt.makecounter(uniqIdGruppeClearUrl,"newClearURL")
            felt.saveToCsv_2(UrlRejserAndCount, 'ListOfUrlRejser', 'count',
                             "myapp/analysisfolder/Luk_Virksomhed/Sunburst/Gruppet_Bruger_PID_RID/Unique_URL_Rejser_Count/"+c+"_Url_Rejser.csv")

        data_slut=mainData
        if (len(data_slut) != 0):

            data_slut = felt.delete_Handlig_Bluer_And_Reset_Index(data_slut)
            listOfFeltRejse_URl = felt.findeFeildOrServerTime(data_slut, listOfuniqUrl, HashlistOfUrl, 'clearField')
            felt.make_Csv_For_FeldList_for_every_URL(listOfuniqUrl, listOfFeltRejse_URl,
                                                         'myapp/analysisfolder/Luk_Virksomhed/Sunburst/Gruppet_Bruger_PID_RID/Unique_Felt_Rejser_Count/' + c + '_')

        data_slut = mainData
        if (len(Data) != 0):

            listOfurlIdAndServerTimeStamp = felt.findeFeildOrServerTime(data_slut, listOfuniqUrl, HashlistOfUrl,'serverTimeStamp')
            listOfurlIdAndDiffrenceTimeStamp = time.calculateTime_URL(listOfurlIdAndServerTimeStamp,listOfurlIdAndServerTimeStamp['Urlid'])
            listOfUrlIdAllTimeStamp, listoflistSecoun = time.calculateTime_total_URL(listOfurlIdAndDiffrenceTimeStamp)

            time.make_Histogram_For_EveryURl(listoflistSecoun,Bruger,c)
            listOfurlAndfeildHandling, Url_Felt_Count = time.feldtTimeCalculate(data_slut, ListOfUniqUserIds, listOfuniqUrl,HashlistOfUrl, listUniqeClearfield,HashListfeild)

            time.saveToCsv_3(listOfurlAndfeildHandling,'collectUrlAndFelt','listIOfurlId',
                         'listOfFeldName', "myapp/analysisfolder/Luk_Virksomhed/UniqueList/PID_RID/"+c+"_Unique_Url_Felt.csv")

            felt.saveToCsv_2(Url_Felt_Count,'url-felt','count','myapp/analysisfolder/Luk_Virksomhed/Sunburst/Gruppet_Bruger_PID_RID/URL_Feild_Count/'+csvname)
            uniqcollectUrlAndFelt,t_quatil=time.histogram_For_EveryFelt_in_EveryURl_Save_Quatiler(listOfurlAndfeildHandling,
                                                            'collectUrlAndFelt',listUniqeClearfield,HashListfeild,'myapp/analysisfolder/Luk_Virksomhed/Histogram/Gruppet_Bruger_PID_RID/Felter_Tidsforbrug/',quatiler_PID_RID,c)
