import numpy as np

def pit(it, *pargs, **nargs):
  import enlighten
  global __pit_man__
  try:
      __pit_man__
  except NameError:
      __pit_man__ = enlighten.get_manager()
  man = __pit_man__
  try:
      it_len = len(it)
  except:
      it_len = None
  try:
      ctr = None
      for i, e in enumerate(it):
          if i == 0:
              ctr = man.counter(*pargs, **{**dict(leave = False, total = it_len), **nargs})
          yield e
          ctr.update()
  finally:
      if ctr is not None:
          ctr.close()


def make_adj_matrix(adj_list, diagonal = 0.0, start = 1) :
    n = len(adj_list)
    mat = np.zeros((n, n))
    for i in range(n) :
        mat[i, i] = diagonal
        for idx in adj_list[i]:
            mat[i, idx-start] = 1
    return mat

def make_undirected(A):
    return np.heaviside(np.maximum(A, A.T), 0)


def create_random_network(n_nodes, p=0.1, diagonal=0.0):
    if p > 0.5:
        A = np.ones((n_nodes, n_nodes))
    else:
        A = np.zeros((n_nodes, n_nodes))
    np.fill_diagonal(A, diagonal)

    n_edges = int(p * (n_nodes * n_nodes / 2))
    n_max = int(n_nodes * (n_nodes - 1) / 2)

    if p > 0.5:
        #n_deedges = int(((n_nodes - 1) * n_nodes) / 2) - n_edges
        n_deedges = int(( (n_nodes * n_nodes / 2 ) - n_edges))

        # print('create {0} edges... by removing {1} edges'.format(n_edges, n_deedges))
        deedge = 0
        i, j = 0, 0
        while True:
            if deedge >= n_deedges: return A
            j += 1
            if j >= n_nodes:
                i = (i + 1) % (n_nodes - 1);
                j = i + 1
            if A[i, j] == 0:
                continue
            elif p >= np.random.randint(1000) / 1000:
                A[i, j] = 0
                A[j, i] = 0
                deedge += 1


    else:
        # print('create {0} edges...'.format(n_edges))
        edge = 0
        i, j = 0, 0

        while True:
            if edge >= n_edges: return A
            j += 1
            if j >= n_nodes:
                i = (i + 1) % (n_nodes - 1);
                j = i + 1
            if A[i, j] == 1:
                continue
            elif p <= np.random.randint(1000) / 1000:
                A[i, j] = 1
                edge += 1



def create_network_with_n_centers(n_nodes, n_centers, randomness=0.0, n_edges=-1, diagonal=0.0, within_cluster=True, connected_centers = True):
    A = np.zeros((n_nodes, n_nodes))
    np.fill_diagonal(A, diagonal)
    if n_edges == -1:
        n_edges = n_nodes * 2
    n_per_center = int(n_nodes / n_centers)

    def cid2node(cid):
        return (cid * n_per_center) % n_nodes

    def find_center(n):
        return (int(n / n_per_center)) % n_centers

    if connected_centers:
        for c_id in range(n_centers):
            A[cid2node(c_id), cid2node((c_id + 1) % n_centers)] = 1

    for _ in range(n_edges):
        node = np.random.randint(n_nodes)
        center = cid2node(find_center(node))
        #if node == center:
        #    center = (center + n_per_center) % n_nodes

        if np.random.random() < randomness:
            if within_cluster:
                center = (center + np.random.randint(n_per_center)) % n_nodes
            else:
                center = (center + np.random.randint(n_centers) * n_per_center + np.random.randint(
                    n_per_center)) % n_nodes

        A[node, center] = 1

    return A


def create_network_with_n_clusters(n_nodes, n_clusters, randomness=0.0, n_edges=-1, diagonal=0.0, random_jump=False):
    A = np.zeros((n_nodes, n_nodes))
    np.fill_diagonal(A, diagonal)

    def jump(n):
        if random_jump:
            return (n * 13 + 7) % n_nodes
        else:
            return n

    for node in range(n_clusters):
        A[jump(node % n_nodes), jump((node + 1) % n_nodes)] = 1
    n_nodes_in_cluster = n_nodes // n_clusters

    if n_edges < 0: n_edges = n_nodes
    for node in range(n_edges):
        node1 = node % n_nodes
        cluster = node1 // n_nodes_in_cluster
        if np.random.random() > randomness:
            node2 = (np.random.randint(n_nodes_in_cluster) + n_nodes_in_cluster * cluster) % n_nodes
        else:
            node2 = np.random.randint(n_nodes)
        A[jump(node1), jump(node2)] = 1

    return A


def create_cluster_ring(n_nodes, n_clusters, randomness=0.0, n_edges=-1, diagonal=0.0):
    A = np.zeros((n_nodes, n_nodes))
    np.fill_diagonal(A, diagonal)

    def jump(n):
        return (n * 13 + 7) % n_nodes

    for node in range(n_clusters):
        A[jump(node % n_nodes), jump((node + 1) % n_nodes)] = 1
    n_nodes_in_cluster = n_nodes // n_clusters

    if n_edges < 0: n_edges = n_nodes
    for node in range(n_edges):
        node1 = node % n_nodes
        cluster = node1 // n_nodes_in_cluster
        if np.random.random() > randomness:
            node2 = (np.random.randint(n_nodes_in_cluster) + n_nodes_in_cluster * cluster) % n_nodes
        else:
            node2 = (np.random.randint(n_nodes_in_cluster) + n_nodes_in_cluster * (
                    (cluster + 1) % n_clusters)) % n_nodes
        A[jump(node1), jump(node2)] = 1

    return A


def create_ring(n_nodes, diagonal=0.0):
    A = np.zeros((n_nodes, n_nodes))
    np.fill_diagonal(A, diagonal)

    for node in range(n_nodes):
        A[node, (node + 1) % n_nodes] = 1

    return A

def make_init_cost(adj_matrix) :
    n = len(adj_matrix)
    cost = adj_matrix.copy()
    for i in range(n):
        for j in range(n) :
            if cost[i,j] < 1:
                cost[i, j] = inf
    return cost