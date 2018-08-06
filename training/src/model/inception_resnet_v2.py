from __future__ import absolute_import
from __future__ import division
from __future__ import print_function


import tensorflow as tf

slim = tf.contrib.slim

def block8(net, scale=1.0, activation_fn=None, scope=None, reuse=None):
  """Builds the 8x8 resnet block."""
  with tf.variable_scope(scope, 'Block8', [net], reuse=reuse):
    with tf.variable_scope('Branch_0'):
      tower_conv = slim.conv2d(net, 96, 1, scope='Conv2d_1x1')
    with tf.variable_scope('Branch_1'):
      tower_conv1_0 = slim.conv2d(net, 96, 1, scope='Conv2d_0a_1x1')
      tower_conv1_1 = slim.conv2d(tower_conv1_0, 144, [1, 3],
                                  scope='Conv2d_0b_1x3')
      tower_conv1_2 = slim.conv2d(tower_conv1_1, 192, [3, 1],
                                  scope='Conv2d_0c_3x1')
    mixed = tf.concat(axis=3, values=[tower_conv, tower_conv1_2])
    up = slim.conv2d(mixed, net.get_shape()[3], 1, normalizer_fn=None,
                     activation_fn=None, scope='Conv2d_1x1')
    net = net + scale * up
    if activation_fn is not None:
      net = activation_fn(net)
  return net

def inception_resnet_v2_conv(inputs, is_training, reuse=None, scope='InceptionResnetV2'):
    end_points = {}
    with tf.variable_scope(scope, 'InceptionResnetV2', [inputs], reuse=reuse):
        with slim.arg_scope([slim.batch_norm], is_training=is_training):
            with slim.arg_scope([slim.conv2d, slim.max_pool2d, slim.avg_pool2d], stride=1, padding='SAME'):
                # 15 x 15 x 64
                net = slim.conv2d(inputs, 64, 3, scope='Conv2d_1a_3x3')
                end_points['Conv2d_1a_3x3'] = net
                # 15 x 15 x 128
                net = slim.conv2d(net, 128, 3, scope='Conv2d_2a_3x3')
                end_points['Conv2d_2a_3x3'] = net

                # 15 x 15 x 256
                with tf.variable_scope('Mixed_5b'):
                    with tf.variable_scope('Branch_0'):
                        tower_conv = slim.conv2d(net, 64, 1, scope='Conv2d_1x1')
                    with tf.variable_scope('Branch_1'):
                        tower_conv1_0 = slim.conv2d(net, 32, 1, scope='Conv2d_0a_1x1')
                        tower_conv1_1 = slim.conv2d(tower_conv1_0, 64, 5,
                                                    scope='Conv2d_0b_5x5')
                    with tf.variable_scope('Branch_2'):
                        tower_conv2_0 = slim.conv2d(net, 64, 1, scope='Conv2d_0a_1x1')
                        tower_conv2_1 = slim.conv2d(tower_conv2_0, 64, 3,
                                                    scope='Conv2d_0b_3x3')
                        tower_conv2_2 = slim.conv2d(tower_conv2_1, 64, 3,
                                                    scope='Conv2d_0c_3x3')
                    with tf.variable_scope('Branch_3'):
                        tower_pool = slim.avg_pool2d(net, 3, stride=1, padding='SAME',
                                                     scope='AvgPool_0a_3x3')
                        tower_pool_1 = slim.conv2d(tower_pool, 64, 1,
                                                   scope='Conv2d_0b_1x1')
                    net = tf.concat(axis=3, values=[tower_conv, tower_conv1_1,
                                                    tower_conv2_2, tower_pool_1])

                end_points['Mixed_5b'] = net

                net = block8(net, scale=0.50, activation_fn=tf.nn.relu)
                net = block8(net, scale=0.50, activation_fn=tf.nn.relu)
                net = block8(net, scale=0.50, activation_fn=tf.nn.relu)
                net = block8(net, scale=0.50, activation_fn=tf.nn.relu)

                end_points['End'] = net

                return net, end_points

def inception_resnet_v2_arg_scope(weight_decay=0.0004,
                                  batch_norm_decay=0.997,
                                  batch_norm_epsilon=0.001):
  """Yields the scope with the default parameters for inception_resnet_v2.
  Args:
    weight_decay: the weight decay for weights variables.
    batch_norm_decay: decay for the moving average of batch_norm momentums.
    batch_norm_epsilon: small float added to variance to avoid dividing by zero.
  Returns:
    a arg_scope with the parameters needed for inception_resnet_v2.
  """
  # Set weight_decay for weights in conv2d and fully_connected layers.
  with slim.arg_scope([slim.conv2d, slim.fully_connected],
                      weights_regularizer=slim.l2_regularizer(weight_decay),
                      biases_regularizer=slim.l2_regularizer(weight_decay)):

    batch_norm_params = {
        'decay': batch_norm_decay,
        'epsilon': batch_norm_epsilon,
    }
    # Set activation_fn and parameters for batch_norm.
    with slim.arg_scope([slim.conv2d], activation_fn=tf.nn.relu,
                        normalizer_fn=slim.batch_norm,
                        normalizer_params=batch_norm_params) as scope:
      return scope