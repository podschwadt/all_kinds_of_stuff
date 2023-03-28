top_n = 50000

with open('unigram_freq.csv') as csv:
  with open('cleaned.txt', 'w') as out_f:
    for i, line in enumerate(csv.readlines()):
      if i == 0:
        continue
      if i > top_n:
        break
      out_f.write(line.split(',')[0] + '\n')
