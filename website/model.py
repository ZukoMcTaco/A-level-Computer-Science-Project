import torch
import torch.nn as nn

class NeuralNet(nn.Module):
    def __init__(self, input_size, hidden_size, num_classes):
        "magic method/constructor which initialises all attributes of the model"
        super(NeuralNet, self).__init__()#will run the constructor of the parent class
        self.l1 = nn.Linear(input_size, hidden_size) #initialises the 1st layer of the neural network
        self.l2 = nn.Linear(hidden_size, hidden_size)#initialises the 1st layer of the neural network
        self.l3 = nn.Linear(hidden_size, num_classes)#initialises the 1st layer of the neural network
        self.relu = nn.ReLU()#calls the activation function
    
    def forward(self, x):
        "method that will allow user to modify neural net's layers"
        output=self.l1(x)
        output= self.relu(output)
        output=self.l2(output)
        output= self.relu(output)
        output=self.l3(output)
        #has no activation and no softmax as it will already apply CrossEntropyLoss
        return output
