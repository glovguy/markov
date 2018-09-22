from src.made_up_words.made_up_words import *


while True:
    userWord = nlp(input('Word to be similar to: '))
    goalVector = userWord.vector
    # [print(x['letter'] + ': ', score(userWord, x)) for x in all_transitions['$']]
    champion = find_next_transition('$', 0, 0, goalVector)
    # print('letter: ', champion['letter'], 'mass: ', champion['mass'])
    ieration = 1
    currentVec = 0
    fakeWord = champion['letter']
    while champion['letter'] != '$' and ieration <20:
        sourceLetter = champion['letter']
        champion = find_next_transition(sourceLetter, currentVec, ieration, goalVector)
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
    print('new word: ', fakeWord[:-1])
