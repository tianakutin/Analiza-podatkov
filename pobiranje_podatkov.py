import csv
import os

import re
import requests

# definirajte URL glavne strani bolhe za oglase z mačkami
knj_url = 'https://www.goodreads.com/list/show/1.Best_Books_Ever?page=1'
# mapa, v katero bomo shranili podatke
knj_directory = 'podatki_knjig'
# ime datoteke v katero bomo shranili glavno stran
knj_filename = 'knjige.html'
# ime CSV datoteke v katero bomo shranili podatke
csv_filename = 'knjige_csv'


def download_url_to_string(url):
    try:
        r = requests.get(url)
    except requests.exeptions.ConnectionError: 
        print('Stran ne obstaja!')
        return None
    if r.status_code == requests.codes.ok:
        return r.text
    else:
        print("Napaka pri prenosu strani:", url)
        return None


def save_string_to_file(text, directory, filename):
    os.makedirs(directory, exist_ok=True)
    path = os.path.join(directory, filename)
    with open(path, 'w', encoding='utf-8') as file_out:
        file_out.write(text)
    return None

def save_page(directory, filename):
    txt = download_url_to_string(knj_url)
    save_string_to_file(txt, directory, filename)
    return None


def read_file_to_string(directory, filename):
    path = os.path.join(directory, filename)
    with open(path, 'r', encoding='utf-8') as file_in:
        return file_in.read()


def stran_v_knjige(page_content):
    rx = re.compile(r'<span itemprop=\'name\'(.*?)&emsp;',
                    re.DOTALL)
    ads = re.findall(rx, page_content)
    return ads




def slovar(block):
    rx = re.compile(r'role=\'heading\' aria-level=\'4\'>(?P<naslov>.*?)</span>'
                    r'<a class="authorName"*?<span itemprop="name">(?P<avtor>.*?)</span></a>'
                    r'<span class="minirating">.*?</span></span>(?P<ocena>.*?)&mdash;'
                    r'&mdash;(?P<stevilo_ocen>.*?)</span>'
                    r'<a href="#" onclick=.*?return false;">(?P<score>).*?</a>',
                    re.DOTALL)
    data = re.search(rx, block)
    ad_dict = data.groupdict()
    return ad_dict


def knjige_iz_datoteke(filename, directory):
    page = read_file_to_string(filename, directory)
    blocks = stran_v_knjige(page)
    ads = [slovar(block) for block in blocks]
    return ads

def ads_frontpage():
    return knjige_iz_datoteke(knj_directory, knj_filename)

###############################################################################
# Obdelane podatke želimo sedaj shraniti.
###############################################################################


def write_csv(fieldnames, rows, directory, filename):
    os.makedirs(directory, exist_ok=True)
    path = os.path.join(directory, filename)
    with open(path, 'w', encoding='utf-8') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)
    return None




def to_csv(ads, directory, filename):
    assert ads and (all(j.keys() == ads[0].keys() for j in ads))
    raise NotImplementedError()


def main(redownload=True, reparse=True):
    save_page(knj_directory, knj_filename)
    ads =stran_v_knjige(read_file_to_string(knj_directory, knj_filename))
    ads_nice = [slovar(ad) for ad in ads]
    to_csv(ads_nice, knj_directory, csv_filename)
    
main()