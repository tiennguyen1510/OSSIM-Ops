import sys

# Standard for CSV for AlienVault OSSIM
title_file = '"IPs";"Hostname";"FQDNs";"Description";"Asset Value";"Operating System";"Latitude";"Longitude";"Host ID";"External Asset";"Device Type"'

file_csv = "serverlist.csv"

# parse format like csv of AlienVault
# "172.104.187.187,192.168.138.194";"WOW-PROD-SERVER14";"";"";"2";"Linux";"";"";"F43AB887BA84DFDF61B11D4AA37ED044";"0";""
format_line = ["","","","","2","Linux","","","","0",""]

def convert(ip, domain):
    format_line[0] = ip
    format_line[1] = domain
    line = '";"'.join(format_line)
    return '"' + line + '"'

def handle(file_location):
    string = ""
    with open(file_location) as file:
        for line in file:
            line = line.split("\t")
            ip = line[2] + "," + line[1]
            domain = line[0]
            string = string + "\n" + str(convert(ip, domain))
        return string

# Location path to format csv
del sys.argv[0]
for file in sys.argv:
    title_file += handle(file)
    
f = open(file_csv, "w")
f.write(title_file)
f.close()