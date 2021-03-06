import json
import urllib.request
import urllib
import datetime
import requests

def get_qwi():
    output = open('data_census_qwi.txt','w')
    URL_base = 'https://api.census.gov/data/timeseries/qwi/rh?'
    variables = 'get=Emp,EmpEnd,EmpS,HirA,Sep,EarnS,EarnHirNS,race,ethnicity'
    startyear = '&time=from+2009+to+'
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
    'metropolitan+statistical+area/micropolitan+statistical+area':[['33460','27'],['33460','55']]
    }
    # Add field headers to the output file.
    output.write('area_code, year, quarter, race, ethnicity, naics, employment, employment_end_of_quarter, employment_stable, hires, separations, avg_monthly_wages_stable, avg_monthly_wages_newhires \n')
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

            # The Census area codes returned from makegeographydict() are
            # janky and start with the state code for WIA geographies, but
            # no state prefix for other geographies. The area code output
            # needs to be adjusted in order to lookup the proper area label.
            if key in ('workforce+investment+area', 'metropolitan+statistical+area/micropolitan+statistical+area'):
                area_code = str(value[1]) + str(value[0])
            else:
                area_code = str(value[0])
            # Iterate through each line of the returned data and convert each
            # data point to a cleaned string.
            for line in json_data[1:]:
                Emp = str(line[0]).replace('None','')
                EmpEnd = str(line[1]).replace('None','')
                EmpS = str(line[2]).replace('None','')
                HirA = str(line[3]).replace('None','')
                Sep = str(line[4]).replace('None','')
                EarnS = str(line[5]).replace('None','')
                EarnHirNS = str(line[6]).replace('None','')
                race = race_dict[str(line[7])].replace(' Alone','')
                ethnicity = ethnicity_dict[str(line[8])]
                year = str(line[9][0:4])
                quarter = str(line[9][-2:])
                naics = str(line[10])
                area_label = geo_dict[area_code]
                # Filter out any record where every data point is None.
                if (
                (
                (len(Emp) > 0) or
                (len(EmpEnd) > 0) or
                (len(EmpS) > 0) or
                (len(HirA) > 0) or
                (len(Sep) > 0) or
                (len(EarnS) > 0) or
                (len(EarnHirNS) > 0)
                ) and
                # Return only records from the major race/ethnicity groups.
                (
                (str(line[7]) == 'A0' and str(line[8]) == 'A0') or
                (str(line[7]) == 'A0' and str(line[8]) == 'A2') or
                (str(line[7]) == 'A1' and str(line[8]) == 'A1') or
                (str(line[7]) == 'A2' and str(line[8]) == 'A1') or
                (str(line[7]) == 'A3' and str(line[8]) == 'A1') or
                (str(line[7]) == 'A4' and str(line[8]) == 'A1') or
                (str(line[7]) == 'A5' and str(line[8]) == 'A1') or
                (str(line[7]) == 'A6' and str(line[8]) == 'A1') or
                (str(line[7]) == 'A7' and str(line[8]) == 'A1')
                )
                 ):
                    output.write(area_code + ',' + year + ',' +  quarter + ',' + race + ',' + ethnicity + ',' + naics + ',' + Emp + ',' + EmpEnd + ',' + EmpS + ',' + HirA + ',' + Sep + ',' + EarnS + ',' + EarnHirNS + '\n')
    output.close()

def makeindustriesstring():
    # Retrieve all 4-digit NAICS codes and construct a string to pass to the API.
    industries = ''
    allindustries = urllib.request.urlopen('https://lehd.ces.census.gov/data/schema/latest/label_industry.csv')
    for line in allindustries.readlines():
        line = line.decode()
        line = line.split(',')
        if len(str(line[0])) == 4 and line[0].isnumeric():
            industries += '&industry=' + str(line[0])
    return industries

def makeindustrydict():
    # Retrieve all NAICS codes and labels and make a dict for look up.
    industry_dict = {}
    industry_list = urllib.request.urlopen('http://lehd.ces.census.gov/data/schema/latest/label_industry.csv')
    for line in industry_list.readlines():
        line = line.decode()
        line = line.split(',')
        industry_dict[line[0]]=line[1].replace('\n','').replace('"','')
    return industry_dict

def makeracedict():
    # Retrieve all race codes and labels and make a dict for look up.
    race_dict = {}
    racelist = urllib.request.urlopen('https://lehd.ces.census.gov/data/schema/latest/label_race.csv')
    for line in racelist.readlines():
        line = line.decode()
        line = line.split(',')
        race_dict[line[0]]=line[1].replace('\n','').replace('"','')
    return race_dict

def makeethnicitydict():
    # Retrieve all ethnicity codes and labels and make a dict for look up.
    ethnicity_dict = {}
    ethnicitylist = urllib.request.urlopen('https://lehd.ces.census.gov/data/schema/latest/label_ethnicity.csv')
    for line in ethnicitylist.readlines():
        line = line.decode()
        line = line.split(',')
        ethnicity_dict[line[0]]=line[1].replace('\n','').replace('"','')
    return ethnicity_dict

def makegeographydict():
    # Retrieve all geography codes and labels and make a dict for look up.
    geo_dict = {}
    geographylist = urllib.request.urlopen('https://lehd.ces.census.gov/data/schema/latest/label_geography.csv')
    geo_file = open('data_qwi_geographies.txt','w')
    for line in geographylist.readlines():
        line = line.rstrip()
        if line:
            line = line.decode()
            line = line.split(',')
            if len(line) == 4:
                geo_dict[line[0]] = line[1].replace('\n','').replace('"','') + ';' + line[2].replace('\n','').replace('"','')
                geo_file.write(geo_dict[line[0]] + ',' + line[1].replace('\n','').replace('"','') + ';' + line[2].replace('\n','').replace('"','') + '\n')
            else:
                geo_dict[line[0]]=line[1].replace('\n','').replace('"','')
                geo_file.write(geo_dict[line[0]] + ',' + line[1].replace('\n','').replace('"','') + ';' + line[2].replace('\n','').replace('"','') + '\n')
    geo_file.close()
    return geo_dict

def main():
    get_qwi()
    print('Enjoy your data!')

if __name__ == '__main__':
    main()
