import random
words=[
    'apple',
    'bannana',
    'orange',
    'coconut',
    'strawberry',
    'lime',
    'grapefruit',
    'lemon',
    'kumqat',
    'blueberry',
    'melon'
]
while True:
    start = input("Press Enter / Return to start or enter Q to quit.")
    if start.lower == 'q':
        break
    secret_word = random.choice(words)
    bad_guesses = []
    good_guesses = []
    while len(bad_guesses) <7  and len(good_guesses != len(list(secret_word)))):

        for letter in secret_word :
            if letter in good_guesses:
                print(letter ,end = ' ')
            else :
                print('_', end=' ')
        print(' ')
        print('strikes:{}/7'.format(len(bad_guesses)))
        print(' ')
        guess = input('guess a letter :').lower()
        if len (guess)!=1:
            print('you can only ')


