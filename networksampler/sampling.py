import numpy as np
import networkx as nx
from .utils import compute_shortest_length_paths_matrix


def sa_sampling(A: np.ndarray, ns: int, p=-4, q=4, r=0.1, D=None, random_seed=None):
    """
    This function a simulated annealing algorithm to extract a node sample, minimizing the geodesi distance and maximizing the network coverage.

    Parameters
    ----------
        A : numpy.ndarray
            The graph adjacency matrix. The graph must be unweighted (all the edges must be 1), undirected
            (the matrix must be symmetrical) and fully connected (a path from each node to each other node must exists).
            For networks larger than 5000 nodes, this process could be really slow. In case of larger networks, evaluate
            the usage of `sa_sampling_twophases`.
        ns : int
            The size of the sample to extract.
        p : int, optional
            The parameter p
        q : int, optional
            The parameter q
        r : float, optional
            The decay rate
        D : {None, numpy.ndarray}, optional
            A precomputed shortest path length matrix.
            Generating this matrix requires finding all the shortest path between each nodes couple,
            and could be a slow operation for large Adjacency matrix. With this parameter you can provide
            a cached matrix
        random_seed :  {None, int, array_like[ints], SeedSequence, BitGenerator, Generator}, optional
            This argument is supposed to be used for output reproducibility.
            A seed to initialize the `BitGenerator`. If None, then fresh,
            unpredictable entropy will be pulled from the OS. If an ``int`` or
            ``array_like[ints]`` is passed, then it will be passed to
            `SeedSequence` to derive the initial `BitGenerator` state. One may also
            pass in a `SeedSequence` instance.
            Additionally, when passed a `BitGenerator`, it will be wrapped by
            `Generator`. If passed a `Generator`, it will be returned unaltered.

    Returns
    ----------
        (numpy.array(dtype=int), int)
            The index array of the sampled nodes
    """

    # Defines the random number generator
    rng = np.random.default_rng(random_seed)

    t = 1
    N = A.shape[0]
    if D is None:
        D = compute_shortest_length_paths_matrix(A)
    S = np.arange(N)

    Sn = np.sort(rng.choice(S, ns, replace=False))
    Sp = np.delete(S, Sn)

    Dpn = np.power(D[Sn][:, Sp], p)
    dp = np.power(Dpn.sum(axis=0), 1 / p)
    Cpq = np.power(np.power(dp, q).sum(), 1 / q)  # TODO verificare

    # target function
    h = 1
    cont = 0

    # simulated annealing

    while h > 0:
        cont = cont + 1;

        h = 0
        for J in range(0, 30):

            pert = rng.choice(Sn, 1, replace=False)
            Sncandidate = Sn.copy()
            candidate = rng.choice(Sp, 1, replace=False)
            Sncandidate[Sncandidate == pert] = candidate
            Sncandidate.sort()

            Sp_new = np.delete(S, Sncandidate)
            Dpn = np.power(D[Sncandidate][:, Sp_new], p)
            dp = np.power(Dpn.sum(axis=0), 1 / p)
            Cpq_new = np.power(np.power(dp, q).sum(), 1 / q)  # TODO verificare

            if Cpq_new <= Cpq:
                prob = 1
            else:
                prob = np.exp((Cpq - Cpq_new) / t)

            if rng.random() <= prob:
                Sn = Sncandidate
                Sp = Sp_new
                Cpq = Cpq_new
                h = h + 1
        t = t - r * t
    return Sn, Cpq


