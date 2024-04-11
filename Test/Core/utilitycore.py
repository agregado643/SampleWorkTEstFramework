import requests


def test_status_url():
     response = requests.get(" https://www.google.com/")
     assert response.status_code == 200

def getMyFiles(path):
     import os
     import pathlib
     thepath = path
     files = []
     # r=root, d=directories, f = files
     for r, d, f in os.walk(path):
          for file in f:
               if '.txt' in file:
                    newfile = thepath.replace('\\','\\\\') + "\\\\" + file
                    files.append(newfile)
              

     files.sort(key=os.path.getmtime,reverse=True)
     for f in files:
          print('printing files:')
          print(f)
     return    files

     