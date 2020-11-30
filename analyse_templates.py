from lxml import etree
import glob
from collections import defaultdict, Counter
import json


def get_entries(xmlfile):
    "Get entries from an XML file."
    root = etree.parse(xmlfile)
    return root.xpath('//entry')


def count_templates(filename):
    "Count the templates for each predicate in a file."
    template_counter = defaultdict(list)
    entries = get_entries(filename)
    for entry in entries:
        otriples = entry.xpath('./originaltripleset/otriple')
        assert len(otriples) == 1 # check to make sure we don't miss anything.
        otriple = otriples[0]
        predicate = otriple.text.split(' | ')[1]
        templates = [template.text for template in entry.xpath('.//template')]
        template_counter[predicate].extend(templates)
    return template_counter


def gather_all(xmlfiles):
    "Gather all templates in one index."
    main_index = defaultdict(list)
    for filename in xmlfiles:
        result = count_templates(filename)
        for predicate, templates in result.items():
            main_index[predicate].extend(templates)
    return main_index


def compute_ratios(index):
    "Compute ratio of unique templates to total templates."
    rows = []
    for predicate, templates in index.items():
        unique_templates = len(set(templates))
        all_templates = len(templates)
        ratio = unique_templates/all_templates
        row = [predicate, unique_templates, all_templates, f"{ratio:.2f}"]
        rows.append(row)
    rows = sorted(rows, key=lambda row:row[-1], reverse=True)
    return rows


def select_ratios(rows, max_per_category, add_last):
    "Select rows with ratios along the entire range of ratios."
    selection = []
    last = None
    for row in rows:
        ratio = row[-1]
        relevant_digit = ratio[-2]
        if relevant_digit != last:
            selection.append(row)
            count = 1
            last = relevant_digit
        elif count < max_per_category:
            selection.append(row)
            count += 1
    if add_last:
        selection.append(rows[-1])
    return selection


def make_latex(table):
    """
    Quick and dirty LaTeX solution to generate the contents of a table.
    """
    lines = [' & '.join(map(str,row))+'\\\\' for row in table]
    table = '\n'.join(lines)
    print(table)


if __name__=="__main__":
    xmlfiles = glob.glob('./webnlg-master/final/en/train/1triples/*.xml')
    index = gather_all(xmlfiles)
    ratios = compute_ratios(index)
    selected_ratios = select_ratios(ratios, max_per_category=2, add_last=True)
    make_latex(selected_ratios)
