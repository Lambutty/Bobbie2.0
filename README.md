# Dashboard written in [Python Dash](https://dash.plotly.com/) and selenium script to open Firefox with cookies

> ## Requirements to display data. 
> Logged in Browser Instance for Hubspot and Zabbix. 
**openFirefox** is a py script that provides automatic login with cookies. The cookies: cookiesHs.pkl and cookiesZabpkl have to be in the same folder.
I ran in problems displaying Zabbix in IFrame on Chrome why im using Firefox -> **You have to have XFRAME Extension(https://addons.mozilla.org/de/firefox/addon/ignore-x-frame-options-header/) 
for Firefox installed in order to see data from zabbix and the autologin script has to start its instance with that specific profil which has the extension installed. Also you need [geckodriver](https://github.com/mozilla/geckodriver/releases) installed which is firefox specific driver for selenium**.
    You can change/setup your Path in the configSelenium.json which has to be in same folder as openFirefox. It needs the Path to geckodriver aswell as to the Profile with the installed xFrame extension already mentioned. You should have **80% percent zoom** of the browser aswell to ensure the best experience and make everything of the diagrams visible inside the frame. 
---

Python 3.9.6 is recommended with following librarys
```cmd
pip install dash 
pip install dash-extensions
pip install dash-bootstrap-components
pip install requests
pip install selenium
pip install pandas
pip install pyautogui
pip install APScheduler
```
---
## Dashboard itself

>* Backend **Flask** , Frontend **React**.js , Diagram generating Assistant plotly.js (*not in use*)
>* Every outside CSS can be easily placed in assets/style.css, no import is needed css is a mess and you probably dont want to lock at it (:
>* in assets you can set a favicon.ico displaying the icon of your application dash finds favicon.ico automatically
>* data.json holds news from newsapi.org with the tag german. Every hour it gets 
refreshed from pysript ScrapeNews if the server is running
>* configSelenium.json contains the path to geckodriver.exe aswell as to you Firefox profile
>* config.json:
just paste the desired information in. Hubspot and Zabbix are respectively a List of the Dashboard URLS.
Newsapi needs a Token, jousFix is your gmeet link. rainviewer is also link
```json
{
    "urls&token":{              
    "HubspotURLS":[],               
    "zabbixURLS":[],
    "newsapiToken":"",
    "jousFix":"",
    "rainViewer":"",
    }
}
```

___
> Overall we have a grid layout with 4 boxes for every different data:
>* Hubspot -> going through a provided list of hubspot Urls shown in IFrame
>* Zabbix ->  going through a provided list of zabbix Urls shown in IFrame
>* NewsFeed -> getting Data from newsapi.org/tag=german (currently with my private key) storing it in data.json which gets updated every hour when the server is running,
currently only displaying the title and the image of the news
>* Rainfall Radar -> provided by https://www.rainviewer.com displayed in IFrame the view of radar should be costumizable via their website where you can generate a new link
>* google meet Button(Jous Fix) -> Opens Google Meet Session, currently in the same browser tab, so after meeting you have to click back with browser
>* User Interaction -> by clicking on Hubspot or Zabbix Frame you can skip to the next Diagram
---
### Known Flaws/Bugs/Problems
> * The Interval for refeshing/changing the IFrames doesnt stop if you manually change them with clicking -> If you click shortly before the iframe automatically refreshes it refreshes again. 
> * The Intervalls apart from the one refreshing the news json are client side. Which means every User sees something different. Maybe a Feature not a bug
> * Paths are hardcoded for openFirefox script as mentioned you have to manually type them in the configSelenium.json.
> * The CSS is pretty bad. Im not sure where the problem exactly lays but i couldnt fix it so far. Maybe it has something to do with the Framework or the IFrames themself but im unsure. Frames scale weirdly and at the moment are only "optimized" when displaying on the desired TV. You should have 80% percent zoom of the browser aswell to ensure the best experience and make everything of the diagrams visible inside the frame. Also CSS of the newsfeed is not well configured to fit in the desired box all the time.
> * New Diagrams should to have the same size as the others. Look at them for reference. Also to ensure visibility.
> * Insecurity of the System itself. Couldnt solve the problem of the need to be logged in to view the Diagrams
> * all configs and the cookies should be outsourced to another platform for security and accessiblity reasons 
> * since there is no generating of diagrams which i thought was required in the first place i probably should have used another framework or plain html,js,css.
> * currently not deployed and running as a development server which is not recommended for production usage -> WSGI server instead
