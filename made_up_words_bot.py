from src.made_up_words.made_up_words import *


def generate_fake_word(goalVector, ignore=[]):
    # [print(x['letter'] + ': ', score(userWord, x)) for x in all_transitions['$']]
    firstLetterIgnores = [eachStr[0] for eachStr in ignore]
    champion = find_next_transition('$$', 0, 0, goalVector, ignore=firstLetterIgnores)
    # print('letter: ', champion['letter'], 'mass: ', champion['mass'])
    ieration = 1
    currentVec = 0
    fakeWord = champion['letter']
    sourceLetters = '$' + fakeWord
    while champion['letter'] != '$' and ieration <20:
        champion = find_next_transition(sourceLetters, currentVec, ieration, goalVector)
        if champion is None:
            print('cannot make word')
            break
        currentVec = vector_added_to_running_average(
            currentVec,
            ieration,
            champion['vector']
        )
        fakeWord += champion['letter']
        # print('letter: ', champion['letter'], 'mass: ', champion['mass'])
        ieration += 1
        sourceLetters = fakeWord[-2:]
    fakeWord = fakeWord[:-1]
    return fakeWord


while True:
    userWord = nlp(input('Word to be similar to: '))
    goalVector = userWord.vector
    fakeWord = generate_fake_word(goalVector)
    ignoreStrs = []
    while fakeWord in all_strings:
        print('generated real word "{}", retrying...'.format(fakeWord))
        ignoreStrs.append(fakeWord)
        fakeWord = generate_fake_word(goalVector, ignoreStrs)
    print('new word: ', fakeWord)
