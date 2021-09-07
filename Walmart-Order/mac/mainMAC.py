import discord
from discord import webhook
from walmartMAC import *
from input import *
from dotenv import load_dotenv
import datetime
import os

#Loads the .env file for the api key
load_dotenv()

#Creates client and guild object
client = discord.Client()
server = client.get_guild(698382958133772288)

#Skus for walmart
PS5DISK = ['994712501', 'Sony PlayStation 5 Video Game Console']
PS5DIGITAL = ['979738052', 'Sony PlayStation 5, Digital Edition Video Game Consoles']
XBOXX = ['141335186','Xbox Series X']
XBOXXHALO = ['288604110', 'Xbox Series X – Halo Infinite Limited Edition Bundle']
CARDS = ''
skusStellar = []
skusKoi = []

#Logging bot in
@client.event
async def on_ready():
    print(f'Logged in as {client.user}')

#Class that filters and manages the webhooks in a sepcified channel
class Client(discord.Client):
    async def on_ready(self):

        #Asking user for date of webhook/checking validity of user input
        question = 'Please enter the date of the webhook(s) in format: mm/dd/yyyy.'
        userInput = check_user_input(question, is_date = True)
        
        userInput = userInput.replace('/','')
        year = userInput[4:]
        month = userInput[:2]
        day = userInput[2:4]

        #Asking User to speicify channel
        webhookChannels = []
        guild = client.get_guild(698382958133772288)
        successCategory = discord.utils.get(guild.categories, id=753697996729745499)
        channels = successCategory.channels
        for channel in channels:
            if channel.name != 'success' and channel.name != 'mates-public-log':
                webhookChannels.append(channel)
        for number, channel in enumerate(webhookChannels):
            print(number, channel.name)

        #Checking validity of user input
        question = 'Enter number of the channel where the webhook(s) are.'
        range = (0, len(webhookChannels))
        userInput = check_user_input(question, in_range=range)
        
        channel = webhookChannels[userInput]
    
            

        #Asking user to specify skus to test for product
        question = "Check for PS5 Disk? Y/N"
        yes = check_user_input(question, y_or_n=True)
        if yes:
            skusStellar.append(PS5DISK[0])
            skusKoi.append(PS5DISK[1])
                
        
        question = "Check for PS5 Digital? Y/N"
        yes = check_user_input(question, y_or_n=True)
        if yes:
            skusStellar.append(PS5DIGITAL[0])
            skusKoi.append(PS5DIGITAL[1])
        
        question = "Check for Xbox X? Y/N"
        yes = check_user_input(question, y_or_n=True)
        if yes:
            skusStellar.append(XBOXX[0])
            skusKoi.append(XBOXX[1])
        
        question = "Check for Xbox X - Halo Edition? Y/N"
        yes = check_user_input(question, y_or_n=True)
        if yes:
            skusStellar.append(XBOXXHALO[0])
            skusKoi.append(XBOXXHALO[1])
        

        #Using user date to find day before and after
        beforeDate = datetime.datetime(int(year), int(month), int(day) + 1, hour=4)
        afterDate = datetime.datetime(int(year), int(month), int(day) - 1, hour=4)

        #Getting the webhhoks from the specified date
        messages = await channel.history(limit=500, before=beforeDate, after=afterDate).flatten()
        koi = 0
        #Filtering messages and getting fields
        contentList = []
        for msg in messages:
            
            #Checking if author is StellarAIO
            if str(msg.author) == 'StellarAIO Checkout#0000':

                #Checking if skus are in embed
                for s in skusStellar:

                    if f"name='Sku', value='{s}'" in str(msg.embeds[0].fields) and len(msg.embeds[0].fields) == 11:

                        #Getting specific fields and cleaning up string
                        user = str(msg.embeds[0].fields[7].value.replace('||', ''))
                        content = []
                        content.append(user)
                        email = str(msg.embeds[0].fields[9].value.replace('||', ''))
                        content.append(email)
                        password = str(msg.embeds[0].fields[10].value.replace('||', ''))       
                        content.append(password)
                        orderNum = str(msg.embeds[0].fields[8].value.replace('||', ''))
                        content.append(orderNum)
                        contentList.append(content)
            
            #Checking if author is KoiAIO
            if str(msg.author) != 'StellarAIO Checkout#0000':

                try:
                    test = msg.embeds[0].fields[3]          
                except:
                    pass
                else:
                    if str(test.value.replace('||', '')) == 'Auto-Gen' and msg.embeds[0].title == 'Koi AIO | Checkout Successful':
                       
                       for s in skusKoi:

                           if str(msg.embeds[0].fields[1].value.replace('||', '')) == s:

                                #Getting specific fields and cleaning up string
                                user = str(msg.embeds[0].fields[6].value.replace('||', ''))
                                content = []
                                content.append(user)
                                email = str(msg.embeds[0].fields[8].value.replace('||', ''))
                                content.append(email)
                                password = str(msg.embeds[0].fields[9].value.replace('||', ''))       
                                content.append(password)
                                orderNum = str(msg.embeds[0].fields[10].value.replace('||', ''))
                                content.append(orderNum)
                                contentList.append(content)
        
        #Calling walmart order checker function
        checkedOrders = walmartOrderTracker(contentList)

        #Calling spreadsheet creator function
        csvFile = csvCreate(checkedOrders[0], checkedOrders[1], checkedOrders[2])
        print('walmartAccount.csv was saved to application folder.')
        await self.close()

#Running program
client = Client()
client.run(os.getenv('TOKEN'))
