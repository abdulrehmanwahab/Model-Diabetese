from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC


#Split the data into training and test
from sklearn.model_selection import train_test_split
from sklearn.model_selection import KFold
from sklearn.model_selection import cross_val_score

#Check accuracy of training data vs test data
from sklearn.metrics import accuracy_score
from sklearn.metrics import classification_report

import joblib
import os
import pathlib



FileName = 'diabetesMD.joblib'  # Name of the file to load



current_dir = pathlib.Path().resolve()
file_path = current_dir.joinpath(FileName)


# Load the model
loadedFile = joblib.load(file_path)  # Load the model using the constructed path

loaded_model = loadedFile['model']
loaded_description = loadedFile['description']

# userValuetoCheck1 = [6,148,72,35,0,33.6,0.627,50]
# userValuetoCheck2 = [6,148,72,35,0,33.6,0.627,50],[10,101,76,48,180,32.9,0.171,63]

def predict_values(values):
    print(f"Received value: {values}")
    
    y_prediction_user1 = loaded_model.predict([values]) #For single value [] is needed
    # # y_prediction_user2 = loaded_model.predict(userValuetoCheck2) #For more than one value [] is not needed
   
    # print("\n Predicted Output: ",y_prediction_user1)
    # print("\nNote:\n",loaded_description)
    return {
        "prediction": y_prediction_user1.tolist(),  # Convert to list if needed
        "description": loaded_description
     }