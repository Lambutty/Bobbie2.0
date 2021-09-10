import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash
import pandas as pd
import random as r
from dash.exceptions import PreventUpdate
from requests.api import get
from scrapeNews import getNews
from dash_extensions.enrich import Output, DashProxy, Input, MultiplexerTransform
from pathlib import Path


#------------------------------------------------------------------------------------------------------------------------------------------------


#Dashboard written in Python dash
#Requirements to run. Logged in Browser Instance for HS and Zabbix. seleniumTestFirefoxMain.py is a script that provides automatic login with cookies.
#I ran in problems displaying Zabbix in IFrame on Chrome why im using Firefox -> !!!You have to have XFRAME Extension(https://addons.mozilla.org/de/firefox/addon/ignore-x-frame-options-header/) 
# for Firefox installed in order to see data from zabbix and the autologin script has to start its instance with that specific profil which has the extension installed further information is in the Script itself!!!
#Backend Flask , Frontend React.js , Diagram generating Assistant plotly.js
#Every outside CSS can be easily placed in assets/style.css, no import is needed css is a mess and you probably dont want to lock at it (:
#in assets you can set a favicon.ico displaying the icon of your application dash finds favicon.ico automatically
#data.json holds news with the tag german. Every hour it gets refreshed if the server is running
#overall we have a grid layout with 4 boxes for every different data:
#Hubspot -> going through a provided list of hubspot Urls shown in IFrame
#Zabbix ->  going through a provided list of hubspot Urls shown in IFrame
#NewsFeed -> getting Data from newsapi.org/tag=german (currently with my private key) storing it in data.json which gets updated every hour when the server is running,
#currently only displaying the title and the image of the news
#Rainfall Radar -> provided by https://www.rainviewer.com displayed in IFrame the view of radar should be costumizable via their website where you can generate a new link
#google meet Button -> Opens Google Meet Session, currently in the same browser tab, so after meeting you have to click back with browser
#User Interaction -> by clicking on Hubspot or Zabbix Frame you can skip to the next Diagram


#------------------------------------------------------------------------------------------------------------------------------------------------
#initialising global News global variable is far from good practice but it helps performance and setting variables

global newsJSON
newsJSON = pd.read_json(Path(__file__).with_name('data.json'))


configPath = Path(__file__).with_name('config.json')
configData = pd.read_json(configPath)


hubspotUrls = configData["urls&token"]["HubspotURLS"]
zabbixUrls= configData["urls&token"]["zabbixURLS"]
jousFix = configData["urls&token"]["jousFix"]
rainViewer = configData["urls&token"]["rainViewer"]
bobbieImg = configData["urls&token"]["bobbieImage"]

#------------------------------------------------------------------------------------------------------------------------------------------------
#get new Newsdata every hour put it into json

from apscheduler.schedulers.background import BackgroundScheduler


def schedule_task_news():
    global newsJSON
    getNews()
    newsJSON = pd.read_json(Path(__file__).with_name('data.json'))
    print("We are updating data.json")

scheduler = BackgroundScheduler()
scheduler.add_job(func=schedule_task_news, trigger="interval", seconds=60*60)
scheduler.start()


#------------------------------------------------------------------------------------------------------------------------------------------------
#defining common functions

def check_if_interval_out_of_range_pre_cardfill(new_interval):
    return new_interval==None or new_interval==-1

def check_if_interval_out_of_range_post_cardfill(new_interval,dashboard_list_length):
    return new_interval==dashboard_list_length-1

def get_trigger_of_callback(callback_context):
    return callback_context.triggered[0]['prop_id'].split('.')[0]


#------------------------------------------------------------------------------------------------------------------------------------------------
#initialising dash app with external stylesheets for dash bootstrap -> dbc , multiplexertransform is for being able to use the same trigger for different callbacks

app = DashProxy(
    external_stylesheets=[dbc.themes.BOOTSTRAP],transforms=[MultiplexerTransform(proxy_location="inplace")]
)


#------------------------------------------------------------------------------------------------------------------------------------------------
# defining grid layout for page -> 2 row and each row has 2 columns

cards =     [
        
       dbc.Row(     [
                html.Div(dbc.Col(id="card1"),id="card1trigger"),
                html.Div(dbc.Col(id="card2"),id="card2trigger"),
                
            ]
            
        ),
        dbc.Row(
            [
                html.Div(dbc.Col(id="card3")),
                html.Div(dbc.Col(id="card4")),
                
            ],
            
        ),
      
    ]

    
#------------------------------------------------------------------------------------------------------------------------------------------------
#defining button for JousFix(gmeet) and the Bobbie Image for top Page

button = dbc.Button("Jous Fix", outline=True, color="success",id="googleMeet",size="lg",href=jousFix,className="button1")
bobbieImage = html.Img(src=bobbieImg,style={"width":"10%","height":"10%"})


#------------------------------------------------------------------------------------------------------------------------------------------------
#general layout for page
#interval initialize callback function with the specific id name defining the time for the interval in -> 
# 1000 = 1 sekunde

