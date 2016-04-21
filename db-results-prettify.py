import pickle

my_author_id = 202938145
print("loading...")
with open('p-items_all','rb') as f:
    p_items = pickle.load(f)
with open('keywords_all','rb') as f:
    kwrds = pickle.load(f)
with open('resolutions_all','rb') as f:
    resol = pickle.load(f)
with open('ph-categories_all','rb') as f:
    ph_cat= pickle.load(f)
with open('v-duration_all', 'rb') as f:
    v_dur = pickle.load(f)

all_info = []
new_item={}
items_count=1
for item in p_items:
    print("item %d from %d" % (items_count,len(p_items)))
    items_count +=1
    pid = item['pi_id']
    if item['media_type'] == 0:
        new_item['media_type'] = 'photo'
    else:
        new_item['media_type'] = 'video'
    new_item['media_id'] = item['media_id']
    new_item['title'] = item['title']
    new_item['description'] = item['description']
    new_item['author_id'] = item['author_id']
    new_item['keywords'] = [kw['keyword'] for kw in kwrds if kw['pi_id'] == pid]
    new_item['resolutions'] = [r['resolution_size'] for r in resol if r['pi_id'] == pid]
    if new_item['media_type'] == 'photo':
        new_item['photos_categories'] = [ct['category_name'] for ct in ph_cat if ct['pi_id'] == pid]
    else:
        new_item['video_duration'] = [dur['duration'] for dur in v_dur if dur['pi_id'] == pid]
    all_info.append(new_item)
print("dumping...")
with open('all_info','wb') as f:
    pickle.dump(all_info,f)
for item in all_info:
    print(item),print('----------------')