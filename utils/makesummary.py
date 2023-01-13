#!/usr/bin/python
import json
import os
import subprocess
from xml.etree import ElementTree as ET

def get_last_update() -> str:
    return subprocess.check_output(
        ['git', 'log', '-n', '1', '--pretty=tformat:%ad (%h)', '--date=short']).decode().strip()

def childtag(parent:ET.Element, *args, **kwargs) -> ET.Element:
    child = ET.Element(*args, **kwargs)
    parent.append(child)
    return child

def texttag(tag:str, text:str, **kwargs) -> ET.Element:
    t = ET.Element(tag, **kwargs)
    t.text = text
    return t

def makelist(summary:str, items:[str]) -> ET.Element:
    details = ET.Element('details')
    details.append(texttag('summary', summary))
    ul = ET.Element('ul')
    details.append(ul)
    ul.extend((texttag('li', item) for item in items))
    return details

if __name__ == '__main__':
    html = ET.Element('html')

    head = childtag(html, 'head')
    head.append(ET.Element('meta', charset='UTF-8'))
    head.append(texttag('title', "llct-calldata stats"))

    body = childtag(html, 'body')
    body.append(texttag('h1', "llct-calldata stats"))
    body.append(texttag('p', f"last updated: {get_last_update()}"))

    div_stats = childtag(body, 'div', attrib={'id': 'completion'})
    div_stats.append(texttag('h2', "completion stats"))

    div_missing = childtag(body, 'div', attrib={'id': 'missing'})
    div_missing.append(texttag('h2', "lists of missing calls"))

    div_unstreamable = childtag(body, 'div', attrib={'id': 'unstreamable'})
    div_unstreamable.append(texttag('h2', "list of unstreamable songs"))

    with open('lists.json') as f:
        metadata = json.load(f)

    for gid, group in enumerate(metadata['groups']):

        missing_songs = [f"{song['title']} (id={gid}{sid+1})"
            for sid, song in enumerate(metadata['songs'][gid])
            if not os.path.exists(f"{group['id']}/{str(sid+1)}")]

        total_cnt = len(metadata['songs'][gid])
        missing_cnt = len(missing_songs)
        available_cnt = total_cnt - missing_cnt

        div_stats.append(texttag(
            'p', f"{group['id']}: {available_cnt}/{total_cnt} ({available_cnt / total_cnt * 100:.2f}%)"))
        div_missing.append(makelist(group['id'], missing_songs))

    div_unstreamable.append(
        makelist('unstreamable',
            (f"{song['title']} (id={gid}{sid+1})"
                for gid, grp in enumerate(metadata['songs'])
                for sid, song in enumerate(grp)
                if not song['metadata'].get('streaming'))
        ))

    with open('index.html', 'w') as f:
        f.write('<!DOCTYPE html>')
        ET.ElementTree(html).write(f, encoding='unicode', method='html')
