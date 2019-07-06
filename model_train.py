'''
 
Description: This code trains the malware detection model

'''

from feature_Extraction import create_vector_single
import pickle
import datetime
import sys
from sklearn import svm
import random
from sklearn.feature_selection import SelectFromModel
from sklearn.svm import LinearSVC
from sklearn.model_selection import KFold
from sklearn.model_selection import cross_val_score


def load_data():
	feature_vector = []
	# Data format
	# Column 0: Class label (1: Malware, 0: Benign)
	# Column 1-19: Features
	with open('final_data.csv','r') as fp:
		for i,line in enumerate(fp):
			if i == 0:
				pass
			else:
				feature_vector.append([int(x.strip()) for x in line.split(',')])
	return feature_vector


'''
Driver Function
Usage: python model_train.py train_test/k-fold
'''
if __name__ == "__main__":

	# Check for arguments
	if len(sys.argv) > 1:
		evaluation_metrics = sys.argv[1]

		# Load the data
		data = load_data()

		# Shuffle the data
		random.shuffle(data)

		# If evaluation metrics is using training and testing
		if evaluation_metrics == "train_test":
			# Divide the data into training and testing in 60:40
			trainLength = int(0.6*len(data))
			# Training Data
			trainX = [x[:-1] for x in data[:trainLength]]
			trainY = [y[-1] for y in data[:trainLength]]

			# Testing Data
			testX = [x[:-1] for x in data[trainLength:]]
			testY = [y[-1] for y in data[trainLength:]]


			# Perform training
			print('Training the data....')
			train_result = {'timestamp': datetime.datetime.now(),'alg_type': 'svm'}
			clf = svm.SVC()
			clf.set_params(kernel='rbf').fit(trainX, trainY)

			print('Accuracy: {:.3f}%'.format(clf.score(testX, testY)*100))
			# Save the trained model so that it can be used later
			pickle.dump(clf, open( "new_train_data.p", "wb" ))
			print('Model trained and saved.')


		else:
			X = [x[:-1] for x in data]
			Y = [y[-1] for y in data]
			k_fold = KFold(5)
			clf = svm.SVC()
			results = []
			i = 1
			
			print('Performing 5-fold cross validation....')
			
			for train, test in k_fold.split(X):
				x = [X[ind] for ind in train]
				y = [Y[ind] for ind in train]
				x_test = [X[ind] for ind in test]
				y_test = [Y[ind] for ind in test]

				clf.set_params(kernel='rbf').fit(x,y)
				score = clf.score(x_test,y_test)
				results.append(score)
				print("[fold {0}]  score: {1:.5f}".format(i, score))
				i+=1

			print('Mean Score: {}'.format(sum(results)/len(results)))

			# Dump the model	
			pickle.dump(clf, open("kfold_train_data.p", "wb"))
			print("Model trained and saved.")


	else:
		print('[+] Usage: python {} <train_test/k-fold>'.format(__file__))
	 

