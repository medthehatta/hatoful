from collections import namedtuple
from mpmath import erfi
from numpy import sqrt, exp, product, pi
from itertools import count
import pandas as pd


class TraitVectorFactory(object):
    def __init__(self, traits):
        self.traits = traits

    def make(self, *lst, **dct):
        if dct:
            return pd.Series(**dct)

        elif lst:
            return pd.Series(lst, index=self.traits)

        else:
            raise ValueError('Need to provide either a list or dict')


class BlobFactory(object):
    def __init__(self, x_max, x_min):
        self.x_max = x_max
        self.x_min = x_min

    def make_elliptical(self, center, variances):
        return EllipticalBlob(center, variances, self.x_max, self.x_min)


class Blob(object):
    def __init__(self):
        pass

    def inner(self, other):
        pass

    def normalization(self):
        return sqrt(self.inner(self))


class EllipticalBlob(Blob):
    """Hyper-Ellipsoidal blob with principal axes aligned with the traits
    Oblique blobs are too complicated.
    """
    def __init__(self, center, variances, x_max, x_min):
        self.center = center
        self.variances = variances
        self.x_max = x_max
        self.x_min = x_min

    def __repr__(self):
        return '<EllipticalBlob @{0}>'.format(
            list(self.center),
        )

    def inner(self, other):
        """Integral of the product of the pdfs over the domain"""
        if type(other) is EllipticalBlob:
            # This is the integral of the product of two diagonal gaussian pdfs
            ms = self.center
            ls = self.variances
            mo = other.center
            lo = other.variances
            x_max = self.x_max
            x_min = self.x_min

            a1 = -ms**2/(2*ls**2)
            a2 = ms/ls**2
            a3 = -1/(2*ls**2)

            b1 = -mo**2/(2*lo**2)
            b2 = mo/lo**2
            b3 = -1/(2*lo**2)

            z1 = a1 + b1
            z2 = a2 + b2
            z3 = a3 + b3

            import pdb
            pdb.set_trace()
            head = 0.5*sqrt(pi/z3)
            exp_part = exp(z1 - z2**2/(4*z3))
            erfi_arg = lambda x: (z2 + 2*x*z3)/(2*sqrt(z3 + 0j))
            erfi_part = lambda x: erfi_arg(x).apply(erfi)

            func = lambda x: head * exp_part * erfi_part(x)

            return func(x_max) - func(x_min)

        elif type(other) is RectangularBlob:
            pass

        else:
            raise ValueError(
                'Must take inner product between EllipticalBlobs '
                'or RectangularBlobs'
            )


class RectangularBlob(Blob):
    """Blobs which are just uniform on the whole domain, but are truncated to
    between two values along one trait.
    """
    def __init__(self, trait, start, stop):
        pass

    def inner(self, other):
        pass


class TraitDistribution(object):
    def __init__(self):
        self.blobs = [] # list of blobs

    def add_blob(self, blob):
        self.blobs.append(blob)
        return self

    def inner(self, blob):
        inners = [blob.inner(our_blob) for our_blob in self.blobs]
        return sqrt(sum(x*x for x in inners))

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


class Beliefs(object):
    """Correlations between traits?"""
    pass

