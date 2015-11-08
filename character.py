from collections import namedtuple
from math import sqrt
from numpy import exp
import pandas as pd


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
    def __init__(self, center, variances):
        self.center = center
        self.variances = variances
        pass

    def inner(self, other):
        """Integral of the product of the pdfs over the domain"""
        if type(other) is EllipticalBlob:
            # Below is a taylor series of the joint pdf.  (Thanks, Wolfram
            # alpha).
            # Integrating the actual expression gives some weird nonstandard
            # functions, so we just use the taylor series
            # TODO: This still needs to be integrated over the domain to get
            # the inner product.
            ms = self.center
            ls = self.variances
            mo = other.center
            lo = other.variances

            # This expression which appears frequently is the harmonic mean of
            # ls and lo, which is kinda cool.
            h = (ls + lo)/(ls*lo)

            # The joint pdf is a polynomial in h with coefficients that have
            # alternating sign.
            h_poly = [h**i for i in range(8)]

            # These coefficients are the reciprocals; they'll be flipped in the
            # final expression.
            reciprocal_coeffs = [1, -2, 81, -48, 384, -3840, 46080, -645120]

            # The result is all multiplied by a factor of this xp below
            xp = exp(0.5*(ms/ls - mo/lo))

            joint_pdf_taylor =
                xp * sum(c1/c2 for (c1, c2) in zip(h_poly, reciprocal_coeffs))

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


class TraitDistribution(object);
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


class Beliefs(object);
    """Correlations between traits?"""
    pass

