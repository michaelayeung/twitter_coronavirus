#!/usr/bin/env python3

# command line arguments
import argparse
parser = argparse.ArgumentParser()
parser.add_argument('--input_paths', nargs='+', required=True,
                    help='List of .lang JSON files to include in the plot')
parser.add_argument('--keys', nargs='+', required=True,
                    help='Hashtags to track')
args = parser.parse_args()

# imports
import os
import json
from collections import defaultdict
from datetime import datetime
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# aggregate data
# total[hashtag][day_of_year] = tweet count
total = defaultdict(lambda: defaultdict(int))

for path in args.input_paths:
    filename = os.path.basename(path)

    # skip combined yearly file
    if filename == 'all.lang':
        continue

    try:
        with open(path) as f:
            tmp = json.load(f)
    except Exception as e:
        print(f"Skipping bad file {path}: {e}")
        continue

    # extract date from filename
    # assumes format like geoTwitter20-03-15.zip.lang
    try:
        year = 2020
        month = int(filename.split('-')[1])
        day = int(filename.split('-')[2].split('.')[0])
        day_of_year = datetime(year, month, day).timetuple().tm_yday
    except Exception as e:
        print(f"Skipping file with unrecognized date format {path}: {e}")
        continue

    # sum counts for each hashtag
    for k in args.keys:
        if k in tmp:
            total[k][day_of_year] += sum(tmp[k].values())
        else:
            total[k][day_of_year] += 0

# plotting
plt.figure(figsize=(10, 6))

for hashtag in args.keys:
    days = sorted(total[hashtag].keys())
    values = [total[hashtag][d] for d in days]
    plt.plot(days, values, label=hashtag)

plt.xlabel('Day of Year')
plt.ylabel('Number of Tweets')
plt.title('Hashtag Trends Over 2020')
plt.tight_layout()
plt.legend()

# save output
os.makedirs("outputs", exist_ok=True)

clean_tags = [h.replace("#", "") for h in args.keys]
filename = f"outputs/hashtags_{'_'.join(clean_tags)}_trend.png"

plt.savefig(filename)
print(f"Saved plot to {filename}")
