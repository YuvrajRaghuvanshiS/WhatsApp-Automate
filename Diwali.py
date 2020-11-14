from src import WhatsAPIDriver
from src.objects.message import Message
import time
import datetime
import sys
import re

# For file logging...\n
logFile=open("diwali.txt", "a")
logFile.write("\n\n\n===========================\n")
logFile.write(str(datetime.datetime.now()))
logFile.write("\n===========================\n\n")
logFile.write("Initiating\n")

driver = WhatsAPIDriver(loadstyles=False)
logFile.write("Waiting for QR...\n")
print('Waiting for QR...\n')

driver.wait_for_login()
while(driver.get_status() != 'LoggedIn'):
    time.sleep(3)
    print("Waiting 3 seconds to get Logged In...\n")
    logFile.write("Waiting 3 seconds to get Logged In...\n")
    continue


print("Bot online...\n")
logFile.write("Bot online...\n")

# get all contacts...
print("Getting list of chats...\n")
logFile.write("Getting list of chats...\n")
allChats = driver.get_all_chats()

#Excluding group chats.
print("Extracting user chats...\n")
logFile.write("Extracting user chats...\n")
allUserChat=[]
for i in allChats:
    if 'User chat' in str(i):
            allUserChat.append(i)

# Excluding unsaved numbers...
print("Taking only saved contacts...\n")
logFile.write("Taking only saved contacts...\n")
savedUserChat=[]
for i in allUserChat:
    if "empty" not in str(i):
        savedUserChat.append(i)


# Sending image
filePath=str(input("Enter path to media file : "))
print("File selected to be sent : ", filePath)
logFile.write("File selected to be sent : ")
logFile.write(filePath) 

# Caption
totalMessages = len(savedUserChat)

for i in range(totalMessages): 
    try:
        phone=re.search(': (.*)@c.us', str(savedUserChat[i])).group(1)
        phone_whatsapp = "{}@c.us".format(phone) # WhatsApp Chat ID
        # Appending Sir/Ma'am to caption if that's in name.
        if "Sir" in str(savedUserChat[i]):
            caption = "Happy Diwali " + re.findall('[A-Z][a-z]\w+',str(savedUserChat[i]))[1] + " Sir\nPS sorry for missing out any salutations I do respect you but it's hard to convey via Python, I selected only first name to make it more personalized...\n-Yuvraj\n" + str(i) + "\\" + str(totalMessages)
        elif "Ma'am" in str(savedUserChat[i]):
            caption = "Happy Diwali " + re.findall('[A-Z][a-z]\w+',str(savedUserChat[i]))[1] + " Ma'am\nPS sorry for missing out any salutations I do respect you but it's hard to convey via Python, I selected only first name to make it more personalized...\n-Yuvraj\n" + str(i) + "\\" + str(totalMessages)
        else : 
            caption = "Happy Diwali " + re.findall('[A-Z][a-z]\w+',str(savedUserChat[i]))[1] + " bro... or IDK sis I really can't ditinguish between genders via script LoL...\nPS sorry for missing out salutations I do respect you but it's hard to convey via Python, I selected only first name to make it more personalized...\n-Yuvraj Raghuvanshi.\n" + str(i) + "\\" + str(totalMessages)
        driver.send_media(filePath, phone_whatsapp, caption)
        #driver.chat_send_message(phone_whatsapp, caption)
        print(i + "\\" + totalMessages + " : Media file was successfully sent to {}".format(phone))
        logFile.write(i + "\\" + totalMessages + " : Media file was successfully sent to {}".format(phone))
        
    except:
        print(str(i) + "\\" + str(totalMessages) + " : Error while trying to send the media file to " + re.findall('[A-Z][a-z]\w+',str(savedUserChat[i]))[1])
        logFile.write(str(i) + "\\" + str(totalMessages) + " : Error while trying to send the media file to " + re.findall('[A-Z][a-z]\w+',str(savedUserChat[i]))[1])

# Closing logFle
logFile.close()