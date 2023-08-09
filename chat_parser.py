import xml.etree.ElementTree as ET
import os, glob
import re
import datetime

#### USER SETTINGS ####
BUILD_NAME_MAP = False
BUILD_DATE_FILE = True
BUILD_DATE_YEAR = 2004
BUILD_DATE_MONTH = 4
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
    fname = "build_file_" + str(start_date) + ".xml"
    if(BUILD_MONTH):
        fname = fname[:-7] + ".xml"
    date_file_out = open(fname, "w", encoding='utf-8')
    date_file_out.write('<?xml version="1.0"?>')
    date_file_out.write("<?xml-stylesheet type='text/xsl' href='MessageLog.xsl'?>")
    date_file_out.write('<Log>')
    
for file in glob.glob(os.path.join(path, "*.xml")):
    file_base = file[:-4].split(' ')[0][10:-10]
    #print(file_base)
        
    tree = ET.parse(file)
    root = tree.getroot()
    
    new_file = True
    
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
                    if(BUILD_MONTH):
                        child.attrib["File"] = file_base
                        msg_to_sort.append(child)
                    else:
                        date_file_out.write(ET.tostring(child, encoding='utf-8').decode())
            
if(BUILD_NAME_MAP):     
    for key in name_map.keys() :
        print(str(key) + ":=:" + str(name_map[key]))
        
if(BUILD_DATE_FILE):
    if(BUILD_MONTH):
        extend = False
        for x in range(1,32):
            file_name = ''
            file_change = False
            prev_msg_time = 0
            prev_msg_written = False
            for msg in msg_to_sort[:]:
                if(file_name != msg.attrib["File"]):
                    file_name = msg.attrib["File"]
                    file_change = True
                    prev_msg_time = 0
                msg_time = 24*60*int(msg.attrib["Date"].split('/')[1])
                msg_time += (int(msg.attrib["Time"].split(':')[0])%12)*60
                msg_time += int(msg.attrib["Time"].split(':')[1])
                if(msg.attrib["Time"].split(' ')[1] == "PM"):
                    msg_time += 12*60
                day = msg.attrib["Date"].split('/')[1]
                if x == int(day) or (prev_msg_written and not file_change and (abs(msg_time - prev_msg_time) < 60)) :
                    date_file_out.write(ET.tostring(msg, encoding='utf-8').decode())
                    msg_to_sort.remove(msg)
                    prev_msg_written = True
                else :
                    prev_msg_written = False
                prev_msg_time = msg_time
                file_change = False
    date_file_out.write('</Log>')

