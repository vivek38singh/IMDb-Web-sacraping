#!/usr/bin/env python
# coding: utf-8

# In[1]:


#import libraries

import requests       
import pandas as pd   
import numpy as np  
from bs4 import BeautifulSoup


# In[2]:


url = 'https://www.imdb.com/search/title/?count=100&groups=top_1000&sort=user_rating'
#send HTTP request
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')


# In[3]:


#create empty list to store result of each section
movie_name = []
year = []
time = []
rating = []
metascore = []
votes = []
gross = []
description = []
Director = []
Stars = []


# In[5]:


movie_data = soup.findAll('div', attrs= {'class': 'lister-item mode-advanced'})
print(movie_data)


# In[17]:


for store in movie_data:
    #getting name of movie
    name = store.h3.a.text
    movie_name.append(name)
    #np.count_nonzero(movie_name)
    
    #getting release date ,here using text.replace() we can remove the bracket.
    year_of_release = store.h3.find('span', class_ = 'lister-item-year text-muted unbold').text.replace('(', '').replace(')', '')
    year.append(year_of_release)
    
    #getting runtime of movie
    runtime = store.p.find('span', class_ = 'runtime').text.replace(' min', '')
    time.append(runtime)
    
    #getting rating of movie
    rate = store.find('div', class_ = 'inline-block ratings-imdb-rating').text.replace('\n', '')
    rating.append(rate)
    
    #getting metascore of movie
    meta  = store.find('span', class_ = 'metascore').text.replace(' ', '') if store.find('span', class_ = 'metascore') else 'NO Score'
    metascore.append(meta)
    
    #gross and votes have same attributes,so here created a common variable and then used indexing to get gross and votes value
    value = store.find_all('span', attrs = {'name': 'nv'})
    
    #getting vote count
    vote = value[0].text
    votes.append(vote)
    
    #getting gross count
    grosses = value[1].text if len(value) >1 else 'No count'
    gross.append(grosses)
    
    #getting description of movie
    desc = store.find_all('p', class_ = 'text-muted')
    description_ = desc[1].text.replace('\n', '') if len(desc) >1 else '*****'
    description.append(description_)
    
    #getting director and stars of movie
    cast = store.find("p", class_ = '')
    cast = cast.text.replace('\n', '').split('|')
    cast = [x.strip() for x in cast]
    cast = [cast[i].replace(j, "") for i,j in enumerate(["Director:", "Stars:"])]
    
    Director.append(cast[0])
    Stars.append([x.strip() for x in cast[1].split(",")])
    
    
    


# In[13]:


#creating a dataframe
movie_DF = pd.DataFrame({'Name of movie': movie_name, 'Year of relase': year, 'Watchtime': time, 'Movie Rating': rating, 'Metascore': metascore, 'Votes': votes, 'Gross collection': gross, 'Description': description, "Director": Director, 'Star': Stars})


# In[19]:


#Save data in excel
movie_DF.to_excel("Top_100_IMDB_Movies.xlsx")
movie_DF.head(20)
 


# In[10]:


np.count_nonzero(movie_name)


# In[ ]:




