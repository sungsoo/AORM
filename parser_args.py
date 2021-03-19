import argparse

def parse_args():
  parser = argparse.ArgumentParser(description="AORM: Arbitrary-order reachability matrix framework")
  parser.add_argument('-m', nargs='?', default='i', help='Methods (i: i-aorm, p: p-aorm, v: v-bfs, s: p-sm)')
  parser.add_argument('-i', nargs='?', default='./datasets/synthetic/ba_graph_n500.gpickle', help='Input graph file path')
  parser.add_argument('-k', nargs='?', default=100, type=int, help='Reachability constraints (k-order)')
  parser.add_argument('-r', type=bool, default=False, help='Real-world network experiment')
  parser.add_argument('-d', type=bool, default=False, help='Directed (True) or undirected (False)')
  parser.add_argument('-p', type=bool, default=False, help='Computations per step unit')
  parser.add_argument('-o', type=bool, default=False, help='Print out the distance matrix')

  return parser.parse_args()