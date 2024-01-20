import csv
from johnson import johnson
from adjacency_list_graph import AdjacencyListGraph
from dijkstra import dijkstra



def my_data(filename):

    my_list = []

    with open(filename) as dataset:
        dataset_reader = csv.reader(dataset, delimiter=",")
        for row in dataset_reader:
            my_list.append(row)
            #ID_counter +=1
        return my_list

data_list = my_data("London Underground data.csv")
for row in data_list:
    print(row)


ID_counter1 = 0
vertices = {}
edges = []
#vertices
for row in data_list:
    line, start_stations, end_stations, duration = row[:4]

    if start_stations not in vertices:
        vertices[start_stations] = ID_counter1 #setting the value of keys(stations) as the ID numbers
        ID_counter1 += 1

#edges
for row in data_list:
    line, start_stations, end_stations, duration = row[:4]
    if end_stations:
        start_stations_id = vertices[start_stations] #assigning the dict values to the keys to the variable here
        end_stations_id = vertices[end_stations]

        #adding the edge to the list
        edges.append((start_stations, end_stations, int(duration)))


for vertice in vertices:
    print(vertice)

for edge in edges:
    print(edge)



#converting the vertices dict to list

vertices_list = list(vertices.items())
print(vertices_list)




#initializing the graph

graph1 = AdjacencyListGraph(len(vertices), False, True)
for edge in edges:
    start_station_id = vertices[edge[0]]
    end_station_id = vertices[edge[1]]
    duration = edge[2]

    # Check if the edge already exists before inserting
    if not graph1.has_edge(start_station_id, end_station_id):
        graph1.insert_edge(start_station_id, end_station_id, duration)

    # Since this is an undirected graph, insert the reverse edge as well
    if not graph1.has_edge(end_station_id, start_station_id):
        graph1.insert_edge(end_station_id, start_station_id, duration)




# Funtion to initialize dijsktra algorithm

def dijkstra1 (graph1, start_station, target_station):

    valid_stations = all(station in vertices for station in [start_station, target_station])

    if valid_stations:

        start_station_index = vertices[start_station]
        target_station_index = vertices[target_station]

        d, pi = dijkstra(graph1, start_station_index)
        if pi[target_station_index] is not None:
            path = []
            current_node = target_station_index
            while current_node is not None:
                path.insert(0,list(vertices.keys())[current_node]) #if the path doesnt recognise int, put the keys here
                current_node = pi[current_node]

            print(f"Shortest path from '{start_station}' to '{target_station}': {'->'.join(path)}")
            print(f"Total duration: {d[target_station_index]} minutes")
        else :

            print("No path found")


    # we pass the start and target stations as arguments in the final statement

    else:
        print("invalid station name")



start_station = input("Enter your station")
target_station = input("Enter your destination")
dijkstra1(graph1, start_station, target_station)