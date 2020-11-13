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
def getPosition(title,index_file):
	for (ind,x) in enumerate(index_file):
		if x[0]==title:
			return ind
	return False

visited = set()
def add_neighbors(all_list,title,index_file):
	# add the out node first
	position = getPosition(title,index_file)
	out_nodes = index_file[position][1]
	for tl in out_nodes:
		if tl in all_list:
			all_list[title].add_out_neighbor(all_list[tl])
			all_list[tl].add_in_neighbor(all_list[title])


def make_graph(index_file,data_file):
	# i need to use pickle here to load the structure in the file so i can work with it easily
	data_file = open_file(data_file);
	index_file = open_file(index_file);
	result={}
	for title in index_file:
		result[title]=Node(title)
	for title in result:
		add_neighbors(result,title,data_file)
	return result;

# dealing with the C part

def bfs(articles_to_node,start,end):
	start = start.lower().strip()
	end = end.lower().strip()
	if start not in articles_to_node:
		print('There is no Node corresponding to the start article title')
		exit()
	if end not in articles_to_node:
		print('There is no node corresponding to the destination article')
		exit()
	count=0
	queue = deque()
	tranversed = set()
	collectns = deque([articles_to_node[start]])
	while len(collectns) > 0:
		current = collectns.pop()
		if current.get_name() in tranversed:
			continue
		tranversed.add(current.get_name())
		if current.get_name().lower().strip()==end:
			return count
		out_nodes = current.get_out_neighbors()
		if len(out_nodes)==0:
			print('The two articles are not connect')
			exit()
		for tmp in out_nodes:
			if tmp.get_name().lower().strip() not in tranversed:
				collectns.appendleft(tmp)
		count+=1
	print('The two articles are not connect')
	exit()

def tranverseBfs(graph,start_node):
	queue = deque()
	tranversed = set()
	collectns = deque([start_node])
	while len(collectns) > 0:
		current = collectns.pop()
		if current.get_name() in tranversed:
			continue
		# this line is to make it an undirected graph
		out_nodes = current.get_out_neighbors()+current.get_in_neighbors()
		links = [x.get_name() for x in out_nodes]
		tranversed.add(current.get_name())
		if len(links)==0 or len(tranversed.difference(set(links)))==0:
			return tranversed
		for tmp in out_nodes:
			if tmp.get_name().lower().strip() not in tranversed:
				collectns.appendleft(tmp)
	return tranversed

def printMinMaxComponent(result):
	sortedResult= sorted(result,key=lambda x:len(x))
	minResult = sortedResult[0]
	maxResult = sortedResult[-1]
	print("Size of component with minimum node is ",len(minResult))
	print("printing articles in the minimum component")
	for x in minResult:
		print(x)
	print("Size of component with maximum node is ",len(maxResult))
	print("printing articles in the maximum component")
	for x in maxResult:
		print(x)


def connected_components(articles_to_node):
	# As stated inthe assignment, this variable will hold nodes that has not be found in a component
	notVisited = set(articles_to_node.keys())
	# this will be the list of sequences
	result = []
	# while all the node has been tried
	while len(notVisited)>0:
		node =articles_to_node[notVisited.pop()]
		current = tranverseBfs(articles_to_node,node)
		result.append(current)
		notVisited =notVisited.difference(current)
	size = [len(x) for x in result]
	print(result)
	printMinMaxComponent(result)
	return size,result
# print('Test 1')
# test_node = make_graph('./datasets/test_index_10.pkl', './datasets/articles_with_links_10.pkl')['8']
# print(test_node.get_name())
# for out_neighbor in test_node.get_out_neighbors():
#    print(out_neighbor.get_name())

test_node = make_graph('./datasets/test_index_10.pkl', './datasets/articles_with_links_10.pkl')
# ttmp =bfs(test_node,'0','2')
# print(ttmp)

sizes,components =connected_components(test_node)
exit()
# print('Test 2')
# test_node_2 = make_graph('./datasets/test_index_13.pkl', './datasets/articles_with_links_13.pkl')['L']
# print(test_node_2.get_name())
# for in_neighbor in test_node_2.get_in_neighbors():
#    print(in_neighbor.get_name())
