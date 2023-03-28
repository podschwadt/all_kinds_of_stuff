import requests
import random
import sys
import os
from hashlib import md5

# default to a list of birds
url = 'https://en.wikipedia.org/wiki/List_of_birds_by_common_name'
if len(sys.argv) > 1:
  url = sys.argv[1]

digest = md5(url.encode('utf-8')).hexdigest()
direcotry = os.path.split(__file__)[0]
file_name = None

for file in os.listdir(direcotry):
  if file.endswith(digest):
    file_name = os.path.join(direcotry, file)

if file_name is None:
  response = requests.get(url=url)
  if not response.ok:
    print(response)
    print(response.json())
    exit(1)

  candidates = []
  for line in response.text.split('\n'):
    if line.startswith('<li>'):
      if '<a href="' in line:
        start = line.find('>', 5)
      else:
        start = line.find('>')
      end = line.find('<', start)
      if (end - start > 2):
        candidates.append(line[start + 1:end])
  file_name = os.path.join(direcotry, url.split('/')[-1] + '_' + digest)
  with open(file_name, 'w') as f:
    for line in candidates:
      f.write(line + '\n')
else:
  with open(file_name, 'r') as f:
    candidates = [l.rstrip() for l in f.readlines()]

print(f'found {len(candidates)} candidates')
print(f'selected: {random.choice(candidates)}')
