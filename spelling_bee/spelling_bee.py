from datetime import date
import os
import random
import sys
import math

# select language
lang = 'eng'

if len(sys.argv) > 1:
  lang = sys.argv[1]
preprocces_file = lang + '_preprocessed.txt'
pengram_file_name = lang + '_pengrams.txt'

today = str(date.today())
random.seed(today)

# check if today's game exist
if not os.path.exists(lang + today + '.game'):
  # create todays game
  with open(pengram_file_name) as f:
    n_pengrams = sum(1 for line in f)
  # randomly pick a pengram
  pengram = random.randint(0, n_pengrams)
  with open(pengram_file_name) as f:
    for i, word in enumerate(f.readlines()):
      if pengram == i:
        pengram = word
        break
  # randomly pick a letter
  letter = pengram[random.randint(0, len(pengram) - 3)]

  # create todays game:
  letters = set(pengram)
  # select all words
  words = []
  with open(preprocces_file) as f:
    for word in f.readlines():
      if letter not in word:
        continue
      set_ = set(word)
      if set_.issubset(letters):
        words.append(word.rstrip())

  # write game file
  with open(lang + today + '.game', 'w') as f:
    # first we write the special letter
    f.write(letter)
    f.write('\n')

    # next we write all the other letters
    letters.remove(letter)
    letters.remove('\n')
    f.write(' '.join(letters))
    f.write('\n')

    # write all correct guesses
    f.write(' '.join(words))
    f.write('\n')

# todays game exist let's load it
with open(lang + today + '.game') as f:
  # read the special letter
  letter = f.readline().rstrip()
  # read the rest of letters
  letters = set(f.readline().rstrip().split())
  # read list of correct guesses
  correct_words = f.readline().rstrip().split()
  # read words guessed so far
  found = []
  while True:
    line = f.readline()
    if not line:
      break
    if len(line) == 1:
      continue
    found.append(line.rstrip())

##########################
# time to for game logic #
##########################

levels = [
    'Kindergarten', 'I can read', 'Elementray School', 'Good Start',
    'I know some words', 'Highschool', 'Moving Up', 'Getting There', 'Good',
    'Going Places', 'Solid', 'Nice',
    'People complement my substantial vocabulary ', 'Great',
    'Not your first Spelling Bee', 'Amazing', 'I have a good Thesauraus',
    'Professor', 'Champion', 'Genius', 'Mega Genius', 'Ultra Giga Genius'
]


# create the scoring system. a word is worth len(word)-3 points
def score_word(word):
  return len(word) - 3


def display(letters, letter, words, correct_words):
  # print letters
  print('    ' + letters[0])
  print(letters[1] + '       ' + letters[2])
  print('    ' + letter)
  print(letters[3] + '       ' + letters[4])
  print('    ' + letters[5])

  # compute score and progress bar
  # max possible score
  max_score = sum(score_word(w) for w in correct_words)
  # genius score
  genius_score = max_score - int(max_score * 0.1)
  current_score = sum(score_word(w) for w in words)
  # + 1  cause first level is nothing
  n_levels = len(levels) + 1
  # 'draw' the progress bar
  box_c = '█'
  # we want increments of 3 between the levels
  delta = genius_score / (n_levels * 3)
  progress_bar = ''
  for i in range(1, n_levels * 3 + 1):
    if current_score > delta * i:
      progress_bar += box_c
    else:
      progress_bar += '-'
    if i % 3 == 0:
      progress_bar += '#'

  # display score:
  score_string = 'Score: ' + str(current_score)
  # add level if we have one:
  if genius_score / n_levels < current_score:
    score_string += ' Current Level: ' + levels[int(
        current_score / genius_score * (n_levels - 1))]

  print(progress_bar)
  print(score_string)

  # found words
  print('Found words: \n', ' '.join(words))


# special commands:
def shuffle(letters, letter, words, correct_words):
  random.shuffle(letters)


def quit(letters, letter, words, correct_words):
  print('Thanks for playing')
  exit()


def show_scores(letters, letter, words, correct_words):
  # max possible score
  max_score = sum(score_word(w) for w in correct_words)
  # genius score
  genius_score = max_score - int(max_score * 0.1)
  delta = genius_score / len(levels)
  print('Score Levels:')
  for i in range(len(levels)):
    print(levels[i], math.ceil((i + 1) * delta))


commands = {
    '#shuffle': shuffle,
    '#s': shuffle,
    '#exit': quit,
    '#e': quit,
    '#scores': show_scores
}


def read_input(letters, letter, words, correct_words):
  guess = input("Input: ")
  # check if special command
  if guess[0] == '#':
    com = commands.get(guess)
    if com == None:
      print("Unknown command. Know commands are: ", commands.keys())
    else:
      com(letters, letter, words, correct_words)
    return
  # check if the guess quilifies
  if letter not in guess:
    print('Word needs to contain', letter)
    return
  for c in guess:
    if c not in letters and c != letter:
      print('Word can not contain', c)
      return
  if guess in words:
    print('Word already found')
    return
  if guess not in correct_words:
    print('Not a known word')
    return
  # found a new word
  # add it file
  with open(lang + today + '.game', 'a') as f:
    f.write(guess)
    f.write('\n')
  # add to the list and sort
  words.append(guess)
  words.sort()
  print("You found a new word! +", score_word(guess))


# main game loop
# the imporant variables are:
# letter: the special letter
# correct_words: words that can be found
# found: words found so far

# some more setup
found.sort()
letters = list(letters)
shuffle(letters, letter, found, correct_words)
# display start screen
if lang == 'eng':
  print('Welcome to Spelling-P!')
elif lang == 'ger':
  print('Willkommen zu Buchstabierbiene!')
else:
  print('Welcome to Spelling-P!')
  print('Playing in unknown language: ', lang)
print('Special commands are ', ' '.join(commands.keys()))
# main game loop
# print(letters)
while True:
  display(letters, letter, found, correct_words)
  read_input(letters, letter, found, correct_words)