def sa_sampling_twophases(A: np.ndarray, ns: int, p=-4, q=4, r=0.1, centrality_measure="betweenness",
                          first_phase_sample_fraction=0.1, D=None, random_seed=None):
    """
    This function a simulated annealing algorithm to extract a node sample, minimizing the geodesi distance and maximizing the network coverage.

    Parameters
    ----------
        A : numpy.ndarray
            The graph adjacency matrix. The graph must be unweighted (all the edges must be 1), undirected
            (the matrix must be symmetrical) and fully connected (a path from each node to each other node must exists)
        ns : int
            The size of the sample to extract
        p : int, optional
            The parameter p
        q : int, optional
            The parameter q
        r : float, optional
            The decay rate
        centrality_measure: {"degree", "closeness", "eigenvector", "betweeness"}, optional
            The centrality measure to use for the first phase node extraction
        ns_firstphase: float, optional
            The number of nodes to sample in the first phase, before applying the
            simulated annealing sampling in the second phase.
        D : {None, numpy.ndarray}, optional
            A precomputed shortest path length matrix.
            Generating this matrix requires finding all the shortest path between each nodes couple,
            and could be a slow operation for large Adjacency matrix. With this parameter you can provide
            a cached matrix
        random_seed :  {None, int, array_like[ints], SeedSequence, BitGenerator, Generator}, optional
            This argument is supposed to be used for output reproducibility.
            A seed to initialize the `BitGenerator`. If None, then fresh,
            unpredictable entropy will be pulled from the OS. If an ``int`` or
            ``array_like[ints]`` is passed, then it will be passed to
            `SeedSequence` to derive the initial `BitGenerator` state. One may also
            pass in a `SeedSequence` instance.
            Additionally, when passed a `BitGenerator`, it will be wrapped by
            `Generator`. If passed a `Generator`, it will be returned unaltered.

    Returns
    ----------
        (numpy.array(dtype=int), int)
            The index array of the sampled nodes
    """

    t = 1
    N = A.shape[0]
    if D is None:
        D = compute_shortest_length_paths_matrix(A)

    Siniz = node_random_sample(A, round(first_phase_sample_fraction*N), centrality_measure)
    Siniz.sort()
    D = D[Siniz, :][:, Siniz]


    N1 = D.shape[0]
    S = np.arange(N1)

    Sn = np.sort(np.random.choice(S, ns, replace=False))
    Sp = np.delete(S, Sn)

    Dpn = np.power(D[Sn][:, Sp], p)
    dp = np.power(Dpn.sum(axis=0), 1/p)
    Cpq = np.power(np.power(dp, q).sum(), 1/q) # TODO verificare

    # Target function
    h=1
    cont=0

    # simulated annealing
    while h > 0:
        cont = cont+1

        h = 0
        for J in range(0, 30):

            pert = np.random.choice(Sn, 1, replace=False)
            Sncandidate= Sn.copy()
            candidate= np.random.choice(Sp, 1, replace=False)
            Sncandidate[Sncandidate==pert] = candidate
            Sncandidate.sort()


            Sp_new = np.delete(S, Sncandidate)
            Dpn = np.power(D[Sncandidate][:,Sp_new], p)
            dp = np.power(Dpn.sum(axis=0), 1/p)
            Cpq_new = np.power(np.power(dp, q).sum(), 1/q) # TODO verificare

            if Cpq_new <= Cpq:
                prob=1
            else:
                prob = np.exp((Cpq-Cpq_new)/t)

            if np.random.random_sample() <= prob:
                Sn=Sncandidate
                Sp=Sp_new
                Cpq=Cpq_new
                h=h+1
        t=t-r*t
    return Siniz[Sn], Cpq


def node_random_sample(A:np.ndarray, k:int, measure="degree", random_seed=None):
    """
    This function extracts from an adjacency matrix a list of k nodes based on the centrality measure selected.

    Parameters
    ----------
        A : numpy.ndarray
            The graph adjacency matrix
        k : int
            The size of the sample to extract
        measure: {"degree", "closeness", "eigenvector", "betweeness"}, optional
            The centrality measure to use
        random_seed :  {None, int, array_like[ints], SeedSequence, BitGenerator, Generator}, optional
            This argument is supposed to be used for output reproducibility.
            A seed to initialize the `BitGenerator`. If None, then fresh,
            unpredictable entropy will be pulled from the OS. If an ``int`` or
            ``array_like[ints]`` is passed, then it will be passed to
            `SeedSequence` to derive the initial `BitGenerator` state. One may also
            pass in a `SeedSequence` instance.
            Additionally, when passed a `BitGenerator`, it will be wrapped by
            `Generator`. If passed a `Generator`, it will be returned unaltered.

    Returns
    ----------
        numpy.array(dtype=int)
            The index array of the sampled nodes
    """

    # Defines the random number generator
    rng = np.random.default_rng(random_seed)

    centralityOptions = {
        "degree": nx.algorithms.degree_centrality,
        "closeness": nx.algorithms.closeness_centrality,
        "betweenness": nx.algorithms.betweenness_centrality,
        "eigenvector": nx.algorithms.eigenvector_centrality,
    }

    if isinstance(measure, str):
        if measure not in centralityOptions:
            raise Exception("Not existing centrality measure")
        measureFunc = centralityOptions[measure]
    elif callable(measure):
        measureFunc = measure
    else:
        raise Exception("Not a valid centrality measure string or function")

    G = nx.from_numpy_array(A)

    z = measureFunc(G)
    p = np.array(list(z.values()))
    t = p / p.sum()

    return rng.choice(t.shape[0], k, p=t, replace=False)