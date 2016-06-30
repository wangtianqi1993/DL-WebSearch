# !/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'wtq'

import numpy as np
import tensorflow as tf
from document_data.data_process.conn_mongo import conn_mongo

client = conn_mongo()
db = client.webSearch


# Parameters
learning_rate = 0.001
training_epochs = 15
batch_size = 10
display_step = 1

# Network Parameters
n_hidden_1 = 3000
n_hidden_2 = 3000
n_input = 30013
# n_classes = 16491
n_classes = 128

# tf Graph input
query = tf.placeholder('float', [None, n_input])
# y = tf.placeholder('float', [None, n_classes])
# document = tf.placeholder('float', [16491, n_input])

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


# ge all query vector
all_query = []

query_find = db.query_doc_similar.find()

p = 0

for item in query_find:
    p += 1
    all_query.append(item['query'])
    if p > 5:
        break


# Create model
def multilayer_perceptron(x, weights, biases):

    # Hidden layer with Tanh activation
    layer_1 = tf.add(tf.matmul(x, weights['h1']), biases['b1'])
    layer_1 = tf.nn.tanh(layer_1)

    # Hidden layer with Tanh activation
    layer_2 = tf.add(tf.matmul(layer_1, weights['h2']), biases['b2'])
    layer_2 = tf.nn.tanh(layer_2)

    # Output layer with linear activation
    out_layer = tf.add(tf.matmul(layer_2, weights['out']), biases['out'])
    return out_layer


# reduce query and documents length from 30013 to 128
query = multilayer_perceptron(query, weights, biases)
document_matrix = []

for item in db.query_answer_vector.find():
    docu = item['answer']
    # change type from int to float
    docu = map(float, docu)

    # change the document type from list to tf.constant
    temp_doc = tf.constant([docu])
    print temp_doc
    temp_score = multilayer_perceptron(temp_doc, weights, biases)
    print temp_score[0, 0]
    document_matrix.append(temp_score[0, 0])

document_matrix = np.mat(document_matrix)
document_matrix = document_matrix.transpose()

# Define loss and optimizer
similar_score = tf.nn.softmax(tf.matmul(query, document_matrix))

true_score = db.query_doc_similar_find({"query": query})
true_score = true_score[0]["similar_score"]
true_score = [true_score]

cost = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(similar_score, true_score))
optimizer = tf.train.GradientDescentOptimizer(learning_rate=learning_rate).minimize(cost)

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
        for i in range(len(all_query)):

            # Run optimization op (backprop) and cost op (to get loss value)
            all_query[i] = map(float, all_query[i])

            all_query[i] = [all_query[i]]
            a, c = sess.run([optimizer, cost], feed_dict={query: all_query[i]})

            # Compute average loss
            avg_cost += c
        # Display logs per epoch step
        if epoch % display_step == 0:
            print "Epoch:", '%04d' % (epoch+1), "cost=", \
                "{:.9f}".format(avg_cost)
    print "Optimization Finished!"

    # # Test model
    # correct_prediction = tf.equal(tf.argmax(pred, 1), tf.argmax(y, 1))
    # # Calculate accuracy
    # accuracy = tf.reduce_mean(tf.cast(correct_prediction, "float"))
    # print "Accuracy:", accuracy.eval({x: mnist.test.images, y: mnist.test.labels})


