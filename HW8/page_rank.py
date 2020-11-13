import provided
import pickle


def loop_nodes(articles_to_nodes,compute_node):
	for article in articles_to_nodes:
		compute_node(articles_to_nodes[article])


def remove_self_links(compute_node):
	compute_node.set_in_neighbors([x for x in compute_node.get_in_neighbors() if x is not compute_node])
	compute_node.set_out_neighbors([x for x in compute_node.get_out_neighbors() if x is not compute_node])


def run_page_rank(index_file, data_file, output_file_name):
	# intialize graph
	graph = provided.Graph(index_file, data_file)
	# remove self links
	graph.compute(loop_nodes, remove_self_links)
	articles_to_nodes =graph.get_articles_to_nodes()
	articles_to_pagerank = page_rank(articles_to_nodes,complete_iteration)
	with open(output_file_name,'wb') as fl:
		pickle.dump(articles_to_pagerank,fl)


def page_rank(articles_to_nodes, compute_node):
	# initialize the probability first
	epsilon=0.0000001
	dampening_rate=0.85
	previous={}
	total_nodes = len(articles_to_nodes)
	for article in articles_to_nodes:
		previous[article]=1/total_nodes
	while True:
		update_values =get_score(previous,articles_to_nodes,dampening_rate)
		for article in articles_to_nodes:
			new_values=compute_node(article,previous,update_values,articles_to_nodes)
			update_values=new_values
		if epsilon > diff(previous,new_values) :
			return previous
		previous = update_values
	return previous



def diff(previous, current):
	score=0
	for article in current:
		score+=abs(current[article] - previous[article])
	return score

def get_score(previous,articles_to_nodes,dampening_rate):
	update_values ={}
	for article in articles_to_nodes:
		# get the new value for the node here
		#update this one after the other
		total_nodes = len(articles_to_nodes)
		in_neighbor = articles_to_nodes[article].get_in_neighbors()
		temp = ((1 - dampening_rate)/total_nodes) + (dampening_rate * (sum([previous[x.get_name()]/len(x.get_out_neighbors()) for x in in_neighbor])))
		update_values[article]=temp
	return update_values

	
def complete_iteration(article, prev_articles_to_prob, articles_to_prob, articles_to_nodes):

	# there will not be any need to perform updates on nodes with out neighbors
	retain=0.15
	out_neighbor = articles_to_nodes[article].get_out_neighbors()
	if len(out_neighbor) > 0:
		return articles_to_prob
	# if not out_neighbor distribute score to all nodes
	print(articles_to_prob[article])
	update_value = (retain/len(articles_to_nodes)) + ((1-retain) *(articles_to_prob[article]/len(articles_to_nodes)))
	for title in articles_to_prob:
		articles_to_prob[title]+=update_value
	return articles_to_prob

# run_page_rank('./datasets/test_index_3.pkl', 'datasets/articles_with_links_3.pkl', './results_3.pkl')



# the function to perform the plot is in this section
def plot1(index_file,data_file,pkl_link):
	articles_to_prob = provided.open_file(pkl_link)
	articles_to_nodes = provided.make_graph(index_file,data_file)
	sorted_articles_to_prob = sorted(articles_to_prob,key=lambda x:articles_to_prob[x], reverse=True)
	to_plot = sorted_articles_to_prob[0:100]
	x_list = []
	y_list =[]
	for (index,title) in enumerate(to_plot):
		x_list.append(index)
		y_list.append(len(articles_to_nodes[title].get_in_neighbors()))
	provided.plot(x_list,y_list,'Article position','article in degree',' article position to in degree plot for top 100 article with highest page rank')

def plot2(index_file,data_file,pkl_link):
	articles_to_prob = provided.open_file(pkl_link)
	articles_to_nodes = provided.make_graph(index_file,data_file)
	sorted_articles_to_prob = sorted(articles_to_prob,key=lambda x:articles_to_prob[x])
	to_plot = sorted_articles_to_prob[0:100]
	x_list = []
	y_list =[]
	for (index,title) in enumerate(to_plot):
		x_list.append(index)
		y_list.append(len(articles_to_nodes[title].get_in_neighbors()))
	provided.plot(x_list,y_list,'Article position','article in degree',' article position to in degree plot for article with lower page rank')


def plot3(index_file,data_file,pkl_link):
	articles_to_prob = provided.open_file(pkl_link)
	articles_to_nodes = provided.make_graph(index_file,data_file)
	sorted_articles_to_prob = sorted(articles_to_prob,key=lambda x:articles_to_prob[x])
	to_plot = sorted_articles_to_prob[0:100]
	x_list = []
	y_list =[]
	previous =0

	for size in range(0,len(articles_to_prob),100):
		articles = list(articles_to_prob.keys())[size:(size+100)]
		x_list.append(size/100)
		y_list.append(sum([len(articles_to_nodes[x].get_in_neighbors()) for x in articles])/len(articles))
		previous=size
	provided.plot(x_list,y_list,'aggregate position','average in degree',' aggregate article position to in average degree plot for article with lower page rank')

plot1('./datasets/test_index_3.pkl', 'datasets/articles_with_links_3.pkl', './results_3.pkl')
plot2('./datasets/test_index_3.pkl', 'datasets/articles_with_links_3.pkl', './results_3.pkl')
plot3('./datasets/test_index_3.pkl', 'datasets/articles_with_links_3.pkl', './results_3.pkl')
# Test code for Part A

# Create graph
# graph = provided.Graph('./datasets/articles_index_20199.pkl', './datasets/articles_with_links_20199.pkl')
# # Remove self links
# graph.compute(loop_nodes, remove_self_links)
# # Make sure all self links are gone
# articles_to_nodes_dict = graph.get_articles_to_nodes()

# for pair in articles_to_nodes_dict.items():
# 	title = pair[0]
# 	node = pair[1]
# 	for in_neighbor in node.get_in_neighbors():
# 		if in_neighbor.get_name() == title:
# 			print(title)
# 	for out_neighbor in node.get_out_neighbors():
# 		if out_neighbor.get_name() == title:
# 			print(title)