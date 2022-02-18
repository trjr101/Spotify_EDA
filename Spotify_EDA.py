#A Spotify Data EDA by Mihir Jetly

#Importing our libraries
from datetime import datetime
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from collections import Counter
import plotly.io as pio
import plotly.graph_objects as go
import plotly.express as px
from plotly.figure_factory import create_distplot

pio.templates['draft'] = go.layout.Template(
    layout_annotations=[
    dict(
        textangle=-30,
        opacity=0.1,
        font=dict(color='black', size=100),
        xref='paper',
        yref='paper',
        x=0.5,
        y=0.5,
        showarrow=False
    )
    ]
)

pio.templates.default = 'draft'

#Now, we want to read in our data and store it in a variable that we will name "dat"
dat = pd.read_csv('data\data.csv', sep="#")

#Set our display settings so that we can see all the data
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', None)

#Display the first and last 5 lines of what we imported
print(dat.head())
print("\n")
print(dat.tail())
print("\n\n")

#Check the data info to see if there are any disparities in the data that needs to be addressed.
print(dat.info())
print("\n\n")

#We now want to process our NaN values

print(dat.isna().sum())
print("\n\n")

dat.dropna(inplace=True)

#Confirm that our NaN values are removed
print(dat.isna().sum())
print("\n\n")

#We create some functions that will be useful later on, just to keep the code neat

#Separate the keyword of "Featuring" or "feat" for getting the number of singers
def get_keyword(s):
    if('featuring' in s.lower()):
        return 'featuring'
    elif 'feat' in s.lower():
        return 'feat'
    else:
        return 'with'

#Now we write a function to check if a song is featured.
def check_song_featured(name):
    keyword = get_keyword(name)
    if_exists = name.lower().find(keyword)
    if if_exists != -1:
        feat = name[if_exists + len(keyword) + 1:-1]
        sep = '&' if '&' in feat else ','
        return [x.strip() for x in feat.split(sep)]
    else:
        return 'None'

#Now we get the number of singers
def get_num_sing(feat):
    if isinstance(feat, list):
        return len(feat) + 1
    else:
        return 1

#Now we want to only get the song name
def get_song_name(name):
    sep = 'feat' if 'feat' in name.lower() else 'with'
    found = name.lower().find(sep)
    if found != -1:
        return name[:found-1].strip() #The -1 is to skip the (
    else:
        return name
#Finished writing all the functions we will need

#Now we want to move this from a pandas dataframe to a numpy array, then separate the genres into a list.
data = dat.to_numpy()

#Clean up the list in order to view each string value by itself.
for i in data:
    i[5] = i[5].lstrip("[").rstrip("]").split(sep=',')
    for j in range(len(i[5])):
        i[5][j] = i[5][j].replace("'","").strip()

#Count the total number of times a song of each Genre has made the top 200 daily songs. This doesn't account for repeats from day to day
res = Counter()

for i in data:
    res.update(i[5])

res = list(res.items())
res.sort(key=lambda x:x[1], reverse=True)

x_label,y = zip(*res)

#Now we want to see how this changes, so let's get the values for each year from 2017-2021

ct2017G = Counter()
ct2018G = Counter()
ct2019G = Counter()
ct2020G = Counter()
ct2021G = Counter()

#Create an if else statement block to get the values from each year

for i in data:
    if("2017" in i[4]):
        ct2017G.update(i[5])
    elif("2018" in i[4]):
        ct2018G.update(i[5])
    elif ("2019" in i[4]):
        ct2019G.update(i[5])
    elif ("2020" in i[4]):
        ct2020G.update(i[5])
    else:
        ct2021G.update(i[5])

#Now we want to create each mapping as a list
ct2017G = list(ct2017G.items())
ct2018G = list(ct2018G.items())
ct2019G = list(ct2019G.items())
ct2020G = list(ct2020G.items())
ct2021G = list(ct2021G.items())

