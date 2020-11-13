"""
Provided Code
"""

import numpy as np
import pickle


class Node:
    """
    A simple implementation of a directed graph.
    """
    def __init__(self, name):
        """
        Input: name, an article title

        Initialize a node and its in-neighbor and out-neighbor lists.
        """
        self._name_ = name
        self._in_neighbors_ = []
        self._out_neighbors_ = []

    def get_name(self):
        """
        Returns the name of the current node.
        """
        return self._name_

    def get_in_neighbors(self):
        """
        Returns in-neighbors of node.
        """
        return self._in_neighbors_

    def get_out_neighbors(self):
        """
        Returns out-neighbors of node.
        """
        return self._out_neighbors_

    def add_in_neighbor(self, node):
        """
        Input: node, a reference to a Node object

        Add an in-neighbor to the node's in-neighbor list.
        """
        self._in_neighbors_.append(node)

    def add_out_neighbor(self, node):
        """
        Input: node, a reference to a Node object

        Add an out-neighbor to the node's out-neighbor list.
        """
        self._out_neighbors_.append(node)


def open_file(file_path):
    """
    Opens a pkl file and return its contents.
    :param file_path: a path to a pickled file
    """
    with open(file_path, 'rb') as handle:
        return pickle.load(handle)

    
def mean_center(matrix):
    """
    Mean center columns of input matrix
    :param matrix: the matrix to mean center
    """
    col_means = np.mean(matrix, axis=0)
    return matrix - col_means


def normalize(matrix):
    """
    Normalize rows of input matrix
    :param matrix: the matrix to mean center
    """
    return matrix / np.linalg.norm(matrix, ord=2, axis=1, keepdims=True)


def create_vectors(vector_data):
    """
    Mean centers and normalizes all vectors in input.
    :param vector_data: a path to a list of vectors
    """
    word_data_unaltered = np.load(vector_data)
    word_data_mean_centered = mean_center(word_data_unaltered)
    return normalize(word_data_mean_centered)

    
def find_neighbors(title_to_node, current_title, list_of_links):
    """
    Finds all neighbors of the current article/node and updates title_to_node
    accordingly. Only considers links which are keys in title_to_node.
    :param title_to_node: dictionary of titles to nodes
    :param current_title: an article title
    :param list_of_links: list of outgoing links from current article
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
    Creates a series of Nodes and returns a dictionary where every article
    key is mapped to its Node reference.
    :param index_file: a path to an index file containing article titles
    :param data_file: a path to a corresponding file of article data
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