import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.collections import PatchCollection,LineCollection
from matplotlib.patches import Circle

import numpy as np

from config import max_difficulty

def visualise_network(nodes,adj,image=None,im_alpha=1,node_size=0.1,edge_width=1,all_treads=None,coords=[0,0],size=None):
    fig,ax=plt.subplots(figsize=(10,10))
    if image is not None:
        ax.imshow(image,cmap=plt.cm.gray,alpha=im_alpha)
    ax.axis('off') 

    if size is None:
        size = [len(image[0]),len(image)]

    xs = nodes["x"].values
    ys = nodes["y"].values


    edge_lines = []
    edge_colours = []
    cmap = mpl.colormaps['Blues']
    #Code for edges
    for i in range(len(adj)):
        for j in range(len(adj)):
            if i>j:
                dist = adj[i,j]
                if dist>0:
                    x1,y1=xs[i],ys[i]
                    x2,y2=xs[j],ys[j]
                    
                    edge_lines.append([(x1,y1),(x2,y2)])
                    edge_colours.append(cmap(1-dist/max_difficulty))
                    
    lc = LineCollection(edge_lines, colors=edge_colours, alpha=1, linewidths=edge_width)               
    ax.add_collection(lc)

    #Code for nodes
    patches = []
    weight_arr = nodes['weight'].values
    type_arr = nodes['type'].values
    cmap = mpl.colormaps['Reds']
    for i in nodes.index:
        x = xs[i]
        y = ys[i]
        weight = weight_arr[i]
        n_type = type_arr[i]

        if n_type == "blood island": #colourings
            node_col = cmap(weight)
            circle = Circle((x, y), node_size,color=node_col)
        else: 
            circle = Circle((x, y), node_size,color="#f2ad00")
        patches.append(circle)

    pc = PatchCollection(patches, alpha=1,match_original=True)
    ax.add_collection(pc)

    #Code to display path generated
    tread_lines = []
    tread_cols = []
    if all_treads is not None:
        col_count = 0
        cmap = mpl.colormaps['rainbow']
        for tread in all_treads:
            tread_col = cmap(col_count/len(all_treads))
            for i in range(len(tread)-1):
                id1 = tread[i]
                id2 = tread[i+1]
                x1,y1 = xs[id1],ys[id1]
                x2,y2 = xs[id2],ys[id2]
                tread_lines.append([(x1,y1),(x2,y2)])
                tread_cols.append(tread_col)
            col_count += 1
    lc = LineCollection(tread_lines, colors=tread_cols, alpha=1, linewidths=3)
    ax.add_collection(lc)

    plt.xlim(coords[0],coords[0]+size[0])
    plt.ylim(coords[1],coords[1]+size[1])

def visualise_network_treads(nodes,adj,tread_counts,image=None,im_alpha=1,node_size=0.1,edge_width=1):
    fig,ax=plt.subplots(figsize=(10,10))
    ax.axis('off') 

    tread_counts = tread_counts / np.max(tread_counts)

    #Code for nodes
    patches = []
    weight_arr = nodes['weight'].values
    cmap = mpl.colormaps['Reds']

    xs = nodes["x"].values
    ys = nodes["y"].values

    for i in nodes.index:
        x = xs[i]
        y = ys[i]

        node_col = cmap(tread_counts[i])
        circle = Circle((x, y), node_size,color=node_col)

        patches.append(circle)

    pc = PatchCollection(patches, alpha=1,match_original=True)
    ax.add_collection(pc)