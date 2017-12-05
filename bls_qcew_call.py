def retrieve_bls():
    import requests
    import json
    import datetime
    thisyear = datetime.date.today().year
    headers = {'Content-type': 'application/json'}
    data = json.dumps({"seriesid":["LAUCT274300000000003"],"startyear":thisyear-9, "endyear":thisyear})
    p = requests.post('https://api.bls.gov/publicAPI/v2/timeseries/data/', data=data, headers=headers)
    json_data = json.loads(p.text)
    outfile = 'results.txt'
    output = open(outfile,'w')
    output.write('series,year,period,value' + '\n')
    for series in json_data['Results']['series']:
        seriesId = series['seriesID']
        for item in series['data']:
            year = item['year']
            period = item['period']
            value = item['value']
            output.write(seriesId + ',' + year + ',' + period +',' + value + '\n')
    output.close()

def main():
    retrieve_bls()

if __name__ == '__main__':
    main()
