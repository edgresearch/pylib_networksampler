Tutorial
========

This tutorial provides a step-by-step guide to using NetworkSampler for
space-filling sampling on networks and semi-supervised node classification
via label propagation.

Package information
-------------------

Start by checking the installed version and dependencies:

.. code-block:: python

    import networksampler
    networksampler.info()


Generating a test network
-------------------------

NetworkSampler includes a utility to generate random networks for testing.
For a more realistic scenario, we use NetworkX to generate a network with
two communities:

.. code-block:: python

    import networkx as nx
    import numpy as np

    # Generate a network with 1000 nodes and two communities
    G = nx.gaussian_random_partition_graph(1000, 500, 100, 0.20, 0.1)
    A = nx.adjacency_matrix(G).todense()

    print(f"Nodes: {A.shape[0]}")
    print(f"Edges: {int(np.sum(A) / 2)}")


Computing the shortest path matrix
-----------------------------------

The space-filling algorithm operates on geodesic distances between nodes.
You can precompute this matrix once and reuse it across multiple sampling runs:

.. code-block:: python

    D = networksampler.compute_shortest_length_paths_matrix(A)

    print(f"Matrix shape: {D.shape}")
    print(f"Max distance: {D.max():.0f}")
    print(f"Mean distance: {D.mean():.2f}")


Space-filling sampling
----------------------

The core function ``sa_sampling`` selects a set of seed nodes that are
well spread across the network, minimizing the coverage criterion via
simulated annealing:

.. code-block:: python

    # Sample 30 nodes (3% of 1000)
    nodes, cost = networksampler.sa_sampling(A, 30, p=-4, q=4, r=0.1, D=D)

    print(f"Sampled nodes: {nodes}")
    print(f"Coverage cost: {cost:.4f}")

The parameters ``p`` and ``q`` control the coverage criterion. The paper
recommends ``p=-4`` and ``q=4`` as they generally achieve the best accuracy.
The parameter ``r`` is the cooling rate for simulated annealing.

If you have a precomputed shortest path matrix, pass it via the ``D``
parameter to avoid recomputing it.

For reproducible results, use the ``random_seed`` parameter:

.. code-block:: python

    nodes, cost = networksampler.sa_sampling(
        A, 30, p=-4, q=4, r=0.1, D=D, random_seed=42
    )


Comparing with other sampling strategies
-----------------------------------------

NetworkSampler also provides centrality-based random sampling through
``node_random_sample``. You can use this to compare the space-filling
design against other strategies:

.. code-block:: python

    # Random sample proportional to degree centrality
    nodes_degree = networksampler.node_random_sample(A, 30, measure="degree")

    # Random sample proportional to betweenness centrality
    nodes_betw = networksampler.node_random_sample(A, 30, measure="betweenness")

    # Random sample proportional to closeness centrality
    nodes_close = networksampler.node_random_sample(A, 30, measure="closeness")

Available centrality measures are: ``degree``, ``closeness``, ``betweenness``,
and ``eigenvector``.


Two-phase sampling for large networks
--------------------------------------

For networks larger than 5000 nodes, the full shortest path matrix becomes
expensive to compute and store. The ``sa_sampling_twophases`` function
addresses this with a two-phase procedure:

1. First, a subgraph is sampled using centrality-based node selection
2. Then, the space-filling design is applied on the subgraph

.. code-block:: python

    nodes, cost = networksampler.sa_sampling_twophases(
        A, ns=10, p=-4, q=4, r=0.1,
        centrality_measure="betweenness",
        first_phase_sample_fraction=0.2
    )

    print(f"Sampled nodes: {nodes}")
    print(f"Coverage cost: {cost:.4f}")

The ``first_phase_sample_fraction`` controls the fraction of nodes retained
in the first phase (default: 0.1). The ``centrality_measure`` parameter
determines how nodes are selected in the first phase.


Computing node centrality measures
-----------------------------------

The utility function ``nodes_centrality_measures`` computes multiple
centrality metrics for all nodes in the network:

.. code-block:: python

    from networksampler.utils import nodes_centrality_measures

    pagerank, degree, closeness, betweenness = nodes_centrality_measures(A)

    # Example: top 5 nodes by betweenness centrality
    top5 = sorted(betweenness, key=betweenness.get, reverse=True)[:5]
    print(f"Top 5 nodes by betweenness: {top5}")


Label propagation example
--------------------------

Here is a complete example combining NetworkSampler with label propagation:

.. code-block:: python

    import networkx as nx
    import numpy as np
    import networksampler

    # 1. Generate a network with two communities
    G = nx.gaussian_random_partition_graph(500, 250, 50, 0.15, 0.05)
    A = nx.adjacency_matrix(G).todense()

    # 2. Assign ground truth labels based on community membership
    partition = G.graph['partition']
    labels = np.zeros(500, dtype=int)
    for i, community in enumerate(partition):
        for node in community:
            labels[node] = i

    # 3. Select seeds using space-filling design
    seeds, cost = networksampler.sa_sampling(A, 15, p=-4, q=4, r=0.1)

    # 4. Label propagation using the graph Laplacian
    n = A.shape[0]
    W = np.array(A, dtype=float)
    D_diag = np.diag(W.sum(axis=1).A1 if hasattr(W.sum(axis=1), 'A1') else W.sum(axis=1))
    L = D_diag - W

    # Partition into unlabeled (u) and seed (s) nodes
    u_mask = np.ones(n, dtype=bool)
    u_mask[seeds] = False
    u_idx = np.where(u_mask)[0]
    s_idx = seeds

    Luu = L[np.ix_(u_idx, u_idx)]
    Lus = L[np.ix_(u_idx, s_idx)]
    fs = labels[s_idx].astype(float)

    # Solve for unlabeled nodes
    fu = np.linalg.solve(Luu, -Lus @ fs)
    predicted = (fu >= 0.5).astype(int)

    # 5. Evaluate accuracy
    accuracy = np.mean(predicted == labels[u_idx])
    print(f"Classification accuracy: {accuracy:.4f}")
