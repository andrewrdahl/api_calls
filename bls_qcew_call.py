def retrieve_bls():
    import requests
    import json
    headers = {'Content-type': 'application/json'}
    data = json.dumps({"seriesid":["LAUCT274300000000003"],"startyear":"2011", "endyear":"2014"})
    p = requests.post('https://api.bls.gov/publicAPI/v2/timeseries/data/', data=data, headers=headers)
    json_data = json.loads(p.text)
    for series in json_data['Results']['series']:
        x=["series id","area","year","period","value"]
        seriesId = series['seriesID']
        for item in series['data']:
            year = item['year']
            period = item['period']
            value = item['value']
            x.append([seriesId,year,period,value])
    return x

def main():
    print(retrieve_bls())

if __name__ == '__main__':
    main()
