"""
List the size of subdirectories 

usage: python dir_size.py <dir>
"""

import os
import sys
import tqdm
from os.path import join, isdir, getsize, abspath
import json

working_dir = '.'

if len(sys.argv) > 1:
  working_dir = sys.argv[1]

dirs = {d: 0 for d in os.listdir(working_dir) if isdir(join(working_dir, d))}
total = 0

pbar = tqdm.tqdm(total=len(dirs), desc='reading subdirecotries')
for d in dirs:
  size = 0
  for path, d_names, f_names in os.walk(join(working_dir, d)):
    pbar.total += len(d_names) + len(f_names)
    pbar.refresh()
    temp_size = 0
    for f in f_names:
      try:
        temp_size += getsize(join(path, f))
      except:
        pass
      pbar.update(1)
    pbar.update(1)
    size += temp_size
  pbar.update(1)
  dirs[d] = size / 1024 / 1024 / 1024
  total += size / 1024 / 1024 / 1024

pbar.close()

# compute longest dirname
l = max([len(d) for d in dirs])

result_string = abspath(working_dir) + ': \n'
for d in dirs:
  temp = d + ':'
  result_string += '  ' + temp + ' ' * (l - len(temp) +
                                        2) + f'{dirs[d]:.3f}' + '\n'

result_string += 'Total: ' + ' ' * (l - len('Total: ') + 4) + f'{total:.3f}\n'
result_string += 'Results in GB'

print(result_string)
