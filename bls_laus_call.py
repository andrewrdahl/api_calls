import requests
import json
import datetime
import urllib.request

def retrieve_bls():
    area_dict = get_areas()
    area_type_dict = {'MT':'Metropolitan Area','CT':'City','ST':'State','CN':'County'}
    measure_type_dict = get_measure_type()
    # Series IDs can be found at https://www.bls.gov/lau/
    series_list = [
        'LAUMT273346000000003',
        'LAUMT273346000000004',
        'LAUMT273346000000005',
        'LAUMT273346000000006',
        'LAUCT274300000000003',
        'LAUCT274300000000004',
        'LAUCT274300000000005',
        'LAUCT274300000000006',
        'LAUCT275800000000003',
        'LAUCT275800000000004',
        'LAUCT275800000000005',
        'LAUCT275800000000006',
        'LAUST270000000000003',
        'LAUST270000000000004',
        'LAUST270000000000005',
        'LAUST270000000000006',
        'LAUCN270030000000003',
        'LAUCN270030000000004',
        'LAUCN270030000000005',
        'LAUCN270030000000006',
        'LAUCN270190000000003',
        'LAUCN270190000000004',
        'LAUCN270190000000005',
        'LAUCN270190000000006',
        'LAUCN270370000000003',
        'LAUCN270370000000004',
        'LAUCN270370000000005',
        'LAUCN270370000000006',
        'LAUCN270530000000003',
        'LAUCN270530000000004',
        'LAUCN270530000000005',
        'LAUCN270530000000006',
        'LAUCN271230000000003',
        'LAUCN271230000000004',
        'LAUCN271230000000005',
        'LAUCN271230000000006',
        'LAUCN271390000000003',
        'LAUCN271390000000004',
        'LAUCN271390000000005',
        'LAUCN271390000000006',
        'LAUCN271630000000003',
        'LAUCN271630000000004',
        'LAUCN271630000000005',
        'LAUCN271630000000006'
    ]
    thisyear = datetime.date.today().year
    # months_dict is a crosswalk from the bls.gov output to a month alias.
    months_dict = {'M01':'January','M02':'February','M03':'March','M04':'April',
    'M05':'May','M06':'June','M07':'July','M08':'August','M09':'September',
    'M10':'October','M11':'November','M12':'December'}
    headers = {'Content-type': 'application/json'}
    data = json.dumps({"seriesid":series_list, "startyear":thisyear-9, "endyear":thisyear})
    p = requests.post('https://api.bls.gov/publicAPI/v2/timeseries/data/', data=data, headers=headers)
    json_data = json.loads(p.text)
    outfile = 'laus_data.txt'
    laus_data = open(outfile,'w')
    laus_data.write('series,area_type,area,year,period,value,measure,footnote,source,retrieved' + '\n')
    for series in json_data['Results']['series']:
        seriesId = series['seriesID']
        # The measure, area, and area_type variables reference slices of the
        # SeriesID that are used by bls.gov to identify various attributes of
        # the Series. These are then translated to aliases with months_dict,
        # measure_type_dict and area_dict.
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

# Pull the table of area names from bls.gov. This is needed as a crosswalk
# from SeriesIDs to area name aliases. The resulting dict is then used in the
# above request function.
def get_areas():
    bls_areas = urllib.request.urlopen('https://download.bls.gov/pub/time.series/la/la.area')
    area_string = []
    for a in bls_areas.readlines():
        line_decode = a.decode()
        line = line_decode.split('\t')
        area_string.append(line)
        area_dict = {}
        # Many area names include a comma between the area name and its state.
        # These must be removed to prevent unintentional breaks in the csv
        # output file.
        for a in area_string:
            key = a[1]
            key_clean = key.replace(",","")
            area_dict[key_clean] = a[2]
    return area_dict

# Pull the table of measure types from bls.gov. This is needed as a crosswalk
# from SeriesIDs to measure aliases. The resulting dict is then used in the
# above request function.
def get_measure_type():
    bls_measure_types = urllib.request.urlopen('https://download.bls.gov/pub/time.series/la/la.measure')
    measure_type_string = []
    for a in bls_measure_types.readlines():
        line_decode = a.decode()
        line = line_decode.split('\t')
        measure_type_string.append(line)
        measure_type_dict = {}
        # The returned strings include extraneous commas that need to be removed
        # before populating measure_type_dict to prevent unintentional breaks in
        # the csv output file.
        for a in measure_type_string:
            key = a[0]
            key_clean = key.replace(",","")
            measure_type_dict[key_clean] = a[1]
    return measure_type_dict

def main():
    retrieve_bls()

if __name__ == '__main__':
    main()
