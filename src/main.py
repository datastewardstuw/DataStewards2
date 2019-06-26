import sys, argparse
import pandas as pd
import json as js
import jinja2
import pdfkit


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


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--dmp', help="path to maDMP (JSON) to convert", type=str, default='../dmps/structure-example.json')
    parser.add_argument('-t', '--temp', help="template to use (HORIZON or FWF)", type=str, default='FWF')

    args = parser.parse_args()

    DMP_FILE = args.dmp
    
    if args.temp == 'HORIZON':
        TEMPLATE_FILE = "h2020.html.jinja"
        # pdfkit
        options = {
            'page-size': 'A4',
            'orientation': 'portrait'
        }
    else: 
        TEMPLATE_FILE = "fwf.html.jinja"
        # pdfkit
        options = {
            'page-size': 'A4',
            'orientation': 'landscape'
        }

    # load dmp 
    dmp = js.load(open(DMP_FILE, 'r'))

    # jinja
    template_loader = jinja2.FileSystemLoader(searchpath="./")
    template_env = jinja2.Environment(loader=template_loader)
    template = template_env.get_template(TEMPLATE_FILE)
    dmp_html = template.render(dmp['dmp'])

    pdfkit.from_string(dmp_html, f"{DMP_FILE}_out.pdf", options=options)


if __name__ == '__main__':
    main()
