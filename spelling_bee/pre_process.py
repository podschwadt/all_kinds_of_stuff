import sys

lang = 'eng'
f_in = 'words_alpha.txt'
if len(sys.argv) > 1:
  f_in = sys.argv[1]
if len(sys.argv) > 2:
  lang = sys.argv[2]

preprocces_file = lang + '_preprocessed.txt'
pengram_file_name = lang + '_pengrams.txt'

count = 0
pg_count = 0
with open(f_in) as in_file:
  with open(preprocces_file, 'w') as out_file:
    with open(pengram_file_name, 'w') as pengram_file:
      for word in in_file.readlines():
        #reject words that are not only alpha
        if not word.rstrip().isalpha():
          continue
        # need to add 1 to all words because the \n
        word = word.lower()
        if len(word) > 4:
          letters = set(word)
          if len(letters) <= 8:
            if len(letters) == 8:
              pengram_file.write(word.lower())
              pg_count += 1
            out_file.write(word.lower())
            count += 1
print('found ', count, 'words and ', pg_count, 'pengrams')
