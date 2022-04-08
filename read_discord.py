import discord
from pygame import mixer
from gtts import gTTS
from bot_config import DISCORD_API_KEY

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
        # if cmp(message.embeds[0].title.split('在')[0], message.embeds[0].title):
        if message.embeds[0].title.split('在')[0] == message.embeds[0].title:
            restaurant = message.embeds[0].title.split('from')[1].split('|')[0]
        else:
            restaurant = message.embeds[0].title.split('在')[1].split('的')[0]
        mytext = str(message.author.nick) + '準備要來訂 Uber Eats 的' + restaurant + '！你各位要訂的快點看Discord。'

    elif message.content.find("https://foodpanda.page.link/") != -1:
        restaurant = message.embeds[0].title.split('menu')[0]
        mytext = str(message.author.nick) + '準備要來訂 foodpanda 的' + restaurant + '！你各位要訂的快點看Discord。'

    elif message.content.find("廣播 ") != -1:
        mytext = 'M U I lab的各位！Oops！' + str(message.author.nick) + '想要宣布：' + message.content.split("廣播")[1]

    elif message.content.find("悄悄話 ") != -1:
        mytext = message.content.split("廣播")[1]

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
