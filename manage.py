import argparse
from loripy.loripy import Loripy

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Loripy - templating language for Python'
    )
    parser.add_argument('filename', help='filename')
    parser.add_argument('destination', help='file to output')
    args = parser.parse_args()
    filename = args.filename
    destination = args.destination

    loripy = Loripy(filename, source_type='file')
    loripy.render(destination)
