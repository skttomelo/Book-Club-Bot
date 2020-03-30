  
from dotenv import load_dotenv
from pathlib import Path
from data import Form
import os
import discord

# get env
env_path = Path('.') / 'config.env'
load_dotenv(dotenv_path=env_path)

forms = {}
inprogress = {}

class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged on as', self.user)

    async def on_message(self, message):
        # don't respond to ourselves but we do need to know where are in the form
        if message.author == self.user:
            return
        if message.content == '!vote':
            await self.vote(message)
            return
        # await dm_chat(message)

    async def vote(self, message):
        # if sender has never created a form
        if message.author.id not in forms:
            temp = {message.author.id: [Form(message.author.id)]}
            temp2 = {message.author.id: False} # the 0 represents the form that will need to be filled out
            forms.update(temp)
            inprogress.update(temp2)

        # if the sender already has a form going
        if inprogress[message.author.id] == True:
            await self.send('You already have a vote form in progress. Please finish it or cancel it using the :x: emoji.')
            return
        
        inprogress[message.author.id] = True
        await message.author.send("Let's begin :smile:\n")

        # grab the form that is incomplete and continue off point that hasn't been filled out
        for form in forms:
            for array in forms[form]:
                if array.completed == True:
                    continue
                for info in array.story_details:
                    if array.story_details[info] == '':
                        await message.author.send(f'{info.title()} (if this doesn\'t exist, please use a :no_entry_sign: emoji):')
                        break

    
    # handles where the sender is in the form process as well as cancelling form if user wants that
    async def form_fill_out(self, message):
        pass
    

    async def dm_chat(self, message):
        if isinstance(message.channel, discord.DMChannel):
            pass
            
            
        



client = MyClient()

client.run(os.getenv('token'))
