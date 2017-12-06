def retrieve_bls():
    import requests
    import json
    import datetime
    import urllib.request
    bls_areas = urllib.request.urlopen('https://download.bls.gov/pub/time.series/la/la.area')
    area_string = []
    for a in bls_areas.readlines():
        line_decode = a.decode()
        line = line_decode.split('\t')
        area_string.append(line)
        area_dict = {}
        for a in area_string:
            area_dict[a[1]] = a[2]
    thisyear = datetime.date.today().year
    headers = {'Content-type': 'application/json'}
    data = json.dumps({"seriesid":['LAUMT273346000000003'],"startyear":thisyear-9, "endyear":thisyear})
    p = requests.post('https://api.bls.gov/publicAPI/v2/timeseries/data/', data=data, headers=headers)
    json_data = json.loads(p.text)
    outfile = 'results.txt'
    output = open(outfile,'w')
    output.write('series,year,period,value,footnote' + '\n')
    for series in json_data['Results']['series']:
        seriesId = series['seriesID']
        for item in series['data']:
            year = item['year']
            period = item['period']
            value = item['value']
            area = area_dict[seriesId[3:18]]
            footnotes=""
            for footnote in item['footnotes']:
                if footnote:
                    footnotes = footnotes + footnote['text'] + ','
            output.write(seriesId + ',' + area + ',' + year + ',' + period +',' + value + ',' + footnotes[0:-1] + '\n')
    output.close()
    print(area_dict)

def main():
    retrieve_bls()

if __name__ == '__main__':
    main()
