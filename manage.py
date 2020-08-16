import argparse
from loripy import Loripy

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
    loripy.sandbox.add_variable('var_name', 10)
    loripy.sandbox.add_variable('user_name', "Костя")
    loripy.process()
    loripy.render(destination)
