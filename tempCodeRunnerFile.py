import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, label_binarize
from sklearn.decomposition import PCA
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.metrics import (
    accuracy_score, classification_report, confusion_matrix, 
    roc_curve, auc
)
from sklearn.neural_network import MLPClassifier
from sklearn.multiclass import OneVsRestClassifier
import seaborn as sns

df = pd.read_csv("C:\Users\Shivam\OneDrive\Desktop\COLLEGE\SEM7\ML\New_folder\dataset\mnist.csv")  
y = df.iloc[:, 0].values
X = df.iloc[:, 1:].values
