#importing the libraries needed 
import pandas as pd
import numpy as np
import requests
from bs4 import BeautifulSoup
from time import sleep
from random import randint

# bot detection bypass.
import random

user_agents_list = [
    'Mozilla/5.0 (iPad; CPU OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.83 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36'
]


#Declaring the headers if forcing english is required. 
#headers = {"Accept-Language": "en-US,en;q=0.5"}

#declaring the list of empty variables, So that we can append the data overall

TalkGroupsDec = []
TalkGroupsHex = []
ModeDEA=[]
AlphaTag=[]
Description =[]
Service = []

# creating an array of values and passing it in the url for dynamic webpages
# range from 1 to 1000 counting by 100

RadioZoneHttp = 'https://www.radioreference.com/db/sid/2560'
RadioFileName = 'BellZone2'

#the whole core of the script
try:
    print ("getting page ", RadioZoneHttp)
    page = requests.get( RadioZoneHttp, headers={'User-Agent': random.choice(user_agents_list)})
 
    page.raise_for_status()

    soup = BeautifulSoup(page.text, 'html.parser')
    #print (soup)
    # top of the area of interest where everything below is the movie
    manyServices = soup.findAll('table', class_='table table-responsive table-sm order-column table-striped table-bordered rrdbTable datatable-lite')

    #print ("manyServices", manyServices)
    # don't flood the server, may also trip bot detection. Sleep b/n 2 or 8 secods to avoid detection
    #sleep(randint(2,8))

    for service in manyServices:
        tableStart = service.tbody
        #print (tableStart)

        # tr contains many td's (that contain our TGs), this list is formed from the tag that contains all the subtags

        manyTGs = tableStart.findAll('tr', class_=None) #tr.findAll('td', class_="noWrapTd")
        #print (manyTGs)

        for oneTG in manyTGs:
            print ("------------------------")
            print (oneTG)
            decTG = oneTG.td.text
            print ("decTG = ", decTG)
            TalkGroupsDec.append(decTG)

            next = oneTG.td.find_next_sibling('td')
            hexTG = next.text
            print ("hexTG = ", hexTG)
            TalkGroupsHex.append(hexTG)

            next = next.find_next_sibling('td')
            #print(next)
            type = next.text
            print ("type  = ", type)
            ModeDEA.append(type)
            
            next = next.find_next_sibling('td')
            #print(next)
            alphaTag = next.text
            print ("short name  = ", alphaTag)
            AlphaTag.append(alphaTag)

            next = next.find_next_sibling('td')
            #print(next)
            desc = next.text
            print ("description = ", desc)
            Description.append(desc)

            next = next.find_next_sibling('td')
            #print(next)
            svc = next.text
            print ("service = ", svc)
            Service.append(svc)
            

        ''' 
        TalkGroupsDec.append(name)
        
        tgDec = service.h3.find('span', class_ = "lister-item-year text-muted unbold").text
        TalkGroupsHex.append(tgDec)
        
        modeDEA = service.p.find("span", class_ = 'runtime').text
        ModeDEA.append(modeDEA)
        
        # this text did not have a class, the word inline-block is used.
        alphaTag = service.find('div', class_ = "inline-block ratings-imdb-rating").text.replace('\n', '')
        AlphaTag.append(alphaTag)
        
        # not all metascores had a value. test with if condition is in the middle (that's weird)
        # if it exists, do assignment on left but if not take value after the else (jesus this language is fucked)
        description = service.find('span', class_ = "metascore").text if service.find('span', class_ = "metascore") else "****"
        Description.append(description)
        
        # not all metascores had a value. test with if condition is in the middle (that's weird)
        # if it exists, do assignment on left but if not take value after the else (jesus this language is fucked)
        service = service.find('span', class_ = "metascore").text if service.find('span', class_ = "metascore") else "****"
        Service.append(service)
        '''


        '''
        # generic snippets of handling other 
        # there is an area we want that has no class name but has a 'name' called 'nv'.
        # but the term 'nv' is used twice in the same tag scope. We can only pick up both 'nv' definitions
        # and then use an array to pick one of N nv items.

        value = store.find_all('span', attrs = {'name': "nv"})
        
        vote = value[0].text
        votes.append(vote)
        
        grosses = value[1].text if len(value)>1 else '%^%^%^'
        gross.append(grosses)
        
        # Description of the Movies -- Not explained in the Video, But you will figure it out. 
        describe = store.find_all('p', class_ = 'text-muted')
        description_ = describe[1].text.replace('\n', '') if len(describe) >1 else '*****'
        AlphaTag.append(description_)
        '''
        
except Exception as e:
    print (e)



#creating a dataframe 
zone2List = pd.DataFrame({ "TG(dec)": TalkGroupsDec, "TG(hex)" : TalkGroupsHex, "Type": ModeDEA,"Alpha-Tag": AlphaTag, "Decscription": Description, "Service" : Service  })

zone2List.head(5)

print (zone2List)   # this makes it pop up to display first and last 5 lines.


# #saving the data in excel format
zone2List.to_excel(RadioFileName + str(".xlsx"))

# #If you want to save the data in csv format
zone2List.to_csv(RadioFileName + str(".csv"))

# %%

