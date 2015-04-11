__author__ = 'Min'
import json
import codecs
import sys
def dump_booktitle(str):
    json_obj = json.loads(str,encoding='utf-8')
    print json_obj['title'].encode('utf-8')

if __name__=='__main__':
    #filepath = sys.argv[1]
    filepath = 'books.json'
    print 'input file: '+filepath
    input_file = codecs.open(filepath,'r',encoding='utf-8')
    while True:
        line = input_file.readline()
        if not line:
            break
        try:
            dump_booktitle(line)
        except:
            pass
