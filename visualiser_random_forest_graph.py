"""
This module provides Visualiser, a class for displaying the status of a collection of edges and sites forming the graph of a simulation.

Requirements
------------
Package matplotlib https://matplotlib.org/ which can be installed via PIP.
Package networkx https://networkx.org/ which can be installed via PIP.
Python 3.7 or higher.



Notes
-----
This module provided as material for the phase 2 project for DM857, DS830 (2023). 
"""

from __future__ import annotations # to use a class in type hints of its members
from typing import List, Optional, Dict
import matplotlib.pyplot as plt
import networkx as nx

class Visualiser:
  """Each instance of this class maintains a window where it displays the status of a given collection of edges and sites forming the graph of a simulation."""
  colour_map={0:plt.cm.Greens,1:plt.cm.Reds}
  no_colour=plt.cm.Greys(100)
  def __init__(self:Visualiser, 
               edges:List[(int,int)],
               Colour_map: Optional[Dict[int:(int,int)]]={},
               pos_nodes: Optional[Dict[int:Tuple[float,float]]]={},
               node_size : Optional[int] = 100,
               vis_labels: Optional[bool] = False,
               window_title : Optional[str]=None)->None:
    """
    Parameters
    ----------
    edges: List[(int,int)]
      List containing the edges (Tuples of 2 vertices) forming the 2D surface for the simulation.
    Colour_map: Dict[int:int]
      Dictionary containing the identity and color of each node
        Colour, expressed as a integer from -256(full-red) to 256(full-green)
    pos_nodes: Optional[Dict[int:Tuple[float,float]]]={},
      Dictionary of key:{x,y} positions identifing the location of each node
    node_size: int, default 100
      Control the size of the drawn nodes
    vis_labels: Optional[bool] = False,
      switch to visualize/hide the labels (used to track the species)
    window_title : Optional[str], default = None
      The title of the window.
    """
    self._edges = edges
    self._vis_labels = vis_labels
    self._H = nx.Graph(self._edges)  # create a Graph dict mapping nodes to nbrs
    self._cmap = [self.no_colour]*self._H.number_of_nodes()
    self._lnodes_edges =[]
    self._window_title=window_title
    for key,val in Colour_map.items():
      if(val>0):
        self._cmap[list(self._H.nodes()).index(key)] = self.colour_map[0](val)
      else:
        self._cmap[list(self._H.nodes()).index(key)] = self.colour_map[1](-val)

    self._node_size = node_size
    # Need to create a layout when doing
    # separate calls to draw nodes and edges
    if(pos_nodes):
      self._pos = pos_nodes
    else:
      self._pos = nx.spring_layout(self._H,k=2)

    self._fig, ax = plt.subplots()
    # title
    if(self._window_title):
      self._fig.canvas.manager.set_window_title(self._window_title)    
    # listen to close events
    self._is_open = True
    def on_close(_)->None:
      self._is_open = False
    self._fig.canvas.mpl_connect('close_event', on_close )
   
  def is_open(self:Visualiser) -> bool:
    """
    Whether the window managed by the visualiser is open or not.
    """
    return self._is_open

  def close(self:Visualiser) -> None:
    """Closes the window destroying this visualiser."""
    plt.close()

  def wait_close(self:Visualiser):
    """
    Suspends the current execution until the visualiser window is manually closed by the user.
    """
    plt.show()

  def update_node_colours(self:Visualiser,Colour_map:Dict[int:int]) -> None:
    """Informs this visualiser that the status of its colours has been updated."""
    if self.is_open() :
      self._cmap = [self.no_colour]*self._H.number_of_nodes()
      for key,val in Colour_map.items():
        if(val>0):
          self._cmap[list(self._H.nodes()).index(key)] = self.colour_map[0](val)
        else:
          self._cmap[list(self._H.nodes()).index(key)] = self.colour_map[1](-val)
    self._replot()

  def update_node_edges(self:Visualiser,lab_map:List[int]) -> None:
    """Informs this visualiser that the status of its labels has been updated."""
    self._lnodes_edges=lab_map
    self._replot()

  def _replot(self:Visualiser) -> None:
    '''Plotting facility'''
    plt.clf()
    nx.draw_networkx_nodes(self._H, self._pos,
                       node_color = self._cmap, node_size = self._node_size,linewidths=1)
    nx.draw_networkx_edges(self._H, self._pos, arrows=False)
    if(self._lnodes_edges):
       lcmap=[self._cmap[i] for i in self._lnodes_edges]
       nx.draw_networkx_nodes(self._H,self._pos,node_color = lcmap,
                              nodelist=self._lnodes_edges, node_size = self._node_size, edgecolors="blue",linewidths=2)
    self._fig.canvas.draw()
    self._fig.canvas.flush_events()
    plt.show(block=False)
    plt.savefig('generic_graph_1.pdf')
    plt.pause(0.2)

  