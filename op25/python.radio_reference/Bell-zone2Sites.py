#importing the libraries needed 
import os  # for cls()
import pandas as pd
import numpy as np
import requests
import pickle
import pprint  
import traceback
import json
import sys
from contextlib import redirect_stdout

from bs4 import BeautifulSoup
from time import sleep
from random import randint

# use pickle instead of json, pickle supports data types like dicts and tuples
#from json import loads, dumps
from pickle import loads, dumps

# bot detection bypass.
import random

# clear console screen
os.system('clear')

#-------------------------------------------------------------------------

op25GoldenDefaultObj = {
    "channels": [
        {
            "name": "control channel", 
            "trunking_sysname": "Example",
            "device": "rtl0",
            "raw_output": "",
            "demod_type": "fsk", 
            "destination": "smartnet", 
            "excess_bw": 0.35, 
            "filter_type": "fsk2", 
            "if_rate": 18000, 
            "enable_analog": "off",
            "symbol_rate": 3600
        }
    ], 
    "devices": [
        {
            "args": "airspy=0", 
            "frequency": 987654321, 
            "gains": "LNA:39", 
            "name": "rtl0", 
            "offset": 0, 
            "ppm": 0.0, 
            "rate": 3000000, 
            "tunable": True
        }
    ],
    "trunking": {
        "module": "tk_smartnet.py",
        "chans": [
            {
                "sysname": "Example",
                "control_channel_list": "987.654321",
                "tgid_tags_file": "",
                "tgid_hold_time": 2.0,
                "blacklist": "",
                "whitelist": "",
                "bandplan_comment": "https://www.radioreference.com/apps/db/?sid=2560",
                "bandplan": "400",
                "bp_comment": "The bp_ parameters are only used by the 400 bandplan",
                "bp_spacing": 0.015,
                "bp_base": 141.015,
                "bp_base_offset": 380,
                "bp_mid": 151.730,
                "bp_mid_offset": 579,
                "bp_high": 154.320,
                "bp_high_offset": 632
            }
        ]
    },
    "audio": {
        "module": "sockaudio.py",
        "instances": [
            {
                "instance_name": "audio0",
                "device_name": "default",
                "udp_port": 23456,
                "audio_gain": 1.0,
                "number_channels": 1
            }
        ]
    },
    "terminal": {
        "module": "terminal.py",
        "terminal_type": "curses",
        "#terminal_type": "http:127.0.0.1:8080",
        "curses_plot_interval": 0.2,
        "http_plot_interval": 1.0,
        "http_plot_directory": "../www/images",
        "tuning_step_large": 1200,
        "tuning_step_small": 100
    }
}

#-------------------------------------------------------------------------
def setupDefaultJason():
    # op25 files are in an obj format? 
    # python works wants a json file in dictionary format.
    # calling above default.json will fault as json.load wants strings not DICTS

    # 1) take op25 dict and convert into json string.
    # 2) convert json string from 1) to jason.dict
    # 3) use json.dict format from 2) for manipulating data
    # notice slight diff b/n op25 dict and the local dict

    op25JsonString = dumps(op25GoldenDefaultObj)  #takes a json dict and makes a string
    #print ("result of converting op25 json obj into json string\n\n", op25JsonString, "\n")

    # an op25 obj is not compatible with a python3 obj. So we had to convert
    # from oj25 obj to string, string to python obj to allow python to manipulate dict members of obj
    global workingJsonObj
    
    workingJsonObj = loads(op25JsonString)
    #print ("result of converting op25 string (python object of type = ", type(tempJsonObj)," )\n")
    #print ("tempJsonObj *** ", tempJsonObj, "\n\n")


#-------------------------------------------------------------------------
def getValueOfKeyInList(list_of_keys, keyName):
    try:
        res = [d.get(keyName, None) for d in list_of_keys]  # res is a list []
        print ("\nkey ", keyName, " = " + str(res))
        return res
    
    except StopIteration:
        raise ValueError("No matching record for ", keyName," found")

def setValueOfKeyInList(dictName, list_of_keys, keyName, value):
    try:
         for d in list_of_keys:
            res = d.get(keyName, None)  # does d have our keys name?
            old = d.get(keyName, None)
            if ( res != None):
                d[keyName] = value
                print( dictName,"->", keyName, " was =", old, "now =", d.get(keyName, None))

    except StopIteration:
        raise ValueError("No dictionary record for ", keyName, " was found")

