from builtins import range
import numpy as np
from random import shuffle
from past.builtins import xrange

def softmax_loss_naive(W, X, y, reg):
    """
    Softmax loss function, naive implementation (with loops)

    Inputs have dimension D, there are C classes, and we operate on minibatches
    of N examples.

    Inputs:
    - W: A numpy array of shape (D, C) containing weights.
    - X: A numpy array of shape (N, D) containing a minibatch of data.
    - y: A numpy array of shape (N,) containing training labels; y[i] = c means
      that X[i] has label c, where 0 <= c < C.
    - reg: (float) regularization strength

    Returns a tuple of:
    - loss as single float
    - gradient with respect to weights W; an array of same shape as W
    """
    # Initialize the loss and gradient to zero.
    loss = 0.0
    dW = np.zeros_like(W)

    #############################################################################
    # TODO: Compute the softmax loss and its gradient using explicit loops.     #
    # Store the loss in loss and the gradient in dW. If you are not careful     #
    # here, it is easy to run into numeric instability. Don't forget the        #
    # regularization!                                                           #
    #############################################################################
    # *****START OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****

    num_train = X.shape[0]
    num_classes = W.shape[1]

    for i in range(num_train):
         scores = X[i, :].dot(W)
         exp = np.exp(scores)
         normalized = exp[y[i]]/np.sum(exp) #reevaluate
         loss += -1 *  np.log(normalized)
         
         for j in range(num_classes):
             normalized = exp[j]/np.sum(exp) #reevaluate
             dW[:, j] += (normalized - (j == y[i])) * X[i]

    #los calculations
    loss /= num_train
    loss += reg * (W ** 2).sum().sum()
    
    
    #regularizing
    dW /= num_train
    dW += 2 * W * reg

    # *****END OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****

    return loss, dW


def softmax_loss_vectorized(W, X, y, reg):
    """
    Softmax loss function, vectorized version.

    Inputs and outputs are the same as softmax_loss_naive.
    """
    # Initialize the loss and gradient to zero.
    loss = 0.0
    dW = np.zeros_like(W)

    #############################################################################
    # TODO: Compute the softmax loss and its gradient using no explicit loops.  #
    # Store the loss in loss and the gradient in dW. If you are not careful     #
    # here, it is easy to run into numeric instability. Don't forget the        #
    # regularization!                                                           #
    #############################################################################
    # *****START OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****

    num_classes = W.shape[1]
    num_train = X.shape[0]
    
    #readjusting scores
    scores = X.dot(W)
    score_change = scores - np.max(scores,axis=1).reshape(-1,1)
    exp_scores = np.exp(score_change)
    softmx = exp_scores / np.sum(exp_scores,axis =1).reshape(-1,1)
    
    #calculating loss
    data_loss = - np.sum(np.log(softmx[np.arange(num_train), y]))
    data_loss /= num_train
    data_loss += reg * np.sum(W*W)
    
    #gradient calculations
    dscores = softmx
    dscores[range(num_train), list(y)] += -1
    dscores /= num_train
    dW = np.dot(X.T, dscores) + reg * W
    
    

    # *****END OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****

    return loss, dW
