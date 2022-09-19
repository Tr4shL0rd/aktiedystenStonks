#!/usr/bin/env python3
import os
import json
import helper
import requests
import datetime
from sys import argv
from rich.table import Table
from rich.console import Console
import datetime
config = helper.loadConfig()

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
def checkTime(onhour:str, onmin:str, offhour:str, offmin:str, now_time:datetime=datetime.datetime.now().time()) -> str:
    '''
        checks if current time is between 2 time slots\n
        takes hour and minute of 2 different time slots
    '''
    # if the hour of time slot 2 is earlier than the hour of time slot 1 
    if offhour < onhour:
        if datetime.time(offhour,offmin) <= now_time <= datetime.time(onhour,onmin):
            return "CLOSED"
        else:
            return "OPEN"
    else:
        if datetime.time(onhour,onmin) <= now_time <= datetime.time(offhour,offmin):
            return "OPEN"
        else:
            return "CLOSED"
def helpFunc() -> None:
    '''
        reads help.txt and prints the data 
    '''
    with open("help.txt", "r") as helpFile:
        lines = helpFile.readlines()
        for line in lines:
            print(line.replace("\n", ""))

def stockPrice() -> list:
    '''
        returns the current price of the listed stocks
    '''
    # url endpoints for stock prices
    urlIndex = {
        "spot": "(NYSE~SPOT)",
        "oil":  "(BRENT~LCO)",
        "jysk": "(CPH~JYSK)",
        "beat": "(NASDAQ~BEAT)",
    }
    # base url for all stock endpoints
    url = "https://aktiedysten.dk/z/chart?q=s.i1d.full"

    # response for each url 
    responseSpot = requests.get(f"{url}{urlIndex['spot']}")
    responseOil  = requests.get(f"{url}{urlIndex['oil']}")
    responseJysk = requests.get(f"{url}{urlIndex['jysk']}")
    responseBeat = requests.get(f"{url}{urlIndex['beat']}")
    # data from each response 
    dataSpot = json.loads(responseSpot.text)
    dataOil  = json.loads(responseOil.text)
    dataJysk = json.loads(responseJysk.text)
    dataBeat = json.loads(responseBeat.text)
    
    # price array from data (might be possible to do it in a smarter way)
    priceSpot = dataSpot["Encoded"]["Data"]
    priceOil  = dataOil["Encoded"]["Data"]
    priceJysk = dataJysk["Encoded"]["Data"]
    priceBeat = dataBeat["Encoded"]["Data"]
    # individual prices from the price array given by data 
    currentPriceSpot = round(priceSpot[-2],1)
    currentPriceOil  = round(priceOil[-1], 1)
    currentPriceJysk = round(priceJysk[-2],1)
    currentPriceBeat = round(priceBeat[-2],1)

    return [currentPriceOil, currentPriceSpot, currentPriceJysk, currentPriceBeat]
def main(load:bool=True):
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
        "beat": "NASDAQ",
    }
    
    # a dict for the script name and description (description is not used anymore (find a way to remove))
    # number to program name
    scripts = {
        "1": "oil.py" ,
        "2": "spot.py",
        "3": "jysk.py",
        "4": "beat.py",
    }
    # letterScripts converts program name string into program index
    # program name to number
    letterScripts = {
        "oil":  "1",
        "spot": "2",
        "jysk": "3",
        "beat": "4",
    }
    # opening and closing times for each market
    openTime = {
        "NYSE":  [(15,00), (22,00)],
        "CPH":   [(9 ,00), (17,00)],
        "BRENT": [(00,00), (23,00)],
        "NASDAQ": [(15,00), (22,00)],
    }
    # prettier way of showing closing-opening times for the table 
    openTimePretty = {
        "NYSE":  "15:00 - 22:00",
        "CPH":   "09:00 - 17:00",
        "BRENT": "00:00 - 00:00",
        "NASDAQ": "15:00 - 22:00",
    }
    # fills the table
    if load:
        helper.clear(1000)
        print("LOADING...")
        # formatted pricing 
        prices = {
            "oil":  f"${str(stockPrice()[0])}",
            "spot": f"${str(stockPrice()[1])}",
            "jysk": f"${str(helper.convertCurrency(stockPrice()[2], fromCurrency='DKK', targetCurrency=config['default_currency_target']))}",
            "beat": f"${str(stockPrice()[3])}",
        }
        for k,v in scripts.items():
            progName = v.split(".py")[0]
            table.add_row(
                k,                                                      # IDX
                progName.title(),                                       # PROGRAM 
                prices[progName],                                       # PRICE
                exchange[progName.lower()],                             # MARKET
                openTimePretty[exchange[progName.lower()]],             # MARKET OPEN TIMES
                str(                                                    # OPEN
                    checkTime(                                          # OPEN
                            openTime[exchange[progName.lower()]][0][0], # (market hour open time)
                            openTime[exchange[progName.lower()]][0][1], # (market minute open time)
                            openTime[exchange[progName.lower()]][1][0], # (market hour close time)
                            openTime[exchange[progName.lower()]][1][1]  # (market minute close time)
                        ) # /checkTime
                    ) # /str
                ) # /add_row
        helper.clear()
        console.print(table)
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
    allCommands = helper.flatten(allCommands)# flattens the list once more
    choice = input(">> ").strip()
    # checks user input against the available commands (switch case might be better)
    if choice in allCommands:
        if choice in commands["help"]:
            helpFunc()
            main(False)
        if choice in commands["reload"]:
            helper.clear(40)
            main(True)
        if choice in commands["exit"]:
            print("EXITING...")
            exit()
    try:
        # checks if user input is alphabetic and is a valid input against letterScripts
        if choice.isalpha() and choice in letterScripts:
            program = scripts[letterScripts[choice]] # converts a name string into the correct program name 
        # checks if user input is a number and less then the amount of available script -1
        elif choice.isdigit() and  int(choice) > len(scripts):
            helper.clear()
            print(f"number cant be higher than {len(scripts)}")
            main()
        else:
            program = scripts[choice]
    except KeyError:
        helper.clear()
        print(f"\"{choice}\" is not a valid program or command!")
        main()
    print(f"starting {program}....")
    os.system(f"python stockScripts/{program}")
try:
    try:
        if argv[1] == "--help" or argv[1] == "-h":
            helpFunc()
            exit()
        if argv[1] == "--version" or argv[1] == "-v" or argv[1] == "version":
            print(f"Aktiedysten Stonks v{config['version']}\nCreated By @Tr4shL0rd")
            exit()
    except IndexError:
        pass
    main()
except KeyboardInterrupt:
    print("Exiting....")
