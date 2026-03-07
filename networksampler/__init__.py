__version__ = "0.9.5"

from .sampling import sa_sampling, node_random_sample, sa_sampling_twophases
from .utils import generate_random_network, compute_shortest_length_paths_matrix

def info():
    """
    Print information about the NetworkSampler package.

    Examples
    --------
    >>> import networksampler
    >>> networksampler.info()
    """
    import sys
    import numpy as np
    import networkx as nx
    import scipy as sp

    print(f"NetworkSampler v{__version__}")
    print(f"Space-filling sampling designs for graphs")
    print()
    print(f"Author:  Emiliano del Gobbo")
    print(f"Paper:   del Gobbo E., Fontanella L., Ippoliti L., Di Zio S., Fontanella S., Cucco A.")
    print(f"         https://doi.org/10.1007/s11634-026-00670-z")
    print(f"Source:  https://github.com/edgresearch/pylib_networksampler")
    print(f"License: LGPL-3.0")
    print()
    print(f"Python:     {sys.version.split()[0]}")
    print(f"NumPy:      {np.__version__}")
    print(f"NetworkX:   {nx.__version__}")
    print(f"Scipy:      {sp.__version__}")