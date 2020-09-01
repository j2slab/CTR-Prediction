=============================
Click Through Rate Prediction
=============================


.. image:: https://img.shields.io/pypi/v/ctr.svg
        :target: https://pypi.python.org/pypi/ctr

.. image:: https://img.shields.io/travis/j2slab/ctr.svg
        :target: https://travis-ci.com/j2slab/ctr

.. image:: https://readthedocs.org/projects/ctr/badge/?version=latest
        :target: https://ctr.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status


.. image:: https://pyup.io/repos/github/j2slab/ctr/shield.svg
     :target: https://pyup.io/repos/github/j2slab/ctr/
     :alt: Updates



The Importance of Click-Through Rates
-------------------------------------

Click-through rate (CTR), the percent of impressions clicked on by the user, 
is not only descriptive but prescriptive. CTR reveals the strength 
(or weakness) and quality of ad copy, imagery, positioning, and keywords. 
CTR also determines ad position as well as the cost of ad placements. 
For instance, Google uses CTR to determine not only the amount paid for 
online advertising but also the placement of the ad on search pages.  
A low CTR reduces the Quality Score; consequently, Google determines that 
the ad is not as relevant as others on the page. Therefore, marketers with low 
CTRs have lower page positions, and to add insult to injury, incur higher 
pay-per-click rates. 

Therefore, accurate CTR prediction is imperative for online marketers.

How Big is the Problem
----------------------
In a word, massive! Global digital ad spending crested $325 billion in 
2019 [1]_, and analysts expect digital ad spending to reach $982.82 billion 
by 2025, at a CAGR of 21.6% [2]_. A McKinsey study shows that using data to 
make better marketing decisions can increase marketing productivity by 
15%-20%. Given the average annual global marketing spend of $ trillion, 
that converts to $200 billion global ad savings [3]_. Accordingly, analysts 
expect the customer analytics market to grow from $10.5 billion in 2020 to 
$24.2 billion by 2025, at a compound annual growth rate (CAGR) of 18.2%. 

Project Scope
-------------
This project aims to evaluate two state-of-the-art deep learning models 
vis-à-vis machine learning techniques such as Logistic Regression, 
Support Vector Machines, and Extreme Gradient Boosting. The two deep 
learning models are:

- Deep Field-weighted Factorization Machine 
- An Ensemble of Diverse Models

Deep Field-weighted Factorization Machine was first proposed by Deng, Pan, 
and Zhou et. al. in their 2020 paper "DeepLight: Deep Lightweight Feature 
Interactions for Accelerating CTR Predictions in Ad Serving" [4]_. The model
scored an AUC of 0.8123 on the Criteo 1TB Click Through Rate dataset, the
highest score to date on the world's largest click-through rate 
benchmark dataset.  

The Ensemble of Diverse Models, proposed by the National Taiwan University
Team was introduced in their paper "A Two-Stage Ensemble of Diverse Models for
Advertisement Ranking in KDD Cup 2012"{5]_.

Deep Field-weighted Factorization Machine (DeepFwFM)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
The embedding-based neural networks, those that map high dimension categorical 
features to lower dimension, continuous predictors,  learn both explicit 
feature interactions through a shallow component and deep feature interactions 
using a deep neural network (DNN) component. These sophisticated models, 
however, come at high computation and memory expense. Computation times are 
on the order of 100 times higher than other state-of-the-art techniques.

This framework accelerates CTR predictions in three respects:

1.	accelerate the model inference via explicitly searching informative 
        feature interactions in the shallow component; 
2.	prune redundant layers and parameters at intra-layer and inter-layer 
        level in the DNN component; 
3.	promote the sparsity of the embedding layer to preserve the 
        most discriminant signals. 

By integrating the above components, this approach accelerates model inference 
on the order of 46X on Criteo dataset with no loss in prediction accuracy. 
This approach is a step towards more effective production deployment of 
complicated embedding-based neural networks for ad serving and 
management. 

An Ensemble of Diverse Models
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
The system ensemble contains the following models: 
1.	Classification Models
        a.	Naïve Bayes
        b.	Logistic Regression       

2.	Regression Models          
        a.	Ridge Regression          
        b.	Support Vector Regression        

3.	Ranking Models        
        a.	Rank Logistic Regression            
        b.	RankNet          

4.	Matrix Factorization Models         
        a.	Regression-Based Matrix Factorization          
        b.	Ranking Based Matrix Factorization                   

Once completed, an empirical evaluation will be conducted on two datasets:

1.      The Criteo Labs Click-Through Rate Dataset [6]_
created using TensorFlow, will be evaluated vis-à-vis the DeepFwFM.


References
----------
.. [1]	EMarketer, “Global Digital Ad Spending Update Q2 2020 - eMarketer 
        Trends, Forecasts & Statistics,” 2019. [Online]. 
        Available: https://www.emarketer.com/content/global-digital-ad-spending-update-q2-2020. 
        [Accessed: 23-Aug-2020].

.. [2]	Mordor Intelligence, “Online Advertising Market | Growth, Trends, and 
        Forecast (2020 - 2025),” 2019. [Online]. 
        Available: https://www.mordorintelligence.com/industry-reports/online-advertising-market. 
        [Accessed: 23-Aug-2020].

.. [3]	Mckinsey, “Digitizing the consumer decision journey | McKinsey,” 2014. 
        [Online]. Available: 
        https://www.mckinsey.com/business-functions/marketing-and-sales/our-insights/digitizing-the-consumer-decision-journey. 
        [Accessed: 23-Aug-2020].

.. [4]	W. Deng, J. Pan, T. Zhou, A. Flores, and G. Lin, “DeepLight: Deep 
        Lightweight Feature Interactions for Accelerating CTR Predictions in 
        Ad Serving,” 2020.

.. [5]	K. Wu et al., “A Two-Stage Ensemble of Diverse Models for Advertisement 
        Ranking in KDD Cup 2012,” KDD KDD Cup Work., 2012.

.. [6]  “IEEE Xplore Full-Text PDF:” [Online]. 
        Available: https://ieeexplore.ieee.org/stamp/stamp.jsp?arnumber=8566156.
        [Accessed: 23-Aug-2020].

Features
--------

* Some really kewl stuff.

license
-------
* Free software: BSD license

Documentation
-------------
TODO

:Authors:
    John James @ nov8.ai      
:Version: 0.1.0
:Dedication: To my Mother.


