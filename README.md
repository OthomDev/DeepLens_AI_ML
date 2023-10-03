# DeepLens_AI_ML
"DeepLens: A Flask-RESTful API for TensorFlow Image Classification"


Introduction
Welcome to DeepLens: Your Intelligent Eye in Image Classification! 

DeepLens is a robust and user-friendly API, crafted meticulously using Flask-RESTful, that leverages the power of TensorFlow and the InceptionV3 model to classify images with precision. This API not only classifies images but also allows users to interact with a MongoDB database to manage user credentials and tokens, ensuring a secure and efficient image classification experience.

What is DeepLens?
DeepLens is an API that allows users to classify images by leveraging a pre-trained deep learning model. Users can send an image URL to the API, which then processes and classifies the image, returning a set of predictions about what the image contains. DeepLens is not just an image classifier - it's a comprehensive solution that manages user authentication, token management, and much more, ensuring that users can classify images securely and efficiently.

Features
User Registration: New users can easily register, obtaining secure credentials and tokens for using the API.

Image Classification: Users can classify images by simply sending an image URL. The API fetches, processes, and classifies the image, returning a set of predictions.

Token Management: Users consume tokens per classification and can refill them through an admin endpoint, ensuring fair usage and management of resources.

Built With
Flask-RESTful: For creating the API endpoints.

TensorFlow: For utilizing the InceptionV3 model to classify images.

MongoDB: For managing user data, credentials, and tokens.

bcrypt: For securely hashing user passwords.
