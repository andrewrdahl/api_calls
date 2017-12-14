import json
import urllib.request
import urllib
import datetime
import requests

def get_qwi():
    output = open('data_census_qwi.txt','w')
    URL_base = 'https://api.census.gov/data/timeseries/qwi/rh?'
    variables = 'get=Emp'
    geographies = '&for=workforce+investment+area:SDA100&in=state:27'
    startyear = '&time=from+2015+to+'
    currentyear = datetime.date.today().year
    races = '&race=A0'
    ethnicities = '&ethnicity=A0'
    industries = makeindustriesstring()
    api_key = '&key=9ae00c2db5c1bafe8af93f69a11b8a263899a930'

    URLpath = URL_base + variables + geographies + startyear + str(currentyear) + races + ethnicities + industries + api_key

    data = urllib.request.urlopen(URLpath)
    data = data.read()
    data = data.decode()
    json_data = json.loads(data)
    return json_data
    output.close()

def makeindustriesstring():
    industries = ''
    allindustries = urllib.request.urlopen('https://lehd.ces.census.gov/data/schema/latest/label_industry.csv')
    for line in allindustries.readlines():
        line = line.decode()
        line = line.split(',')
        if len(str(line[0])) == 4:
            industries += '&industry=' + str(line[0])
    return industries

def main():
    print(get_qwi())

if __name__ == '__main__':
    main()
