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
    race_dict = makeracedict()
    ethnicity_dict = makeethnicitydict()
    industry_dict = makeindustrydict()
    geo_dict = makegeographydict()
    # API keys can be registered at https://api.census.gov/data/key_signup.html
    api_key = '&key=9ae00c2db5c1bafe8af93f69a11b8a263899a930'
    # The get_geos dict contains the geographies to be retrieved. The dict keys
    # are the area predicates called in the API request. The value of each key
    # is a nested list in which the first item of each individual list is the
    # area code and the second item is the respective state.
    get_geos = {
    'workforce+investment+area':[['SDA100','27'],['SDA090','27'],['SDA120','27'],['SDA140','27'],['SDA150','27'],['SDA160','27']],
    'metropolitan+statistical+area/micropolitan+statistical+area':[['33460','27']]
    }
    # Add field headers to the output file.
    output.write('area_code, area_label, year, quarter, race, ethnicity, naics, employment, employment_end_of_quarter, employment_stable, hires, separations, avg_monthly_wages_stable, avg_monthly_wages_newhires \n')
    # Iterate through each key and each list within its values from get_geos.
    for key in get_geos.keys():
        for value in get_geos[key]:
            # Construct the URL string for the api call.
            thisgeo = '&for=' + key + ":" + value[0] + '&in=state:' + value[1]
            URLpath = URL_base + variables + thisgeo + startyear + str(currentyear) + industries + api_key
            # Call the constructed URL and open the returned data.
            data = urllib.request.urlopen(URLpath)
            data = data.read()
            data = data.decode()
            json_data = json.loads(data)
            # Iterate through each line of the returned data and convert each
            # data point to a cleaned string.
            if key == 'workforce+investment+area':
                area_code = str(value[1]) + str(value[0])
            else:
                area_code = str(value[0])
            for line in json_data[1:]:
                Emp = str(line[0]).replace('None','')
                EmpEnd = str(line[1]).replace('None','')
                EmpS = str(line[2]).replace('None','')
                HirA = str(line[3]).replace('None','')
                Sep = str(line[4]).replace('None','')
                EarnS = str(line[5]).replace('None','')
                EarnHirNS = str(line[6]).replace('None','')
                race = race_dict[str(line[7])]
                ethnicity = ethnicity_dict[str(line[8])]
                year = str(line[9][0:4])
                quarter = str(line[9][-2:])
                naics = str(line[10])
                area_label = geo_dict[area_code]
                # The Census area codes returned from makegeographydict() are
                # janky and start with the state code for WIA geographies, but
                # no state prefix for other geographies. The area code output
                # needs to be adjusted in order to lookup the proper area label.
                output.write(area_code + ',' + area_label + ',' + year + ',' +  quarter + ',' + race + ',' + ethnicity + ',' + naics + ',' + Emp + ',' + EmpEnd + ',' + EmpS + ',' + HirA + ',' + Sep + '\n')
    output.close()

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

def makegeographydict():
    geo_dict = {}
    geographylist = urllib.request.urlopen('https://lehd.ces.census.gov/data/schema/latest/label_geography.csv')
    for line in geographylist.readlines():
        line = line.rstrip()
        if line:
            line = line.decode()
            line = line.split(',')
            geo_dict[line[0]]=line[1].replace('\n','').replace('"','')
    return geo_dict

def main():
    print(get_qwi())
    print('Enjoy your data!')

if __name__ == '__main__':
    main()
