import csv
import os, sys
import tensorflow as tf
import classify_image
import math
from generate_lsh import Generate_LSH

# Class takes in the csv file that contains database vectors
class Deep_Learning:
	def __init__(self, database_path):
		self.database_path = database_path
		self.image_id = []
		self.lsh_deep_learning = Generate_LSH(database_path, 1008)
		self.lsh_deep_learning.generate_hash()
		classify_image.maybe_download_and_extract()

	""" computes similarity index between query and each image
	 	from self.image_dataset
	 	Method: euclidian distance 
	 	Time: Linear scan
	"""
	def compute_similarity(self, query_data):
		image_dists = {}
		i = 0
		with open(self.database_path, 'r') as reader:
			csv_reader = csv.reader(reader)	
			for database_image in csv_reader:
				keyword = database_image.pop(0)

				#normalized distance
				image_dists[keyword] = self.euclidean_distance(query_data, database_image)

		return image_dists

	"""	searches LSH index and returns top 16 results
	"""
	def find_similar_images(self, query_data):
		image_dists = {}
		lsh_results = self.lsh_deep_learning.search_lsh(query_data)

		for value in lsh_results:
			vector = value[0][0]
			keyword = value[0][1]
		
			# normalized distance
			image_dists[keyword] = self.euclidean_distance(query_data, vector)

		return image_dists

	""" takes query_path and runs it on deep_learning API "classify_image"
		returns a list of vectors as query_data then computes similarity index
		returns an unsorted list of similarity vector for every image
	"""
	def search_deeplearning(self, query_path):
		query_data = classify_image.run_inference_on_image(query_path)
		
		# uses linear search
		image_similarity = self.compute_similarity(query_data.tolist())
		
		# uses LSH
		#image_similarity = self.find_similar_images(query_data.tolist())

		return image_similarity

	"""	Finds euclidean distance given 2 vectors
	"""
	def euclidean_distance(self, query_data, database_image):
		diff_sum = 0
		sum_1 = 0
		sum_2 = 0
		for j in xrange(len(query_data)):
			diff_sum += math.pow(float(database_image[j])-float(query_data[j]), 2)
			sum_1 += math.pow(float(database_image[j]), 2)
			sum_2 += math.pow(float(query_data[j]), 2)

		return math.sqrt(diff_sum/math.sqrt(sum_1*sum_2))

