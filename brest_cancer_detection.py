# -*- coding: utf-8 -*-
"""Brest_cancer_detection.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1DX8gXEyqCC3RtBRhizc7dp_OGwnNqPwC

This project is about the Brest Cancer Detection. In this we are going to train our modle on the basis of given dataset where their are two type of case either patient is Banine or Malignant. Where Banine refers to negitive which means patient is safe and Maligent reffers to positive means patient is having cancer. In this project we take dataset of 569 patient in "data.csv file" where 357 are Banine and 212 are Maligant.


importing pandas for reading csv-files
"""

import pandas as pd

"""Reading csv-file"""

data = pd.read_csv("/content/drive/MyDrive/data.csv")

"""printing the data """

data

data.columns

"""Here we are going to remove the data column which are useless or NAN("not a number") columns """

#nan and datafiltering starts
data.drop(data.columns[32],axis=1,inplace=True)

"""After removing the Nan values printing the data set"""

data

#length of data set 
len(data)

"""From here we are going to diving the testing and training data which we is also a start the data set filtiringin 7:3 ratio where 70% of data is training data and 30% of dataset length is testing data."""

#dividing data in test and training data
training_data_len=int((len(data))*0.7)

#training data length
training_data_len

#testing data length calculation
testing_data_len=int((len(data)*0.3))

testing_data_len

#putting data as trainging and testing on the basisi of m,b by boolean masking
neg_class_data=data[data["diagnosis"]=="B"]

#Displaying the of Bainie dataset
neg_class_data

neg_class_data.shape

#By using the massboolean initinging the pos_class_data set with Manine dataset
pos_class_data=data[data[data.columns[1]]=="M"]

pos_class_data

pos_class_data.shape

"""After seprating the malingent and banine data we are putting the set by half of training data set length"""

train_neg_data=neg_class_data.iloc[0:training_data_len//2,]

train_neg_data.shape

train_pos_data=pos_class_data.iloc[0:training_data_len//2,]

train_pos_data.shape

training_data=pd.concat([train_neg_data,train_pos_data],0)

training_data

test_neg_data=neg_class_data.iloc[training_data_len//2:,]

test_neg_data.shape

test_pos_data=pos_class_data.iloc[training_data_len//2:,]

test_pos_data.shape

test_data=pd.concat([test_neg_data,test_pos_data],0)

test_data

"""Now we are going to implement the Matplotlib library with the pyplot as plt to display the graph and other representation."""

import matplotlib.pyplot as plt

training_data.columns

#finding corelations betweeen data before that finding the points between 2 columns
plt.scatter(training_data[training_data.columns[2]],training_data[training_data.columns[3]])

#correlation
training_data.corr()

"""Replacing the value of B and M by 0 and 1 in training data for the preventing future error because modle takes the decimal value."""

#now deriving the data for the best condtions before data replaing m and b for proper result
test_data[data.columns[1]].replace(to_replace=['B','M'],value=[0,1],inplace=True)

test_data

"""Replacing the value of B and M by 0 and 1 in training data for the preventing future error because modle takes the decimal value."""

training_data[data.columns[1]].replace(to_replace=['B','M'],value=[0,1],inplace=True)

training_data

#storing the correlation data
corr_matrix=training_data.corr()

from sklearn.naive_bayes import GaussianNB
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report

"""Now storing all the thrashold values in the thrashold value.

"""

threshold_list = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]

"""Initilizing the max_precision_recall and best_threshold for finding the best thrashold value at which we are getting the maximum values.

"""

max_precision_recall = 0  # to store the max value of precision and recall obtained
best_threshold = 0

"""Now we are going to do calculating the result on the basis of different thrashold value and store all the columns which are satisfying the "**bold boolean mask of thrashold valuetext**".On the basis of it we are filtering the data(both testing and training data).
After this we are training the model and then we are predicting the testing data for each threshold value.
later in the last on the basis of max precision ,f1_score and accuracy we are calculating corr_thrashold report and printing best threshold for a particular thrashold value.


"""

# iterate through each value of the  threshold_list
for corr_threshold in threshold_list:
  # prepare a dictionary of the filtered columns for each threshold
  D = dict(corr_matrix[training_data.columns[1]] > corr_threshold)
  
  filtered_columns = []   # create an empty list to store the names of columns that will be used in feature selection
  # now, we will append the names of all the columns that will have a True value in the dictionary D
  for col in list(D.keys()):
    if D[col] == True:
      filtered_columns.append(col)  # append to the list

  # get the data of only those columns that have the correlation coefficient greater than `corr_threshold`
  filtered_training_data = training_data[filtered_columns]
  
  # the correct answers are stored in another dataframe `answers`
  answers = filtered_training_data[data.columns[1]]

  # the input features to be used are stored in another dataframe `input_features`
  input_features = filtered_training_data.drop(data.columns[1], axis=1)

  # check if all the columns have been filtered out, then no need for training the model with an empty dataset
  if(input_features.shape[1] == 0): # if no columns have been selected
    print("No columns selected for Pearson Correlation Threshold", corr_threshold)
    continue  # force the next iteration of the loop

  # create an object of GaussianNB
  naive_bayes_algo = GaussianNB()
  # training the model on the train data
  naive_bayes_algo.fit(X=input_features, y=answers) 

  # now filter the testing dataset accorfing the filtered columns obtained
  filtered_testing_data = test_data[filtered_columns]
  testing_answers = filtered_testing_data[data.columns[1]]  # the correct asnwers to be used for testing 
  testing_input_features = filtered_testing_data.drop(data.columns[1], axis=1)  # the filterd testing dataset to be used for testing 
  
  # testing the trained model
  exam_answers = naive_bayes_algo.predict(X=testing_input_features)

  # comparing the original and obtained values
  report_dict = classification_report(y_true=testing_answers, y_pred=exam_answers, output_dict=True)  # for finding the values of precision and recall
  report = classification_report(y_true=testing_answers, y_pred=exam_answers)
  
  # find the sum of precision and recall
  sum = report_dict['macro avg']['precision'] + report_dict['macro avg']['recall']
  if sum > max_precision_recall:
    max_precision_recall = sum
    best_threshold = corr_threshold   # store the best value of threshold
  # print the classification report for each value of the correlation threshold
  print("Classification report for Pearson Correlation Threshold:", corr_threshold)
  print(report)


print("Best value of Pearson Correlation Coefficient: ", best_threshold)





