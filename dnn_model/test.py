__author__ = 'wtq'

# import numpy as np
# import tensorflow as tf
#
# query = [[0.1, 0.2, 0.3, 0.4]]
# doc = [
#   [0.1, 0.2, 0.3, 0.4],
#   [0.4, 0.5, 0.6, 0.5],
#   [0.5, 0.6, 0.7, 0.3]
# ]
# doc = np.mat(doc).transpose()
#
# q = tf.placeholder('float64', [None, 4])
# m = [[0.2, 0.3, 0.2, 0.1]]
# score = tf.nn.softmax_cross_entropy_with_logits(q, m)
#
# init = tf.initialize_all_variables()
#
# with tf.Session() as sess:
#   sess.run(init)
#   result = sess.run(score, feed_dict={q: query})
#   print result

a = [1, 2, 34, 3, 2, 4, 2]
a = map(float, a)
print a

def indices(lst, element):
    result = []
    offset = -1
    while True:
        try:
            offset = lst.index(element, offset+1)
        except ValueError:
            return result
        result.append(offset)
print indices(a, 2)
