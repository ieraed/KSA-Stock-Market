import json
import sys

def count(path):
    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        print(path, '->', len(data))

if __name__ == '__main__':
    for p in sys.argv[1:]:
        count(p)
