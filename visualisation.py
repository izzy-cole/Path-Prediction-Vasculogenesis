import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.collections import PatchCollection
from matplotlib.patches import Circle

from config import max_difficulty

def visualise_network(nodes,adj,image=None,im_alpha=1,node_size=0.1):
    fig,ax=plt.subplots(figsize=(10,10))
    if image is not None:
        ax.imshow(image,cmap=plt.cm.gray,alpha=im_alpha)
    ax.axis('off') 

    #Code for nodes
    patches = []
    for i in nodes.index:
        x,y,weight,type = nodes[["x","y","weight","type"]].loc[i]

        if type == "blood island": #colourings
            cmap = mpl.colormaps['Reds']
            node_col = cmap(weight)
            circle = Circle((x, y), node_size,color=node_col)
        else: 
            circle = Circle((x, y), node_size,color="#f2ad00")
        patches.append(circle)

    p = PatchCollection(patches, alpha=1,match_original=True)
    ax.add_collection(p)

    #Code for edges
    for i in adj:
        for j in adj:
            dist = adj.loc[i,j]
            if dist>0:
                x1,y1=nodes[["x","y"]].loc[i]
                x2,y2=nodes[["x","y"]].loc[j]
                cmap = mpl.colormaps['Blues']
                edge_col = cmap(1-dist/max_difficulty)
                ax.plot([x1,x2],[y1,y2],alpha=1,linewidth=2,color=edge_col)