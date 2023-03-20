import discord
from config import settings
import datetime
from asyncio import run_coroutine_threadsafe
import asyncio
import threading
from time import sleep
mentionFlag = threading.Event()
screamingFlag = threading.Event()
mentionFlag.set()
intents = discord.Intents.all()
def screamingThread():
    from pygame import mixer 
    mixer.init()
    mixer.music.load(settings["audioPath"])
    while(True):
        screamingFlag.wait()
        time = datetime.datetime.isoformat(datetime.datetime.now(),timespec="seconds")
        print(f"        started screaming ({time})")
        while(screamingFlag.is_set()):
            mixer.music.play()
            time = datetime.datetime.isoformat(datetime.datetime.now(),timespec="seconds")
            print(f"        screamed ({time})",end="\r")
            sleep(settings["screamInterval"])
screamThread = threading.Thread(target=screamingThread, daemon=True)

async def reaction_coro(message):
    await message.clear_reaction("👀")
    await message.add_reaction("✅")
    mentionFlag.set()
def inputThread(message,loop):
    print("    Waiting your response")
    screamingFlag.set()
    input()
    time = datetime.datetime.isoformat(datetime.datetime.now(),timespec="seconds")
    print(f"    Response ({time})")
    screamingFlag.clear()
    run_coroutine_threadsafe(reaction_coro(message),loop)

class MyClient(discord.Client):
    def usersToNicknames(user, usersList):
        nicknames = []
        for user in usersList:
            nicknames.append(user.name)
        print(nicknames)
        return nicknames
    async def on_message(self,message): 
        if(mentionFlag.is_set() and message.mentions!=[] and settings["username"] in self.usersToNicknames(message.mentions)):
            print(f"\n({datetime.datetime.now()}) PINGED by {message.author} with text: {message.content}")
            mentionFlag.clear()
            await message.add_reaction("👀")
            thread = threading.Thread(target=inputThread,args=[message,asyncio.get_event_loop()])
            thread.start()
            
myClient = MyClient(intents=intents)
screamThread.start()
myClient.run(settings['token'])

"""
    1. Response spam fix ✓
    2. Change userID to nicknames ✓
    3. Change  bot for regular client ☓
"""
