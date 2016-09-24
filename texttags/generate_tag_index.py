import os, sys
import utility.util as util
import csv
from texttags.PorterStemmer import PorterStemmer

test_tags = "./texttags/test_text_tags.txt"
train_tags = "./texttags/train_text_tags.txt"

# extracts a dictionary of image-tag_name pair
def extract_tags(tag_text):
	image_tags = {}

	with open(tag_text, 'r') as reader:
		#lines = reader.readlines()
		lines = [line.rstrip('\n') for line in reader]

	for one_line in lines:
		words = one_line.split()
		image_tags[words.pop(0)] = words

	return image_tags

# stems tags (words which are plural are removed etc)
def stem_words(tag_dict):
	stemmer = PorterStemmer()
	for image, tags in tag_dict.iteritems():
		stemmed_tags = []
		if tags:
			for tag in tags:
				stemmed_tag = stemmer.stem(tag, 0, len(tag)-1)
				if stemmed_tag not in stemmed_tags:	
					stemmed_tags.append(stemmed_tag)
		
		tag_dict[image] = stemmed_tags

	return tag_dict

def create_list_of_tags(tag_dict):
	list_of_tags = []
	for (image, tags) in tag_dict.iteritems():
		if tags:
			for tag in tags:
				if tag not in list_of_tags:
					list_of_tags.append(tag)

	return list_of_tags

def create_tag_csv(input_path, tag_text):
	image_ids = util.get_image_ids(input_path)
	tag_dict = stem_words(extract_tags(tag_text))

	#list_of_tags = create_list_of_tags(tag_dict)

	with open("tag_text.csv", 'w') as output:
		writer = csv.writer(output)
		for image_name in image_ids:
			if image_name in tag_dict.keys():
				row = tag_dict[image_name]
				row.insert(0, image_name)
				writer.writerows([row])
			else:
				row = []
				row.append(image_name)
				writer.writerows([row])


# run this to generate tag csv
#create_tag_csv(util.query_path, test_tags)
#create_tag_csv(util.database_path, train_tags)
tag_lists =  create_list_of_tags(stem_words(extract_tags(train_tags)))
print len(tag_lists)

