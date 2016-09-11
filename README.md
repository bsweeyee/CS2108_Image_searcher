# CS2108_Image_searcher
Code and stuff for CS2108!

A brief outline of what is to be done:

 1. For each feature (i.e color histogram, deep learning (Visual Concept), SIFT extractor (Visual Keywords), text (image tags)),
    extract a csv file. 
    
    CSV file:
    
    row: image name
    
    column: vector extracted from feature extractor programme
   
    Save the csv file and name it according to its respective feature
    
 2. When a user selects an image to be searched:

      a. take query image and run it with a feature extractor software
      
      b. for each database image, take query image result and compute the similarity index (use euclidian distance, remember to normalize!) using the associated database feature csv computed in part 1
      
      c. repeat a-b for each different feature extractor
      
      d. with the similarity index of every image from each feature vector, find a final similarity index array by summing up
         for every image, their similarity index with the respective hyper parameter
         
      e. get the top 16 images, and show to user

 3. Allow user to select which features to use during image search

 4. UI improvements
 
 5. Do analysis by computing F1 score = 2 * (precision * recall) / (precision + recall) 
  
  <b>An example:</b>
  
  I have 4 feature extractor: Visual keyword, Visual Concept, Text, Color histogram
  
  I have a database of 1000 images: image_one.jpg, image_two.jpg, ... image_one_thousand.jpg
  
  1. for each feature, i run it through all the images in the database to get a csv file
     
     what should be inside a csv file:
     
     image_one.jpg:    value 1, value 2, value 3 ...
     
     image_two.jpg:    value 1, value 2, value 3 ...
     
     ...              ...
     
     image_one_thousand.jpg:   value 1, value 2, value 3 ...
  
  2. User selects an image he wants to search
  
     Take query and run it through the 4 feature extractor to get 4 different feature vectors
     
     what should be returned after running feature extractor:
     
     query.jpg:    value 1, value 2, ...
     
     Take the results, do a similarity computation with every image in the associated feature
     
     Similarity results for a single feature:
     
     image_one and query:    similarity_value_1
     
     image_two and query:    similarity_value_2

     ...

     image_one_thousand and query:    similarity_value_1000
  
  3. for every image:
  
     final_result = a * visual_keyword[i] + b * visual_concept[i] + c * text[i] + d * color_histogram[i]
     where a+b+c+d = 1
     
  4. Top 16 results will be shown to user using this final_result value
