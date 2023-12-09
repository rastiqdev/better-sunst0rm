from datetime import datetime

import requests
import re
import wikitextparser as wtp

DEVICE_REGEX = re.compile(r'(iPhone|AppleTV|iPad|iPod)[0-9]+,[0-9]+')

def get_key_page(identifier: str, buildid: str) -> str:
    params = {
        'action': 'query',
        'list': 'search',
        'srsearch': f'Keys: {buildid} ({identifier})',
        'srwhat': 'title',
        'srlimit': '1',
        'format': 'json',
        'srnamespace': '2304',
    }
    resp = requests.get(
        'https://theapplewiki.com/api.php', params=params
    )
    if resp.status_code != 200:
        pass
    else:
        search = resp.json()

    if search['query']['searchinfo']['totalhits'] == 0:
        raise ValueError(
            f'No Firmware Keys page for device: {identifier}, buildid: {buildid}.'
        )

    params = {
        'action': 'parse',
        'prop': 'wikitext',
        'page': search['query']['search'][0]['title'],
        'format': 'json',
        'formatversion': 2,
    }
    resp = requests.get(
        'https://theapplewiki.com/api.php', params=params
    )
    if resp.status_code != 200:
        pass

    data = resp.json()

    return data['parse']['wikitext']


def parse_page(data: str, identifer: str, boardconfig: str = None) -> dict:
    data = (
        ' '.join([x for x in data.split(' ') if x != ''])
        .replace('{{', '{| class="wikitable"')
        .replace('}}', '|}')
    )

    page = wtp.parse(data)
    page_data = {}
    for entry in page.tables[0].data()[0]:
        key, item = entry.split(' = ')
        page_data[key] = item

    if boardconfig is not None:
        if ('Model' not in page_data.keys()) and ('Model2' not in page_data.keys()):
            return page_data

        if boardconfig.lower() not in [x.lower() for x in page_data.values()]:
            raise ValueError(
                f'Boardconfig: {boardconfig} for device: {identifer} is not valid!'
            )

        if page_data['Model2'].lower() == boardconfig.lower():
            for key in page_data:
                if '2' in key:
                    page_data[key.replace('2', '')] = page_data[key]

        for key in list(page_data.keys()):
            if '2' in key:
                del page_data[key]

    response = {
        'identifier': page_data['Device'],
        'buildid': page_data['Build'],
        'codename': page_data['Codename'],
        'restoreramdiskexists': 'RestoreRamdisk' in page_data,
        'updateramdiskexists': 'UpdateRamdisk' in page_data,
        'keys': [],
    }

    for component in page_data:
        if component in (
            'Version',
            'Build',
            'Device',
            'Model',
            'Codename',
            'Baseband',
            'DownloadURL',
        ):
            continue

        if any(component.endswith(x) for x in ('Key', 'IV', 'KBAG')):
            continue

        image = {
            'image': component,
            'filename': page_data[component],
            'date': datetime.now().isoformat(),
        }

        if any(component == x for x in ('RootFS', 'RestoreRamdisk', 'UpdateRamdisk')):
            image['filename'] += '.dmg'

        for key in ('IV', 'Key') if component != 'RootFS' else ('Key',):
            if component + key not in page_data.keys():
                continue

            if all(
                x not in page_data[component + key]
                for x in ('Unknown', 'Not Encrypted')
            ):
                image[key.lower()] = page_data[component + key]

        if (
            ('iv' not in image.keys())
            and ('key' not in image.keys())
            and not image['filename'].endswith('.dmg')
        ):
            continue

        if 'iv' in image and 'key' in image:
            image['kbag'] = image['iv'] + image['key']

        response['keys'].append(image)

    return response

def get_firmware_keys(identifier: str, boardconfig: str, buildid: str) -> dict:
    page = get_key_page(identifier, buildid)

    return parse_page(page, identifier, boardconfig)