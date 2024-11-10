import networkx as nx
import matplotlib.pyplot as plt

from map import Map

def draw_map(map: Map):
  G = nx.Graph()

  print("Preparing to draw the map.")
  for place_id in map.get_all_places_ids():
    place = map.get_place_by_id(place_id)
    print(f"Adding {place['name']} to the map.")

    x, y = place['coords']
    G.add_node(int(place_id), pos=(x, y), place_data=place, name=place['name'])

    for neighbor_id in map.get_neighbors_ids_by_place_id(place_id)["land"]:
      route = map.get_route(place_id, neighbor_id)
      G.add_edge(place_id, neighbor_id, route_data=route["land"])

  pos = nx.get_node_attributes(G, 'pos')

  place_sizes = [G.nodes[node]["place_data"]['population'] / 5000 for node in G.nodes]  # Adjust size by population
  places_names = {node: G.nodes[node]['name'] for node in G.nodes}

  speed_colors = {50: "g", 90: "y", 100: "m", 120: "r"}
  route_colors = [speed_colors[G.edges[edge]["route_data"]["max_speed"]] for edge in G.edges]  # Adjust size by population

  nx.draw_networkx_nodes(G, pos, node_size=place_sizes, alpha=0.6)
  nx.draw_networkx_edges(G, pos, edge_color=route_colors, width=3, alpha=0.5)
  nx.draw_networkx_labels(G, pos, labels=places_names, font_size=8, font_color="black", verticalalignment='bottom')
  
  # Clean up plot to remove axis and spines
  plt.gca().set_xticks([])
  plt.gca().set_yticks([])
  plt.gca().spines['top'].set_visible(False)
  plt.gca().spines['right'].set_visible(False)
  plt.gca().spines['bottom'].set_visible(False)
  plt.gca().spines['left'].set_visible(False)
  
  plt.show()
