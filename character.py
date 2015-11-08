from collections import namedtuple
import math


class Blob(object):
    def __init__(self):
        pass

    def inner(self, other):
        pass


class EllipticalBlob(Blob):
    def __init__(self, center, variance):
        pass

    def inner(self, other):
        pass


class RectangularBlob(Blob):
    def __init__(self, trait, start, stop):
        pass

    def inner(self, other):
        pass


class TraitDistribution(object);
    def __init__(self):
        self.blobs = [] # list of blobs

    def add_blob(self, blob):
        self.blobs.append(blob)
        return self

    def inner(self, blob):
        inners = [blob.inner(our_blob) for our_blob in self.blobs]
        return math.sqrt(sum(x*x for x in inners))

    def normalize(self):
        pass


class CharacterModel(object):
    def __init__(self, name, affect, trait_distribution):
        self.name = name
        self.affect = affect
        self.trait_distribution = trait_distribution


class Character(object):
    def __init__(self):
        self.name = name
        self.traits = {}
        self.acquaintances = [] # list of CharacterModels
        self.beliefs = [] # list of Beliefs


class Beliefs(object);
    pass


"""
    # Correlations between traits
    {
        'trait1': {
            'trait1': 0,
            'trait2': -1,
        },
    }


  | S | I | P
--------------
S | 0 |   |
--------------
I |   | 0 |  
--------------
P |   |   | 0





"""

