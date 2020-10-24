from src import WhatsAPIDriver
from src.objects.message import Message
import time
import datetime
import sys
import re

# For file logging...\n
logFile=open("send_to_contacts.txt", "a")
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
userChat=[]
for i in allChats:
    if 'User chat' in str(i):
            userChat.append(i)
groupChats=[]
for i in allChats:
    if 'User chat' not in str(i):
            groupChats.append(i)
logFile.write("Send to groups : 0\n")
logFile.write("Send to all chats : 1\n")
print("Excluded groups/broadcast from chat list...\n")
logFile.write("Excluded following groups/broadcast from chat list...\n")

for i in groupChats:
    
    logFile.write(re.sub('chat.*?us','chat - Name Protected',str(i),flags=re.DOTALL))
    logFile.write("\n")

# Sending media (Documents)
filePath=str(input("Enter path to media file : "))
print("File selected to be sent : ", filePath)
logFile.write("File selected to be sent : ")
logFile.write(filePath) 
logFile.write(" ,this log file...\n")

for i in range(len(userChat)): 
    try:
        phone=re.search(': (.*)@c.us', str(userChat[i])).group(1)
        phone_whatsapp = "{}@c.us".format(phone) # WhatsApp Chat ID
        caption = "Testing a media sender!"
        driver.send_media(filePath, phone_whatsapp, caption)
        driver.chat_send_message(phone_whatsapp, caption)
        print("Media file was successfully sent to {}".format(phone))
        
    except:
        print("Error while trying to send the midia file.")

# Closing logFle
logFile.close()