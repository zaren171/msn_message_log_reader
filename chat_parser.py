import xml.etree.ElementTree as ET
import os, glob
import re
import datetime

#### USER SETTINGS ####
BUILD_NAME_MAP = False
BUILD_DATE_FILE = True
BUILD_DATE_YEAR = 2006
BUILD_DATE_MONTH = 6
BUILD_DATE_DAY = 0
#######################

BUILD_MONTH = False

if(BUILD_DATE_DAY == 0):
    BUILD_MONTH = True
    BUILD_DATE_DAY = 1
    
start_date = datetime.date(BUILD_DATE_YEAR, BUILD_DATE_MONTH, BUILD_DATE_DAY)
if(BUILD_MONTH):
    end_date = datetime.date(BUILD_DATE_YEAR, BUILD_DATE_MONTH + 1, BUILD_DATE_DAY)
else:
    end_date = datetime.date(BUILD_DATE_YEAR, BUILD_DATE_MONTH, BUILD_DATE_DAY + 1)


path = "chat_logs"
dup_check = []
msg_to_sort = []
name_map = {}

global date_file_out
if(BUILD_DATE_FILE):
    date_file_out = open("date_file_"+str(start_date)+".xml", "w", encoding='utf-8')
    date_file_out.write('<?xml version="1.0"?>')
    date_file_out.write("<?xml-stylesheet type='text/xsl' href='MessageLog.xsl'?>")
    date_file_out.write('<Log>')
    
for file in glob.glob(os.path.join(path, "*.xml")):
    file_base = file[:-4].split(' ')[0][10:-10]
    #print(file_base)
        
    tree = ET.parse(file)
    root = tree.getroot()
    
    if(BUILD_NAME_MAP):
        for child in root:
            if "Message" in child.tag :
                if child[0][0].attrib["FriendlyName"] in name_map :
                    name_map[child[0][0].attrib["FriendlyName"]].add(file_base)
                else :
                    name_map[child[0][0].attrib["FriendlyName"]] = {file_base}
                    
    if(BUILD_DATE_FILE):
        for child in root:
            if "Message" in child.tag :
                date = child.attrib["Date"].split('/')
                message_date = datetime.date(int(date[2]), int(date[0]), int(date[1]))
                if(message_date >= start_date and message_date < end_date):
                    #print(ET.tostring(child, encoding='utf-8'))
                    if(BUILD_MONTH):
                        msg_to_sort.append(child)
                    else:
                        date_file_out.write(ET.tostring(child, encoding='utf-8').decode())
            
if(BUILD_NAME_MAP):     
    for key in name_map.keys() :
        print(str(key) + ":=:" + str(name_map[key]))
        
if(BUILD_DATE_FILE):
    if(BUILD_MONTH):
        for x in range(1,32):
            for msg in msg_to_sort:
                day = msg.attrib["Date"].split('/')[1]
                if x == int(day):
                    date_file_out.write(ET.tostring(msg, encoding='utf-8').decode())
    date_file_out.write('</Log>')

