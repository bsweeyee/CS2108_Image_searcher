import os, sys
from lshash import LSHash
import csv
import numpy
import classify_image

hash_size = 6
database_path = "./deep_learning.csv"

class Generate_LSH(object):

	def __init__(self, database_path, vector_length):
		self.database_path = database_path
		self.lsh = LSHash(hash_size, vector_length)

	def get_image_dataset_vectors(self):
		image_dataset = []
		with open(self.database_path, 'r') as reader:
			csv_reader = csv.reader(reader)	
			for row in csv_reader:
				image_dataset.append(row)

		return image_dataset

	def generate_hash(self):
		image_data = self.get_image_dataset_vectors()	
		for vector in image_data:
			temp_vector = []
			keyword = vector.pop(0)
			for i in xrange(len(vector)):
				temp_vector.append(float(vector[i]))

			self.lsh.index(temp_vector, keyword)

	def search_lsh(self, query_vector):
		query = []
		for value in query_vector:
			query.append(float(value))

		return self.lsh.query(query, num_results=16, distance_func="true_euclidean")

print "done"

