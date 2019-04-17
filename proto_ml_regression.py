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
import pickle

features = []
classLabels = []
impurities = []
datafile = ''
outfile = ''

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

def dataFileToArray():
  with open(datafile, 'r') as f:  
    data = list(list(rec) for rec in csv.reader(f, delimiter=';')) #reads csv into a list of lists
    for row in range(len(data)):
      for item in range(len(data[row])):
        if data[row][item] == '':
          data[row][item] = '0'
  data = [i for i in data[1:]]
  newdata = []
  global impurities
  for row in data:
    newdata.append([float(j) for j in row[1:]])
    impurities.append(row[0])

  global features, classLabels
  data = np.array(newdata)
  features = data[1:,:]
  classLabels = data[1,:]

  features = features.transpose()
  classLabels = classLabels.transpose()

def LRToOutFile():
  with open(outfile, 'w') as file:
    file.write("3 fold scores for linear regression\n______________________________\n")
    for score in cvs(LR(fit_intercept = False), features, classLabels, cv = 3).tolist():
      file.write(" " + str(score))
    file.write("\n\n _____Coefficients_____\n")
    reg = LR(fit_intercept = True).fit(features, classLabels)
    for feature, coef in zip(impurities, reg.coef_):
      file.write(feature + ": " + str(coef) + "\n")

def RunRegressionAnalysis(dfile, outputfile):
  global datafile, outfile
  datafile = dfile
  outfile = outputfile
  dataFileToArray()
  LRToOutFile()
  print("3 fold scores for linear regression\n", cvs(LR(fit_intercept = False), features, classLabels, cv = 3).tolist(),"\n __________________________________\n")
  reg = LR(fit_intercept = True).fit(features, classLabels)
  for feature, coef in zip(impurities, reg.coef_):
    print(feature, coef)

if __name__ == "__main__":
  RunRegressionAnalysis(sys.argv[1], sys.argv[2])