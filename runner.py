import os
import re
from tkinter import E
from rich.table import Table
from rich.console import Console
import requests
def wifiCheck():
    try:
        return requests.get("https://www.google.com").status_code
    except requests.ConnectionError:
        print("Could not connect to wifi")
        print("Exiting...")
        exit()
def main():
    wifiCheck()
    console = Console()
    table = Table(title="STONK TOOLS")
    table.add_column("INDEX")
    table.add_column("PROGRAM")
    table.add_column("INFO")

    scripts = {
        "1": ["oil.py", "Oil Stock Prices"],
        "2": ["spot.py", "Spotify Stock Prices"],
    }
    letterScripts = {
        "oil": "1",
        "spot": "2",
    }
    for k,v in scripts.items():
        table.add_row(k,v[0].split('.py')[0].title(), v[1])
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
main()