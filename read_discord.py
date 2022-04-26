import discord
from pygame import mixer
from gtts import gTTS
from bot_config import DISCORD_API_KEY

from util.ParseUbereats import parse_ubereats_receipt
from util.ParseUbereats import parse_ubereats_url

client = discord.Client()

@client.event
#當機器人完成啟動時
async def on_ready():
    print('目前登入身份：', client.user)

@client.event
#當有訊息時
async def on_message(message):

    # The text that you want to convert to audio
    mytext = ''
    restaurant = ''

    if message.content.find("https://eats.uber.com/") != -1:
        parseMessage = ''
        try:
            if len(message.embeds) > 0:
                parseMessage = message.embeds[0].title
            else:
                parseMessage = parse_ubereats_url(message.content.split('\n')[1])

            if parseMessage.split('在')[0] == parseMessage:
                restaurant = parseMessage.split('from')[1].split('|')[0]
            else:
                restaurant = parseMessage.split('在')[1].split('的')[0]

            mytext = str(message.author.nick) + '準備要來訂 Uber Eats 的' + restaurant + '！你各位要訂的快點看Discord。'

        except Exception as e:
            mytext = str(message.author.nick) + '準備要來訂 Uber Eats！你各位要訂的快點看Discord。'

    elif message.content.find("https://foodpanda.page.link/") != -1:
        parseMessage = ''
        if len(message.embeds) > 0:
            parseMessage = message.embeds[0].title
            restaurant = parseMessage.split('menu')[0]
            mytext = str(message.author.nick) + '準備要來訂 foodpanda 的' + restaurant + '！你各位要訂的快點看Discord。'
        else:
            mytext = str(message.author.nick) + '準備要來訂 foodpanda 了！你各位要訂的快點看Discord。'

    elif message.content.find("廣播 ") != -1:
        mytext = str(message.author.nick) + '說' + message.content.split("廣播 ")[1]

    elif message.content.find("悄悄話 ") != -1:
        mytext = message.content.split("悄悄話 ")[1]
        await message.delete()

    if str(message.attachments) != "[]": # If there is it gets the filename from message.attachments
        split_v1 = str(message.attachments).split("filename='")[1]
        filename = str(split_v1).split("' ")[0]
        if filename.find("Receipt") != -1: # Checks if it is a UberEats_Receipt file
            try:
                await message.attachments[0].save(fp="Receipt/{}".format("ubereats-receipt.pdf")) # saves the file
                receipt_message = parse_ubereats_receipt()
                print(receipt_message['message'])
                await message.channel.send(receipt_message['message'])
                mytext = receipt_message['restaurant'] + '的錢已經在discord上了喔，大家記得付錢給' + str(message.author.nick)
                await message.delete()
            except Exception as e:
                mytext = 'UberEats的錢已經在discord上的副檔了喔，大家記得付錢給' + str(message.author.nick)


    if mytext != '':
        # Log Message
        print(mytext)
        # Language in which you want to convert
        language = 'zh-tw'

        # Passing the text and language to the engine,
        # here we have marked slow=False. Which tells
        # the module that the converted audio should
        # have a high speed
        myobj = gTTS(text=mytext, lang=language, slow=False)

        # Saving the converted audio in a mp3 file
        myobj.save("read_sentance.mp3")

        # Play the audio
        mixer.init()
        mixer.music.load('read_sentance.mp3')
        mixer.music.play()

client.run(DISCORD_API_KEY)
