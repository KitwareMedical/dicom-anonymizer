"""
Download a web page and try to scrap the DICOM fields and their anonymization command from it.

Written by Mohammad Khawar Zia
"""

import fire
import requests

from collections import defaultdict
from bs4 import BeautifulSoup


dicom_fields_header = """# Tags anonymized in DICOM standard
# Documentation for groups meaning can be found in default associated actions.
# https://dicom.nema.org/medical/dicom/current/output/chtml/part15/chapter_e.html

"""

dicom_fields_footer = """# Contains all previous tags into one array
ALL_TAGS = []
ALL_TAGS.extend(D_TAGS)
ALL_TAGS.extend(Z_TAGS)
ALL_TAGS.extend(X_TAGS)
ALL_TAGS.extend(U_TAGS)
ALL_TAGS.extend(Z_D_TAGS)
ALL_TAGS.extend(X_Z_TAGS)
ALL_TAGS.extend(X_D_TAGS)
ALL_TAGS.extend(X_Z_D_TAGS)
ALL_TAGS.extend(X_Z_U_STAR_TAGS)
"""


def scrap_profiles(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")

    headers = [th.text for th in soup.find(attrs={'id': 'table_E.1-1'}).parent.find('table').find('thead').find_all('strong')]
    data = []


    for tr in soup.find(attrs={'id': 'table_E.1-1'}).parent.find('table').find('tbody').find_all('tr'):
        tmp = {key: value.text.strip() for key, value in dict(zip(headers, tr.find_all('td'))).items() if key in ['Attribute Name', 'Tag', 'Basic Prof.']}
        tmp2 = (tmp.get('Tag'), tmp.get('Attribute Name'), tmp.get('Basic Prof.'))
        data.append(tmp2)

    data = sorted(data, key=lambda ele: (ele[2], ele[1]))


    profiles = defaultdict(list)
    fields_to_skip = {
        'Private Attributes',
    }
    for tag, name, profile in data:
        if name in fields_to_skip:
            continue

        if name == 'Curve Data':
            new_tag = '(0x5000, 0x0000, 0xFF00, 0x0000)'
        elif name == 'Overlay Comments':
            new_tag = '(0x6000, 0x4000, 0xFF00, 0xFFFF)'
        elif name == 'Overlay Data':
            new_tag = '(0x6000, 0x3000, 0xFF00, 0xFFFF)'
        else:
            new_tag = list(tag)
            new_tag.insert(6, '0x')
            new_tag.insert(6, ' ')
            new_tag.insert(1, '0x')
            new_tag = ''.join(new_tag)

        name = name.replace('\u200b', '').replace('\n', '')
        string = f'{new_tag}, # {name}'
        profiles[profile].append(string)

    return profiles


def create_DICOM_fields(profiles):
    dicom_fields = ""
    for tag, tag_list, comment in (
        ('D', 'D_TAGS', '# Replaced tags'),
        ('Z', 'Z_TAGS', "# Replaced with empty values (0, '', ...)"),
        ('X', 'X_TAGS', '# Deleted tags'),
        ('U', 'U_TAGS', '# Replace UID'),

        ('Z/D', 'Z_D_TAGS', '# Replace element according to the VR'),
        ('X/Z', 'X_Z_TAGS', '# Set the value to empty according to the VR'),
        ('X/D', 'X_D_TAGS', "# Replace element according to the VR"),

        ('X/Z/D', 'X_Z_D_TAGS', '# Replace element according to the VR'),
        ('X/Z/U*', 'X_Z_U_STAR_TAGS',
        '# Replace element with UI as VR, else replace according to VR with empty values'),
    ):
        dicom_fields += f'{comment}\n{tag_list} = [\n'
        for profile in profiles.get(tag):
            dicom_fields += f'    {profile}\n'
        dicom_fields += ']\n\n'

    return dicom_fields_header + dicom_fields + dicom_fields_footer


def main(
        url="https://dicom.nema.org/medical/dicom/current/output/chtml/part15/chapter_e.html",
        output_path='dicomanonymizer/dicomfields.py'):
    profiles = scrap_profiles(url)
    file_content = create_DICOM_fields(profiles=profiles)
    with open(output_path, 'w') as file:
        file.write(file_content)

if __name__ == '__main__':
  fire.Fire(main)