import json

with open('data/raw_data/swift.json', 'r') as file:
    data = json.load(file)


unique_sources = set(article['title'] for article in data)

# for source in unique_sources:
#     print(source)
    
print(len(unique_sources))
print(len(data))

from collections import defaultdict

# Create a dictionary to count each source
source_counts = defaultdict(int)

# Iterate through the data to count each source
for article in data:
    source_counts[article['title']] += 1

# Print duplicate sources
for source, count in source_counts.items():
    if count > 1:
        print(source)