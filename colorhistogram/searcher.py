# import the necessary packages
import numpy as np
import csv
import cv2
from colordescriptor import ColorDescriptor
import math

# Class takes in the csv file that contains database vectors
class Searcher:
	def __init__(self, indexPath):
		# store our index path
		self.indexPath = indexPath

	def search(self, queryFeatures):
		# initialize our dictionary of results
		results = {}

		# open the index file for reading
		with open(self.indexPath) as f:
			# initialize the CSV reader
			reader = csv.reader(f)

			# loop over the rows in the index
			for row in reader:
				# parse out the image ID and features, then compute the
				# chi-squared distance between the features in our index
				# and our query features
				features = [float(x) for x in row[1:]]
				d = self.euclidian_distance(features, queryFeatures)

				# now that we have the distance between the two feature
				# vectors, we can udpate the results dictionary -- the
				# key is the current image ID in the index and the
				# value is the distance we just computed, representing
				# how 'similar' the image in the index is to our query
				results[row[0]] = d

			# close the reader
			f.close()

		# returns an unsorted list of similarity vectors for every image
		return results

	def euclidian_distance(self, histA, histB):
		# compute the normalized euclidian distance
		diff_sum = 0
		sum_1 = 0
		sum_2 = 0
		for j in xrange(len(histB)):
			diff_sum += math.pow(float(histA[j]) - float(histB[j]), 2)
			sum_1 += math.pow(float(histA[j]), 2)
			sum_2 += math.pow(float(histB[j]), 2)

		d = math.sqrt(diff_sum/math.sqrt(sum_1*sum_2))
		# return the normalized euclidian distance
		return d