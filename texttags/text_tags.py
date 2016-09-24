import os, sys
import csv
import math

class TextTags(object):
	# init requires file location
	def __init__(self, database_tags_list, query_tags_list):
		self.database_tags_list = database_tags_list
		self.query_tags_list = query_tags_list
		self.total_number_of_tags = 7177

	# search image tags
	def tags_search(self, query):
		# check if query has tags
		text_tag_dist = {}
		query_tags = []

		query_tags = self.return_query_tags(query)

		with open(self.database_tags_list, 'r') as reader:
			csv_reader = csv.reader(reader)
			for image_database_tags in csv_reader:
				image_name = image_database_tags.pop(0)
				if image_database_tags and query_tags:
					# calculate tag distance
					text_tag_dist[image_name] = self.calculate_distance(query_tags, image_database_tags)
				else:
					text_tag_dist[image_name] = math.sqrt(self.total_number_of_tags)

		return text_tag_dist

	# return query tags
	def return_query_tags(self, query):
		query_basename = os.path.basename(query)
		with open(self.query_tags_list) as reader:
			csv_reader = csv.reader(reader)
			for image_query_tags in csv_reader:
				if query_basename in image_query_tags:
					image_query_tags.pop(0)
					return image_query_tags

	# calculate cosine similarity
	# assumptions: no repeat tags, 1:1 search case 
	# 			   with no word stemming
	# returns the distance between the number of tags in the database with the
	# number of matching tags 
	# i.e. the higher the count is, the lower the distance, hence the more similar it is with the image
	def calculate_distance(self, query_tags, database_tags):
		distance = 0.0
		count = 0.0
		for tag in query_tags:
			if tag in database_tags:
				count += 1.0

		return math.sqrt(self.total_number_of_tags - count)

#text_tag = TextTags("./tag_text_database.csv", "./tag_text_query.csv")
#print text_tag.tags_search("./0018_375723120.jpg")
#print text_tag.return_query_tags("./0018_375723120.jpg")