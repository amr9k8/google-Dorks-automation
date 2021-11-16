from logging import exception
from os import symlink, times
import re
import time
from googleapiclient.discovery import build

def banner1():
    print("""
    
  ____                   _        ____             _        
 / ___| ___   ___   __ _| | ___  |  _ \  ___  _ __| | _____ 
| |  _ / _ \ / _ \ / _` | |/ _ \ | | | |/ _ \| '__| |/ / __|
| |_| | (_) | (_) | (_| | |  __/ | |_| | (_) | |  |   <\__ |
 \____|\___/ \___/ \__, |_|\___| |____/ \___/|_|  |_|\_\___/
                   |___/
    _         _                        _   _               _____           _
   / \  _   _| |_ ___  _ __ ___   __ _| |_(_) ___  _ __   |_   _|__   ___ | |
  / _ \| | | | __/ _ \| '_ ` _ \ / _` | __| |/ _ \| '_ \    | |/ _ \ / _ \| |
 / ___ \ |_| | || (_) | | | | | | (_| | |_| | (_) | | | |   | | (_) | (_) | |
/_/   \_\__,_|\__\___/|_| |_| |_|\__,_|\__|_|\___/|_| |_|   |_|\___/ \___/|_|


# A Simple Tool To Automate  Google Dorks and Fetch All Results Inside TXT File
# Coded By Amr-Khaled - @Amr9k8

    """)

# How it Works 
# 1) use api with one key and one query to get 100 search result in 10 requests ,
# to get all items : . ceil(total result // 10 ) = number of request


# Each key can make 100 search queries per day as max quota 
#This JSON API fetch only 100 result per query 
# max 10 result per page , so 'start' will be 1, 11, 21 , 31 ,41 ,51 ,61 .. 91  

def google_search(search_term, api_key, cse_id, **kwargs):
      
        service = build("customsearch", "v1", developerKey=api_key)
        try:
              res = service.cse().list(q=search_term, cx=cse_id, **kwargs).execute()
              return res
        except Exception as e:
              return e

def getResult(res):
        Errors = str(res)
        if Errors.startswith("<HttpError 429"):
             print("\n\n This Key not Working \n\n")
             return 0
        elif Errors.startswith("<HttpError 400"):
            print("\n\nsearch results of current query exceeded 100\n\n")
            return 0 
        else:
            #may be errors is here: keys change with every request so we can't index them , lets make solution to return whole response without any indexing
            # no res['items'] then may be no results!
            try:
                #return [res['queries']['request'][0]['totalResults'],res['items'] ]
                return res['items']
            except Exception as e:
                print("\nNo  Items Found :\n")
                return 0


def get_total_requests(query,api_key,my_cse_id):
#to get calculate requests needed to fetch all items : "approximate_to_next_int(total result / 10 ) = number of requests"

    raw_result = google_search(query,api_key,my_cse_id,num=10,start=1)
    final_result = getResult(raw_result)

    if final_result != 0: # check if no errors found
        totalitems = int(final_result[0])
        if totalitems < 100:
            x = totalitems/10
            if(x-int(x)== 0): # 30/10 => 3 request
                return x
            else:
                return int(x+1) # 31/10 =>3.1 request = 4 request
        else:
            return 10 # like 130 or more will limited to 100 items only so need 10 requests
    elif final_result == 0:
        return 0
def test_api_key(query,api_key,my_cse_id):
    raw_result = google_search(query,api_key,my_cse_id,num=10,start=1)
    final_result = getResult(raw_result)
    return final_result
    



apiFile = "D:\\Users\\Amr\\Desktop\\github\\Automate Google Search\\GCSE Keys pool.txt"
dorksrc = "D:\\Users\\Amr\\Desktop\\github\\Automate Google Search\\dork_List.txt"
resultsPath = "D:\\Users\\Amr\\Desktop\\github\\Automate Google Search\\results.txt"
API_Bank = []
Dorks_Bank = []
key_counter = 0
query_counter = 1 
my_cse_id = "df2f99b92c861cec1"

banner1()

with(open(apiFile,'r')) as KeyList:
      for oneKey in KeyList:
            oneKey = oneKey.strip()
            API_Bank.append(oneKey)

with(open(dorksrc,'r',encoding='utf-8')) as dorksList:
      for onedork in dorksList:
            onedork = onedork.strip()
            Dorks_Bank.append(onedork)

print("[+] Scanning Started \n")
test_key = test_api_key("test",API_Bank[key_counter],my_cse_id)
while(test_key == 0):
    print("[+] Skipping Used Api Keys , Current Key["+str(key_counter)+ "] , Please Wait ...",end='\r')
    key_counter+=1
    test_key = test_api_key("test",API_Bank[key_counter],my_cse_id)





while key_counter < len(API_Bank)+1:#run till all keys are consumed 
    print("Working on API-Key ["+str(key_counter)+"] : "+API_Bank[key_counter])
    if len(Dorks_Bank) == 0:
        print("Finshed Queries" )
        break
    for j in range(1,len(Dorks_Bank)+1,1):
        test_key = test_api_key("test",API_Bank[key_counter],my_cse_id)
        if test_key != 0:
            query = Dorks_Bank.pop()
            query_counter += 1 
            total_requests = 100
            print("Working on Query Num#["+str(query_counter)+ "]: "+query)
            page_number =1
            for i in range (1,total_requests+1,1):#number of requests to send
                raw_result = google_search(query,API_Bank[key_counter],my_cse_id,num=10,start=page_number)
                final_result = getResult(raw_result)
                if(final_result == 0):
                    break
                text="\n\n\n###################################################################################################################################################################\n\n"\
                      +"\n"+str(final_result)+"\n\n\n"
                with(open(resultsPath,'a',encoding='utf-8')) as txtFile:
                        txtFile.write(text)
                page_number+=10
        else:
            print("Quota Time Limit Exceeded for Current Key,Switching to Next Key ...")
            time.sleep(2)
            key_counter+=1
            break

print("\n\nData Saved Successfully\n\n")

