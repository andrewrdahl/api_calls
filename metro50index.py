import json
import urllib.request
import urllib
import datetime

def makegeographydict():
    # Retrieve all geography codes and labels and make a dict for look up.
    geo_dict = {}
    geographylist = urllib.request.urlopen('https://lehd.ces.census.gov/data/schema/latest/label_geography.csv')
    for line in geographylist.readlines():
        line = line.rstrip()
        if line:
            line = line.decode()
            line = line.split(',')
            if len(line) == 4:
                if line[3] == 'M':
                    geo_dict[line[0]] = [
                    line[1].replace('\n','').replace('"','') + ';' + line[2].replace('\n','').replace('"',''),
                    line[0][:2],
                    line[0][2:]
                    ]
    return geo_dict

def main():
    print(makegeographydict())

if __name__ == '__main__':
    main()
