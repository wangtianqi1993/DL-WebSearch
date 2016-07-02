# !/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'wtq'

import numpy as np
import tensorflow as tf
from pymongo import MongoClient
# from document_data.data_process.conn_mongo import conn_mongo


client = MongoClient('127.0.0.1', 27017)
db = client.webSearch


# Parameters
learning_rate = 0.1
training_epochs = 15
batch_size = 10
display_step = 1

# Network Parameters
n_hidden_1 = 500
n_hidden_2 = 500
n_input = 3004
# n_classes = 16491
score_len = 16456
n_classes = 128

# tf Graph input
query = tf.placeholder('float', [None, n_input])
documents = tf.placeholder('float', [None, n_input])
true_score = tf.placeholder('float', [None, score_len])
drop_prob = tf.placeholder("float")

# Store layers weights & bias
weights = {
    'h1': tf.Variable(tf.random_normal([n_input, n_hidden_1])),
    'h2': tf.Variable(tf.random_normal([n_hidden_1, n_hidden_2])),
    'out': tf.Variable(tf.random_normal([n_hidden_2, n_classes]))
}
biases = {
    'b1': tf.Variable(tf.random_normal([n_hidden_1])),
    'b2': tf.Variable(tf.random_normal([n_hidden_2])),
    'out': tf.Variable(tf.random_normal([n_classes]))
}


# get all document vector
all_document = []
for item in db.query_answer_vector.find():
    all_document.append(item['answer'])

all_query = []
all_score = []
sign = 0
temp_query = []
temp_score = []
for item in db.query_doc_similar.find():

    temp_query.append(item['query'])
    temp_score.append(item['similar_score'])
    sign += 1
    if sign > 29:
        sign = 0
        all_query.append(temp_query)
        all_score.append(temp_score)
        temp_query = []
        temp_score = []


# Create model
def multilayer_perceptron(x, weights, biases):
    # Hidden layer with Tanh activation
    layer_1 = tf.add(tf.matmul(x, weights['h1']), biases['b1'])
    layer_1 = tf.nn.relu(layer_1)

    # Hidden layer with Tanh activation
    layer_2 = tf.add(tf.matmul(layer_1, weights['h2']), biases['b2'])
    layer_2 = tf.nn.relu(layer_2)

    # using drop out
    layer2_drop = tf.nn.dropout(layer_2, drop_prob)

    # Output layer with linear activation
    out_layer = tf.add(tf.matmul(layer2_drop, weights['out']), biases['out'])
    return out_layer


# reduce query and documents length from 30013 to 128
query_dimension = multilayer_perceptron(query, weights, biases)
document_matrix = multilayer_perceptron(documents, weights, biases)

# 查询与文档都归一化为单位向量，方便计算consin距离
norm1 = tf.sqrt(tf.reduce_sum(tf.square(query_dimension), 1, keep_dims=True))
normal_query = query_dimension / norm1

norm2 = tf.sqrt(tf.reduce_sum(tf.square(document_matrix), 1, keep_dims=True))
normal_document = document_matrix / norm2
# transpose document
# document_transpose = tf.transpose(document_matrix)

# Define loss and optimizer

similar_score = tf.nn.softmax(0.6*tf.matmul(normal_query, normal_document, transpose_b=True))
entropy = true_score*tf.log(similar_score)
cross_entropy = -tf.reduce_sum(entropy)
# cost = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(similar_score, true_score))

optimizer = tf.train.AdagradOptimizer(learning_rate=learning_rate).minimize(cross_entropy)

# Initializing the variables
init = tf.initialize_all_variables()

# Launch the graph
with tf.Session() as sess:
    sess.run(init)
    # Training cycle
    for epoch in range(training_epochs):
        avg_cost = 0.
        # total_batch = int(mnist.train.num_examples/batch_size)
        # Loop over all batches
        i = 0
        # 这里可以一条一条的加载query
        # for items in db.query_doc_similar.find():
        for i in range(0, len(all_query)):
            # i = 0
            # i += 1
            # if i > 20:
            #     break
            query_item = []
            label_score = []
            print 'in session'
            # Run optimization op (backprop) and cost op (to get loss value)
            for j in range(0, len(all_query[i])):
                q = all_query[i][j]
                scores = all_score[i][j]

                label_score.append(map(float, scores))
                query_item.append(map(float, q))
                # query_item = [query_item]

            a, c, nq, nd, s, ens = sess.run([optimizer, cross_entropy, normal_query, normal_document, similar_score, entropy],
                            feed_dict={query: query_item, documents: all_document, true_score: label_score, drop_prob: 0.5})

            # Compute average loss
            avg_cost += c
            # print 'query_dimension', nq
            # print 'document_dimension', nd
            # print 'similar_score', s
            print 'cost ', c/30
            print 'entropy', ens
        # Display logs per epoch step
        # if epoch % display_step == 0:
        print "Epoch:", '%04d' % (epoch + 1), "cost=", \
            "{:.9f}".format(avg_cost)

    print "Optimization Finished!"

    # # Test model
    # correct_prediction = tf.equal(tf.argmax(pred, 1), tf.argmax(y, 1))
    # # Calculate accuracy
    # accuracy = tf.reduce_mean(tf.cast(correct_prediction, "float"))
    # print "Accuracy:", accuracy.eval({x: mnist.test.images, y: mnist.test.labels})
