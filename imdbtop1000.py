import requests
from requests import get
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np

from time import sleep
from random import randint

# Set Accept-Language header as English of US.
headers = {"Accept-Language": "en-US,en;q=0.5"}

titles = []
years = []
time = []
imdb_ratings = []
metascores = []
votes = []
us_gross = []
genres = []
certificates = []
stars = []
descriptions = []

# There are 50 movies on each page, so the parameter starts from 1 and stops at 1001
# np.arrange() is a function in Python library, it  returns evenly spaced values within a given interval
# arrange(start, stop, step) Values are generated within the half-open interval [start, stop), with spacing between values given by step
pages = np.arange(1, 1001, 50)

for page in pages:
    # Request from the server the content of the web page by using get(), and store the server’s response in the variable page
    page = requests.get("https://www.imdb.com/search/title/?groups=top_1000&start=" + str(page) + "&ref_=adv_nxt",
                        headers=headers)
    # Parse the content of current iteration of request
    soup = BeautifulSoup(page.text, 'html.parser')
    # Store all of the data by selecting class lister-item mode-advanced
    movie_div = soup.find_all('div', class_='lister-item mode-advanced')

    # sleep() function suspends execution of the current thread for a given number of seconds while the randint() function returns a random integer
    sleep(randint(2, 10))

    # Use for loop to extract each movie's information and use the text attribute to get the contents
    # Append the data into dataset
    for container in movie_div:
        # Getting movie name
        name = container.h3.a.text
        titles.append(name)

        # Getting year
        year = container.h3.find('span', class_='lister-item-year').text
        years.append(year)

        # Getting runtime
        runtime = container.p.find('span', class_='runtime') if container.p.find('span', class_='runtime') else ''
        time.append(runtime)

        # Getting rating
        imdb = float(container.strong.text)
        imdb_ratings.append(imdb)

        # Getting metascore
        m_score = container.find('span', class_='metascore').text if container.find('span', class_='metascore') else ''
        metascores.append(m_score)

        # Scrape two nv containers since both of them include votes and gross
        nv = container.find_all('span', attrs={'name': 'nv'})

        # Getting vote
        vote = nv[0].text
        votes.append(vote)

        # Getting gross
        grosses = nv[1].text if len(nv) > 1 else ''
        us_gross.append(grosses)

        # Getting genre
        genre = container.find('span', class_='genre').text if container.find('span', class_='genre') else ''
        genres.append(genre)

        # Getting certificate
        certificate = container.find('span', class_='certificate').text if container.find('span',
                                                                                          class_='certificate') else ''
        certificates.append(certificate)

        # Getting star
        star = container.find('p', class_='').text if container.find('p', class_='') else ''
        stars.append(star)

        # Getting description
        dp = container.find_all('p', class_='text-muted') if container.find_all('p', class_='text-muted') else ''
        description = dp[1].text
        descriptions.append(description)

# Attach all the data to the pandas dataframe.
movies = pd.DataFrame({
    'movie': titles,
    'year': years,
    'imdb': imdb_ratings,
    'metascore': metascores,
    'votes': votes,
    'us_grossMillions': us_gross,
    'timeMin': time,
    'genre': genres,
    'certificate': certificates,
    'stars': stars,
    'descriptions': descriptions
})

# Use replace() to remove the ‘,’ , ‘(', and ‘)’ strings
# Use astype() to make it numeric
movies['votes'] = movies['votes'].str.replace(',', '').astype(int)

# Use the str accessor to access the value of each row as a string, and takes the -5:-1 slice from it. Then converts the result to int.
movies.loc[:, 'year'] = movies['year'].str[-5:-1].astype(int)


movies['timeMin'] = movies['timeMin'].astype(str)
movies['timeMin'] = movies['timeMin'].str.extract('(\d+)').astype(int)

# Use Pandas str.extract to remove all string characters, and save the value as type int,\d+ means matching one or more digits.


movies['metascore'] = movies['metascore'].str.extract('(\d+)')
movies['metascore'] = pd.to_numeric(movies['metascore'], errors='coerce')
# Use pd.to_numeric to convert argument to a numeric type. The default return dtype is float64 or int64. If ‘coerce’, then invalid parsing will be set as NaN.

movies['us_grossMillions'] = movies['us_grossMillions'].map(lambda x: x.lstrip('$').rstrip('M'))
movies['us_grossMillions'] = pd.to_numeric(movies['us_grossMillions'], errors='coerce')
# rstrip(): returns a new string with trailing whitespace removed
# lstrip(): returns a new string with leading whitespace removed

movies['genre'] = movies['genre'].str.replace('\n', '').astype(str)
movies['certificate'] = movies['certificate'].astype(str)
movies['stars'] = movies['stars'].astype(str)
movies['descriptions'] = movies['descriptions'].astype(str)



# Print dataframe
print(movies)

# Print the datatypes of columns
print(movies.dtypes)

# Print the missing data and how much data is missing
print(movies.isnull().sum())

# Save scraped data to a CSV file
movies.to_csv('Top 1000 movies.csv')