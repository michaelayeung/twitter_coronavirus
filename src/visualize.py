#!/usr/bin/env python3

# command line args
import argparse
parser = argparse.ArgumentParser()
parser.add_argument('--input_path', required=True)
parser.add_argument('--key', required=True)
parser.add_argument('--percent', action='store_true')
args = parser.parse_args()

# imports
import os
import json
import matplotlib.pyplot as plt

# open the input path
with open(args.input_path) as f:
    counts = json.load(f)

# make sure the key exists
if args.key not in counts:
    raise KeyError(f'{args.key} not found in {args.input_path}')

# normalize the counts by the total values
if args.percent:
    for k in counts[args.key]:
        if k in counts['_all'] and counts['_all'][k] != 0:
            counts[args.key][k] /= counts['_all'][k]

# sort items from high to low, keep top 10
items = sorted(counts[args.key].items(), key=lambda item: (item[1], item[0]), reverse=True)[:10]

# re-sort top 10 from low to high for plotting
items = sorted(items, key=lambda item: (item[1], item[0]))

# print the count values
for k, v in items:
    print(k, ':', v)

# split into labels and values
labels = [k for k, v in items]
values = [v for k, v in items]

# create output filename
base = os.path.basename(args.input_path)
safe_key = args.key.replace('#', 'hashtag_')
output_path = base + '.' + safe_key + '.png'

# make bar graph
plt.figure(figsize=(12, 6))
plt.bar(labels, values)
plt.xlabel('Keys')
plt.ylabel('Percent' if args.percent else 'Values')
plt.title(f'Top 10 values for {args.key}')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()

# save image
plt.savefig(output_path)
print('saved plot to', output_path)
