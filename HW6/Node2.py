"""
Created on Fri Oct 23 07:06:38 2020

@author: Work
"""

import pickle
from collections import deque


class Node():
	"""This is the Node class for working on the graph"""
	def __init__(self, name):
		self.name = name
		self.in_neighbors=[]
		self.out_neighbors=[]
		self.in_degree =[]
		self.out_degree =[]
	def get_name(self):
		return self.name

	def get_in_neighbors(self):
		return self.in_neighbors

	def get_out_neighbors(self):
		return self.out_neighbors

	def add_in_neighbor(self,node):
		self.in_neighbors.append(node)

	def add_out_neighbor(self,node):
		self.out_neighbors.append(node)
        
        
        
def open_file(file_path):
   """
   Opens a pkl file and return its contents.
   """
   with open(file_path, 'rb') as handle:
       return pickle.load(handle)
 
    
def add_neighbors(title_index, visited_title, list_of_links):
    
    visited_node = title_index[visited_title]
    
    for x in list_of_links:
        if x in title_index:
            visited_node.add_out_neighbor(title_index[x])
            title_index[x].add_in_neighbor(visited_node)

def make_graph(index_file,data_file):
	# i need to use pickle here to load the structure in the file so i can work with it easily
	
    result = {}
    index_file = open_file(index_file)
    data_file = open_file(data_file)

    for x in index_file:
        result[x] = Node(x)
        
    for index in data_file:
        add_neighbors(result, index[0], index[1])     
        
    return result
 
def bfs(graph, start, end):
    # maintain a queue of paths
    queue = []
    # push the first path into the queue
    queue.append([start])
    while queue:
        # get the first path from the queue
        path = queue.pop(0)
        # get the last node from the path
        node = path[-1]
        # path found
        if node == end:
            return path
        # enumerate all adjacent nodes, construct a new path and push it into the queue
        for adjacent in graph.get(node, []):
            new_path = list(path)
            new_path.append(adjacent)
            queue.append(new_path)


# test_node = make_graph(indexfile, datafile)
# print (bfs(test_node, '1', '11'))    

indexfile = r'D:\COMP614\hw6_graph\test_index_10.pkl'
datafile  = r'D:\COMP614\hw6_graph\articles_with_links_10.pkl'


links = [('0', ['9'], 0),
         ('1', ['6'], 0),
         ('2', [], 0),
         ('3', ['4'], 0),
         ('4', ['3'], 0),
         ('5', [], 0),
         ('6', [], 0),
         ('7', ['6'], 0),
         ('8', ['1', '6', '7'], 0),
         ('9', ['2'], 0)]

# print('Test 1')
# test_node = make_graph(indexfile, datafile)['8']
# print(test_node.get_name())
# for out_neighbor in test_node.get_out_neighbors():
#     print(out_neighbor.get_name())
    
# print(test_node)   
    
ttmp =bfs(links,'0','2')
print(ttmp)