from discord.ext import commands
import json
import discord
import time
import difflib
import asyncio
import os
import sys
import json ,pprint
import urllib.request

TOKEN = os.environ.get('token')
client_id = "your client_id" 
client_secret = "your client_secret" 
translator = googletrans.Translator()
client = discord.Client()
intents = discord.Intents.default()
intents.members = True
client = commands.Bot(intents=intents, command_prefix='>')

langcode = ['ko', 'en', 'ja', 'zh-CN', 'zh-TW', 'vi', 'id', 'th', 'de', 'ru', 'es', 'it', 'fr']

@client.event
async def on_ready():
    print(client.user.name)
    print("봇 구동 시작")
    game = discord.Game(">info | Translator")

@client.command(aliases=['translate', 'tl', 'trans', 't'])
async def translation(ctx, tonumber):  

    if tonumber in langcode:

        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel

        embed = discord.Embed(title = "Please enter the sentence you want to translate.", color = 0x62c1cc)
        embed.set_footer(text = f"{ctx.message.author.name}", icon_url = ctx.message.author.avatar_url)                 
        await ctx.send(embed = embed)    

        while True:
            sentence = await client.wait_for("message", check=check)
            for i in langcode:
                if sentence.content == ">translation {}".format(i):   
                    break;  
                if sentence.content == ">trans {}".format(i):   
                    break;  
                if sentence.content == ">translate {}".format(i):   
                    break;  
                if sentence.content == ">tl {}".format(i):   
                    break;    
                if sentence.content == ">t {}".format(i):   
                    break;              

            print("translation {}".format(sentence.content))
            if sentence.content == ">stop":          
                embed = discord.Embed(title = "__***The translation mode has ended.***__", 
                                        description = "The translator is turning off.", color = 0x62c1cc)
                embed.set_footer(text = f"{ctx.message.author.name}", icon_url = ctx.message.author.avatar_url)                 
                await ctx.send(embed = embed)
                break

            for fine in langcode: 
                if sentence.content == ">translation {}".format(fine) :
                    await ctx.send("The translator is already running. | ***Change the language.***")
                    return             
                if sentence.content == ">trans {}".format(i):   
                    await ctx.send("The translator is already running. | ***Change the language.***")
                    return  
                if sentence.content == ">translate {}".format(i):   
                    await ctx.send("The translator is already running. | ***Change the language.***")
                    return  
                if sentence.content == ">tl {}".format(i):   
                    await ctx.send("The translator is already running. | ***Change the language.***")
                    return    
                if sentence.content == ">t {}".format(i):   
                    await ctx.send("The translator is already running. | ***Change the language.***")
                    return            

            if sentence.content is not None:

                #언어감지 예제
                data = "query=" + sentence.content
                url = "https://openapi.naver.com/v1/papago/detectLangs" #언어감지 api url
                request = urllib.request.Request(url)
                request.add_header("X-Naver-Client-Id",client_id)
                request.add_header("X-Naver-Client-Secret",client_secret)
                response = urllib.request.urlopen(request, data=data.encode("utf-8"))
                rescode = response.getcode()

                if(rescode==200):
                    response_body = response.read()
                    #print(response_body.decode('utf-8'))
                    trans_text = json.loads(response_body.decode('utf-8'))
                    srclang = trans_text['langCode']           

                else:
                    print("Error Code:" + rescode)
                
                

                url = "https://openapi.naver.com/v1/papago/n2mt" #nmt url
                encText = urllib.parse.quote(sentence.content)
                data = "source={}&target={}&text=".format(srclang, tonumber) + encText

                request = urllib.request.Request(url)
                request.add_header("X-Naver-Client-Id",client_id)
                request.add_header("X-Naver-Client-Secret",client_secret)

                response = urllib.request.urlopen(request, data=data.encode("utf-8"))
                rescode = response.getcode()

                if(rescode==200):
                    response_body = response.read()
                    data = response_body.decode('utf-8')
                    data = json.loads(data)
                    result = data['message']['result']['translatedText']
                    #print(result)
                    embed = discord.Embed(title = "{}".format(result),
                                        description = "Original: {}".format(sentence.content), color = 0x62c1cc)
                    embed.set_footer(text = f"{ctx.message.author.name}", icon_url = ctx.message.author.avatar_url)                 
                    await ctx.send(embed = embed)

                else:
                    print("Error Code:" + rescode)


    else:
        embed = discord.Embed(title = "The sentence is too long or the language code is wrong.", 
                              description = "The translator is turning off.", color = 0x62c1cc)
        embed.set_footer(text = f"{ctx.message.author.name}", icon_url = ctx.message.author.avatar_url)                 
        await ctx.send(embed = embed)



@client.command()
async def info(ctx):
    
    embed = discord.Embed(title = "A very useful translator.", 
            description = "안녕하세요 번역기봇 입니다. \n영어가 잔뜩있어 외국에서 만든것같지만 국산입니다.", color = 0x62c1cc)
    embed.add_field(name="> Commands", value = "**`translation`**, **`translate`**, **`trans`**, **`tl`**, **`t`**, **`stop`**\n\n\n",inline = False)                       
    embed.add_field(name="> How to use", value = "**example:** **`translation en`**, **`tl ja`**, **`t ko`**\nThen Enter the sentence you want to translate.\n\n**example**:\t**`>tl ko`** -> **`hello`** -> **`안녕`**\nIf you want to end it, **`>stop`**\n\n\n",inline = False)
    embed.add_field(name="> Language codes", value = "korean = **`ko`** japanese = **`ja`**, Simplified Chinese = **`zh-cn`**\nTraditional Chinese = **`zh-tw`**\nHindi = **`hi`**, English = **`en`**, Spanish = **`es`**\nFrench = **`fr`**, German = **`de`**, Portuguese = **`pt`**, Vietnamese = **`vi`**\n Indonesian = **`id`**, Persian = **`fa`**, Arabic = **`ar`**, Myanmar = **`mm`**\n Thai = **`th`**, Russian = **`ru`**, Italian = **`it`**\n\n\n",inline = False)
    embed.set_thumbnail(url="https://cdn.discordapp.com/app-icons/928341349223256064/5fb7957f1360c9abf6fb38ddb0f6b0a7.png?size=64")
    embed.set_footer(text = f"{ctx.message.author.name}", icon_url = ctx.message.author.avatar_url)                 
    await ctx.send(embed = embed)

                   
client.run("{}".format(TOKEN), bot=True)   
