from __future__ import print_function
import json
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.decomposition import NMF, LatentDirichletAllocation
import pickle
n_topics = 30
n_top_words = 20


def print_top_words(model, feature_names, n_top_words):
    for topic_idx, topic in enumerate(model.components_):
        print("Topic #%d:" % topic_idx)
        print(" ".join([feature_names[i]
                        for i in topic.argsort()[:-n_top_words - 1:-1]]))
    print()

print("Loading dataset...")

my_author=202938145

with open('all_info', 'rb') as f:
    info = pickle.load(f)


# my_items = [item for item in info if item['author_id'] == my_author]
corpus = [' '.join(x['keywords']) for x in info]

print("Extracting tf-idf features for NMF...")
tfidf_vectorizer = TfidfVectorizer()
tfidf = tfidf_vectorizer.fit_transform(corpus)
# Fit the NMF model
print("Fitting the NMF model with tf-idf features")
nmf = NMF(n_components=n_topics, random_state=1, alpha=.1, l1_ratio=.5).fit(tfidf)
print("\nTopics in NMF model:")
tfidf_feature_names = tfidf_vectorizer.get_feature_names()
print_top_words(nmf, tfidf_feature_names, n_top_words)

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
# print_top_words(lda, tf_feature_names, n_top_words)