# Не доделано
import  pickle
import matplotlib.pyplot as plt
import numpy as np

my_author=202938145

with open('all_info', 'rb') as f:
    info = pickle.load(f)
with open('categories_used.pickle','rb') as f:
    c_used = pickle.load(f)
# with open('categories_not_used.pickle','rb') as f:
#     c_not_used = pickle.load(f)

my_items = [item for item in info if item['author_id'] == my_author and item['media_type']==0]
not_my_items = [item for item in info if item['author_id'] != my_author and item['media_type']==0]
del info
stat = np.zeros(len(c_used))
for i in my_items:
    tmp_c = [ct for ct in i['photos_categories']]
    for c in tmp_c:
        stat[c_used.index(c)] +=1
print(stat)
plt.bar(np.arange(len(c_used)),stat,width=1,color='r')
plt.xticks(np.arange(len(c_used)), c_used)
# plt.show()
