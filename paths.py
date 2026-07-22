import cv2
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import networkx as nx
import os
import random
#import scipy

from config import max_difficulty
import visualisation

def initialise_nodes(image):
    #set up a simple network where each pixel is a node
    nodes = pd.DataFrame(data=None, columns=["x","y","type","weight"]) #main datastructure

    nodes_list = []

    #set up nodes
    height = len(image)
    width = len(image[0])
    for x in range(width):
        for y in range(height):
            pixel = image[y][x]
            #openCV uses BGR data (not RGB)
            #set up rough estimates of colours (to allow for compression errors)

            #Red: ignore (not part of model to save processing)
            #White-black: blood island (varying intensity)
            #Green: posterior spawn point
            red = pixel[2]>150 and pixel[1]<90 and pixel[0]<90 
            green = pixel[2]<30 and pixel[1]>130 and pixel[0] <30
            intensity = np.mean(pixel)/255

            if green: 
                nodes_list.append({"x": x, "y": y, "type": "posterior", "weight": 0})
            elif not red: 
                nodes_list.append({"x": x, "y": y, "type": "blood island", "weight": intensity})

    nodes = pd.DataFrame(nodes_list)
    return nodes


def coords_to_id(nodes,x,y):
   id_list =  nodes[(nodes["x"]==x) & (nodes["y"]==y)].index
   if len(id_list)==0:
       return -1
   elif len(id_list)==1:
       return id_list[0]
   else:
       print("Error: multiple nodes found with same (x,y) coordinates")

def difficulty_fn(weight1,weight2):
    return (1-max_difficulty)*min(weight1,weight2)+max_difficulty

def initialise_edges(nodes):
    n = len(nodes.index)
    adj = np.full((n,n),np.nan)
    weights = nodes["weight"].values
    xs = nodes["x"].values
    ys = nodes["y"].values

    coord_to_id = {}
    for i in range(n):
        coord = (xs[i],ys[i])
        coord_to_id[coord] = i

    for i in nodes.index:
        x1 = xs[i]
        y1 = ys[i]
        weight1 = weights[i]
        neighbours = [[x1-1,y1],[x1,y1-1],[x1-1,y1-1],[x1+1,y1],[x1,y1+1],[x1+1,y1+1],[x1-1,y1+1],[x1+1,y1-1]]
        for j in neighbours:
            x2,y2 = j[0],j[1]
            neighbour_id = coord_to_id.get((x2, y2), -1)
            if neighbour_id != -1: #check neighbour exists (e.g. not part of red "ignored" zone)
                weight2 = nodes.loc[neighbour_id,"weight"]

                #Use the difficulty function to determine the edge "difficulty"/weight
                new_diff = difficulty_fn(weight1,weight2)

                adj[i,neighbour_id] = new_diff
                adj[neighbour_id,i] = new_diff
    return adj

def gen_networkx_graph(nodes,adj):
    G = nx.Graph()

    for i in nodes.index:
        node = nodes.loc[i]
        #G.add_node(i)#,weight=node["weight"])
        G.add_nodes_from([(i, {"x": int(node["x"]), "y": int(node["y"]), "weight":float(node["weight"])})])

    for i in range(len(adj)):
        for j in range(len(adj)):
            weight = adj[i,j]
            if not np.isnan(weight):
                G.add_edge(i,j,weight=weight)
    #nx.draw(G, with_labels=True)
    return G


def stochastic_paths(nodes,adj,n,start_type="posterior",end_type="blood island",display_paths=False,display_treads=True,image=None):
    G = gen_networkx_graph(nodes,adj)
    print("Network generation finished")
    random.seed(1)

    all_tread = []
    tread_counts = np.zeros(len(nodes))
    start_list = nodes[nodes["type"]==start_type].index
    end_list = nodes[nodes["type"]==end_type].index
    if len(start_list)==0:
        print("Error: no valid start points")
        return -1
    for i in range(n):
        start_id = random.choice(start_list)
        end_id = random.choice(end_list)

        sp = nx.shortest_path(G,start_id,end_id,weight="weight")
        all_tread.append(sp)
        for j in sp:
            tread_counts[j] += 1

    if display_paths:
        visualisation.visualise_network(nodes,adj,all_treads=all_tread,image=image,im_alpha=0)
        plt.show()

    if display_treads:
        visualisation.visualise_network_treads(nodes,adj,tread_counts,image=image,im_alpha=0.5)
        plt.show()
    #return net,path_tread


def cellular_growth():
    print("testing")
    #Set up a growth function

def cellular_automata(nodes,adj,radius):
    #Setup a square kernel of radius R, set the centre to 0, and normalise
    #todo: make kernel circular
    kernel = np.ones((2*radius+1,2*radius+1))
    kernel[radius,radius] = 0
    kernel = kernel / np.sum(kernel)

    #Setup a 2d array node structure A
    #Apply the convolution to get the neighbour weight
    U = scipy.signal.convolve2d(A, kernel, mode='same', boundary='wrap')
    #Compare U to the growth function and update A

def epoch(nodes,adj,n_paths, strength):
    print("test")
    #Generate n random paths
    #Add the tread information with some weight
    #Run cellular automata
    #Repeat, animate


#Model flow:
#1. Read image and set up a network of nodes and edges, with weights depending on the node intensity (difficulty parameter). Diagonals?
#2. Generate random paths from a start point in green to end points
#3. Record the number of times a path is used in total and use this to create path tread predictions
#4. Display this


#5. Create an "iterating" model (git branch) where random paths work in an iterating loop, updating the node and adjacency weights
#6. Add some factors of cellular automata to maintain or decay existing nodes
#7. File handling and saving

