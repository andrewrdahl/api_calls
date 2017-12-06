import requests
import json
import datetime
import urllib.request

def retrieve_bls():
    area_dict = get_areas()
    area_type_dict = {'MT':'Metropolitan Area','CT':'City','ST':'State','CN':'County'}
    measure_type_dict = get_measure_type()
    series_list = get_series()
    thisyear = datetime.date.today().year
    months_dict = {'M01':'January','M02':'February','M03':'March','M04':'April',
    'M05':'May','M06':'June','M07':'July','M08':'August','M09':'September',
    'M10':'October','M11':'November','M12':'December'}
    headers = {'Content-type': 'application/json'}
    data = json.dumps({"seriesid":series_list,"startyear":thisyear-9, "endyear":thisyear})
    p = requests.post('https://api.bls.gov/publicAPI/v2/timeseries/data/', data=data, headers=headers)
    json_data = json.loads(p.text)
    outfile = 'laus_data.txt'
    laus_data = open(outfile,'w')
    laus_data.write('series,area_type,area,year,period,value,measure,footnote,source,retrieved' + '\n')
    for series in json_data['Results']['series']:
        seriesId = series['seriesID']
        for item in series['data']:
            year = item['year']
            period = months_dict[item['period']]
            measure = measure_type_dict[seriesId[-2:]]
            value = item['value']
            area = area_dict[seriesId[3:18]].replace(',','')
            area_type = area_type_dict[seriesId[3:5]]
            retrieved = str(datetime.date.today())
            footnotes=""
            for footnote in item['footnotes']:
                if footnote:
                    footnotes = footnotes + footnote['text'] + ','
            laus_data.write(
            seriesId + ',' +
            area_type + ',' +
            area + ',' +
            year + ',' +
            period +',' +
            measure + ',' +
            value + ',' +
            footnotes[0:-1] + ',' +
            'Bureau of Labor Statistics: LAUS,' +
            retrieved + '\n'
            )
    laus_data.close()

def get_areas():
    bls_areas = urllib.request.urlopen('https://download.bls.gov/pub/time.series/la/la.area')
    area_string = []
    for a in bls_areas.readlines():
        line_decode = a.decode()
        line = line_decode.split('\t')
        area_string.append(line)
        area_dict = {}
        for a in area_string:
            key = a[1]
            key_clean = key.replace(",","")
            area_dict[key_clean] = a[2]
    return area_dict

def get_measure_type():
    bls_measure_types = urllib.request.urlopen('https://download.bls.gov/pub/time.series/la/la.measure')
    measure_type_string = []
    for a in bls_measure_types.readlines():
        line_decode = a.decode()
        line = line_decode.split('\t')
        measure_type_string.append(line)
        measure_type_dict = {}
        for a in measure_type_string:
            key = a[0]
            key_clean = key.replace(",","")
            measure_type_dict[key_clean] = a[1]
    return measure_type_dict

def get_series():
    series_list = []
    series_file = open('laus_series.csv','r')
    series_lines = series_file.readlines()
    for line in series_lines:
        series_list.append(line.replace('\n',''))
    series_file.close()
    return series_list

def main():
    retrieve_bls()

if __name__ == '__main__':
    main()
