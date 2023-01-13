import os
import json
import shutil

if __name__ == '__main__':
    os.mkdir('dist')

    with open('lists.json') as f:
        metadata = json.load(f)

    shutil.copy('index.html', 'dist')
    shutil.copy('lists.json', 'dist')
    for group in metadata['groups']:
        shutil.copytree(group['id'], f"dist/{group['id']}")
