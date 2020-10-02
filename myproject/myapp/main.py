# Main.ipynb changes to .py file

# sys.path.insert(1, 'analysisfolder')
# import os
# file_list=os.listdir()
# print (file_list)
import os
import pandas as pd
from myapp.analysisfolder import M_URL_Felt as felt
from myapp.analysisfolder import M_Time as time
from myapp.analysisfolder import M_PID_RID as PID_RID
from .tools import delete_all_files
# import ConnectionToMysql as connection
import sys


def get_data(myinput, mode):
	if mode == "mysql":
		from .analysisfolder import ConnectionToMysql as connection
		rootconn = connection.dockerConnection()
		Data = pd.DataFrame(connection.sqlQuery("SELECT * FROM Luk_Virksomhed", rootconn))
		Data = Data.rename(
			columns={0: 'id', 1: 'forloebVarighed', 2: 'virkStartForloebsId', 3: 'cvr', 4: 'cvrIndberet', 5: 'RID',
					 6: 'PID', 7: 'serverTimeStamp', 8: 'formURL', 9: 'feltType', 10: 'feltId', 11: 'feltNavn',
					 12: 'handling'})
	else:
		Data = pd.read_csv(myinput["csvSelected"], sep=';', dtype='str')
	return Data


def do_algoritm(myinput, mode):
	# rootconn = connection.dockerConnection()
	# Data= pd.DataFrame(connection.sqlQuery("SELECT * FROM Luk_Virksomhed",rootconn)) #TODO
	delete_all_files()
	main_Data= get_data(myinput, mode)
	Data = main_Data.copy()

	#print('-----------\\\\\\\n\n\n\n\n\n---\n\n\n', type(Data), Data.keys())
	#print('+++\\\\\\\n\n\n\n\n\n---\n\n\n', type(main_Data), main_Data.keys())

	Data,listOfuniqUrl,HashlistOfUrl,listUniqeClearfield,HashListfeild,ListOfUniqUserIds = time.make_ready_new_columns(Data)
	#print(Data)
	uniqIdGruppeClearUrl = felt.findURLRejser(Data,"id","clearURL", "newClearURL")

	uniqIdGruppeClearUrl = felt.enterNumbersInsteadOfName(uniqIdGruppeClearUrl,HashlistOfUrl,listOfuniqUrl)

	UrlRejserAndCount = felt.makecounter(uniqIdGruppeClearUrl,"newClearURL")

	felt.saveToCsv_2(UrlRejserAndCount,'ListOfUrlRejser','count',"myapp/analysisfolder/Luk_Virksomhed/Sunburst/Alle_Bruger/Unique_UrlRejser_&_Count.csv")

	felt.saveToCsv_2(listOfuniqUrl,'urlName','urlNumber',"myapp/analysisfolder/Luk_Virksomhed/UniqueList/UniqueUrl.csv")

	felt.saveToCsv_2(listUniqeClearfield,'FeildName','numberOfField',"myapp/analysisfolder/Luk_Virksomhed/UniqueList/UniqueFeildList.csv")

# ----------------------------------------------
	Data = main_Data.copy()

	Data= felt.delete_Handlig_Bluer_And_Reset_Index(Data)

	Data, listOfuniqUrl ,HashlistOfUrl ,listUniqeClearfield, HashListfeild, ListOfUniqUserIds = time.make_ready_new_columns(Data)

	listOfUrlIdAndFeltRejse = felt.findeFeildOrServerTime(Data,listOfuniqUrl,HashlistOfUrl,'clearField')

	#listOfUrlIdAndFeltRejse = felt.enters_Numbers_Instead_Of_Felt_Name(listOfUrlIdAndFeltRejse,HashListfeild)

	felt.make_Csv_For_FeldList_for_every_URL(listOfuniqUrl,listOfUrlIdAndFeltRejse,'myapp/analysisfolder/Luk_Virksomhed/Sunburst/Alle_Bruger/Unique_Felt_Rejser_And_Count_Every_URL/')
# ----------------------------------------------
	Data = main_Data.copy()

	Data,listOfuniqUrl,HashlistOfUrl,listUniqeClearfield,HashListfeild,ListOfUniqUserIds = time.make_ready_new_columns(Data)

	listOfurlIdAndServerTimeStamp=felt.findeFeildOrServerTime(Data, listOfuniqUrl, HashlistOfUrl, 'serverTimeStamp')

	listOfurlIdAndDiffrenceTimeStamp=time.calculateTime_URL(listOfurlIdAndServerTimeStamp,listOfurlIdAndServerTimeStamp['Urlid'])


	listOfUrlIdAllTimeStamp,listoflistSecoun=time.calculateTime_total_URL(listOfurlIdAndDiffrenceTimeStamp)

	time.make_Histogram_For_EveryURl(listoflistSecoun,'Alle_Bruger',"")

	listOfurlAndfeildHandling,Url_Felt_Count=time.feldtTimeCalculate( Data,ListOfUniqUserIds,listOfuniqUrl,HashlistOfUrl,listUniqeClearfield,HashListfeild)

	uniqcollectUrlAndFelt,t_quatil=time.histogram_For_EveryFelt_in_EveryURl_Save_Quatiler(listOfurlAndfeildHandling,
	'collectUrlAndFelt', listUniqeClearfield, HashListfeild,'myapp/analysisfolder/Luk_Virksomhed/Histogram/Alle_Bruger/Felter_Tidsforbrug/','quatiler',"")
#----------------------------------------------
	Data = main_Data.copy()

	PID_RID.make_Analyse_For_PId_RID(Data, 14, 'quatiler_PID_RID', 'Gruppet_Bruger_PID_RID')




#Data = pd.read_csv(myinput["csvSelected"], sep=';', dtype='str')
	#PID_RID.make_Analyse_For_PId_RID(Data, 14, 'quatiler_PID_RID', 'Gruppet_Bruger_PID_RID')
# time.saveToCsv_3(listOfurlAndfeildHandling, 'collectUrlAndFelt', 'listIOfurlId', 'listOfFeldName',("myapp/analysisfolder/Luk_Virksomhed/UniqueList/Unique_Url_Felt.csv")
# felt.saveToCsv_2(Url_Felt_Count, 'url-felt', 'count', "myapp/analysisfolder/Luk_Virksomhed/UniqueList/URL_Felt_Count.csv")
#Data=Data.rename(columns={0: 'id',1: 'forloebVarighed',2: 'virkStartForloebsId' ,3: 'cvr', 4:'cvrIndberet',5:'RID', 6:'PID',7:'serverTimeStamp',8:'formURL',9:'feltType',10:'feltId',11:'feltNavn',12:'handling'})

#
