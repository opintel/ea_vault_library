
from PyPDF2 import PdfFileReader,PdfFileWriter 

from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5

import zipfile
import csv
import base64

import logging
import os
logging.basicConfig(level=logging.DEBUG)

from dotenv import load_dotenv
load_dotenv(os.getcwd()+"/.env")

class Ea_Vault_Library :
    
    def __init__(self,parameters={'path':'','key':'','key_private_path':'','doc_name':'','doc_type':''}):

        self.path = parameters['path'] +parameters['doc_type']+"/"
        self.key = parameters['key']
        self.key_private_path = parameters['key_private_path']
        self.doc_name = parameters['doc_name']
        self.doc_type = parameters['doc_type']




    def setKey(self, key):

        self.key = str(key)

    def setDocName(self, doc_name):

        self.doc_name = str(doc_name)

    def setDocType(self, doc_type):

        self.doc_type = str(doc_type)

    def setInputPathFile(self, input_path_file):

        self.input_path_file = str(input_path_file)

    def setOutputPathFile(self, output_path_file):

        self.output_path_file = str(output_path_file)

    def setCadenaEncodeHash(self, cadena_encode):

        self.cadena_encode = str(cadena_encode)



    def getKey(self):

        return(self.key)

    def getDocName(self):

        return (self.doc_name)

    def getDocType(self):

        return (self.doc_type)

    def getInputPathFile(self):

        return (self.input_path_file)

    def getOutputPathFile(self, input_path_file):

        return (self.output_path_file)

    def getCadenaEncodeHash(self, cadena_encode):

        return (self.cadena_encode)

    def getAtribsFile(self):
        return ("'"+
                self.doc_name+"','"+
                self.doc_type+"','"+
                self.output_path_file.replace("_encrypt.pdf",".zip")+"','"+
                self.cadena_hash+"'")




    def createEncryptFilePdf(self):

        if not os.path.exists(self.path):
            os.makedirs(self.path)
        
        self.input_path_file= self.path+ self.doc_name+".pdf"
        self.output_path_file = self.path+self.doc_name+"_encrypt.pdf"
        
        pdf_reader = PdfFileReader(str(self.input_path_file))
        pdf_writer = PdfFileWriter()
        pdf_writer.appendPagesFromReader(pdf_reader)
        pdf_writer.encrypt(user_pwd=self.key,owner_pwd=self.key)
        
        
        with open(self.output_path_file,'wb') as output_file:
            pdf_writer.write(output_file)
            
        logging.debug("Method: saveEncryptFilePdf finished")

    def createZipFile(self):
        
        with zipfile.ZipFile(self.path+self.doc_name+".zip","w") as archivo_zip:
            archivo_zip.write(self.output_path_file,self.doc_name+"_encrypt.pdf")
            os.remove(self.input_path_file)
            os.remove(self.output_path_file)
        
        archivo_zip.close()
        logging.debug("Method: createZipFile finished")

    def unzipZipFile(self):
        
        with zipfile.ZipFile(self.output_path_file,"r") as archivo_zip:
            archivo_zip.extractall(self.output_path_file.replace(self.doc_name+".zip",""))
            os.rename(self.output_path_file.replace(".zip","_encrypt.pdf"),self.output_path_file.replace(".zip",".pdf"))
            pdf_reader = PdfFileReader(self.output_path_file.replace(".zip",".pdf"))
            pdf_reader.decrypt(password=self.key)

            pdf_writer = PdfFileWriter()
            pdf_writer.appendPagesFromReader(pdf_reader)

            with open(self.output_path_file.replace(".zip",".pdf"), 'wb') as output_file:
                pdf_writer.write(output_file)

        logging.debug("Method: unzipZipFile finished")
        

    def createFileHash(self):
        
        #===================================Hashing======================================================
        file = open(self.input_path_file, 'rb')
        encoded_string = base64.b64encode(file.read())
        
        with open(self.key_private_path, 'r') as f:
            key = RSA.importKey(f.read())
            
        hasher = SHA256.new(encoded_string)
        signer = PKCS1_v1_5.new(key)
        signature = signer.sign(hasher)
        cadena_encode=base64.b64encode(signature)

        #===================================Se guarda en base de datos===================================
        self.cadena_hash=str(cadena_encode).replace("b'","").replace("'","")
        #===================================Se guarda en base de datos===================================
    
        #===================================Hashing======================================================
        logging.debug("Method: createFileHash finished")

           

                
            