def setDictInListOfDict(dictName1, listName, subDictName, value):
    try:
        # the root DICTionary contains a LIST that contains DICTionaries
        topDictionary = workingJsonObj[dictName1]
        hasAlist = topDictionary[listName]

        #print ("\n", type(topDictionary),"topDictionary = ", topDictionary, "\n")
        #print ("\n", type(hasAlist),"hasAlist = ", hasAlist, "\n")

        for aSubDictionary in hasAlist:
            # the list actually only contains ONE dictionary
            #print ("\n", type(subDictionary), " searching subDictionary = ", subDictionary, "\n")
            old = aSubDictionary[subDictName]
            aSubDictionary[subDictName] = value

        #print("old=", old, "new=", value)
    except:
        raise ValueError("No dictionary record for ", subDictName, " was found")

def setValueOfKeyInDict(dictName, keyName, value):
    try:
        list = workingJsonObj[dictName] 
        setValueOfKeyInList(dictName, list, keyName, value)    
    except:
        raise ValueError("No dictionary record for ", keyName, " was found")
        
def getValueOfKeyInDict(dictName, keyName):
    try:
        list = workingJsonObj[dictName]
        return getValueOfKeyInList(list, keyName)    
    except:
        raise ValueError("No dictionary record for ", keyName, " was found")
        

def testModifyJson():
    # modify simple and complicated values

    print ("demod_type = ", getValueOfKeyInDict('channels', 'demod_type'))
    setValueOfKeyInDict('channels', 'demod_type', 'testing' )
    print ("demod_type = ", getValueOfKeyInDict('channels', 'demod_type'))




def    printWorkingJson( headerMessage ):
    #ttps://stackoverflow.com/questions/55944758/read-a-pickled-dictionary-python
    # make a python data pretty printer.
    print ("\n\n", headerMessage , "  -----------------------------------------------\n")

    #** PrettyPrinter width=1, force each element to have its own personal line or it bashes them ALL into 80 charwidth
    toScreen = pprint.PrettyPrinter(indent=4, width=1, sort_dicts=False)
    toScreen.pprint(workingJsonObj)

    serialized = json.dumps(workingJsonObj)
    print (serialized)

    global shortDispName

    #https://stackoverflow.com/questions/4675728/redirect-stdout-to-a-file-in-python
    fileName = "smartnet-"+ shortDispName + ".jason"
    with open(fileName, "w") as outfile:
        with redirect_stdout(outfile):
            print(serialized)
        #toFile = pprint.PrettyPrinter(indent=4, width=1, stream=outfile, sort_dicts=False)
        #toFile.pprint(workingJsonObj)


#-------------------------------------------------------------------------
user_agents_list = [
    'Mozilla/5.0 (iPad; CPU OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.83 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36'
]


#Declaring the headers if forcing english is required. 
#headers = {"Accept-Language": "en-US,en;q=0.5"}

#declaring the list of empty variables, So that we can append the data overall
SiteTable = []
SiteNumbers = []
SiteNameLong = []
SiteNameShort = []
SiteLocations = []

shortDispName = ''
voiceChans=[]
ctrlChans=[]

RadioZoneHttpRoot = 'https://www.radioreference.com'
RadioZoneTGnSites     = RadioZoneHttpRoot + '/db/sid/2560'

oldSiteNum = -1

def hairball():
        
    # we are getting ready to collect a new site.
    # Dump the data of the old site now!
    # call any Json format routines now !
    global voiceChans, ctrlChans 
    
    voiceChans = voiceChans[:-1]
    #ctrlChans = ctrlChans[:-1]


    print ("")
    print ("voiceChans channels :", voiceChans)
    print ("ctrlChans  channels :", ctrlChans)

    #whatever json calls
    setupDefaultJason()
    #printWorkingJson("BEFORE")
    #setValueOfKeyInDict('channels', 'trunking_sysname', shortDispName )
    #  ',',join(somelist)  ... convert list to comma delimited string
    setDictInListOfDict('trunking', 'chans', 'control_channel_list', ','.join(ctrlChans))
    printWorkingJson("AFTER")

