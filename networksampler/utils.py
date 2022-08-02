import numpy as np
import networkx as nx
from scipy.sparse import csr_matrix
from scipy.sparse.csgraph import shortest_path


def compute_shortest_length_paths_matrix(A: np.ndarray):
    """
    Compute the shortest length path matrix

    Parameters
    ----------
        A : numpy.ndarray
            The graph adjacency matrix

    Returns
    -------
        numpy.array(dtype=int)
            The shortest length path matrix, 2D array containing data with `int` type.

    Examples
    --------
    Here we use the function to generate the matrix, from `A` adjacency matrix:

    >>> import networksampler
    >>> D = networksampler.utils.compute_shortest_length_paths_matrix(A)
    >>> D
    array([ 0.30220482,  0.86820401,  0.1654503 ,  0.11659149,  0.54323428]) # random
    """

    graph = csr_matrix(A)
    dist_matrix = shortest_path(csgraph=graph, directed=False)

    return dist_matrix


def generate_random_network(nodes_num=1000):
    """
    Generate a random network with unweighted and undirected edges. The main purpose of this function is as test tool.

    :param int nodes_num: Number of nodes in the network
    :return: Adjacency matrix
    :rtype: (numpy.ndarray)
    """

    A = np.triu(np.random.randint(2, size=(nodes_num,nodes_num)), 1)
    A = A + A.T

    return A

def nodes_centrality_measures(A):

    """
    This function extracts from an adjacency matrix dictionaries of several centrality measures: "degree", "closeness", "eigenvector", "betweeness".

    Parameters
    ----------
        A : numpy.ndarray
            The graph adjacency matrix

    Returns
    --------
        (dictionary, dictionary, dictionary, dictionary,)
            A tuple of dictionaries matching in order: "degree", "closeness", "eigenvector", "betweeness".
    """

    G = nx.from_numpy_array(A)

    node_pageranks = nx.pagerank(G)
    node_degree = nx.degree_centrality(G)
    node_clos = nx.closeness_centrality(G)
    node_betw = nx.betweenness_centrality(G)

    return node_pageranks, node_degree, node_clos, node_betw

