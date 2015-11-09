from character import *
import pandas as pd
import numpy as np

traits = ['strength','intelligence','sociability']
trf = TraitVectorFactory(traits)

rng = {'x_min': trf.make(-2, -2, -2), 'x_max': trf.make(2, 2, 2)}
blf = BlobFactory(**rng)

zero = trf.make(0, 0, 0)
q1 = trf.make(1, 1, 0)

e = blf.make_elliptical(q1, trf.make(0.2, 0.2, 0.2))
