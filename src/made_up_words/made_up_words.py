from math import sqrt
import spacy
import numpy

nlp = spacy.load('en_core_web_sm')

all_strings = [s for s in nlp.vocab.strings]
all_transitions = {}


def vector_added_to_running_average(runningAvVec, runningTotal, vec):
    return (
            (runningAvVec * runningTotal) + vec
        ) / (runningTotal+1)


def add_vector_to_destination(matchDest, vec):
    matchDest['vector'] = vector_added_to_running_average(
        matchDest['vector'],
        matchDest['mass'],
        vec
    )
    matchDest['mass'] += 1


def build_transition(source, destLetter):
    dests = all_transitions.get(source)
    if dests is None:
        all_transitions[source] = []
        dests = all_transitions[source]
    matchDest = next(
        (d for d in dests if d['letter'] == destLetter),
        None
    )
    if matchDest is None:
        matchDest = { 'letter': destLetter, 'mass': 0, 'vector': 0 }
        dests.append(matchDest)
    vec = nlp(s).vector
    add_vector_to_destination(matchDest, vec)


for s in all_strings[2000:2110]:
    source = '$'
    destLetter = s[0]
    build_transition(source, destLetter)
    for i in range(0, len(s)-1):
        source = s[i]
        destLetter = s[i+1]
        build_transition(source, destLetter)
    build_transition(s[-1], '$')


def potential_new_vector(currentVec, sourceVec):
    return sourceNode


def score(goalVector, currentVec, currentTotal, destNode):
    vec = vector_added_to_running_average(currentVec, currentTotal, destNode['vector'])
    return numpy.linalg.norm(vec-goalVector)


def find_next_transition(sourceLetter, currentVec, currentTotal, goalVector):
    return min(
        all_transitions[sourceLetter],
        key=lambda n: score(goalVector, currentVec, currentTotal, n)
    )
