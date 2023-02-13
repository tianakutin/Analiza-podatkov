import csv
import os

import re
import requests


knj_url = 'https://www.goodreads.com/list/show/1.Best_Books_Ever?page='

knj_directory = 'podatki_knjig'
knj_filename = 'knjige.html'
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


def save_string_to_file(text):
    os.makedirs(knj_directory, exist_ok=True)
    path = os.path.join(knj_directory, knj_filename)
    with open(path, 'w', encoding='utf-8') as file_out:
        file_out.write(text)
    return None

def save_page(url):
    txt = download_url_to_string(url)
    save_string_to_file(txt)
    return None


def read_file_to_string():
    path = os.path.join(knj_directory, knj_filename)
    with open(path, 'r', encoding='utf-8') as file_in:
        return file_in.read()


def stran_v_knjige(page_content):
    rx = re.compile(r'<span itemprop=\'name\'(.*?)&emsp;',
                    re.DOTALL)
    knjige = re.findall(rx, page_content)
    return knjige




def slovar(block):
    patterns = patterns = [
        r'role=\'heading\' aria-level=\'4\'>(?P<naslov>.*?)</span>',
        r'<a class="authorName".*?<span itemprop="name">(?P<avtor>.*?)</span></a>',
        r'<span class="minirating">.*?</span></span>(?P<ocena>.*?) avg rating &mdash;',
        r'&mdash;(?P<stevilo_ocen>.*?) ratings</span>',
        r'<a href="#" onclick=.*?return false;">score: (?P<score>.*?)</a>',
        r'<a id="loading_link.*?return false;">(?P<stevilo_glasov>.*?) people voted</a>'
    ]

    knj_dict = {}
    for pattern in patterns:
        rx = re.compile(pattern, re.DOTALL)
        data = re.search(rx, block)
        knj_dict.update(data.groupdict())

    return knj_dict


def knjige_iz_datoteke():
    page = read_file_to_string(knj_filename, knj_directory)
    blocks = stran_v_knjige(page)
    knjige = [slovar(block) for block in blocks]
    return knjige

def knjige_frontpage():
    return knjige_iz_datoteke()

def write_csv(fieldnames, rows):
    os.makedirs(knj_directory, exist_ok=True)
    path = os.path.join(knj_directory, csv_filename)
    with open(path, 'w', encoding='utf-8') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)
    return None

def to_csv(knjige):
    assert knjige and (all(j.keys() == knjige[0].keys() for j in knjige))
    write_csv(knjige[0].keys(), knjige)

def main(redownload=True, reparse=True):
    knjige_nice = []

    for i in range(1, 11):
        url = knj_url + str(i)
        save_page(url)

        knjige = stran_v_knjige(read_file_to_string())

        knjige_nice.extend([slovar(knjiga) for knjiga in knjige])

    to_csv(knjige_nice)
    
main()