import csv
import sys
import warnings
from sklearn.decomposition import PCA
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

def getData(file):
  global classLabels, features
  data = np.loadtxt(fname = file, delimiter = ';')
  features = data[1:,:]
  classLabels = data[0,:]
  print(features)
  features = features.transpose()
  classLabels = classLabels.transpose()
  return features.tolist(), classLabels.tolist()

def dataFileToArray(file):
  with open(file, 'rU') as f:  
    reader = csv.reader(f)
    data = list(list(rec) for rec in csv.reader(f, delimiter=',')) #reads csv into a list of lists
    for row in range(len(data)):
      for item in range(len(data[row])):
        if data[row][item] == '':
          data[row][item] = '0'
  datarray = [i for i in data[1:]]
  
  newdata = []
  for row in datarray:
    newdata.append(row[1:])

  global features, classLabels
  returndata = np.array(newdata)
  features = returndata[1:,:]
  classLabels = returndata[0,:]
  print(features)
  features = features.transpose()
  classLabels = classLabels.transpose()



def main():
  file_name = sys.argv[1]
  dataFileToArray(file_name)
                  
  print(len(features[0]))
  print(findOptimalComponents())
  print(classLabels)
  print("10 fold scores for linear regression\n", cvs(LR(fit_intercept = False), features, classLabels, cv = 10).tolist(),"\n __________________________________\n")
  reg = LR(fit_intercept = True).fit(features, classLabels)
  print(reg.coef_)

if __name__ == "__main__":
    main()