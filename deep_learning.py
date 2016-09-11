import csv
import os, sys
import tensorflow as tf
import classify_image
import math

# Class takes in the csv file that contains database vectors
class Deep_Learning:
	def __init__(self, database_path):
		self.database_path = database_path
		self.image_dataset = []
		self.image_id = []

	# takes pre-computed deep_learning vectors from database_path (a csv most likely)
	# and places them into a list name 'self.image_dataset'
	def get_image_dataset_vectors(self):
		i = 0
		with open(self.database_path, 'r') as reader:
			csv_reader = csv.reader(reader)	
			for row in csv_reader:
				self.image_dataset.append(row)
				self.image_id.append(self.image_dataset[i].pop(0))
				i += 1

	# computes similarity index between query and each image
	# from self.image_dataset
	# Method: euclidian distance

	def compute_similarity(self, query_data):
		image_dists = {}
		i = 0
		for image in self.image_dataset:
			diff_sum = 0
			sum_1 = 0
			sum_2 = 0
			for j in xrange(len(query_data)):
				diff_sum += math.pow(float(image[j])-float(query_data[j]), 2)
				sum_1 += math.pow(float(image[j]), 2)
				sum_2 += math.pow(float(query_data[j]), 2)
			#normalized distance
			image_dists[self.image_id[i]] = math.sqrt(diff_sum/math.sqrt(sum_1*sum_2))
			i += 1

		return image_dists

	# takes query_path and runs it on deep_learning API "classify_image"
	# returns a list of vectors as query_data then computes similarity index
	# returns an unsorted list of similarity vector for every image

	def search_deeplearning(self, query_path):
		self.get_image_dataset_vectors()
		query_data = classify_image.run_inference_on_image(query_path)
		image_similarity = self.compute_similarity(query_data.tolist())

		return image_similarity
