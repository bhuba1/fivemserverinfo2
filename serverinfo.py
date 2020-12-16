from bs4 import BeautifulSoup
from pynput.keyboard import Key, Listener
from os import system 
from datetime import datetime
from selenium.webdriver.firefox.options import Options
from os import path
from colorama import init
from colorama import Fore, Back, Style

init()

import os.path
import time
import threading
import sys
import json
import selenium.webdriver as webdriver

serverList = ["https://servers.fivem.net/servers/detail/rgl7rg"]

globalPlayerList = []
playerList = [] 
watchList = []

options = Options()
options.add_argument('--headless')
driver = webdriver.Firefox(options=options)
driver.get(serverList[0])
time.sleep(1)

def getData(url):
    soup = BeautifulSoup(driver.page_source,'html.parser')
    
    return soup

def getServerName(soup):
    try:
        serverName = soup.findAll("div", {"class": "title"})[0].getText()
    except (IndexError):
        print ("The page didn't loaded properly :(")
        print(soup)
        #time.sleep(1)
        #getServerName(soup)
        sys.exit();
    return serverName

def getPlayerCount(soup):
    playerCount = soup.findAll("div", {"class": "players-count"})[0].getText().replace("group ", "")
    
    return playerCount

def getPlayerList(soup):
    players = []
    playersDiv = soup.findAll("div", {"class": "details-panel players"})[0]
    
    lis = playersDiv.findAll("li");
    for li in lis:
         players.append(li.getText())
    
    return players

def saveToFile(file="players.txt"):
    if len(globalPlayerList) == 0:
        return False
    
    with open(file, "w", encoding="utf-8") as f:
        json.dump([ob.__dict__ for ob in globalPlayerList], f, indent=2, ensure_ascii=False)
    print("Saved player datas")

def readFromFile(file="players.txt"):
    if ((not path.isfile(file)) or (os.stat(file).st_size == 0)):
        return []
    with open(file, "r", encoding="utf-8") as f:
        data = json.load(f)
        print("Read player datas")
        return data
        
def on_release(key, ):
    #driver.quit()
    #sys.exit("ESC pressed")
    if (key == Key.esc):
        driver.quit()
        sys.exit("ESC pressed")

def printPlayer():
    for player in playerList:
        if player.name in watchList:
            
            print(Style.BRIGHT + Fore.WHITE + Back.GREEN)
            print(player)
            print(Style.RESET_ALL)
        else:
            print(player)
            print()

def loadWatchList(file="watchlist.txt"):
    with open(file, "r", encoding="utf-8") as f:
        return f.read().split("\n")

def loop(datas):
    while(True):
        global playerList
        _ = system("cls")
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        print(current_time)
        print("\n|" + "-" * 30 + "| FiveM Server Info |" + "-" * 30 + "|\n")
        
        soup = getData(serverList[0])
        serverName = getServerName(soup)
        playerCount = getPlayerCount(soup)
        players = getPlayerList(soup)

        print(serverName)
        print(playerCount)
        [print(player) for player in players]
        print("\n|" + "-" * 81 + "|\n")
        time.sleep(10)

def main():
    global watchList
    #datas = readFromFile()
    datas = "#"
    #watchList = loadWatchList()
    print("loading...")
    x = threading.Thread(target=loop, args=(datas,))
    x.setDaemon(True)
    
    try:        
        x.start()
        with Listener( on_release=on_release ) as listener:
            listener.join()
    except (KeyboardInterrupt, SystemExit):
        sys.exit()
        

if __name__ == "__main__":
    main()