def serve_layout():
    
    return html.Div([
        dcc.Interval(id='my-interval1', interval=50*1000),#card1    hubspot
        dcc.Interval(id='my-interval2', interval=50*1000),#card2    zabbix
        dcc.Interval(id='my-interval3', interval=14*1000),#card3    news           
        dcc.Interval(id='my-interval4', interval=80*1000),#card4    weather 
        
        html.Div(bobbieImage,className="bobbieimage"),#topimage bobbie of webpage
        
        html.Div(cards,id="cards"),#predefined cards object gets put into div and gets id
        
        html.Div(button,className="button1"),#google meet button

        
    ])


#------------------------------------------------------------------------------------------------------------------------------------------------
#fully set app layout

app.layout = serve_layout


#------------------------------------------------------------------------------------------------------------------------------------------------
#callback functions are functions that are called from specific events either from intervals, button press or more complex calls.
#they can have multiple amounts of inputs aswell as outputs where you have to define the id and value of a component, example: 
# Input('myinterval'=id,'n-intervals'=number of times the interval has happened as int)
#it needs a decorator with @nameofyourapp.callback, it binds a function that only can be called via the callback
#output have to be dash components
#------------------------------------------------------------------------------------------------------------------------------------------------
#we will return dash bootstrap components and refresh them with the updated data
#------------------------------------------------------------------------------------------------------------------------------------------------
#on callback configuring the Card component for Hubspot 


@app.callback(
    [
        Output('card1', 'children'), 
        Output('my-interval1', 'n_intervals')
    ],
    [Input('my-interval1', 'n_intervals'), Input('card1trigger','n_clicks')])
def display_output(n_intervals,n_clicks): 
    
    
    hubspotUrlList=hubspotUrls
    new_interval=n_intervals
    
    triggerdID = get_trigger_of_callback(dash.callback_context)
    
    if triggerdID == "card1trigger":
        new_interval+=1
        if new_interval >= len(hubspotUrlList):
            new_interval=0
    
            
    if check_if_interval_out_of_range_pre_cardfill(new_interval):
        #setting up interval for when server starts just get first element or when we are out of range
        new_interval=0
    
    card =[
        dbc.CardHeader("Hubspot"),
        dbc.CardBody(
            [ 
                
                html.Iframe(src=hubspotUrlList[new_interval],className="hubspot"),   
            ],

        className="outerdiv"),
    ]

    if check_if_interval_out_of_range_post_cardfill(new_interval,len(hubspotUrlList)): #prevent index of out range Error
        new_interval=-1
    
    return dbc.Card(card, color="primary", inverse=True, className="generalcardclass"),new_interval


#------------------------------------------------------------------------------------------------------------------------------------------------
#on callback configuring the Card component for Zabbix

@app.callback(
    [
        Output('card2', 'children'), 
        Output('my-interval2', 'n_intervals')
    ],
    [Input('my-interval2', 'n_intervals'), Input('card2trigger','n_clicks')])
def display_output(n_intervals,n_clicks):
    
    new_interval=n_intervals  
    
    #x1 is new interval              
    zabbixUrlsList=zabbixUrls

    triggerdID = get_trigger_of_callback(dash.callback_context)
    
    if triggerdID == "card2trigger":
        new_interval+=1
        if new_interval >= len(zabbixUrlsList):
            new_interval=0

    if check_if_interval_out_of_range_pre_cardfill(new_interval):
        new_interval=0
    
    #setting x1 for when server starts just get first element
    card =[
        dbc.CardHeader("Zabbix"),
        dbc.CardBody(
            [
                html.Iframe(src=zabbixUrlsList[new_interval], className="zabbix"),   
            ],
            className="outerdiv"
        ),
    ]
    
    if check_if_interval_out_of_range_post_cardfill(new_interval,len(zabbixUrlsList)):
        new_interval=-1
    
    return dbc.Card(card, color="primary", inverse=True, className="generalcardclass"),new_interval


#------------------------------------------------------------------------------------------------------------------------------------------------
#on callback configuring the Card component NewsFeed

@app.callback(
    Output('card3', 'children'),
    [Input('my-interval3', 'n_intervals')])
def display_output(n_intervals):
    
    global newsJSON
    article=newsJSON["articles"][r.randint(0,len(newsJSON["articles"])-1)]
    
    karte =[
        dbc.CardHeader("News"),
        dbc.CardBody(html.Div(
            [
                html.H1(article["title"]),
                html.Img(src=article["urlToImage"], style={'height':'30%', 'width':'30%'}),                                     
                  
            ]
        ),
        className="")
    ]
    return dbc.Card(karte, color="primary", inverse=True, className="generalcardclass")


#------------------------------------------------------------------------------------------------------------------------------------------------
#on callback configuring the Card component Weather

@app.callback(
    Output('card4', 'children'),
    [Input('my-interval4', 'n_intervals')])

def display_output(n_intervals):
    karte =[
        dbc.CardHeader("Weather"),
        dbc.CardBody(
            [
                html.Iframe(className="weather-iframe", src=rainViewer, style={"width":"100%","height":"100%"}),   
            ]
        ),
    ]
    return dbc.Card(karte, color="primary", inverse=True, className="generalcardclass")


#"https://www.rainviewer.com/map.html?loc=52.5229,13.4033,5&oFa=0&oC=0&oU=0&oCS=1&oF=1&oAP=1&rmt=4&c=1&o=83&lm=0&th=0&sm=1&sn=1" <- bigger Map
#------------------------------------------------------------------------------------------------------------------------------------------------


if __name__ == "__main__":
    app.run_server()#host='0.0.0.0' for whole network