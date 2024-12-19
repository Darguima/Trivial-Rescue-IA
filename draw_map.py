import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from typing import Literal

from map import Map

def draw_map(map: Map, map_type: Literal["matrix", "real"] = "matrix", print_progress: bool = True):
  if not print_progress:
    print = lambda *args, **kwargs: None

  G = nx.Graph()

  print("Preparing to draw the map.", end="\r")
  for city in map.get_all_cities():
    print(f"Adding {city['name']} to the map.", end="\r")

    city_id = city["id"]

    draw_type = "map_coords" if map_type == "real" else "matrix_coords"
    x, y = city[draw_type]
    G.add_node(str(city_id), pos=(x, y), place_data=city, name=city['name'])

    for neighbor_id in city["neighbors"]["land"]:
      road = map.get_routes_between_cities(city_id, neighbor_id)["land"]
      G.add_edge(str(city_id), str(neighbor_id), route_data=road)

  print("Map drawn.                           ", end="\r")

  pos = nx.get_node_attributes(G, 'pos')

  place_sizes = [G.nodes[node]["place_data"]['population'] / 5000 for node in G.nodes]  # Adjust size by population
  place_colors = ["r" if G.nodes[node]["place_data"]['capital_info'] != None else 'b' for node in G.nodes]

  speed_colors = {50: "g", 90: "y", 100: "m", 120: "r"}
  route_colors = [speed_colors[G.edges[edge]["route_data"]["max_speed"]] for edge in G.edges]  # Adjust size by population

  nx.draw_networkx_nodes(G, pos, node_color=place_colors,node_size=place_sizes, alpha=0.6)
  nx.draw_networkx_edges(G, pos, edge_color=route_colors, width=3, alpha=0.5)

  labels = nx.get_node_attributes(G, 'name')
  nx.draw_networkx_labels(G, pos, labels, font_size=12)

  # Create legend for edges
  plt.legend(
    handles=[
      Line2D([0], [0], marker='o', color='w', markerfacecolor="r", markersize=10, alpha=0.6, label="Capital"),
      Line2D([0], [0], marker='o', color='w', markerfacecolor="b", markersize=10, alpha=0.6, label="Non-Capital"),
      Line2D([0], [0], color="g", lw=3, alpha=0.5, label="50 km/h"),
      Line2D([0], [0], color="y", lw=3, alpha=0.5, label="90 km/h"),
      Line2D([0], [0], color="m", lw=3, alpha=0.5, label="100 km/h"),
      Line2D([0], [0], color="r", lw=3, alpha=0.5, label="120 km/h")
    ],
    title="Legend",
    bbox_to_anchor=(0.05, 0.3),     # Fine-tune the legend position (x, y)
    borderaxespad=0.0             # Padding between the legend and the plot
  )

  # Clean up plot to remove axis and spines
  plt.gca().set_xticks([])
  plt.gca().set_yticks([])
  plt.gca().spines['top'].set_visible(False)
  plt.gca().spines['right'].set_visible(False)
  plt.gca().spines['bottom'].set_visible(False)
  plt.gca().spines['left'].set_visible(False)
  
  plt.show()
