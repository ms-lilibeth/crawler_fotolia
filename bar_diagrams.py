import  pickle
import matplotlib.pyplot as plt
import numpy as np

my_author=202938145

with open('all_info', 'rb') as f:
    info = pickle.load(f)


my_items = [item for item in info if item['author_id'] == my_author]
other_videos=[]
for x in info:
    if x['media_type'] == 1 and x['author_id']!=my_author:
        try:
            other_videos.append(x['video_duration'][0])
        except:
            continue
# other_videos = [d['video_duration']  \
#                 if info['media_type']==1 and info['author_id']!=my_author]
other_videos.sort()
min1 = 0
max1 = other_videos[-1]
periods1 = np.arange(min1, max1 + 10, step=10)
stat1=np.zeros(len(periods1))
for v in other_videos:
    stat1[(v-min1)//10] +=1
stat1 = stat1 / sum(stat1)
#отсекаем значения, близкие к нулю
tmp_i=None
for i in range(-len(stat1)+1,0,1):
    if stat1[i] < 0.01:
        tmp_i = i
    else:
        break
if tmp_i != None:
    stat1 = stat1[:tmp_i]
    periods1 = periods1[:tmp_i]

plt.xticks(periods1, [str(p) for p in periods1] )
print(periods1), print(stat1)
my_videos=[]
for x in info:
    if x['media_type']==1 and x['author_id']==my_author:
        try:
            my_videos.append(x['video_duration'][0])
        except:
            continue
# my_videos = [d for d in info['video_duration'] if info['media_type']==1 and info['author_id']==my_author]
my_videos.sort()
min2 = 0
max2 = my_videos[-1]
periods2 = np.arange(min2, max2 + 10, step=10)
stat2=np.zeros(len(periods2))
for v in my_videos:
    stat2[(v-min2)//10] +=1
stat2 = stat2 / sum(stat2)
#отсекаем значения, близкие к нулю
tmp_i=None
for i in range(-len(stat2)+1,0,1):
    if stat2[-i] < 0.01:
        tmp_i = i
    else:
        break
if tmp_i != None:
    stat2 = stat2[:-tmp_i]
    periods2 = periods2[:-tmp_i]

# Two subplots sharing both x/y axes
f, (ax1, ax2) = plt.subplots(2, sharex=True, sharey=True)
rects1 = ax1.bar(periods1,stat1,width=10,color='b')
# ax1.set_title('Sharing both axes')
rects2 = ax2.bar(periods2, stat2,width=10, color='r')

# Fine-tune figure; make subplots close to each other and hide x ticks for
# all but bottom plot.
f.subplots_adjust(hspace=0)
plt.setp([a.get_xticklabels() for a in f.axes[:-1]], visible=False)

def autolabel(rects,ax):
    # attach some text labels
    for rect in rects:
        height = rect.get_height()
        ax.text(rect.get_x() + rect.get_width()/2., 1.01*height,
                '%d%%' % int(height*100),
                ha='center', va='bottom', fontsize=12)

autolabel(rects1,ax1)
autolabel(rects2,ax2)
plt.show()
