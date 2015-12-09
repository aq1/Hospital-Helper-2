import sys
import json

import unidecode

sys.path.append('../')
import options


def write(f, s):
    # f.write('#: x.py:1\n')
    f.write('msgid "{}"\nmsgstr "{}"\n\n'.format(unidecode.unidecode(s), s.replace('_', ' ')))

structure = json.loads(options.INIT_STRUCTURE)


header = r'''msgid ""
msgstr ""
"Content-Type: text/plain; charset=UTF-8\n"
"Language: ru\n"
'''
with open('translation.pot', 'w', encoding='utf8') as f:
    f.write(header)
    f.write('\n\n')
    for item in structure:
        for arg in item['args']:
            write(f, arg['name'])

        write(f, item['name'])
        try:
            write(f, item['group'])
        except KeyError:
            pass