def parseOneRecord(aRecord):

    global oldSiteNum, voiceChans, ctrlChans, shortDispName

    aSiteNum = aRecord.find('td', class_='data-text fit')

    if ( aSiteNum != None):

        if ( aSiteNum != oldSiteNum):
            hairball()
 
        oldSiteNum = aSiteNum
        voiceChans = []
        ctrlChans = []

        # recover the gps co-ordinates. -------------------------- 
        print ("\n===================================================")
        #auxLink = <td style="width: 100%"><a href="/db/site/28154">Harcourt (HARCOU)</a></td>
        auxLink = aRecord.find('td', style='width: 100%')
        textLink = str(auxLink) # convert object to simple text
        #print ("textLink = ", textLink)
        
        breakupText = textLink.split(' ')
        relGPSlink = breakupText[3].split('"')[1]  # gps link is in element 1
        fullGPSlink = RadioZoneHttpRoot + relGPSlink

        # back to real parsing of sites  --------------------------------------

        #print ("------ aSiteNum = \n", aSiteNum, "\n")
        #print ("--- aSiteNum.text =", aSiteNum.text, "\n")
        decSiteNumber = int(aSiteNum.text.split(' ')[0])
        SiteNumbers.append(decSiteNumber)
        print ("decSiteNum :", decSiteNumber)
        print ("fullGPSlink = ", fullGPSlink)

        aFullName = aRecord.find('td', style='width: 100%')
        #print("--- aFullName =\n", aFullName, "\n")
        
        longDisplayName = aFullName.text.split('(')[0] # long display name is left of (blah)
        print ("long Display:", longDisplayName)
        SiteNameLong.append(longDisplayName)

        shortDispName = aFullName.text.split('(')[1].split(')')[0]  # display name is inside (blah)
        SiteNameShort.append(shortDispName)
        print ("short Display:", shortDispName)

        aAffiliation = aRecord.find('td', style='width: 100%', class_='noWrapTd')
        #print ("-----\naLocation = ", aAffiliation)
        print ("aAffiliation :", aAffiliation.text)
        SiteLocations.append(aAffiliation.text)

    else:
        #print ("note: parsing a frequency only row\n", aRecord, "\n")
        print ("note: parsing a frequency only row\nadding more voice/control")

    # all records have frequencies in them.

    listcFreqs = aRecord.findAll('td', class_='data-text crtl-pri')
    for aFreq in listcFreqs:
        cFreq = aFreq.text[:-1]  #drop the trailing c
        print ("----- cFreq =", cFreq)
        ctrlChans.append(cFreq)
 
    # findAll using just class='data-text' does implied WILDCARD like 'data-text*'
    # above picks up too many 'data-text*' hits
    # restrict findall to do a whole word exact match 
    # lamda is a narrow scope function inside a function call :)
    # https://stackoverflow.com/questions/22726860/beautifulsoup-webscraping-find-all-finding-exact-match

    listvFreqs = aRecord.findAll(lambda tag: 
                                    tag.name =='td' 
                                    and tag.get('class') == ['data-text'])

    for aFreq in listvFreqs:
        vFreq = aFreq.text
        print ("----- vFreq =", vFreq)
        voiceChans.append(vFreq)
 


#-------------------------------------------------------------------------
#*** try:
#***    raise NotImplementedError("No error")

#the whole core of the script
try:

    print ("getting page ", RadioZoneTGnSites)

    # randomize the 'browser' we are using so it gets by bot detection
    page = requests.get( RadioZoneTGnSites, headers={'User-Agent': random.choice(user_agents_list)})
 
    page.raise_for_status()

    soup = BeautifulSoup(page.text, 'html.parser')
    #print (soup)
    # top of the area of interest where everything below is the movie

    aSiteNum = soup.find('div', id ='sites_div')
    #print("============================================\n print aSite \n", aSite, "\n")

    SiteTable = aSiteNum.find('table', class_='table table-sm table-responsive table-bordered')
    #print ("===========================================\n siteTable = ", SiteTable, "\n\n")

    manyRecords = aSiteNum.findAll('tr')
    #print ("==========================================\n", manyRecords)

    skipFirst = True

    for aRecord in manyRecords:

        # first entry is pretty layout and database stuff
        if  (skipFirst == True) :
            skipFirst = False
            #print("skipping header text layout ?\n", aRecord, "\n")
            continue


        #print ("---------------------------- aRecord = \n", aRecord, "\n")

        #creating a dataframe   
        siteDataTable = pd.DataFrame({ "SiteNum": SiteNumbers, "Long Name" : SiteNameLong, "Short Name" : SiteNameShort, "Location": SiteLocations } )

        parseOneRecord(aRecord)

    # don't strand the last site processed, there won't be a following site
    # to force it to cough out site data
    #                 
    print ("")
    print ("voiceChans channels :", voiceChans)
    print ("ctrlChans  channels :", ctrlChans)

    #whatever json calls

    print()
        
    # if this is ever printed, print only first and last 5 entries
    #siteDataTable.head(5)

    # this makes the console display the table.
    # It is required for python3 but not for python2
    print (siteDataTable)   
        

    # #saving the data in excel format
    siteDataTable.to_excel(shortDispName + str(".xlsx"))

    #If you want to save the data in csv format
    siteDataTable.to_csv(shortDispName + str(".csv"))

except Exception as e:
    #https://stackoverflow.com/questions/1278705/when-i-catch-an-exception-how-do-i-get-the-type-file-and-line-number
    print(traceback.format_exc())
    #print ("OH SHIT, caught an exception" , e)


except Exception as e:
    print (e)
