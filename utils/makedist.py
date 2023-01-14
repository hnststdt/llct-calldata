#!/usr/bin/python
import os
import json
import shutil

def as_response(data):
    return {
        'result': 'success',
        'data': data
    }

if __name__ == '__main__':
    os.mkdir('dist')

    shutil.copy('index.html', 'dist')

    with open('lists.json') as f:
        metadata = json.load(f)

    with open('dist/lists', 'w') as f:
        json.dump(as_response(metadata), f)

    os.mkdir('dist/call')
    for gid, group in enumerate(metadata['groups']):
        for sid in range(len(metadata['songs'][gid])):
            if (os.path.exists(f"{group['id']}/{sid+1}")):
                shutil.copy(f"{group['id']}/{sid+1}/call.json" ,f"dist/call/{gid}{sid+1}")