#Sort in descending order
ct2017G.sort(key=lambda x:x[1], reverse=True)
ct2018G.sort(key=lambda x:x[1], reverse=True)
ct2019G.sort(key=lambda x:x[1], reverse=True)
ct2020G.sort(key=lambda x:x[1], reverse=True)
ct2021G.sort(key=lambda x:x[1], reverse=True)

#Split each list into 2 variables to plot
x1G,y1G = zip(*ct2017G)
x2G,y2G = zip(*ct2018G)
x3G,y3G = zip(*ct2019G)
x4G,y4G = zip(*ct2020G)
x5G,y5G = zip(*ct2021G)

#plot each year into a bar chart, but all at once in subplots
fig, axs = plt.subplots(2,3)

plt.rc('font', size=10)

p1 = axs[0,0].bar(x_label[:5],y[:5], width=0.5)
p2 = axs[0,1].bar(x1G[:5],y1G[:5], width=0.5)
p3 = axs[0,2].bar(x2G[:5],y2G[:5], width=0.5)
p4 = axs[1,0].bar(x3G[:5],y3G[:5], width=0.5)
p5 = axs[1,1].bar(x4G[:5],y4G[:5], width=0.5)
p6 = axs[1,2].bar(x5G[:5],y5G[:5], width=0.5)
axs[0,0].title.set_text('Overall most listened to Genres 2017-2021')
axs[0,1].title.set_text('Top 5 genres 2017')
axs[0,2].title.set_text('Top 5 genres 2018')
axs[1,0].title.set_text('Top 5 genres 2019')
axs[1,1].title.set_text('Top 5 genres 2020')
axs[1,2].title.set_text('Top 5 genres 2021')

axs[0,0].bar_label(p1, label_type='edge')
axs[0,1].bar_label(p2, label_type='edge')
axs[0,2].bar_label(p3, label_type='edge')
axs[1,0].bar_label(p4, label_type='edge')
axs[1,1].bar_label(p5, label_type='edge')
axs[1,2].bar_label(p6, label_type='edge')

plt.show()

#Now that we have the top Genres, we want to continue on to engineer the rest of our features for a more in depth EDA
dat["Year"] = dat["Date"].apply(lambda x: datetime.strptime(x, "%Y-%m-%d").year)
dat["Month"] = dat["Date"].apply(lambda x: datetime.strptime(x, "%Y-%m-%d").month)
dat["DayOfWeek"] = dat["Date"].apply(lambda x: datetime.strptime(x, "%Y-%m-%d").isoweekday())
#Get the number of artists, and track names without the additional artists.
dat["Featuring"] = dat["Track Name"].apply(lambda x: check_song_featured(x))
dat["Number of Singers"] = dat["Featuring"].apply(lambda x: get_num_sing(x))
dat["Track Name"] = dat["Track Name"].apply(lambda x: get_song_name(x))

#Now we view the first 5 lines to see what our dataframe looks like
print(dat.head())

#Now we want to find out which songs have lasted the longest in the top position
first_pos_occ = dat.loc[dat['Position']==1].groupby('Track Name').count()
first_pos_occ = first_pos_occ.sort_values(by='Position', ascending=False).reset_index()[:10]

fig = go.Figure()
fig.add_trace(go.Bar(x=first_pos_occ['Track Name'], y=first_pos_occ['Position']))
fig.update_layout(title='Spotify Top 10 Tracks Lasting in First Position', xaxis_title='Track Name', yaxis_title='Number of Days')

fig.show()

#Now we finish off with getting the top 5 artists for each year

yearly_artist = dat.groupby(['Year', 'Artist']).sum()['Streams']
yearly_artist = yearly_artist.reset_index().sort_values(by=['Year', 'Streams'],ascending=False)

df = pd.DataFrame()
for year in sorted(yearly_artist.Year.unique()):
    df = pd.concat([df, yearly_artist.loc[yearly_artist.Year == year][:5]])

fig = px.bar(data_frame=df,x='Artist',y='Streams', animation_frame='Year')

fig.update_layout(title='Spotify Top 5 Most Streamed Artists by Year', xaxis_title='Artist', yaxis_title='Yearly Streams')

fig.show()