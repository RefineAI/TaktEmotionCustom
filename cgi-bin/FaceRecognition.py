import face_recognition

picture_of_me = face_recognition.load_image_file("/home/icarus/projects/AgeGender/images/known/Bharat-Krish.jpg")
my_face_encoding = face_recognition.face_encodings(picture_of_me)[0]

# my_face_encoding now contains a universal 'encoding' of my facial features that can be compared to any other picture of a face!
print "Signature: " + str(my_face_encoding)
unknown_picture = face_recognition.load_image_file("/home/icarus/projects/AgeGender/images/unknown/IMG_3343.JPG")
unknown_face_encoding = face_recognition.face_encodings(unknown_picture)[0]
print "Unknown Image: " + str(unknown_picture)
# Now we can see the two face encodings are of the same person with `compare_faces`!

results = face_recognition.compare_faces([my_face_encoding], unknown_face_encoding)

if results[0] == True:
    print "Bharat Krish"
else:
    print "Unknown face"