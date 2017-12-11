import urllib.request
import urllib

def qcewGetAreaData(year, area):
    results = open('qcew_data.csv','w')
    out = []
    urlPath = "http://data.bls.gov/cew/data/api/[YEAR]/a/area/[AREA].csv"
    urlPath = urlPath.replace("[YEAR]",year)
    urlPath = urlPath.replace("[AREA]",area.upper())
    httpStream = urllib.request.urlopen(urlPath)
    httpread = httpStream.read()
    httpdecode = httpread.decode()
    for h in httpdecode.split():
        results.write(str(h) + '\n')
    results.close()

def main():
    qcewGetAreaData('2016', 'C3346')

if __name__ == '__main__':
    main()
