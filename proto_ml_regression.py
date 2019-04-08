from sklearn.decomposition import PCA
import sys
import warnings
from sklearn.linear_model import LinearRegression as LR
from sklearn.preprocessing import KBinsDiscretizer as KBD
from sklearn.model_selection import cross_val_score as cvs
from sklearn.model_selection import LeaveOneOut
from sklearn.model_selection import train_test_split
import numpy as np
import math

features = []
classLabels = []

warnings.simplefilter("ignore")

def findOptimalComponents():
  min_error = 0
  optn = 0
  reg = LR(fit_intercept = True)
  for n in range(1, len(features[0])):
    pca = PCA(n)
    pca.fit(features)
    newfeatures = pca.transform(features)
    n_error = cvs(reg, newfeatures, classLabels, cv = 3).tolist()
    n_avg = avg(n_error)
    print(n_avg, n)
    if abs(n_avg) < min_error or min_error == 0:
      min_error = n_avg
      optn = n
      
  return optn, min_error
  
def avg(lst): 
    return sum(lst) / len(lst) 

def getData():
  global classLabels, features
  data = np.loadtxt(fname = './trimmed_large_dataset#2.csv', delimiter = ';')
  features = data[1:,:]
  classLabels = data[0,:]
  print(features)
  features = features.transpose()
  classLabels = classLabels.transpose()
  return features.tolist(), classLabels.tolist()

def main():
    getData()  
                    
    print(len(features[0]))
    print(findOptimalComponents())
    print(classLabels)
    print("10 fold scores for linear regression\n", cvs(LR(fit_intercept = False), features, classLabels, cv = 10).tolist(),"\n __________________________________\n")
    reg = LR(fit_intercept = True).fit(features, classLabels)
    print(reg.coef_)

if __name__ == "__main__":
    main()