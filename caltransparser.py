import requests
from bs4 import BeautifulSoup
import json
import re

# define the source url
source_url = 'http://www.dot.ca.gov'

#get the html data from source url
page = requests.get(source_url+"/contact-us")

#parse htlm data
soup = BeautifulSoup(page.text, 'html.parser')

#keys
json_tags = ['office_name', 'office_link', 'office_address', 'office_city',
'office_state', 'office_zip', 'office_phone', 'mail_address',
'mail_pobox', 'mail_city', 'mail_state', 'mail_zip', 'mail_phone']

# initialize json schema

def initialize_json_row():
    json_row = dict([(tag,None) for tag in json_tags])
    return json_row

#Convert raw data to json

def row_to_json(row):

    #filter td tags from the row
    cols = row.find_all('td')

    #to exclude unwanted rows
    if(len(cols)==5):
        column_0 = cols[0]
        column_1 = cols[1]
        column_2 = cols[2]
        column_3 = cols[3]
        json_data = initialize_json_row()


        off_nm_link = [info.strip() for info in column_0.text.split("\n")][0].split()

        json_data["office_name"] = re.sub(r'^[^a-zA-Z0-9]*|[^a-zA-Z0-9]*$', '', off_nm_link[0] + " " + off_nm_link[1])
        json_data["office_link"] = source_url if re.sub(r'^[^a-zA-Z0-9]*|[^a-zA-Z0-9]*$', '', off_nm_link[0] + " " + off_nm_link[1]) == 'Headquarters' else source_url + off_nm_link[0].lower().replace('rict', '') + off_nm_link[1]

        office = [i for i in [info.strip() for info in column_1.text.split("\n")] if i]

        json_data["office_address"] = office[0].split(',')[0].strip()
        json_data["office_city"] = office[1].split('CA')[0].split(',')[0].strip()
        json_data["office_state"] = 'CA'
        json_data["office_zip"] = office[1].split('CA')[1].strip()

        phn = [k.strip() for k in column_3.text.split(' ')]
        if len(phn) == 2:
            json_data["office_phone"] = re.sub(r'^[^0-9]*|[^0-9]*$', '', phn[0]) + '-' + [k.strip() for k in column_3.text.split(' ')][1]
        else:
            h_phn = column_3.text.split("\n")[2].strip()
            v_phn = [k.strip() for k in h_phn.split(' ')][0]
            json_data["office_phone"] = re.sub(r'^[^0-9]*|[^0-9]*$', '', v_phn) + '-' + [k.strip() for k in h_phn.split(' ')][1]

        mail_i = [info.strip() for info in column_2.text.split("\n")]
        mail_o = [i for i in mail_i if i]
        if len(mail_o) > 2:
            mail_o.remove('Attn: Public Affairs')

        json_data["mail_address"] = None if len(re.findall('[p|P].+[o|O.]', mail_o[0])) > 0 else mail_o[0].split(',')[0]
        json_data["mail_pobox"] = mail_o[0] if len(re.findall('[p|P].+[o|O.]', mail_o[0])) > 0 else None
        json_data["mail_city"] = mail_o[1].split('CA')[0].strip().strip(',')
        json_data["mail_state"] = 'CA'
        json_data["mail_zip"] = mail_o[1].split('CA')[1].strip()
        json_data["mail_phone"] = None

        return json_data

# method to call row_to_json function

def caltrans_json():
    rows = soup.find_all('tr')
    data = list(filter(lambda row: row is not None ,[row_to_json(row) for row in rows]))
    return data

#print json data

print(json.dumps(caltrans_json(), indent=4))