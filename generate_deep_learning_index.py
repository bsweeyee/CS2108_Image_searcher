import os, sys
import utility.util as util
import csv
import tensorflow as tf
import deeplearning.classify_image as classify_image

""" takes multiple images and runs deep learning feature
		on all images, outputting as csv file
	"""
def create_deep_learning_index():
	jpg_paths = util.get_jpg_paths(util.database_path)
	with open('deep_learning_2.csv', 'w') as output:
		writer = csv.writer(output)

		for image_path in jpg_paths:
			image_id = os.path.basename(image_path)
			
			with tf.Graph().as_default():	
				predictions = classify_image.run_inference_on_image(image_path)
			
			vectorArray = predictions.tolist()
			vectorArray.insert(0, image_id)
			writer.writerows([vectorArray])

create_deep_learning_index()