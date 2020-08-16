import inline as inline
import matplotlib as matplotlib
import pandas as pd
import numpy as np
# %matplotlib inline
import matplotlib
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import plotly.figure_factory as ff
import plotly.express as px
from plotly.subplots import make_subplots
from plotly.validators.scatter.marker import SymbolValidator
data = pd.read_csv('/Users/annawang/icloud/Documents/sentiment environment/NPL/5company/company.csv')
print(data.shape)
print(data.head())
# reformat the headings
data = data.rename(columns={'A': 'screen_name',
                            'B': 'created_at',
                            'C': 'tweet_id',
                            'D': 'text',
                            'E': 'extended_tweet',
                            'F': 'in_reply_to_screen_name',
                            'G': 'in_reply_to_status_id',
                            'H': 'retweet_count',
                            'I': 'favorite_count',
                            'J': 'truncated',
                            'K': 'language',
                            'L': 'in_reply_to_user_id'})
# remove the first unnecessary row
data = data.drop(data.index[0])
print(data.shape)
print(data.head())
# subset data for the GoldmanSachs company
SPGlobal = data['screen_name'] == 'SPGlobal'
SPGlobal = data[SPGlobal]
# select the datetime, the targeted LIWC output variables, and the integral text data
SPGlobal = SPGlobal[['created_at','we','negate','compare','affect','posemo','negemo','anx','anger',
                             'sad','social','family','friend','female','male','certain','health','achieve',
                             'reward','risk','work','leisure','home','death','swear','netspeak','extended_tweet']]
# for the datetime column keep the date only
SPGlobal['created_at'] = SPGlobal['created_at'].str.split(' ').str[0]
# convert the data type
SPGlobal.created_at = pd.to_datetime(SPGlobal.created_at, format='%Y-%m-%d')
# aggregate all columns at days except the text data concatenated but separated by '||'
SPGlobal = SPGlobal.groupby('created_at').agg(we=pd.NamedAgg(column='we', aggfunc=sum),
                                                           negate=pd.NamedAgg(column='negate', aggfunc=sum),
                                                           compare=pd.NamedAgg(column='compare', aggfunc=sum),
                                                           affect=pd.NamedAgg(column='affect', aggfunc=sum),
                                                           posemo=pd.NamedAgg(column='posemo', aggfunc=sum),
                                                           negemo=pd.NamedAgg(column='negemo', aggfunc=sum),
                                                           anx=pd.NamedAgg(column='anx', aggfunc=sum),
                                                           anger=pd.NamedAgg(column='anger', aggfunc=sum),
                                                           sad=pd.NamedAgg(column='sad', aggfunc=sum),
                                                           social=pd.NamedAgg(column='social', aggfunc=sum),
                                                           family=pd.NamedAgg(column='family', aggfunc=sum),
                                                           friend=pd.NamedAgg(column='friend', aggfunc=sum),
                                                           female=pd.NamedAgg(column='female', aggfunc=sum),
                                                           male=pd.NamedAgg(column='male', aggfunc=sum),
                                                           certain=pd.NamedAgg(column='certain', aggfunc=sum),
                                                           health=pd.NamedAgg(column='health', aggfunc=sum),
                                                           achieve=pd.NamedAgg(column='achieve', aggfunc=sum),
                                                           reward=pd.NamedAgg(column='reward', aggfunc=sum),
                                                           risk=pd.NamedAgg(column='risk', aggfunc=sum),
                                                           work=pd.NamedAgg(column='work', aggfunc=sum),
                                                           leisure=pd.NamedAgg(column='leisure', aggfunc=sum),
                                                           home=pd.NamedAgg(column='home', aggfunc=sum),
                                                           death=pd.NamedAgg(column='death', aggfunc=sum),
                                                           swear=pd.NamedAgg(column='swear', aggfunc=sum),
                                                           netspeak=pd.NamedAgg(column='netspeak', aggfunc=sum),
                                                           text_agg=pd.NamedAgg(column='extended_tweet', aggfunc=lambda x: x.str.cat(sep='||')))
# lowercase the text data
SPGlobal['text_agg'] = SPGlobal['text_agg'].str.lower()
# create the dummy variable for text data

SPGlobal['dummy_key'] = SPGlobal['text_agg'].apply(lambda x: 1 if ('covid' in x)|('pandemic' in x)|('coronavirus' in x) else 0)

print(SPGlobal['dummy_key'])
print(SPGlobal.head())
# plot the trends
x_axis = SPGlobal.index
fig = go.Figure()
annotations = []

for i in range(0,25,1):
  y = SPGlobal.iloc[:,i].values.flatten().tolist()
  fig.add_trace(go.Scatter(x=x_axis[:], y=y,
                    mode='lines',
                    name=SPGlobal.columns[i]))

y = SPGlobal.iloc[:, 26].values.flatten().tolist()
y = [j * 120-10 for j in y]
print(y)
raw_symbols = SymbolValidator().values
print(raw_symbols)
symbols = []
for i in range(0,len(raw_symbols),2):
    name = raw_symbols[i+1]
    symbols.append(raw_symbols[i])
    # y.append(name.replace("-open", "").replace("-dot", ""))
    # x.append(name[len(y[-1]):])

fig.add_trace(go.Scatter(x=x_axis[:], y=y,
                       mode='markers', marker_symbol = raw_symbols[5],
                        marker_color = 'red',marker_size =5,
                       name=SPGlobal.columns[26]))

# fig = go.Figure(go.Scatter(mode="markers", x=namevariants, y=namestems, marker_symbol=symbols,
#                            marker_line_color="midnightblue", marker_color="lightskyblue",
#                            marker_line_width=2, marker_size=15,
#                            hovertemplate="name: %{y}%{x}<br>number: %{marker.symbol}<extra></extra>"))

fig.update_yaxes(range=[0,300])
# Title
annotations.append(dict(xref='paper', yref='paper', x=0, y=1.05,
                              xanchor='left', yanchor='bottom',
                              text='LIWC Output for SPGlobal',
                              font=dict(family='Arial',
                                        size=18,
                                        color='rgb(37,37,37)'),
                              showarrow=False))
fig.update_layout(annotations=annotations,
                  autosize=False,
                  width=1200,
                  height=500,
                  margin=dict(l=10, r=10, b=50, t=50, pad=4))
fig.show()