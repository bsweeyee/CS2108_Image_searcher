import os, sys
import csv

""" A utility module with a bunch of functions that 
	manipulates csv vector files
 	and images in database
""" 

# returns a list of image category folder paths from "database" folder
# eg. '...something.../database/alley'

STUPID_DS_STORE = "/Users/Brandon/Dropbox/NUS/Y3S1/CS2108/Lab/Assignment_1/Our_Image_Searcher/database/.DS_Store"

# modify this to the database path to extract from database image
database_path = "/Users/Brandon/Dropbox/NUS/Y3S1/CS2108/Lab/Assignment_1/Our_Image_Searcher/database"
query_path = "/Users/Brandon/Dropbox/NUS/Y3S1/CS2108/Lab/Assignment_1/Our_Image_Searcher/query"

def get_image_paths():
	i = 1

	data_path = database_path
	image_paths = []

	for i in xrange(len(os.listdir(data_path))):
		image_paths.append(os.path.join(data_path, os.listdir(data_path)[i]))

	if (image_paths[0] == STUPID_DS_STORE):
		image_paths = image_paths[1::]
	
	return image_paths

# returns a list of full individual image directory path 
# from all the image category folders
# eg. '...something.../database/alley/0028_1070815604.jpg'

def get_jpg_paths():
	image_paths_array = get_image_paths()
	jpg_paths = []
	
	for i in xrange(len(image_paths_array)):
		a_image_path = os.listdir(image_paths_array[i])
		for j in xrange(len(a_image_path)):
			jpg_paths.append(os.path.join(image_paths_array[i], a_image_path[j]))

	return jpg_paths

# returns a list of image name + extension from each image
# eg. '0028_1070815604.jpg'

def get_image_ids():
	image_ids = []

	image_paths = get_image_paths()
	for i in xrange(len(image_paths)):
		a_image_path = os.listdir(image_paths[i])
		for j in xrange(len(a_image_path)):
			image_ids.append(a_image_path[j])

	return image_ids

# returns a list of image categories from the database
# eg. 'alley'

def get_image_groups():
	image_paths = get_image_paths()
	image_group = []
	for image in image_paths:
		image_group.append(os.path.basename(image))

	return image_group

# returns a dictionary of jpg path in an image group
# eg. {'alley':[something.../alley/1_jpg, something.../alley/2_jpg, ...], 'horses':[something.../horses/1_jpg, something.../horses/2_jpg,...], ...}
def get_query_image_groups_path_jpg(input_path):
	image_groups = get_image_groups()
	image_group_path = []
	result_list = {}
	for group_name in image_groups:
		image_group_path.append(os.path.join(input_path, group_name))

	for i in xrange(len(image_group_path)):
		if image_group_path[i] != STUPID_DS_STORE:
			image_list = os.listdir(image_group_path[i])
			if image_list[0] == ".DS_Store":
				image_list.pop(0)
			image_list_path = []
			for image_name in image_list:
				image_list_path.append(os.path.join(image_group_path[i], image_name))
			result_list[image_groups[i]] = image_list_path

	return result_list

#print get_query_image_groups_path_jpg()
#print get_image_paths()
#output_vectors()
#print "Done!"
		