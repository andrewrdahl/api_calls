import json
import urllib.request
import urllib
import datetime
import requests

def get_qwi():
    output = open('data_census_qwi.txt','w')
    URL_base = 'https://api.census.gov/data/timeseries/qwi/rh?'
    variables = 'get=Emp,EmpEnd,EmpS,HirA,Sep,EarnS,EarnHirNS,race,ethnicity'
    startyear = '&time=from+2015+to+'
    currentyear = datetime.date.today().year
    industries = makeindustriesstring()
    api_key = '&key=9ae00c2db5c1bafe8af93f69a11b8a263899a930'
    geographies = [
    '&for=workforce+investment+area:SDA100,SDA090,SDA150&in=state:27',
    '&for=metropolitan+statistical+area/micropolitan+statistical+area:33460&in=state:27'
    ]
    geo_labels = {'SDA100':'City of Minneapolis WSA','SDA090':'Hennepin/Carver WSA','SDA150':'Ramsey County WSA','33460':'Minneapolis-St. Paul-Bloomington, MN-WI (MN part)'}
    race_dict = makeracedict()
    ethnicity_dict = makeethnicitydict()
    industry_dict = makeindustrydict()

    for g in geographies:
        thisgeo = str(g)
        URLpath = URL_base + variables + thisgeo + startyear + str(currentyear) + industries + api_key

        data = urllib.request.urlopen(URLpath)
        data = data.read()
        data = data.decode()
        json_data = json.loads(data)
        for line in json_data[1:]:
            Emp = str(line[0])
            EmpEnd = str(line[1])
            EmpS = str(line[2])
            HirA = str(line[3])
            Sep = str(line[4])
            EarnS = str(line[5])
            EarnHirNS = str(line[6])
            race = str(line[7])
            ethnicity = str(line[8])
            year = str(line[9][0:4])
            quarter = str(line[9][-2:])
            industry = str(line[10])
            state = str(line[11])
            area = str(line[12])
            area_label = geo_labels[str(line[12])]
            output.write(area + ',' + year + ',' + quarter + ',' + race + ',' + ethnicity + ',' + industry + ',' + Emp + ',' + EmpEnd + ',' + EmpS + ',' + HirA + ',' + Sep + '\n')
    output.close()
    print(race_dict)
    print(ethnicity_dict)

def makeindustriesstring():
    industries = ''
    allindustries = urllib.request.urlopen('https://lehd.ces.census.gov/data/schema/latest/label_industry.csv')
    for line in allindustries.readlines():
        line = line.decode()
        line = line.split(',')
        if len(str(line[0])) == 4 and line[0].isnumeric():
            industries += '&industry=' + str(line[0])
    return industries

def makeindustrydict():
    industry_dict = {}
    industry_list = urllib.request.urlopen('http://lehd.ces.census.gov/data/schema/latest/label_industry.csv')
    for line in industry_list.readlines():
        line = line.decode()
        line = line.split(',')
        industry_dict[line[0]]=line[1].replace('\n','').replace('"','')
    return industry_dict

def makeracedict():
    race_dict = {}
    racelist = urllib.request.urlopen('https://lehd.ces.census.gov/data/schema/latest/label_race.csv')
    for line in racelist.readlines():
        line = line.decode()
        line = line.split(',')
        race_dict[line[0]]=line[1].replace('\n','').replace('"','')
    return race_dict

def makeethnicitydict():
    ethnicity_dict = {}
    ethnicitylist = urllib.request.urlopen('https://lehd.ces.census.gov/data/schema/latest/label_ethnicity.csv')
    for line in ethnicitylist.readlines():
        line = line.decode()
        line = line.split(',')
        ethnicity_dict[line[0]]=line[1].replace('\n','').replace('"','')
    return ethnicity_dict

def main():
    print(makeindustrydict())

if __name__ == '__main__':
    main()
