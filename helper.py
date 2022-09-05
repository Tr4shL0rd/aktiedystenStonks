import subprocess


def popUp(message: str, timeout=5, stockName="STOCKNAME"):
    try:
        subprocess.Popen(["notify-send", "-a", stockName,
                        "-t", str(timeout*1000), message])
    except FileNotFoundError:
        pass


def clear(amount=32) -> str:
    print("\n"*amount)
