import cv2
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import networkx as nx
import os
import random
from config import max_difficulty

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
    adj = pd.DataFrame(data=np.full((n,n),np.nan))

    for i in nodes.index:
        x1,y1,weight1 = nodes.loc[i,"x"],nodes.loc[i,"y"],nodes.loc[i,"weight"]

        neighbours = [[x1-1,y1],[x1,y1-1],[x1-1,y1-1],[x1+1,y1],[x1,y1+1],[x1+1,y1+1],[x1-1,y1+1],[x1+1,y1-1]]
        for j in neighbours:
            x2,y2 = j[0],j[1]
            neighbour_id = coords_to_id(nodes,x2,y2)
            if neighbour_id != -1: #check neighbour exists (e.g. not part of red "ignored" zone)
                weight2 = nodes.loc[neighbour_id,"weight"]

                #Use the difficulty function to determine the edge "difficulty"/weight
                new_diff = difficulty_fn(weight1,weight2)

                adj.loc[i,neighbour_id] = new_diff
                adj.loc[neighbour_id,i] = new_diff
    return adj

#Model flow:
#1. Read image and set up a network of nodes and edges, with weights depending on the node intensity (difficulty parameter). Diagonals?
#2. Generate random paths from a start point in green to end points
#3. Record the number of times a path is used in total and use this to create path tread predictions
#4. Display this


#5. Create an "iterating" model (git branch) where random paths work in an iterating loop, updating the node and adjacency weights
#6. Add some factors of cellular automata to maintain or decay existing nodes
#7. File handling and saving
