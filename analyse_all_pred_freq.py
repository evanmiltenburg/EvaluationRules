from lxml import etree
import glob
from collections import defaultdict, Counter
import seaborn as sns
from matplotlib import pyplot as plt
import pandas as pd
import csv

def get_entries(xmlfile):
    "Get entries from an XML file."
    root = etree.parse(xmlfile)
    return root.xpath('//entry')


def get_predicate_list(entry):
    """
    Get a list of triples from an entry.
    An entry may contain one or more predicates.
    """
    triple_list = []
    triples = entry.xpath('./modifiedtripleset/mtriple') # Issue with the test set: otriple instead of mtriple.
    for triple in triples:
        triple_list.append(tuple(triple.text.split(' | ')))
    return triple_list


def get_pred_counts(entries):
    """
    Count how often each predicate occurs in a list of entries.
    An entry may contain one or more predicates.
    """
    triples = []
    for entry in entries:
        triples.extend(get_predicate_list(entry))
    
    preds = [t[1] for t in triples]
    return Counter(preds)


if __name__=="__main__":
    xmlfiles = glob.glob('./webnlg-master/final/en/train/*triples/*.xml')

    all_counts = Counter()
    for file in xmlfiles:
        entries = get_entries(file)
        counts = get_pred_counts(entries)
        all_counts += counts
        print(file)
        print(counts,'\n')


    print("All counts:")
    print(all_counts)

    total = sum(all_counts.values())
    ten_percent = total // 10
    most_common = all_counts.most_common()
    fraction = 0
    for i, (pred, count) in enumerate(reversed(most_common),start=1):
        fraction += count
        print(i, pred,count, "percentage:", (fraction/total) * 100)

    data = defaultdict(list)
    for key,count in all_counts.items():
        data['predicate'].append(key)
        data['count'].append(count)


    df = pd.DataFrame.from_dict(data)
    df = df.sort_values(['count']).reset_index(drop=True)

    with open('predicate_frequency_all.csv','w') as f:
        writer = csv.writer(f)
        writer.writerow(['Predicate', 'Count'])
        writer.writerows(all_counts.most_common())

    # Select columns using threshold value.
    # df = df.loc[df['count'] > 5]
    plt.figure(figsize=(16, 6))
    plt.rcParams.update({'font.size': 14})
    ax = sns.barplot(x='count',y='predicate', data=df,color="red",edgecolor='red')
    ax.tick_params(top=False, bottom=False, left=False, right=False, labelleft=True, labelbottom=True)
    labels = ax.get_yticklabels()
    for i, label in enumerate(labels, start=2): # manipulate start to get other labels.
        if not i % 10 == 0:                     # start at 2 to avoid an awkwardly long label.
            label.set_visible(False)
    plt.annotate("country", (2150,245),(2150,200), arrowprops=dict(arrowstyle="->"), ha='center')
    ax.set_xlabel('')
    ax.set_ylabel('')

    plt.tight_layout()
    plt.savefig('predicate_frequency_all.pdf')
