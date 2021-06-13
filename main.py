import requests
from threading import Thread
from colorama import Fore
import logging
from time import sleep
from os import system

logging.basicConfig(level=logging.INFO, format="%(message)s")

system("")

names = open('usernames.txt', 'r').read().splitlines()  # read names from file


def check(name):
    r = requests.get(f'https://discords.com/api-bio/user/details/{name}')
    if r.status_code == 404:
        logging.info(f"{Fore.GREEN}[AVAILABLE] {name}")
        with open('available.txt', 'a') as f:
            f.write(name + '\n')
    elif r.status_code == 200:
        logging.info(f"{Fore.RED}[UNAVAILABLE] {name}")
    else:
        logging.info(f"{Fore.RED}[ERROR] Received status code {r.status_code} on {name}")


print(f"{Fore.GREEN}Started check for {len(names)} usernames on dsc.bio")

threads = []
for name in names:
    threads.append(Thread(target=check, args=[name]))
for t in threads:
    t.start()
    sleep(0.2)
    # sleeping to prevent getting ratelimited too much
for t in threads:
    t.join()

print(f"{Fore.GREEN}Done checking.")
print(Fore.RESET)
