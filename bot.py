  
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
        await self.form_fill_out(message)

    async def vote(self, message):
        # if sender has never created a form
        if message.author.id not in forms:
            temp = {message.author.id: [Form(message.author.id)]}
            temp2 = {message.author.id: False} # the 0 represents the form that will need to be filled out
            forms.update(temp)
            inprogress.update(temp2)
        elif inprogress[message.author.id] == False:
            # if the sender has made a form before, but doesn't have a form going
            forms[message.author.id].append(Form(message.author.id))
        
        # if the sender already has a form going
        if inprogress[message.author.id] == True:
            await message.author.send('You already have a vote form in progress. Please finish it or cancel it by sending the :x: emoji.')
            return

        
        
        inprogress[message.author.id] = True
        await message.author.send("Let's begin :smile:\n\nIf at any point you would like to cancel the form, please send the :x: emoji.")

        # grab the form that is incomplete and continue off point that hasn't been filled out
        for form in forms:
            for array in forms[form]:
                if array.completed == True:
                    continue
                for info in array.story_details:
                    if array.story_details[info] == '':
                        await message.author.send(f'{info.title()} (if this doesn\'t exist, please message a :no_entry_sign: emoji):')
                        break

    
    # handles where the sender is in the form process as well as cancelling form if user wants that
    async def form_fill_out(self, message):
        
        if await self.dm_chat(message):
            # grab most recent message from user and bot

            if message.author.id == self.user.id:
                return

            # if the user responds with an x emoji we cancel the form... eventually when I add that in
            if message.content == ':x:':
                return
            
            # if it's from the user then we want to store that answer
            # after that we want to ask the next question if there exist one
            # otherwise we mark the form as completed and mark inprogress as false
            for form in forms:
                for array in forms[form]:
                    if array.completed == True:
                        continue
                    next_blank = False
                    for info in array.story_details:
                        if next_blank == True:
                            await message.author.send(f'{info.title()} (if this doesn\'t exist, please message a :no_entry_sign: emoji):')
                            return
                        if array.story_details[info] == '':
                            array.story_details[info] = message.content
                            next_blank = True # now that we have filled in this blank, we need to prompt the user for the next item to fill out
                            if info == 'length':
                                array.completed = True
                                inprogress[message.author.id] = False
                                await message.author.send('Thank you for filling out this request :smile: Your request will be reviewed soon :nerd:')
                                
    async def dm_chat(self, message):
        return isinstance(message.channel, discord.DMChannel)
            
            
        



client = MyClient()

client.run(os.getenv('token'))
