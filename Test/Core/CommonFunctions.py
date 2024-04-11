
import datetime
import os

from robot.libraries.BuiltIn import BuiltIn
from robot.api import logger
from io import StringIO
import hashlib

class CommonFunctions():
    @staticmethod
    def decode_utf8(strvalue):
        '''Decode any string using utf8. 
        This is required when we use a text which is not in English language'''
        return strvalue.decode('utf8')
    
    @staticmethod
    def encode_utf8(strvalue):
        '''Decode any string using utf8. 
        This is required when we use a text which is not in English language'''
        return strvalue.encode('utf-8')
    
    @staticmethod
    def convert_upper(stringval):
        return stringval.upper()
    
    @staticmethod
    def convert_lower(stringval):
        return stringval.lower()    


    @staticmethod
    def getmd5hash(file, block_size=2**20):
        md5 = hashlib.md5()
        while True:
            data = file.read(block_size)
            if not data:
                break
            md5.update(data.encode('utf8'))
        logger.info("for %s: %s"%(file, md5.hexdigest()))
        return md5.hexdigest()


    @staticmethod
    def compareFileMD5(file1, file2):
        #if (CommonFunctions.getmd5hash(open(file1, 'r')) == CommonFunctions.getmd5hash(open(file2, 'r'))):
           # logger.info("Files Matched!") 
        assert (CommonFunctions.getmd5hash(open(file1, 'r')) == CommonFunctions.getmd5hash(open(file2, 'r')))==True
        if not(CommonFunctions.getmd5hash(open(file1, 'r')) == CommonFunctions.getmd5hash(open(file2, 'r'))):
            logger.info("Files Not Matched! - file 1 has %s and file 2 has %s"%(CommonFunctions.getmd5hash(open(file1, 'r')),CommonFunctions.getmd5hash(open(file2, 'r'))))


    @staticmethod
    def compareContents(f1,f2):
        import filecmp
        #if filecmp.cmp(filename1, filename2, shallow=False):
        assert (filecmp.cmp(f1, f2, shallow=False))==True


    @staticmethod
    def compFile(f1, f2):
        import filecmp
        assert(filecmp.cmp(f1, f2, shallow=False))==True


    @staticmethod
    def readlineignorespaces(f1):
        lines = []
        with open(f1) as f:
            for line in f:
                line = line.strip()
                if line:
                    lines.append(line)
        logger.info(lines[1:])

    @staticmethod
    def loadJson(f1):
        import json
        with open(f1) as f:
            data = json.load(f)
        return  data
    
    @staticmethod
    def removeignoredfields(datajson):
        import json
        json_dict = json.loads(datajson)
        
        try:

            print(json_dict)
            print('now doing the removal')
            with open('C:\\tests\\Core\\ignorelist.txt') as f2:
                for item2 in f2:
                    item2 = item2.rstrip()
                    print('\n***************\nchecking ', item2, ' if its in the data json\n*********\n')
                    if item2 in json_dict:
                        print('found',item2, ' at json')
                        json_dict.pop(item2,None)
                        print('after deletion: ', json_dict, '\n*****\n' )
                        
            print('this is the modified:\n')
            print(json_dict)
            print('\n')
            return json.dumps(json_dict)

        except Exception as e:
            print('error is: ' ,e)
            return false

        



    @staticmethod
    def sortandCompare(f1, f2):
        import json, xmltodict
        from pathlib import Path
        json1 = ''
        json2 = ''
        try:
            with open(f1) as _f1:
                ext = os.path.splitext(f1)[-1].lower()
                print('file extension:', ext)
                if ext == ".json":
                    print("its json")
                    json1 = CommonFunctions.loadJson(f1)
                    json1 = CommonFunctions.removeignoredfields(json.dumps(json1, sort_keys=True))
                    json2 = CommonFunctions.loadJson(f2)
                    json2 = CommonFunctions.removeignoredfields(json.dumps(json2, sort_keys=True))

                elif ext == ".xml":
                    print("its xml")
                    json1 = CommonFunctions.xmltojson(f1)
                    json1 = CommonFunctions.removeignoredfields(json.dumps(json1, sort_keys=True))
                    json2 = CommonFunctions.xmltojson(f2)
                    json2 = CommonFunctions.removeignoredfields(json.dumps(json2, sort_keys=True))
           
            print('\n---after removal from ignored list--\n')
            print(json1)
            print(json2)
            assert(CommonFunctions.compareList(json1,json2))==False
        
        except Exception as e:
            print('error is: ', e)
            assert(CommonFunctions.compareList(json1,json2))==False
            
    @staticmethod
    def xmltojson(f1):
        import json
        import xmltodict
        with open(f1) as f:
            data = json.loads(json.dumps((xmltodict.parse(f))))
        return data

    @staticmethod
    def readLinesIgnoreWs(f1):
        with open(f1, 'r') as file:
            data = file.read().replace('\n', '')
        return data.replace(' ','')

    @staticmethod
    def compareList(l1, l2):
        import dictdiffer , json
        hasdifference = False      
        a_dict =   json.loads(l1)
        b_dict = json.loads(l2)
        for diff in list(dictdiffer.diff(a_dict, b_dict)):
            if diff:
                hasdifference = True
                print (diff)
        return hasdifference

    @staticmethod
    def compareByLines(f1, f2):
        import difflib, sys, json
        hasdifferent=False
        diff = difflib.ndiff(json.dumps(f1),json.dumps(f2))    
        if diff:
            print('has difference')
            hasdifferent = True
        for i,line in enumerate(diff):
            if line.startswith(' '):
                continue
            print('*: {}, text: {}'.format(i,line))  
        return hasdifferent


    @staticmethod
    def percentagediff(f1, f2):
        from difflib import SequenceMatcher
        text1 = open(f1).read()
        text2 = open(f2).read()
        m = SequenceMatcher(None, text1, text2)
        print(m.ratio())

    @staticmethod
    def checkdiff(f1, f2):
        import difflib
        with open(f1) as file_1:
            file_1_text = file_1.readlines()
 
        with open(f2) as file_2:
            file_2_text = file_2.readlines()

        # get percentage
        from difflib import SequenceMatcher
        text1 = open(f1).read()
        text2 = open(f2).read()
        m = SequenceMatcher(None, text1, text2)
        print("percentage got" + m.ratio())
 
        # Find and print the diff:
        for line in difflib.unified_diff(
                file_1_text, file_2_text, fromfile='file1.txt',
                tofile='file2.txt', lineterm=''):
            print(line)
        