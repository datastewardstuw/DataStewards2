import pandas as pd
import json as js
import jinja2
import pdfkit


def parse_sentences(path, dmp_format='csv'):
    """
    :param path: path to senctences file
    :param dmp_format: format of senctence file (json or csv)
    :return: pandas dataframe of sentence ids and sentences
    """

    # parse sentences file and store sentence parts in format <segment_id><segement_content>
    # where segement content is the text that comes before the respective id in the sentences file

    return pd.read_csv(path, sep=';', header=None)


def parse_madmp(path):
    """
    :param path: path to madmp file
    :return: dictionary containing maDMP
    """

    return js.load(open(path, 'r'))


def parse_mapping(path):
    """
    :param path: path to mappings file
    :return: dictionary containing mapping
    """

    return js.load(open(path, 'r'))


def iterate_dicts(madmp, tplt, result):
    for key, val in madmp.items():
        t = type(val)
        if t is dict:
            print(f"dict {key}")
            if key in tplt:
                result = iterate_dicts(val, tplt[key], result)

        elif t is list:
            print(f"list {key}")
            for idx, l in enumerate(val):
                if key in tplt:
                    result = iterate_dicts(l, tplt[key], result)

        elif t is str or t is int or t is float:
            print(f"str/num {key}")
            if key in tplt:
                if tplt[key] not in result:
                    result[tplt[key]] = []
                result[tplt[key]].append((key, val))

    return result


def map_to_questions(madmp, template):
    """
    :param madmp: parsed maDMP dict
    :param template: which template to use (Horizon 2020 or FWF)
    :return: dict where questions are keys, lists of sentences are values
    """

    return iterate_dicts(madmp, template, dict())


def create_document(mapping, dmp_format):
    """
    :param mapping: dict containing mapping of maDMP fields to template
    :param dmp_format: template format
    :return: formatted document (html or pdf) todo
    """





    # css = None
    # if dmp_format is 'horizon2020':
    #     css = 'horizon2020.css'
    # elif dmp_format is 'fwf':
    #     css = 'fwf.css'
    #
    # pdfkit.from_file('file.html', options={}, css=css, output_path='out.pdf')

    return None


mapping = parse_mapping('./mapping_horizon2020.json')
# print(parse_sentences('./sentences.csv'))
dmp = parse_madmp('../structure-example.json')
print(dmp)
# print(map_to_questions(dmp, mapping))

templateLoader = jinja2.FileSystemLoader(searchpath="./")
templateEnv = jinja2.Environment(loader=templateLoader)
TEMPLATE_FILE = "fwf.html.jinja"
template = templateEnv.get_template(TEMPLATE_FILE)
outputText = template.render(dmp['dmp'])

print(outputText)
