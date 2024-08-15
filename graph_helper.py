"""
This module provides a set of helper functions, to:
voronoi_to_edges: generate collection of edges defining a planar graph.
edges_planar: verifies if the given set of edges defines a planar graph

Requirements
------------

Package networkx https://networkx.org/ which can be installed via PIP.
Package scipy https://scipy.org/  which can be installed via PIP.
Package 
Python 3.7 or higher.





Notes
-----
This module provided as material for the phase 2 project for DM857, DS830 (2023). 
"""

import numpy as np
import networkx as nx
from scipy.spatial import Voronoi
from typing import List, Optional, Dict,Tuple 
def voronoi_to_edges(minpoints:int,npoints:Optional[int]=0)->Tuple[List[Tuple[int,int]],Dict[int,Tuple[float,float]]]:
  '''
   Generates a random planar graph containing at least minpoints (based on the Voronoi graph)

   Parameters:
   ----------
   minpoints: Minimal number of points requested for the graph
   npoints: Number of points in the Voronoi graph generation
   
   Return: Tuple[edges,coord_map]
   ----------
   edges: List[(int,int)]
      List containing the edges (Tuples of 2 vertices) forming the 2D surface for the simulation.
   coord_map: Dict[int:(float,float)]
      Dictionary containing the coordinate of each vertex (expressed as a tuple of float in [0,1]x[0,1])
  '''
  if(minpoints<4):
     raise Exception("voronoi_to_edges, the number of points must be larger than 3")
  if(npoints<4):
     npoints=minpoints
  points=np.random.rand(npoints,2)
# we get the voronoi diagram
  vor = Voronoi(points)
# storage variable
  res=[]
  map={}
  jj=0
# Add an edge for each ridge in the Voronoi diagram that connects two points in the range [0,1] 
  for simplex in vor.ridge_vertices:
      if -1 not in simplex:
          i, j = simplex
          p = vor.vertices[i]
          q = vor.vertices[j]
          if 0 <= p[0] <= 1 and 0 <= p[1] <= 1 and 0 <= q[0] <= 1 and 0 <= q[1] <= 1:
              if tuple(p) not in map:
                 map[tuple(p)]=jj
                 jj+=1
              if tuple(q) not in map:
                 map[tuple(q)]=jj
                 jj+=1
              res.append((tuple(p), tuple(q)))
  if len(map) < minpoints:
   return voronoi_to_edges(minpoints, npoints+1)
  else:
   return [(map[i[0]],map[i[1]]) for i in res],{v: k for k, v in map.items()}
  

def edges_planar(edges=List[Tuple[int,int]])-> bool:
  '''  Verifies if the graph defined by the edges is planar
  Parameters:
   ----------
  edges: List[(int,int)]
      List containing the edges (Tuples of 2 vertices) forming the graph.

  Return: Bool

    '''
  return nx.is_planar(nx.Graph(edges))