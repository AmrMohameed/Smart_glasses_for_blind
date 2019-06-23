# Smart glasses for blind

- ##  Project Aims

  Face recognition for “Blind People” aims to develop the best and most comfortable way for interaction between the blind people and their    surrounding environment the main core of this project is to make the blind people's life equally compared to the normal paper life.


  ![legally-blind-person-dog-clouds-1200x630](https://user-images.githubusercontent.com/37952915/59888573-9d1a4e80-93c8-11e9-8462-926b4f2a2111.jpg)


 




-  ## What's the project? and how it work?

    In our proposed system, camera network is built by placing a camera at the blind's glasses.
    The cameras provide scene around faces of people and the objects of his surrounding , then inform blind user what and who is on the front of him.
In this process, matching-based face recognition is performed to find out the faces in the dataset (CSV file).

   
     ![power supply](https://user-images.githubusercontent.com/37952915/59888392-ba9ae880-93c7-11e9-93a0-6c568809d9ce.PNG)


- ## Requirements and analysis:

  ### Software:
   #### Face recogntion step by step: 
     recognize faces with 98% accuracy which is pretty much as good as humans can do!
   this is the steps to recognize face:
   
    1. First, look at a picture and find all the faces in it

    2. Second, focus on each face and be able to understand that even if a face is turned in a weird direction or in bad lighting, it is still the same person.

    3. Third, be able to pick out unique features of the face that you can use to tell it apart from other people like how big the eyes are, how long the face is, etc.

    4. Finally, compare the unique features of that face to all the people you already know to determine the person’s name.
    

    To know more about face recogntion you may look over this researches:

  https://github.com/ageitgey/face_recognition#face-recognition

  https://medium.com/@ageitgey/machine-learning-is-fun-part-4-modern-face-recognition-with-deep-learning-c3cffc121d78

  http://www.csc.kth.se/~vahidk/papers/KazemiCVPR14.pdf

  https://gist.github.com/ageitgey/ae340db3e493530d5e1f9c15292e5c74


 -  ## Examples of input & output:
 
 
 ![Capture](https://user-images.githubusercontent.com/37952915/59889655-a1953600-93cd-11e9-9c90-1d234e644e98.PNG)
 
 
 
 
 ![Capture - Copy - Copy](https://user-images.githubusercontent.com/37952915/59890497-744a8700-93d1-11e9-9904-b7432d53e9f9.PNG)




![Capture - Copy](https://user-images.githubusercontent.com/37952915/59890596-ea4eee00-93d1-11e9-9196-d5cbed844846.PNG)




![Capture - Copy - Copy - Copy](https://user-images.githubusercontent.com/37952915/59890622-094d8000-93d2-11e9-9922-d002296eee14.PNG)


   #
   #### object detection step by step:
   
   1. Break the image into overlapping image tiles.
   2. Feed each image tile into a small neural network.
   3. Save the results from each tile into a new array.
   4. Downsampling.
   
   To know more about object detection you may look over this researches:
   
   https://medium.com/@ageitgey/machine-learning-is-fun-part-3-deep-learning-and-convolutional-neural-networks-f40359318721
   http://tflearn.org/
   https://github.com/tflearn/tflearn/tree/master/examples#tflearn-examples
   https://gist.github.com/ageitgey/a40dded08e82e59724c70da23786bbf0
   
   
   
   -  ## Examples of input & output:
   
   
   
   ![Detected-with-YOLO--Schreibtisch-mit-Objekten](https://user-images.githubusercontent.com/37952915/59918978-8571b300-9426-11e9-83aa-8786873711fe.jpg)

   
   
   
   
      
![Captureff](https://user-images.githubusercontent.com/37952915/59920536-1f3b5f00-942b-11e9-8454-02c6dbe35d02.PNG)
      
      
  
