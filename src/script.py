import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'auto_document_filing.settings')
django.setup()

from django.core.files.storage import FileSystemStorage
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent


print("Checking....is this script working ??")

from upload.views import upload
from upload.models import Book

books = Book.objects.all()
paths = []
fileNames = []
for book in books:
    #print(book.pdf)
    final_path = str(BASE_DIR)+ "/src/Documents/" + str(book.pdf)

    # delete that path from the database
    Book.objects.filter(pdf = book.pdf).delete()

    paths.append(final_path)
    #print(final_path)
    file_name = os.path.basename(final_path)
    #print(file_name)
    fileNames.append(file_name)


#for  (file_path , file_name) in zip(paths,fileNames):
#    print(file_path,file_name)

from pymongo import MongoClient


client = MongoClient('mongodb://localhost:27017/')
#print(client.server_info())

# print all the databases
for db in client.list_databases():
    print(db)
db = client['ADF_project']
#print(db)
collection = db['upload_studentform']
#print(collection)

import PyPDF2

def insert_doc(file_path,file_name,client,db_name,collection_name):
    db = client[db_name]
    my_collection = db[collection_name]
    
    pdffileobj=open(file_path,'rb')
    pdfreader=PyPDF2.PdfFileReader(pdffileobj)
    num_pages = pdfreader.numPages
    
    for i in range(num_pages):
        #print("***Page No.", i+1,"***");
        pageobj=pdfreader.getPage(i)
        text=pageobj.extractText()
        #print(text)
        mydict = { "file_name": file_name, "file_path": file_path , "content_text":text,"page_number":i+1}
        x = my_collection.insert_one(mydict)

# Inputs

#file_path = '/home/piyush/Downloads/Harvard_UChicago_JD.pdf'
#file_name = 'Harvard_UChicago_JD.pdf'
db_name = 'ADF_project'
collection_name = 'upload_studentform'

#my_database = client.ADF_project
#collection.createIndex({'file_name':1},{'unique':True})

for (file_path,file_name) in zip(paths,fileNames):
    insert_doc(file_path,file_name,client,db_name,collection_name)

  

#for doc in ((client[db_name])[collection_name]).find():
#    print(doc)

