#!/usr/bin/env python3
#
# author: Thiago Ribeiro
# desc: Transform OVAL xml files into python dict
#
import sys
import xml.etree.ElementTree as etree
import pprint

class OvalError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        raise Exception(self.value)

class OvalParser:
    """
    Parse OVAL files
    """
    def __init__(self, xml_file):
        if len(xml_file) < 5:
            print('Please, specify the xml filepath')
            sys.exit(1)

        try:
            self.xmL = etree.parse(xml_file)
        except OSError as e:
            print('Was not possible to open the file %s. "%s"' % (xml_file, e))
            sys.exit(1)

        self.oval = {
            'generator': {
                'product_name': '', 'product_version': '',
                'schema_version': '', 'timestamp': ''
            },
            'definitions': {
                'metadata': {
                    'title': '', 'description': '', 'family': '',
                    'platform': '',
                },
            }
        }

        self.root = self.xmL.getroot()
        self.set_namespaces()

    def get_params(self, items):
        _params = {}
        if type(items) is list or tuple:
            for x, v in items:
                _params[x] = v

        return _params

    def set_namespaces(self):
        self.ns = {
            'oval': 'http://oval.mitre.org/XMLSchema/oval-definitions-5',
            'common': 'http://oval.mitre.org/XMLSchema/oval-common-5',
            'ios': 'http://oval.mitre.org/XMLSchema/oval-definitions-5#ios',
            'unix': 'http://oval.mitre.org/XMLSchema/oval-definitions-5#unix',
            'independent': 'http://oval.mitre.org/XMLSchema/oval-definitions-5\
            #independent',
        }

    def get_generator(self):
        generator = self.root.find('oval:generator', self.ns)

        if type(generator) is etree.Element:
            prod_name = generator.find('common:product_name', self.ns)
            prod_version = generator.find('common:product_version', self.ns)
            schema_version = generator.find('common:schema_version', self.ns)
            timestamp = generator.find('common:timestamp', self.ns)

            if prod_name is not None:
                self.oval['generator']['product_name'] = prod_name.text

            if prod_version is not None:
                self.oval['generator']['product_version'] = prod_version.text

            if schema_version is not None:
                self.oval['generator']['schema_version'] = schema_version.text

            if timestamp is not None:
                self.oval['generator']['timestamp'] = timestamp.text

    def get_definitions(self):
        for definitions in self.root.findall('oval:definitions', self.ns):
            for definition in definitions.findall('oval:definition', self.ns):
                self.get_metadata(definition)

    def get_metadata(self, definition):
        if type(definition) is etree.Element:
            metadata = definition.find('oval:metadata', self.ns)

            if type(metadata) is etree.Element:
                title = metadata.find('oval:title', self.ns)
                desc = metadata.find('oval:description', self.ns)
                affected = metadata.find('oval:affected', self.ns)

                if title is not None:
                    self.oval['definitions']['metadata']['title'] = title.text

                if desc is not None:
                    self.oval['definitions']['metadata']['description'] = desc.text

                if affected is not None:
                    params = self.get_params(affected.items())
                    if 'family' in params.keys():
                        self.oval['definitions']['metadata']['family'] = params['family']

                    platform = affected.find('oval:platform', self.ns)

                    if platform is not None:
                        self.oval['definitions']['metadata']['platform'] = platform.text

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Please, specify the xml filepath')
        sys.exit(1)

    read_file = sys.argv[1:][0]

    parse = OvalParser(read_file)
    parse.get_generator()
    parse.get_definitions()
    print(parse.oval)