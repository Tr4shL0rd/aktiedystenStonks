#!/usr/bin/env python3
import os
import json
import helper
import requests
import datetime
from rich.table import Table
from rich.console import Console

def wifiCheck():
    '''
        pings www.google.com and checks if any errors happen
    '''
    try:
        requests.get("https://www.google.com")
    except requests.ConnectionError:
        print("Could not connect to wifi")
        print("Exiting...")
        exit()
def checkTime(onhour, onmin, offhour, offmin):
    now = datetime.datetime.now()
    now_time = now.time()
    if int(offhour) < int(onhour):
        if datetime.time(int(offhour),int(offmin)) <= now_time <= datetime.time(int(onhour),int(onmin)):
            return "CLOSED"
        else:
            return "OPEN"
    else:
        if datetime.time(int(onhour),int(onmin)) <= now_time <= datetime.time(int(offhour),int(offmin)):
            return "OPEN"
        else:
            return "CLOSED"

def stockPrice():
    # url endpoints for stock prices
    urlIndex = {
        "spot": "(NYSE~SPOT)",
        "oil":  "(BRENT~LCO)",
        "jysk": "(CPH~JYSK)",
    }
    # base url for all stock endpoints
    url = "https://aktiedysten.dk/z/chart?q=s.i1d.full"

    # response for each url 
    responseSpot = requests.get(f"{url}{urlIndex['spot']}")
    responseOil  = requests.get(f"{url}{urlIndex['oil']}")
    responseJysk = requests.get(f"{url}{urlIndex['jysk']}")
    # data from each response 
    dataSpot = json.loads(responseSpot.text)
    dataOil  = json.loads(responseOil.text)
    dataJysk = json.loads(responseJysk.text)
    # price array from data (might be possible to do it in a smarter way)
    priceSpot = dataSpot["Encoded"]["Data"]
    priceOil  = dataOil["Encoded"]["Data"]
    priceJysk = dataJysk["Encoded"]["Data"]
    # individual prices from the price array given by data 
    currentPriceSpot = round(priceSpot[-2], 1)
    currentPriceOil  = round(priceOil[-1], 1)
    currentPriceJysk = round(priceJysk[-2],1)
    return [currentPriceOil, currentPriceSpot, currentPriceJysk]
def main():
    # checks wifi connection
    wifiCheck()
    console = Console()
    # Table columns
    table = Table(title="-|STONKS TOOLS|-")
    table.add_column("IDX")
    table.add_column("PROGRAM")
    table.add_column("PRICE")
    table.add_column("MARKET")
    table.add_column("OPEN TIME")
    table.add_column("OPEN")
    # each name of the exchanges used
    exchange = {
        "spot": "NYSE",
        "oil": "BRENT",
        "jysk": "CPH",
    }
    
    # a dict for the script name and description (description is not used anymore (find a way to remove))
    # number to program name
    scripts = {
        "1": ["oil.py" , "Oil Stock Prices"],
        "2": ["spot.py", "Spotify Stock Prices"],
        "3": ["jysk.py", "Jysk Stock Prices"],
    }
    # letterScripts converts program name string into program index
    # program name to number
    letterScripts = {
        "oil":  "1",
        "spot": "2",
        "jysk": "3",
    }
    
    # formatted pricing 
    prices = {
        "oil":  f"${str(stockPrice()[0])}",
        "spot": f"${str(stockPrice()[1])}",
        "jysk": f"{str(stockPrice()[2])}DKK",
    }
    # opening and closing times for each market
    openTime = {
    "NYSE": [(15,00), (22,00)],
    "CPH":  [(9,00),  (17,00)],
    "BRENT": [(00,00), (23,00)],
    }
    # prettier way of showing closing-opening times for the table 
    openTimePretty = {
        "NYSE": "15:00 - 22:00",
        "CPH": "09:00 - 17:00",
        "BRENT": "00:00 - 00:00"
    }
    # fills the table
    for k,v in scripts.items():
        table.add_row(
            k,                                                                  # IDX
            v[0].split('.py')[0].title(),                                       # PROGRAM 
            prices[v[0].split('.py')[0]],                                       # PRICE
            exchange[v[0].split('.py')[0].lower()],                             # MARKET
            openTimePretty[exchange[v[0].split('.py')[0].lower()]],             # MARKET OPEN TIMES
            str(                                                                # OPEN
                checkTime(                                                      # OPEN
                        openTime[exchange[v[0].split('.py')[0].lower()]][0][0], # (market hour open time)
                        openTime[exchange[v[0].split('.py')[0].lower()]][0][1], # (market minute open time)
                        openTime[exchange[v[0].split('.py')[0].lower()]][1][0], # (market hour close time)
                        openTime[exchange[v[0].split('.py')[0].lower()]][1][1]  # (market minute close time)
                    ) # /checkTime
                ) # /str
            ) # /add_row
    # overview of the commands
    commands = {
        "help":   ["help", "h"],
        "reload": ["reload", "r"],
        "exit":   ["quit", "exit", "q", "stop"],
        }
    # converts the items of allCommands into a list and flattens said list 
    for key in (allCommands := helper.flatten(list(commands.items()))):  
        # Removes key dupes
        allCommands.remove(key) 
    allCommands = helper.flatten(allCommands) # flattens the list once more
    console.print(table)
    choice = input(">> ").strip()
    # checks user input against the available commands (switch case might be better)
    if choice in allCommands:
        if choice in commands["help"]:
            print(allCommands)
        if choice in commands["reload"]:
            helper.clear(40)
            main()
        if choice in commands["exit"]:
            print("EXITING...")
            exit()
    try:
        # checks if user input is alphabetic and is a valid input against letterScripts
        if choice.isalpha() and choice in letterScripts:
            program = scripts[letterScripts[choice]][0] # converts a name string into the correct program name 
        # checks if user input is a number and less then the amount of available script -1
        elif choice.isdigit() and  int(choice) > len(scripts):
            helper.clear()
            print(f"number cant be higher than {len(scripts)}")
            main()
        else:
            program = scripts[choice][0]
    except KeyError:
        helper.clear()
        print(f"\"{choice}\" is not a valid program or command!")
        main()
    print(f"starting {program}...")
    os.system(f"python {program}")
try:
    main()
except KeyboardInterrupt:
    print("Exiting....")
