import joblib
import pandas as pd

class Node():
    def __init__(self, feature=None, left=None, right=None, gain=None, value=None):
        self.feature = feature
        self.left = left
        self.right = right
        self.gain = gain
        self.value = value
    
class DecisionTree():
    def __init__(self):
        self.root = joblib.load("root.joblib")

    def predict(self, x, node):
            if node.value is not None:
                return node.value
            if x[node.feature] == 1.0:
                return self.predict(x, node.left)  # Return the result of recursive call
            else:
                return self.predict(x, node.right)  # Return the result of recursive call
            
    def get_prediction(self, x):
        return self.predict(x, self.root)

if __name__ == "__main__":
    data = joblib.load("X_train.joblib")
    x = data.loc[0]
    decision_tree = DecisionTree()
    prediction = decision_tree.get_prediction(x)
    print("prediction:", prediction)