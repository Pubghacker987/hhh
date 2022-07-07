
from dis import pretty_flags
import os
from pyrogram import Client, filters
from sqlalchemy import outerjoin
from bot.helpers.utils import CustomFilters
from bot.helpers.downloader import download_file, utube_dl
from bot.helpers.gdrive_utils import GoogleDrive
from bot import DOWNLOAD_DIRECTORY, LOGGER
from bot.config import Messages, BotCommands
from subprocess import call, check_output
from pytz import timezone 
from datetime import datetime
import json
from urllib.request import urlopen
from pyrogram import Client, filters
import PTN



def getTitle(title, audio):
    ottList = ['AMZN', 'NF', 'DSNP', 'Tamil TV Toons', 'DSCV', 'DSNP+', 'TATAPLAY', 'LG', 'LGP', 'Voot', 'VootKids', 'HMAX']
    completeTitle = ""
    groupTitle = "AtoZCartoonist"
    title = title.replace(" ", ".")
    data = PTN.parse(title)

    completeTitle += "[" + groupTitle + "]" + " "
    type = ""

    if "season" not in data:
        type += "Movie"

    if type == "Movie":
        if "title" in data:
            completeTitle += data['title'] + ""
    else:
        if "title" in data:
            completeTitle += data['title'] + " - "

      
    if "season" in data:
        if data['season'] < 9:
            completeTitle += "S" + str('0') + str(data['season'])
        else:
            completeTitle += "S" + str(data['season']) 
    else:
        type += "Movie"

    if type != "Movie":
        if "episode" in data:
            if data['episode'] < 9:
                completeTitle += "E" + str('0') + str(data['episode'])  + " - "
            else:
                completeTitle += "E" + str(data['episode'])  + " - "
        else:
            completeTitle += ""

    
    
    if type == "Movie":
        completeTitle += ""

    else:
        if str(data['excess'][0]).startswith('Series'):
            completeTitle += data['excess'][1].replace("." , " ")  + " "
        elif str(data['excess'][0]).startswith('Shorts'):
            completeTitle += data['excess'][1].replace("." , " ")  + " "
        else:
            completeTitle += data['excess'][0].replace("." , " ")  + " "
        

    

    if "resolution" in data:
        completeTitle += "[" + data['resolution'] + "] HEVC 10bit"  + " "
    else: 
        completeTitle += ""  
   

    

    completeTitle += "[" + audioListTitle(audio) + "]" + " "
    if "ESub" in title.replace(".", " "):
        completeTitle += "ESub"
    if "MSub" in title.replace(".", " "):
        completeTitle += "MSubs"

    for i in ottList:
        if i in completeTitle:
            completeTitle += completeTitle.replace(i , "")



    return completeTitle




def isolang(data):
  url = "https://pastebin.com/raw/SYfRPYDY"
  response = urlopen(url)
  data_json = json.loads(response.read())
  arr = []
  for i in data_json:
    if data == i['alpha3-b']:
      c = i["English"]
      arr.append(c)
  return arr[0]   



def audioListTitle(data):
  string = ""
  for i in data:
    string += f'{isolang(i)}-' 
  return string[:-1]
  





def ffpb(filepath):
    output = check_output(['ffprobe', filepath ,'-show_entries', 'stream=index:stream_tags=language', '-select_streams', 'a', '-of' , 'compact=p=0:nk=1'])
    return output.decode('utf-8')





def isocode(data):
  url = "https://pastebin.com/raw/SYfRPYDY"
  response = urlopen(url)
  data_json = json.loads(response.read())
  language = data
  arr = []
  for i in data_json:
    a = i
    if language == a['English']:
      data = a['alpha3-b']
      arr.append(data)  
  return arr[0]  



def audioStreamsList(filepath):
  ffprobeJson = ffpb(filepath).split()
  arr = []
  # 0|hin
  for i in ffprobeJson:
    arr.append(i[-3:])
  return arr 



def isolang(data):
  url = "https://pastebin.com/raw/SYfRPYDY"
  response = urlopen(url)
  data_json = json.loads(response.read())
  arr = []
  for i in data_json:
    if data == i['alpha3-b']:
      c = i["English"]
      arr.append(c)
  return arr[0]     


def rearrangeAudio(orignalList):
  arr = []
  priority = ['hin', 'tam', 'tel', 'mal' , 'kan', 'mar', 'ben', 'ori', 'guj', 'asm', 'pan' , 'eng']

  for i in priority:
    if i in orignalList:
      arr.append(i)
    else:
      pass
  return arr    






def mux(filepath, audioList):
    try:

      basefilepath, extension = os.path.splitext(filepath)
      orgFileName = os.path.basename(basefilepath)
      
      f = open("./settings.txt", "r")
      setting = f.read()

      output_filepath = ""

      if setting == "NO":
        output_filepath += orgFileName + "AtoZCartoonist" + ".mkv"
      elif setting == "YES":
        output_filepath += getTitle(orgFileName , audioList).rstrip() + ".mkv"

      language = ""

      for i in audioList:
        language += f'-map 0:a:m:language:{i} '


      video_opts = "-map 0:v:0"
    
      copy_opts = "-map 0:s? -c copy -strict experimental -disposition:a:0 default "

      add_opts = '-metadata:s:a title=AtoZCartoonist -metadata:s:v:0 title=AtoZCartoonist'
      
      out = call(['ffmpeg', '-i', filepath] + video_opts.split() + language.split() + copy_opts.split() + add_opts.split() + [output_filepath])
      os.remove(filepath)
      return output_filepath
    except Exception as e:
      return


@Client.on_message(filters.private & filters.incoming & filters.text & (filters.command(BotCommands.Audio_Arrange)) & CustomFilters.auth_users)
def _arrangeAudio(client, message):
    user_id = message.from_user.id
    if not message.media: 
        sent_message = message.reply_text('🕵️**Checking link...**', quote=True)
        if message.command:
            link = message.command[1]
        else:
            link = message.text

        link = link.strip()
        filename = os.path.basename(link)
        dl_path = DOWNLOAD_DIRECTORY
        LOGGER.info(f'Download:{user_id}: {link}')
        sent_message.edit(Messages.DOWNLOADING.format(link))
        result, file_path = download_file(link, dl_path)

        if result == True:
          sent_message.edit(f"**Muxing...\n\nPlease Wait**")
            

          new_file = mux(file_path, rearrangeAudio(audioStreamsList(file_path)))
          if new_file:
              sent_message.edit("**Muxed Successfully**")
              sent_message.edit("**Uploading...**")
              msg = GoogleDrive(user_id).upload_file(new_file)
              sent_message.edit(msg)
              LOGGER.info(f'Deleteing: {file_path}')
              os.remove(new_file)


        else:
            sent_message.edit(
            Messages.DOWNLOAD_ERROR.format(file_path, link))

