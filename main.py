import sys
import numpy as np
import time
from tqdm import tqdm
import pandas as pd
import networkx as nx
import warnings
warnings.filterwarnings("ignore")
sys.setrecursionlimit(10**7)

from loader import *
from utils import *
from parser_args import *
from apsp import *

if __name__ == '__main__':

  ######################################################
  # Parameters to setup
  ######################################################
  args = parse_args()
  directed = args.d
  input_file_path = args.i
  n_k = args.k + 1
  sk = ''
  if n_k > 100:
    sk = 'max'
  else:
    sk = str(args.k)
  per_step = args.p
  # print(f'# args.o: {args.o}')
  

  ######################################################
  # Load a network
  ######################################################
  if (args.r == True):
    A, n, m = load_networks(input_file_path)
    print(f'# [{input_file_path}]- |N|: {n}, |E|: {m}')
  else:
    A, n, m = load_networkx_pickle(input_file_path)
    print(f'# [{input_file_path}]- |N|: {n}, |E|: {m}')

  if is_disconnected_graph(A.tolist()):
    print(f'# {input_file_path} is disconnected graph.')

  ######################################################
  # Do experiments
  ######################################################
  runtimes = []
  if (args.m == 'i'): 
    print(f'# compute I-AORM [{input_file_path}]: {sk}-order')
    if per_step == True:    
      for i_k in pit(range(2, n_k), color = 'green'):
        start = time.perf_counter()
        D = apsp_AormIterator(A, k=i_k, method = 'edge') 
        finish = time.perf_counter() 
        i_aorm_time = round(finish-start, 3)
        runtimes.append(i_aorm_time)
    else:
      start = time.perf_counter()
      D = apsp_AormIterator(A, k=-1, method = 'edge') 
      finish = time.perf_counter() 
      i_aorm_time = round(finish-start, 3)
      runtimes.append(i_aorm_time)
    if (args.o == True):
      print('# All-pairs shortest paths distance matrix')
      print(D)
    print(f'# I-AORM completed [{input_file_path}]: {sk}-order, {runtimes} secs')    
  elif (args.m == 'm'):
    runtimes.clear()
    print(f'# compute M-AORM [{input_file_path}]: {sk}-order')
    A = np.array(A, dtype=float)
    if per_step == True:          
      for i_k in pit(range(2, n_k), color = 'green'):
        start = time.perf_counter()
        D = apsp_AormIterator(A, k=i_k, method = 'matmult') 
        finish = time.perf_counter()
        p_aorm_time = round(finish-start, 3)
        runtimes.append(p_aorm_time)
    else:
      start = time.perf_counter()
      D = apsp_AormIterator(A, k=-1, method = 'matmult') 
      finish = time.perf_counter()
      p_aorm_time = round(finish-start, 3)
      runtimes.append(p_aorm_time)
    if (args.o == True):
      print('# All-pairs shortest paths distance matrix')
      print(D)          
    print(f'# M-AORM completed [{input_file_path}]: {sk}-order, {runtimes} secs' )    
  elif (args.m == 'v'):
    runtimes.clear()
    print(f'# compute V-BFS [{input_file_path}]: {sk}-order')    
    if per_step == True:
      max_order = 1          
      for i_k in tqdm(range(2, n_k)):
        start = time.perf_counter()
        D, max_order = apsp_inc_bfs_matrix(A, i_k)        
        finish = time.perf_counter()
        v_bfs_time = round(finish-start, 3)
        runtimes.append(v_bfs_time)
        print(f'# BFS max-order: {max_order}')
    else:
        start = time.perf_counter()
        D = apsp_bfs_matrix(A) 
        finish = time.perf_counter()
        v_bfs_time = round(finish-start, 3)
        runtimes.append(v_bfs_time)
    if (args.o == True):
      print('# All-pairs shortest paths distance matrix')
      print(D)
    print(f"# V-BFS [{input_file_path}, k={n_k-1}]: {runtimes}")    
  elif (args.m == 'p'):
    runtimes.clear()
    A = make_undirected(A)
    if is_disconnected_graph(A.tolist()):
      print(f'# {input_file_path} is disconnected graph.')
    else: 
      print(f'# compute P-SM [{input_file_path}]: {sk}-order')    
      start = time.perf_counter()
      D = apsp_seidel(A, len(A))
      finish = time.perf_counter()
      p_sm_time = round(finish-start, 3)
      runtimes.append(p_sm_time)
    if (args.o == True):
      print('# All-pairs shortest paths distance matrix')
      print(D)      
      print(f"# P-SM [{input_file_path}, k={n_k-1}]: {runtimes}")       
  elif (args.m == 'x'):
    if (directed):
      G = nx.from_pandas_adjacency(pd.DataFrame(A), create_using=nx.DiGraph)
    else:
      G = nx.from_pandas_adjacency(pd.DataFrame(A))
    G.name = input_file_path
    print(nx.info(G))
    runtimes.clear()
    if per_step == True:
      for i in pit(range(1, n_k), color = 'cyan'):
        start = time.perf_counter()
        path = dict(nx.all_pairs_shortest_path(G, i))
        finish = time.perf_counter()
        runtime = round(finish-start, 3)
        runtimes.append(runtime)
      print(f'# Incremental NX APSP [{input_file_path}, k={n_k-1}]: {runtimes} secs')
    else:
      start = time.perf_counter()
      path = dict(nx.all_pairs_shortest_path(G))
      finish = time.perf_counter()
      runtime = round(finish-start, 3)
      runtimes.append(runtime)
      print(f'# NX APSP [{input_file_path}]: {runtimes} secs')