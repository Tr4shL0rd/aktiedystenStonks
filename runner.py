#!/usr/bin/env python3
import os
import json
import requests
import datetime
from rich.table import Table
from rich.console import Console
def wifiCheck():
    try:
        return requests.get("https://www.google.com").status_code
    except requests.ConnectionError:
        print("Could not connect to wifi")
        print("Exiting...")
        exit()
def checkTime(onhour, onmin, offhour, offmin):
    now = datetime.datetime.now()
    now_time = now.time()
    # If we're actually scheduling at night:
    if int(offhour) < int(onhour):
        # Check to see if we're in daylight times (ie. off schedule)
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
    urlIndex = {
        "spot": "(NYSE~SPOT)",
        "oil":  "(BRENT~LCO)",
        "jysk": "(CPH~JYSK)",
    }
    url = "https://aktiedysten.dk/z/chart?q=s.i1d.full"

    responseSpot = requests.request("GET", f"{url}{urlIndex['spot']}")
    responseOil  = requests.request("GET",  f"{url}{urlIndex['oil']}")
    responseJysk = requests.request("GET", f"{url}{urlIndex['jysk']}")

    dataSpot = json.loads(responseSpot.text)
    dataOil  = json.loads(responseOil.text)
    dataJysk = json.loads(responseJysk.text)

    priceSpot = dataSpot["Encoded"]["Data"]
    priceOil  = dataOil["Encoded"]["Data"]
    priceJysk = dataJysk["Encoded"]["Data"]

    currentPriceSpot = round(priceSpot[-2], 1)
    currentPriceOil  = round(priceOil[-1], 1)
    currentPriceJysk = round(priceJysk[-2],1)
    return [currentPriceOil, currentPriceSpot, currentPriceJysk]
def main():
    wifiCheck()
    console = Console()
    table = Table(title="-|STONKS TOOLS|-")
    table.add_column("IDX")
    table.add_column("PROGRAM")
    table.add_column("DESCRIPTION")
    table.add_column("PRICE")
    table.add_column("MARKET")
    table.add_column("OPEN TIME")
    table.add_column("OPEN")
    exchange = {
        "spot": "NYSE",
        "oil": "BRENT",
        "jysk": "CPH",
    }
    
    scripts = {
        "1": ["oil.py", "Oil Stock Prices"],
        "2": ["spot.py", "Spotify Stock Prices"],
        "3": ["jysk.py", "Jysk Stock Prices"],
    }
    letterScripts = {
        "oil":  "1",
        "spot": "2",
        "jysk": "3",
    }
    

    prices = {
        "oil":  f"${str(stockPrice()[0])}",
        "spot": f"${str(stockPrice()[1])}",
        "jysk": f"{str(stockPrice()[2])}DKK",
    }
    openTime = {
    "NYSE": [(15,00), (22,00)],
    "CPH":  [(9,00),  (17,00)],
    "BRENT": [(00,00), (23,00)],
    }
    openTimePretty = {
        "NYSE": "15:00 - 22:00",
        "CPH": "09:00 - 17:00",
        "BRENT": "00:00 - 00:00"
    }
    for k,v in scripts.items():
        table.add_row(
            k,                                                                  # IDX
            v[0].split('.py')[0].title(),                                       # PROGRAM 
            v[1],                                                               # DESCRIPTION
            prices[v[0].split('.py')[0]],                                       # PRICE
            exchange[v[0].split('.py')[0].lower()],                             # MARKET
            openTimePretty[exchange[v[0].split('.py')[0].lower()]],             # MARKET OPEN TIMES
            str(                                                                # OPEN
                checkTime(                                                      # OPEN
                        openTime[exchange[v[0].split('.py')[0].lower()]][0][0], # OPEN (market hour open time)
                        openTime[exchange[v[0].split('.py')[0].lower()]][0][1], # OPEN (market minute open time)
                        openTime[exchange[v[0].split('.py')[0].lower()]][1][0], # OPEN (market hour close time)
                        openTime[exchange[v[0].split('.py')[0].lower()]][1][1]  # OPEN (market minute close time)
                    ) # /checkTime
                ) # /str
            ) # /add_row

    console.print(table)
    choice = input("Number: ").strip()

    if choice.isalpha() and choice in letterScripts:
        program = scripts[letterScripts[choice]][0]
    elif choice.isdigit() and  int(choice) > len(scripts):
        print(f"number cant be higher than {len(scripts)}")
    else:
        program = scripts[choice][0]
    print(f"starting {program}...")
    os.system(f"python {program}")
try:
    main()
except KeyboardInterrupt:
    print("Exiting....")