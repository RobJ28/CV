import csv
from urllib.parse import unquote

import requests
from bs4 import BeautifulSoup

from pprint import pprint as pp
from unidecode import unidecode

import codecs
from os import system, name

# load page to BS4
def load_page(url):
    content = requests.get(url).content
    return BeautifulSoup(content, "lxml")

# clear screen
def clear():
      # for windows
    if name == 'nt':
        _ = system('cls')
      # for mac and linux(here, os.name is 'posix')
    else:
        _ = system('clear')

def main():
    base_url = "https://volby.cz/pls/ps2017nss/ps3?xjazyk=CZ"
    region_url = 'https://volby.cz/pls/ps2017nss/'

    # timeout is set to 5 second and print OK
    try:
        s = requests.Session()
        page_response = s.get(base_url, timeout=5)
        if page_response.status_code == 200:
            # print('Connection is OK')
            pass
        else:
            print(page_response.status_code)
            # notify, try again
    except requests.Timeout as e:
        print("It is time to timeout")
        print(str(e))

    # soup for main page
    soup = load_page(base_url)

    # all h3 tags on main page
    regions = soup.find_all("h3", "kraj")
    dict_reg = {}

    # url for regions
    for region in regions:
        name = region.text
        region_link = region.find('a')
        url = region_url + region_link.get('href')
        #dictionary name of regions - url
        dict_reg.update({name : url})

    #dictionary, wich get back URL based shortcut from dictionary dict_reg
    short_reg = {'A' : dict_reg.get('Hlavní město Praha'),
                 'S' : dict_reg.get('Středočeský kraj'),
                 'C' : dict_reg.get('Jihočeský kraj'),
                 'P' : dict_reg.get('Plzeňský kraj'),
                 'K' : dict_reg.get('Karlovarský kraj'),
                 'U' : dict_reg.get('Ústecký kraj'),
                 'L' : dict_reg.get('Liberecký kraj'),
                 'H' : dict_reg.get('Královéhradecký kraj'),
                 'E' : dict_reg.get('Pardubický kraj'),
                 'M' : dict_reg.get('Olomoucký kraj'),
                 'T' : dict_reg.get('Moravskoslezský kraj'),
                 'B' : dict_reg.get('Jihomoravský kraj'),
                 'Z' : dict_reg.get('Zlínský kraj'),
                 'J' : dict_reg.get('Kraj Vysočina'),
                 }

    # print menu for choice region
    def menu():
        template = "Vyber {} pro {}"
        for key, value in dict_reg.items():
            for key2, value2 in short_reg.items():
                if value == value2:
                    print(template.format(key2, key))

    # menu
    choice = True
    while choice:
        menu()
        reg_choice = input('Vyber kraj: ').upper()

        if reg_choice in short_reg.keys():
            url = short_reg.get(reg_choice)
            soup_region = load_page(url)
            choice = False
        else:
            clear()
            print('Vybral sis špatně zkus to znovu:')
            print()

    #soup for summary table for chosen region
    summary_table = soup_region.find('table', {'id' : 'ps311_t1'})
    # replace br tags for " "
    for br in summary_table("br"):
        br.replace_with(" ")

    # SUMMARY_TABLE
    # words in th header
    header = []
    for th in summary_table.find_all('th'):
        header.append(th.text.strip())

    # numbers in td header
    numbers = []
    for td in summary_table.find_all('td'):
        numbers.append(unidecode(td.text.strip()))
    # print(header,numbers)

    # RESULTS_TABLE
    table = soup_region.find_all('div', {'class' : 't2_470'})

    # HEADER TH
    header_results = []
    for th in table[0].find_all('th'):
        header_results.append(th.text.strip())
    # print(header_results)

    # DATA RESULTS
    def load_result(index_table):
        political_party = []
        for tr in table[index_table].find_all('tr'):
            party = []
            for td in tr.find_all('td'):
                party.append(unidecode(td.text.strip()))
            if party != []:
                political_party.append(party)
        return political_party

    # join table 1 and 2 (class: t2_470)
    complete_table = load_result(0) + load_result(1)
    # pp(complete_table)

    #region csv name
    reg = soup_region.find('h3').text.strip()
    name_csv = reg[6:] + '.csv'

    # WRITING DATA TO CSV
    with codecs.open(name_csv, "w", "utf-8") as file:
        file_writer = csv.writer(file, delimiter=',')
        file_writer.writerow([reg])
        file_writer.writerow([])
        file_writer.writerow([header[0] + ' ' + header[7], header[1], header[2], header[3], header[4], header[5], header[6]])
        file_writer.writerow([numbers[0], numbers[3], numbers[4], numbers[5], numbers[6], numbers[7], numbers[8]])
        file_writer.writerow([])
        file_writer.writerow([header_results[0] + ' ' + header_results[3],header_results[0] + ' ' + header_results[4],header_results[1] + ' ' + header_results[5], header_results[1] + ' ' + header_results[6]])
        for party in complete_table:
            file_writer.writerow([party[0], party[1], party[2], party[3]])
        print()
        print(f'CSV with name {name_csv} was created.')

if __name__ == '__main__':
    main()
