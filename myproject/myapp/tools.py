# tools.py #Add
from zipfile import ZipFile 
import os 
from django.core.files import File as DjangoFile
from .models import FileData


def delete_this_dir(mydir):
    filelist = [f for f in os.listdir(mydir) if '.' in f[-5:]]
    for f in filelist:
        os.remove(os.path.join(mydir, f))


def delete_all_files():
    main_dir = 'myapp/analysisfolder/Luk_Virksomhed/'
    #FileData.objects.all().delete()
    delete_this_dir(main_dir + 'Histogram/Alle_Bruger/URL_Tidsforbrug/')
    delete_this_dir(main_dir + 'Histogram/Alle_Bruger/Felter_Tidsforbrug/')
    delete_this_dir(main_dir + 'Histogram/Gruppet_Bruger_PID_RID/Felter_Tidsforbrug/')
    delete_this_dir(main_dir + 'Histogram/Gruppet_Bruger_PID_RID/URL_Tidsforbrug')
    delete_this_dir(main_dir + 'Quatiler')
    delete_this_dir(main_dir + 'Sunburst/Alle_Bruger/Unique_Felt_Rejser_And_Count_Every_URL/')
    delete_this_dir(main_dir + 'Sunburst/Alle_Bruger/')
    delete_this_dir(main_dir + 'Sunburst/Gruppet_Bruger_PID_RID/Unique_Felt_Rejser_Count/')
    delete_this_dir(main_dir + 'Sunburst/Gruppet_Bruger_PID_RID/URL_Feild_Count/')
    delete_this_dir(main_dir + 'Sunburst/Gruppet_Bruger_PID_RID/Unique_URL_Rejser_Count/')
    delete_this_dir(main_dir + 'UniqueList')
def get_all_file_paths(directory):
  
    # initializing empty file paths list 
    file_paths = [] 
  
    # crawling through directory and subdirectories 
    for root, directories, files in os.walk(directory):
        #print("root",root)
        #print("directories",directories)
        #print("files",files)
        for filename in files:
            # join the two strings in order to form the full filepath. 
            filepath = os.path.join(root, filename) 
            file_paths.append(filepath) 
  
    # returning all file paths 
    return file_paths         
  
def tozip(directory,path):
	os.chdir(path)
    # path to folder which needs to be zipped
	directory = '.'
    # calling function to get all file paths in the directory 
	file_paths = get_all_file_paths(directory)
	#print("\n\n*\n\n****\n", file_paths)
    # printing the list of all files to be zipped 
	#print('Following files will be zipped:')
	for file_name in file_paths:
		print(file_name)
    # writing files to a zipfile 
	with ZipFile('../../analysisfolder/Luk_Virksomhed/Luk_Virksomhed.zip','w') as zip:
        # writing each file one by one 
		for file in file_paths:
			zip.write(file)
	print('All files zipped successfully!') 
	file_obj1 = DjangoFile(open('../../analysisfolder/Luk_Virksomhed/Luk_Virksomhed.zip', mode='rb'), name='Luk_Virksomhed.zip')
	os.chdir("../../..")

	return file_obj1
# if __name__ == "__main__": 
#     main() 