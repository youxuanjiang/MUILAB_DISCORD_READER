#導入 Discord.py
import discord
from pygame import mixer
#client 是我們與 Discord 連結的橋樑
client = discord.Client()

#調用 event 函式庫
@client.event
#當機器人完成啟動時
async def on_ready():
    print('目前登入身份：', client.user)

@client.event
#當有訊息時
async def on_message(message):
    #排除自己的訊息，避免陷入無限循環
    if message.author == client.user:
        return

    # Import the required module for text
    # to speech conversion
    from gtts import gTTS

    # The text that you want to convert to audio
    mytext = str(message.author.nick) + '說' + message.content
    print(mytext)

    # Language in which you want to convert
    language = 'zh-tw'

    # Passing the text and language to the engine,
    # here we have marked slow=False. Which tells
    # the module that the converted audio should
    # have a high speed
    myobj = gTTS(text=mytext, lang=language, slow=False)

    # Saving the converted audio in a mp3 file
    myobj.save("welcome1.mp3")

    # Play the audio
    mixer.init()
    mixer.music.load('welcome1.mp3')
    mixer.music.play()

client.run('OTYxNTcxOTkxMzIyNzc1NTcz.Yk67sw.FFy2fJFkfSfs3s08DMvSWiAlHgA')
