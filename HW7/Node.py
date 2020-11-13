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
	return false

visited = set()
def add_neighbors(node,title,index,index_file):
	# add the out node first
	if title in visited:
		return node
	visited.add(title)
	out_nodes = index_file[index][1]
	for tl in out_nodes:
		ttt = Node(tl)
		pos = getPosition(title,index_file)
		node.add_out_neighbor(add_neighbors(ttt,tl,pos,index_file))
	# add in add_neighbor
	for ind in index_file:
		if title in ind[1]:
			tt =Node(ind[0])
			pos = getPosition(ind[0],index_file)
			node.add_in_neighbor(add_neighbors(tt,ind[0],pos,index_file))
	return node

def make_graph(index_file,data_file):
	# i need to use pickle here to load the structure in the file so i can work with it easily
	data_file = open_file(data_file);
	index_file = open_file(index_file);
	result={}
	for (index,title) in enumerate(index_file):
		temp = Node(title)
		reference = index_file[index]
		temp = add_neighbors(temp,title,index,data_file)
		result[title]=temp
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
	count=1
	queue = deque()
	tranversed = set()
	collectns = deque([articles_to_node[start]])
	while len(collectns) > 0:
		current = collectns.pop()
		print(current.get_name())
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
				print(tmp.get_name())
				collectns.appendleft(tmp)
		count+=1
	print('The two articles are not connect')
	exit()


print('Test 1')
test_node = make_graph('./datasets/test_index_10.pkl', './datasets/articles_with_links_10.pkl')
# print(test_node.get_name())
# for out_neighbor in test_node.get_out_neighbors():
#    print(out_neighbor.get_name())

ttmp =bfs(test_node,'0','2')
print(ttmp)

print('Test 2')
test_node_2 = make_graph('./datasets/test_index_13.pkl', './datasets/articles_with_links_13.pkl')['L']
print(test_node_2.get_name())
for in_neighbor in test_node_2.get_in_neighbors():
   print(in_neighbor.get_name())
