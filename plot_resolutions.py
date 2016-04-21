import  pickle
import matplotlib.pyplot as plt
from matplotlib import cm
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.ticker import LinearLocator, FormatStrFormatter
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import TruncatedSVD, NMF
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.manifold import TSNE

my_author=202938145

with open('all_info', 'rb') as f:
    info = pickle.load(f)


# my_items = [item for item in info if item['author_id'] == my_author]
my_items = [item for item in info if item['author_id'] != my_author and item['media_type'] == 1]
resol_set = set()
for item in my_items:
    for r in item['resolutions']:
        resol_set.add(r)

data_to_plot=[]
X = []
Y =[]
items_to_kick = []
for r in resol_set:
    try:
        pair = [int(s) for s in r.split() if s.isdigit()]
        Y.append(pair[1])
        X.append(pair[0])
        data_to_plot.append(len([i for i in my_items if r in i['resolutions']]))
    except:
        items_to_kick.append(r)
        continue

data_to_plot = np.asarray(data_to_plot)
X = np.asarray(X)
Y = np.asarray(Y)
# sum = data_to_plot.sum()
# #data_to_plot = [e/sum for e in data_to_plot]


# X, Y = np.meshgrid(X, Y)
# Plotting ---------------------
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
hist, xedges, yedges = np.histogram2d(X, Y, bins=30)

elements = (len(xedges) - 1) * (len(yedges) - 1)
xpos, ypos = np.meshgrid(xedges[:-1] + 0.25, yedges[:-1] + 0.25)

xpos = xpos.flatten()
ypos = ypos.flatten()
zpos = np.zeros(elements)
dx = 160 * np.ones_like(zpos)
dy = dx.copy()
dz = hist.flatten()

ax.bar3d(xpos, ypos, zpos, dx, dy, dz, color='b', zsort='average')

plt.show()
# ax = fig.gca(projection='3d')
# #plt.hist(data_to_plot,bins=len(resol_set),facecolor='red')
# x=np.arange(0,len(resol_set))
# plt.plot(x,data_to_plot)
# # plt.hist(data_to_plot,len(resol_set))
# surf = ax.plot_surface(X, Y, data_to_plot, rstride=1, cstride=1, cmap=cm.coolwarm,
#                        linewidth=0, antialiased=False)
# #ax.set_zlim(-1.01, 1.01)
#
# # ax.zaxis.set_major_locator(LinearLocator(10))
# # ax.zaxis.set_major_formatter(FormatStrFormatter('%.02f'))
#
# fig.colorbar(surf, shrink=0.5, aspect=5)
#
# plt.show()