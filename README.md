# Bayes
Python implementations of Naive Bayes algorithm variations with sklearn-like API.

## Algorithms

#### Complement Naive Bayes

<p align='justify'>
Complement Naive Bayes classifier performs classification by the following equation:
<p align='center'><img  src='https://github.com/krzjoa/Bayes/blob/master/img/eq_cnb.png'></p>
Where:
<p align='left'><img  src='https://github.com/krzjoa/Bayes/blob/master/img/cnb_explanation.png'></p>

More: <i><a href='https://people.csail.mit.edu/jrennie/papers/icml03-nb.pdf'>Tackling the Poor Assumptions of Naive Bayes Text Classifiers</a></i>
 by Rennie J. D. M. et al. 

</p>

#### Weight-normalized Complement Naive Bayes

This method is described in the paper: 
<i><a href='https://people.csail.mit.edu/jrennie/papers/icml03-nb.pdf'>Tackling the Poor Assumptions of Naive Bayes Text Classifiers</a></i>
#### Negation Naive Bayes

<i><a href='http://www.aclweb.org/anthology/R11-1083.pdf'>Negation Naive Bayes for Categorization of Product Pages on the Web</a></i>

#### Universal-set Naive Bayes

<i><a href='http://aia-i.com/ijai/sample/vol5/no1/1-13.pdf'>New Naive Bayes Methods using Data from All Classes</a></i>

#### Selective Naive Bayes

<i><a href='http://aia-i.com/ijai/sample/vol5/no1/1-13.pdf'>New Naive Bayes Methods using Data from All Classes</a></i>

#### Locally Weighted Naive Bayes

<i><a href='http://www.cs.waikato.ac.nz/~eibe/pubs/UAI_200.pdf'>Locally Weighted Naive Bayes</a></i>


## Usage

Bayes classifiers API mimics [Scikit-Learn](http://scikit-learn.org/stable/modules/classes.html) API, so usage is very simple.


``` python
from Bayes.classifiers import ComplementNB
from sklearn.datasets import fetch_20newsgroups
from sklearn.feature_extraction.text import CountVectorizer


vectorizer = CountVectorizer()
categories = ['alt.atheism', 'talk.religion.misc',
              'comp.graphics', 'sci.space']

# Train set
newsgroups_train = fetch_20newsgroups(subset='train',
                                          categories=categories, shuffle=True)
X_train = vectorizer.fit_transform(newsgroups_train.data)
y_train = newsgroups_train.target

# Test set
newsgroups_test = fetch_20newsgroups(subset='test',
                                          categories=categories, shuffle=True)
X_test = vectorizer.fit_transform(newsgroups_test.data)
y_test = newsgroups_test.target

# Score 
cnb = ComplementNB()
cnb.fit(X_train, y_train).accuracy_score(X_test, y_test)
```




## TODO list
* Weighted Complement Naive Bayes
* Negation Naive Bayes
* Locally Weighted Naive Bayes
* Universal-set Naive Bayes Classifier
* Selective Naive Bayes Classifier
* Add project Wiki
