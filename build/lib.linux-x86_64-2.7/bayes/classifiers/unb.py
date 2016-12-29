#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
from sklearn.preprocessing import LabelBinarizer

from base import BaseNB


# Author: Krzysztof Joachimiak


class UniversalSetNB(BaseNB):

    '''
    Universal-set Naive Bayes classifier

    Parameters
    ----------
    alpha: float
        Smoothing parameter

    References
    ----------
    Komiya K., Ito Y., Kotani Y. (2013).
    New Naive Bayes Methods using Data from All Classes

    http://aia-i.com/ijai/sample/vol5/no1/1-13.pdf
    '''

    def __init__(self, alpha=1.0):
        super(UniversalSetNB, self).__init__()

        # Params
        self.alpha = alpha
        self.alpha_sum_ = None
        self._check_alpha_param()

        # Computed attributes
        self.classes_ = None
        self.class_counts_ = None
        #self.complement_class_log_proba_ = None
        self.class_log_proba_ = None
        self.complement_features_ = None
        self.features_ = None

    # @property
    # def complement_class_count_(self):
    #     from bayes.utils import get_complement_matrix
    #     size = self.class_counts_.shape[1]
    #     return self.class_counts_.dot(get_complement_matrix(size))
    #
    # @property
    # def complement_class_log_proba_(self):
    #     all_samples_count = np.float64(np.sum(self.class_counts_))
    #     self.class_log_proba_ = np.log(self.class_counts_ / all_samples_count)
    #     return


    def fit(self, X, y):
        self._reset()
        self._partial_fit(X, y)
        return self

    def partial_fit(self, X, y, classes=None):
        self._partial_fit(X, y, classes=classes, first_partial_fit=not self.is_fitted)
        return self

    def predict(self, X):
        return self.classes_[np.argmax(self.predict_log_proba(X), axis=1)]

    def predict_log_proba(self, X):
        self._check_is_fitted()
        return self._log_proba(X) - self._complement_log_proba(X)

    def get_params(self):
        return self.__dict__

    def set_params(self, **params):
        self.__dict__.update(params)
        return self

    # Making predictions
    def _complement_log_proba(self, X):
        denominator = np.sum(self.complement_features_, axis=0) + self.alpha_sum_
        features_weights = np.log((self.complement_features_ + self.alpha) / denominator)
        features_doc_logprob = self.safe_matmult(X, features_weights.T)
        return (features_doc_logprob) + self.complement_class_log_proba_

    def _log_proba(self, X):
        denominator = np.sum(self.features_, axis=0) + self.alpha_sum_
        features_weights = np.log((self.features_ + self.alpha) / denominator)
        features_doc_logprob = self.safe_matmult(X, features_weights.T)
        return (features_doc_logprob) + self.complement_class_log_proba_

    # Fitting model

    def _partial_fit(self, X, y, classes=None, first_partial_fit=None):

        if first_partial_fit and not classes:
            raise ValueError("classes must be passed on the first call "
                         "to partial_fit.")

        if not self.is_fitted:
            self.alpha_sum_ = X.shape[1] * self.alpha

        if classes:
            self.classes_ = classes

        lb = LabelBinarizer()
        y_one_hot = lb.fit_transform(y)
        self.class_counts_ = np.sum(y_one_hot, axis=0)

        if not self.classes_:
            self.classes_ = lb.classes_

        self._class_log_prob()
        self._features_in_class(X, y_one_hot)
        self.is_fitted = True

    def _class_log_prob(self):
        '''
        Compute complement probability of class occurence
        '''
        all_samples_count = np.float64(np.sum(self.class_counts_))
        self.class_log_proba_ = np.log(self.class_counts_ / all_samples_count)

    def _features_in_class(self, X, y_one_hot):
        '''

        Compute complement features counts

        Parameters
        ----------
        X: numpy array (n_samples, n_features)
            Matrix of input samples
        y_one_hot: numpy array (n_samples, n_classes)
            Binary matrix encoding input
        '''
        if not self.is_fitted:
            self.complement_features_ = X.T.dot(np.logical_not(y_one_hot))
            self.features_ = X.T.dot(y_one_hot)
        else:
            self.complement_features_ += X.T.dot(np.logical_not(y_one_hot))
            self.features_ += X.T.dot(y_one_hot)

    def _reset(self):
        '''

        Reset object params for refit

        '''
        self.classes_ = None
        self.class_counts_ = None
        self.class_log_proba_ = None
        self.complement_features_ = None
        self.complement_class_counts_ = None
        self.class_log_proba_ = None