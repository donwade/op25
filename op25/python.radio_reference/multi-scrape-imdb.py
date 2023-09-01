# %%
"""
## Scraping Multiples pages of IMDB at a time to fetch top 1000 movies data.
"""

# %%
"""
_*If you have any doubts, you may reach me out on <b>hustlewithzidd@gmail.com<b>*_
"""

# %%
"""
_*<b>Edit: Added the Description part of Movie in the Dataframe (July-15-2021)<b>*_
"""

# %%
"""
_*<b>Kindly support me by subscribing my channel and <b>endorsing my skills in linkedIn : https://www.linkedin.com/in/sivasahukar95/<b>*_
"""

# %%


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

movie_name = []
year = []
time=[]
rating=[]
metascore =[]
votes = []
gross = []
description = []

# creating an array of values and passing it in the url for dynamic webpages
# range from 1 to 1000 counting by 100

#pages = np.arange(1,1000,100)
pages = np.arange(1,200,100)   # testing... only get 2 pages of the 100 available

#the whole core of the script
try:
    for page in pages:
        print ("getting page ", page)
        page = requests.get("https://www.imdb.com/search/title/?groups=top_1000&sort=user_rating,desc&count=100&start="+str(page)+"&ref_=adv_nxt", headers={'User-Agent': random.choice(user_agents_list)})
        page.raise_for_status()

        soup = BeautifulSoup(page.text, 'html.parser')

        # top of the area of interest where everything below is the movie
        movie_data = soup.findAll('div', attrs = {'class': 'lister-item mode-advanced'})

        # don't flood the server, may also trip bot detection. Sleep b/n 2 or 8 secods to avoid detection
        sleep(randint(2,8))

        for store in movie_data:
            name = store.h3.a.text
            movie_name.append(name)
            
            year_of_release = store.h3.find('span', class_ = "lister-item-year text-muted unbold").text
            year.append(year_of_release)
            
            runtime = store.p.find("span", class_ = 'runtime').text
            time.append(runtime)
            
            # this text did not have a class, the word inline-block is used.
            rate = store.find('div', class_ = "inline-block ratings-imdb-rating").text.replace('\n', '')
            rating.append(rate)
            
            # not all metascores had a value. test with if condition is in the middle (that's weird)
            # if it exists, do assignment on left but if not take value after the else (jesus this language is fucked)
            meta = store.find('span', class_ = "metascore").text if store.find('span', class_ = "metascore") else "****"
            metascore.append(meta)
            
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
            description.append(description_)
        
except Exception as e:
    print (e)



#creating a dataframe 
movie_list = pd.DataFrame({ "Movie Name": movie_name, "Year of Release" : year, "Watch Time": time,"Movie Rating": rating, "Meatscore of movie": metascore, "Votes" : votes, "Gross": gross, "Description": description  })



# %%
movie_list.head(5)

print (movie_list)   # this makes it pop up to display first and last 5 lines.


# %%
# #saving the data in excel format
movie_list.to_excel("Top 1000 IMDb movies.xlsx")

# #If you want to save the data in csv format
movie_list.to_csv("Top 1000 IMDb movies.csv")

# %%

