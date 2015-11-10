from collections import namedtuple
from mpmath import erfi
from numpy import sqrt, exp, product, pi, frompyfunc
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
        return sqrt(self.inner(self, normalize=False))


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

    def inner(self, other, normalize=True):
        """Integral of the product of the pdfs over the domain"""
        if type(other) is EllipticalBlob:
            # This is the integral of the product of two diagonal gaussian pdfs
            ms = self.center
            ls = self.variances
            mo = other.center
            lo = other.variances

            # We need the domain to integrate over.  Even though the integral
            # over the whole space is gonna be finite, the error of omission
            # won't be large, and other blobs will need to be truncated to a
            # domain because their integrals would otherwise not be finite.
            x_max = self.x_max
            x_min = self.x_min

            # We actually want these blobs to be normalized over the domain,
            # but in first computing the normalization factor we can't rely on
            # the normalization factor existing!  So in the normalization()
            # call, we set normalize to False.  It should be True in every
            # other call.
            norm_self = self.normalization() if normalize else 1
            norm_other = other.normalization() if normalize else 1

            # Save off the traits so we can reconstitute the answer as a pandas
            # series.
            traits = x_max.index

            # The exponent of the Gaussian is a quadratic function.  Take the
            # quadratic coefficients from the Gaussian case so we can use the
            # integral on an arbitrary "exponential of a quadratic"
            a0 = -ms**2/(2*ls**2)
            a1 = ms/ls**2
            a2 = -1/(2*ls**2)

            # Get the coefficients for the other exponential in the product
            b0 = -mo**2/(2*lo**2)
            b1 = mo/lo**2
            b2 = -1/(2*lo**2)

            # These reduced coefficients are all that are required in the
            # solution.
            z0 = a0 + b0
            z1 = a1 + b1
            z2 = a2 + b2

            # Integral (thanks Wolfram Alpha) is: head * exp_part * erfi_part
            head = 0.5*sqrt(pi/(z2+0j))
            exp_part = exp(z0 - z1**2/(4*z2))

            # We got erfi() from mpmath, which uses weird internal types (so it
            # can do high-precision stuff).  Vectorize erfi with numpy and
            # apply it to erfi_arg -- the argument to erfi -- which is still a
            # pandas series.
            erfi_arg = lambda x: (z1 + 2*x*z2)/(2*sqrt(z2 + 0j))
            erfi_part = lambda x: frompyfunc(erfi, 1, 1)(erfi_arg(x))

            # Now the function will end up returning a numpy array of mpmath
            # floats.
            func = lambda x: head * exp_part * erfi_part(x)

            res = func(x_max) - func(x_min)
            normed_res = res / (norm_self*norm_other)

            # By the end of this type-switching nonsense, we have a numpy array
            # of mpmath complex numbers that we need to turn back into a pandas
            # series of real python floats.
            return pd.Series([float(m.real) for m in normed_res], index=traits)

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
    def __init__(self, blobs=[]):
        self.blobs = blobs

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

