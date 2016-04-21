import  pickle
import matplotlib.pyplot as plt
import numpy as np
from sklearn.decomposition import TruncatedSVD, NMF
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.manifold import TSNE
import pickle

my_author=202938145

with open('all_info', 'rb') as f:
    info = pickle.load(f)

info = [item for item in info if item['media_type']==0]
my_items = [item for item in info if item['author_id'] == my_author]
# v_num = len([item for item in my_items if item['media_type']==1])
# print("Number of videos in my portfolio: %d" % (v_num))
# print("Number of photos in my portfolio: %d" % (len(my_items)-v_num))


# corpus = [' '.join(x['photos_categories']) for x in info]
# vectorizer0 = TfidfVectorizer(min_df=200)
# X = vectorizer0.fit_transform(corpus)
# words0 = list(vectorizer0.get_feature_names())
# words0 = np.asarray(words0)

not_my_items = [item for item in info if item['author_id'] != my_author]

for x in not_my_items:
    x['photos_categories'] = [kw for kw in x['photos_categories']]
corpus = [' '.join(x['photos_categories']) for x in not_my_items]
vectorizer1 = TfidfVectorizer()
X = vectorizer1.fit_transform(corpus)
Xt_X = X.T.dot(X)

svd = TruncatedSVD(n_components=60)
pre_data = svd.fit_transform(Xt_X)
tsne = TSNE(n_components=2)
data_to_plot = tsne.fit_transform(pre_data)

words1 = list(vectorizer1.get_feature_names())
words1 = np.asarray(words1)

for x in my_items:
    x['photos_categories'] = [kw for kw in x['photos_categories']]
corpus = [' '.join(x['photos_categories']) for x in my_items]
vectorizer2 = TfidfVectorizer()
X = vectorizer2.fit_transform(corpus)
Xt_X = X.T.dot(X)

svd = TruncatedSVD(n_components=60)
pre_data = svd.fit_transform(Xt_X)
tsne = TSNE(n_components=2)
data_to_plot = tsne.fit_transform(pre_data)



words2 = list(vectorizer2.get_feature_names())
words2 = np.asarray(words2)
needed=[]
both = []
not_in_my = []
for (i, element) in enumerate(pre_data):
    x_coord = element[0]
    y_coord = element[1]
    if words2.__contains__(words1[i]):
        plt.scatter(x_coord, y_coord, c="red")
        txt = plt.text(x_coord, y_coord, words1[i], fontsize=12)
        plt.setp(txt,color="red")
        both.append(words1[i])
    else:
        plt.scatter(x_coord, y_coord, c="blue")
        # print(words1[i])
        needed.append(words1[i])
        txt = plt.text(x_coord, y_coord, words1[i], fontsize=12)
        plt.setp(txt, color="blue")
        not_in_my.append(words1[i])
with open('categories_used.pickle' , 'wb') as f:
    pickle.dump(both,f)
with open('categories_not_used.pickle','wb') as f:
    pickle.dump(not_in_my,f)
# for (i, element) in enumerate(data_to_plot2):
#     x_coord = element[0]
#     y_coord = element[1]
#     if not words1.__contains__(words2[i]):
#         plt.scatter(x_coord, y_coord, c="green", fontsize=12)
#         in_my_only +=1
        # txt = plt.text(x_coord, y_coord, words1[i], fontsize=6)
        # plt.setp(txt, color="green")

# plt.show()


# from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
# from sklearn.decomposition import NMF, LatentDirichletAllocation
# n_topics = 30
# n_top_words = 20
#
#
# def print_words(model, feature_names, needed):
#     for topic_idx, topic in enumerate(model.components_):
#         print("Topic #%d:" % topic_idx)
#         print(" ".join([feature_names[i]
#                         for i in range(0,len(topic)) if needed.__contains__(feature_names[i])]))
#     print()
#
#
# print("Extracting tf-idf features for NMF...")
# # tfidf_vectorizer = TfidfVectorizer()
# tfidf = vectorizer0.fit_transform(corpus)
# # Fit the NMF model
# print("Fitting the NMF model with tf-idf features")
# nmf = NMF(n_components=n_topics, random_state=1, alpha=.1, l1_ratio=.5).fit(tfidf)
# print("\nTopics in NMF model:")
# tfidf_feature_names = vectorizer0.get_feature_names()
# print_words(nmf, tfidf_feature_names, needed)
#
# print("Extracting tf features for LDA...")
# tf_vectorizer = CountVectorizer(min_df=500)
# tf = tf_vectorizer.fit_transform(corpus)
# print("Fitting LDA models with tf features")
# lda = LatentDirichletAllocation(n_topics=n_topics, max_iter=5,
#                                 learning_method='online', learning_offset=50.,
#                                 random_state=0)
# lda.fit(tf)
# print("\nTopics in LDA model:")
# tf_feature_names = tf_vectorizer.get_feature_names()
# print_words(lda, tf_feature_names, needed)

