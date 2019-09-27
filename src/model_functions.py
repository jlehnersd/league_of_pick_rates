#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 26 16:38:24 2019

@author: jeremy_lehner
"""

import numpy as np


def adjusted_r2(X_test, y_test, y_pred):
    """
    Calculates the adjusted R^2 from the residuals of the test set predictions

    Parameters
    ----------
    X_test : pandas data frame
             Test data set
    y_test : pandas series
             Actual win rates from the test set
    y_pred : numpy array
             Predicted win rates for the test set

    Returns
    -------
    r2_adj : float
                 An OLS linear regression model
    prediction : numpy array
                 Contains the predicted pick rates for the test set
    mse
    """

    # Get number of observations and number of features in test set
    n_obs = len(y_test)
    n_feat = X_test.shape[1]

    # Calculate sum of squares quantities
    ss_residual = sum((y_test - y_pred)**2)
    ss_total = sum((y_test - np.mean(y_test))**2)

    # Calculate R^2 scores
    r2 = 1.0 - (ss_residual / ss_total)
    r2_adj = 1.0 - (1.0 - r2) * (n_obs - 1.0) / (n_obs - n_feat - 1.0)

    return r2_adj
