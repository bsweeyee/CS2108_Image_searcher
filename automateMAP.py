import os, sys
import utility.util as util
from Tkinter import *
from UI_search import UI_class

all_database_category_paths = util.get_image_groups_path_jpg(util.database_path)
all_query_category_paths = util.get_image_groups_path_jpg(util.query_path)

def search_and_write_all_categories(window):

	with open("MAP_results.txt", 'w') as output:
		for (category, path) in all_query_category_paths.iteritems():
			MAP_value = search_from_one_category(category, path, window)
			out_string = str(category) + " : " + str(MAP_value) + "\n"
			output.write(out_string)
			print "one category done"

# function_1:
# take in all images from category -> go through search -> return MAP value -> store into file
def search_from_one_category(query_category_name, query_category_paths, window):
	result_list = {}
	query_category_base = []

	# pass the paths for the currently searched category path in the database
	database_category_paths = all_database_category_paths[query_category_name]

	for path in query_category_paths:
		#input into search
		print "searching..."
		# modify here to check which feature to search in
		results_tuple = window.get_image_search_results(path, 0, 1)
		result_list[os.path.basename(path)] = results_tuple

	return calculate_MAP(result_list, database_category_paths)

# function_2:
# calculate p
# 1. take all returned images and check with category images
# 2. if same, correct += 1
# 3. calcuate and return p
def calculate_p(query_category, query_results, database_category_paths):
	correct_result = 0.0
	AveP = 0.0
	print "calculating Ave(p)..."

	for i in xrange(len(query_results)):
		for j in xrange(len(database_category_paths)) :
			if query_results[i][1] == os.path.basename(database_category_paths[j]):
				correct_result += 1.0
				AveP += (correct_result / (j+1))

	if (correct_result > 0):
		AveP /= correct_result
	
	print "Ave(p) done!"

	return AveP

# function_3:
# calculate MAP
# 1. for all input images in same category, find p
# 2. add all the p and divide by number of queries made
def calculate_MAP(result_list, database_category_paths):
	total_p = 0.0
	for (key, value) in result_list.iteritems():
		total_p += calculate_p(key, value, database_category_paths)

	print "MAP print done!"
	print total_p / len(result_list)
	return total_p / len(result_list)


root = Tk()
window = UI_class(root)
search_and_write_all_categories(window)
