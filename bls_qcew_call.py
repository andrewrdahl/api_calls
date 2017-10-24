def retrieve_bls():
    import requests
    import json
    headers = {'Content-type': 'application/json'}
    data = json.dumps({"seriesid": ['CUUR0000SA0','SUUR0000SA0'],"startyear":"2011", "endyear":"2014"})
    p = requests.post('https://api.bls.gov/publicAPI/v2/timeseries/data/', data=data, headers=headers)
    json_data = json.loads(p.text)
    for series in json_data['Results']['series']:
        x=["series id","year","period","value","footnotes"]
        seriesId = series['seriesID']
        for item in series['data']:
            year = item['year']
            period = item['period']
            value = item['value']
            if 'M01' <= period <= 'M12':
                    x.append([seriesId,year,period,value])
    return x

def main():
    print(retrieve_bls())

if __name__ == '__main__':
    main()
