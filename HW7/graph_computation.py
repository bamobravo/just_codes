import provided
import math
import random
import numpy as np

#initializing variables
# word_data = provided.create_vectors("./datasets/word_data.npy")
# articles = provided.open_file("./datasets/articles_index_20199.pkl")
# transform_matrix = np.load("./datasets/transform_matrix.npy").T

word_data = provided.create_vectors("./data/word_data.npy")
articles = provided.open_file("./data/articles_index_20199.pkl")
transform_matrix = np.load("./data/transform_matrix.npy").T

class Graph:
	"""docstring for Graph"""
	def __init__(self,index_file,data_file):
		"""
		build the graph by calling make_graph of the provided class
		index_file title list
		data_file  file containing article mapping information
		"""
		self.graph_data = provided.make_graph(index_file,data_file)

	def compute(self,graph_operation,node_operation):
		"""
		A higher order function that separate graph operation from node operation
		graph_operation an operation to be performed on the whole graph
		node_operation an function that is perform a node of the graph

		"""
		return graph_operation(self.graph_data,node_operation)

def average(graph_data,node_operation):
	"""
	A graph operation that calulate average of values
	"""
	result =0;
	for title in graph_data:
		result+=node_operation(graph_data[title])
	return result/len(graph_data)

def maximum(graph_data,node_operation):
	"""
	this is a graph operation that calculates the maximum value
	graph_data: a dictionary of article title and node
	node_operation: the node operation to apply the maximum operation on

	"""
	# initialize to the minimum obtainable value first
	result=0
	for title in graph_data:
		node_value = node_operation(graph_data[title])
		if node_value > result:
			result= node_value

	return result

def calculate_out_degree(node):
	"""
	calculate the out degree of a node
	node: the node to calculate the out degree
	"""
	return len(node.get_out_neighbors())

def calculate_total_degree(node):
	"""
	calculate the total degree of a node
	node: the node to calculate the total degree
	"""
	return len(node.get_in_neighbors()+node.get_out_neighbors())

def build_vector_dictionary(word_data,graph_data,transform_matrix):
	"""
	This function build a dictionary of article title and the corresponding vector
	word_data: the vector list
	graph_data: the graph_representation
	"""
	article_vector={}
	for (index,article) in enumerate(graph_data):
		if not word_data[index].all():
			continue
		article_vector[article]=provided.np.dot(word_data[index],transform_matrix)
	return article_vector

def average_pca(graph_data,node_operation):
	"""
	Calculate the average pca
	graph_data: the graph representation
	node_operation: the function for getting node values
	"""
	# word_data = provided.create_vectors("./datasets/word_data.npy")
	# articles = provided.open_file("./datasets/articles_index_20199.pkl")
	# transform_matrix = np.load("./datasets/transform_matrix.npy").T
	article_vector=build_vector_dictionary(word_data,graph_data,transform_matrix)
	value_sum=0;
	for article in graph_data:
		value_sum+=node_operation(article,article_vector,graph_data)
	return value_sum/len(graph_data)

def compute_random_node_distance(article,vectors,graph_data):
	vector1=vectors[article]
	vector2=choose_article_vector(article,vectors,graph_data,True)
	if isinstance(vector2,int) and vector2==0:
		return 0
	return compute_euclidean_distance(vector1,vector2)

def compute_random_neighbor_distance(article,vectors,graph_data):
	vector1=vectors[article]
	vector2=choose_article_vector(article,vectors,graph_data)
	if isinstance(vector2,int) and vector2==0:
		return 0
	return compute_euclidean_distance(vector1,vector2)

	
def choose_article_vector(article,vectors,graph_data,all=False):
	neighbor = [graph_data[x] for x in graph_data if graph_data[x].get_name()!=article ] if all else graph_data[article].get_out_neighbors()
	if len(neighbor)==0:
		return 0
	position =random.randint(0,len(neighbor)-1)
	name = neighbor[position].get_name()
	if not name in vectors or not vectors[name].all():
		return False
	return vectors[name]

def compute_euclidean_distance(vector1,vector2):
	"""
	This function compute the euclidean distance between two vectors
	vector1: the first vector
	vector2: the second vector
	"""
	summation=0
	for index in range(len(vector1)):
		summation+=(vector1[index]-vector2[index])**2
	return math.sqrt(summation)

# g = Graph('./datasets/test_index_10.pkl', './datasets/articles_with_links_10.pkl')
# print("Graph with 10 nodes")
# print("Average out-degree:", g.compute(average, calculate_out_degree))
# print("Maximum out-degree:", g.compute(maximum, calculate_out_degree))
# print("Average degree:", g.compute(average, calculate_total_degree))
# print("Maximum degree:", g.compute(maximum, calculate_total_degree))
 
# g = Graph('./datasets/test_index_13.pkl', './datasets/articles_with_links_13.pkl')
# print("Graph with 13 nodes")
# print("Average out-degree:", g.compute(average, calculate_out_degree))
# print("Maximum out-degree:", g.compute(maximum, calculate_out_degree))
# print("Average degree:", g.compute(average, calculate_total_degree))
# print("Maximum degree:", g.compute(maximum, calculate_total_degree))

# g = Graph('./datasets/articles_index_20199.pkl', './datasets/articles_with_links_20199.pkl')
# print(g.compute(average_pca, compute_random_node_distance))
# print(g.compute(average_pca, compute_random_neighbor_distance))
g = Graph('./data/articles_index_20199.pkl', './data/articles_with_links_20199.pkl')
print(g.compute(average_pca, compute_random_node_distance))
print(g.compute(average_pca, compute_random_neighbor_distance))