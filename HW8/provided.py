"""
Homework 8 Provided Code
"""

from matplotlib import pyplot as plt
import pickle


class Node:
    """
    A simple implementation of a directed graph.
    """

    def __init__(self, name):
        """
        Initialize the graph with a node represented as a string.
        :param name: title of article
        """
        self._name_ = name
        self._in_neighbors_ = []
        self._out_neighbors_ = []

    def get_name(self):
        """
        Returns name of node.
        :return: name/title of node
        """
        return self._name_

    def get_in_neighbors(self):
        """
        Returns in-neighbors of node.
        :return: in-neighbors of node
        """
        return self._in_neighbors_

    def get_out_neighbors(self):
        """
        Returns out-neighbors of node.
        :return: out-neighbors of node
        """
        return self._out_neighbors_

    def set_in_neighbors(self, in_neighbor_list):
        """
        Sets in-neighbors of node.
        :param: in_neighbor_list: list of in_neighbors of current node
        """
        self._in_neighbors_ = in_neighbor_list

    def set_out_neighbors(self, out_neighbor_list):
        """
        Sets out-neighbors of node.
        :param: out_neighbor_list: list of out_neighbors of current node
        """
        self._out_neighbors_ = out_neighbor_list

    def add_in_neighbor(self, node):
        """
        Add an in-neighbor represented as an instance of the Node class to the node's in-neighbor list.
        :param node: instance of Node class
        """
        self._in_neighbors_.append(node)

    def add_out_neighbor(self, node):
        """
        Add an out-neighbor represented as an instance of the Node class to the node's out-neighbor list.
        :param node: instance of Node class
        """
        self._out_neighbors_.append(node)


class Graph:
    """
    A simple interface for graph traversal.
    """

    def __init__(self, index_file, data_file):
        """
        Initializes the article to Node dictionary.
        :param index_file: path to index file
        :param data_file: path to article link data file
        """
        self._node_dict_ = make_graph(index_file, data_file)

    def get_articles_to_nodes(self):
        """
        Getter for _node_dict_.
        :return: the article to nodes dictionary this graph uses
        """
        return self._node_dict_

    def compute(self, graph_operation, node_operation):
        """
        Given two functions where the first functions makes use of the second function,
        performs a graph traversal operation. Assumes graph_operation uses node_operation as an argument.
        :param graph_operation: higher order function which uses node_operation and _node_dict_
        :param node_operation: node function
        :return: the return value of calling graph_operation with _node_dict_ and node_operation as parameters
        """
        return graph_operation(self._node_dict_, node_operation)


def open_file(file_path):
    """
    Opens a pkl file and return its contents.
    :param file_path: path to pkl file
    :return: contents of pkl file
    """
    with open(file_path, 'rb') as handle:
        return pickle.load(handle)


def find_neighbors(title_to_node, current_title, list_of_links):
    """
    Given a dictionary of titles to nodes, a current title, and a list of
    outgoing links from the current article, updates the neighbor set of the
    current article. Neighbors must be a key in title_to_node. Does not create self-links.

    :param title_to_node: dictionary of article titles to node references
    :param current_title: an article title
    :param list_of_links: a list of outgoing links from the current article
    """
    # Get current node by searching dictionary.
    current_node = title_to_node[current_title]

    # Only add valid links to the current node's neighbor set.
    for link in list_of_links:
        # We should only add links that exist in the data set.
        if link in title_to_node:
            # Update the current node's neighbor set AND the
            # neighbor's parent set.
            current_node.add_out_neighbor(title_to_node[link])
            title_to_node[link].add_in_neighbor(current_node)


def make_graph(index_file, data_file):
    """
    :param index_file: path to index file
    :param data_file: path to data file
    :return: dictionary of article titles to node references

    Creates a series of Nodes (connected components/graphs) and returns a dictionary where every article
    key is mapped to its node reference.
    """
    title_to_node = {}
    # Returns a list of article titles
    article_titles = open_file(index_file)
    # Returns a list of three element tuples where each tuple contains an
    # article title, list of links going out of that article, and length of the article.
    article_data = open_file(data_file)

    # Create a node reference for every article
    for title in article_titles:
        title_to_node[title] = Node(title)

    # Populate neighbor and parent lists for every node
    for info in article_data:
        find_neighbors(title_to_node, info[0], info[1])

    return title_to_node


def plot(x_list, y_list, x_title, y_title, plot_title):
    """
    :param x_list: a list containing the values to plot on the x-axis. This must
    be the same length as y_list.
    :param y_list: a list containing the values to plot on the y-axis. This must
    be the same length as x_list.
    :param x_title: a string representing the title to display on the horizontal axis.
    :param y_title: a string representing the title to display on the vertical axis.
    :param plot_title: a string represengint the title to display above the plot
    :return: None

    Given values to plot and labels, displays a plot. This assumes the values in
    x_list and y_list match up. For example, the fifth point on the plot would
    be represented in coordinate form by (x_list[4], y_list[4]).
    """
    assert (len(x_list) == len(y_list))
    plt.plot(x_list, y_list)
    plt.xlabel(x_title)
    plt.ylabel(y_title)
    plt.title(plot_title)
    plt.show()

