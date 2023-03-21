import sys
import colorama
from colorama import Fore
colorama.init(autoreset=True)
from datetime import datetime

class Logger(object):

    def info(self, quote):
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        log = Fore.LIGHTGREEN_EX + f"[{current_time}] " + Fore.LIGHTYELLOW_EX + "[MKVTagger] " + Fore.LIGHTBLACK_EX + "INFO: " + Fore.LIGHTWHITE_EX + f"{quote}"
        print(log)

    def error(self, quote, exit=0):
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        log = Fore.LIGHTGREEN_EX + f"[{current_time}] " + Fore.LIGHTYELLOW_EX + "[MKVTagger] " + Fore.LIGHTRED_EX + "ERROR: " + Fore.LIGHTWHITE_EX + f"{quote}"
        print(log)
        if exit == 1: sys.exit()

    def warning(self, quote, exit=0):
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        log = Fore.LIGHTGREEN_EX + f"[{current_time}] " + Fore.LIGHTYELLOW_EX + "[MKVTagger] " + Fore.LIGHTBLACK_EX + "WARNING: " + Fore.LIGHTWHITE_EX + f"{quote}"
        print(log)
        if exit == 1: sys.exit()