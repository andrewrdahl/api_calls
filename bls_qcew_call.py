import urllib.request
import urllib
import datetime

def makeqcewcsv():
    qcewlist = retrieveqcewlist()
    output = open('data_bls_qcew.txt','w')
    output.write('area_fips,own_code,naics,agglvl_code,size_code,year,qtr,diclosure_code,annual_avg_estabs,annual_avg_emplvl,total_annual_wages'+'\n')
    for row in qcewlist:
        area_fips = row[0].replace('"','')
        own_code = row[1].replace('"','')
        naics = row[2].replace('"','')
        agglvl_code = row[3].replace('"','')
        size_code = row[4].replace('"','')
        year = row[5].replace('"','')
        qtr = row[6].replace('"','')
        disclosure_code = row[7].replace('"','')
        annual_avg_estabs = row[8].replace('"','')
        annual_avg_emplvl = row[9].replace('"','')
        total_annual_wages = row[10].replace('"','')

        output.write(
        area_fips + ',' +
        own_code + ',' +
        naics + ',' +
        agglvl_code + ',' +
        size_code + ',' +
        year + ',' +
        qtr + ',' +
        disclosure_code + ',' +
        annual_avg_estabs + ',' +
        annual_avg_emplvl + ',' +
        total_annual_wages + '\n'
        )
    output.close()


def retrieveqcewlist():
    thisyear = datetime.date.today().year
    areas = ['C3562','C3108']
    qcewlist = []
    for y in range(thisyear-4,thisyear):
            for a in areas:
                urlPath = 'http://data.bls.gov/cew/data/api/' + str(y) + '/a/area/' + a + '.csv'
                httpStream = urllib.request.urlopen(urlPath)
                for line in httpStream.readlines()[1:]:
                    line = line.decode()
                    line = str(line)
                    line = line.split(',')
                    if ((len(line[2].replace('"','')) == 6) or
                    (len(line[2].replace('"','')) == 4) or
                    ((len(line[2].replace('"','')) == 2) and line[3] == '0')):
                        qcewlist.append(line)
    return qcewlist

def main():
    makeqcewcsv()

if __name__ == '__main__':
    main()
