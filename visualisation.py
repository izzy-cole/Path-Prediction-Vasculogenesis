import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.collections import PatchCollection,LineCollection
from matplotlib.patches import Circle

from config import max_difficulty

def visualise_network(nodes,adj,image=None,im_alpha=1,node_size=0.1,edge_width=1):
    fig,ax=plt.subplots(figsize=(10,10))
    if image is not None:
        ax.imshow(image,cmap=plt.cm.gray,alpha=im_alpha)
    ax.axis('off') 

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
    x_arr = nodes['x'].values
    y_arr = nodes['y'].values
    weight_arr = nodes['weight'].values
    type_arr = nodes['type'].values
    cmap = mpl.colormaps['Reds']
    for i in nodes.index:
        x = x_arr[i]
        y = y_arr[i]
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
