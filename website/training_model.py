import json
from random import shuffle # imports the json library
from nltk_utils import tokenise, stem, bag_of_words,np 


import torch 
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader
from model import NeuralNet





with open("intents.json","r") as f: #will open the intents file in read mode 
    intents = json.load(f)

all_words = [] #list that will contain all the words
tags = [] # list which contains the tags
xy = [] #list that will contain the patterns and tags 

for intent in intents["intents"]: # will iterate through the intents 
    tag = intent['tag'] 
    tags.append(tag)# will append the tags into the tags list
    for pattern in intent['patterns']:
        w=tokenise(pattern) # tokenise module applied to the pattern
        all_words.extend(w) #extends the word into the all words list
        xy.append((w, tag)) #appends the tokenised patttern and tag

ignore_words = ['?',"!",".",","] #list contains all the characters that the algorithm will ignore.
all_words = [stem(w) for w in all_words if w not in ignore_words] # stems each word in the list and ignores punctuation 
all_words = set(all_words)#sorts and sets the elements in all_words
tags = sorted(set(tags))#sorts and sets the elements in tags


X_train= [] #training data containing the bag of words
y_train = [] #training data containing the associated number for each tag

for (pattern_sentence, tag) in xy: #goes through the tags and patterns in the list
    bag=bag_of_words(pattern_sentence, all_words) #applies the bag of words function
    X_train.append(bag)
    label = tags.index(tag)
    y_train.append(label) # labels added into the y_train list
X_train = np.array(X_train)
y_train = np.array(y_train)

class ChatDataset(Dataset):
    "Class for the chatbot's training dataset"
    def __init__(self):
        "method that will initialise all the variables in each instance of the class"
        self.n_samples = len(X_train) #initialises n_samples attribute
        self.x_data = X_train#initialises x_data attribute
        self.y_data = y_train#initialises y_data attribute
    
    def __getitem__(self, index):
        "Method that will return the index of the x and y data"
        return self.x_data[index], self.y_data[index]
    
    def __len__(self):
        "Method that will return the no. of samples"
        return  self.n_samples


#hyper parameters to be used to make the model
batch_size=8 
hidden_size=8
output_size=len(tags)
input_size = len(X_train[0])
learning_rate=0.001
num_of_epochs = 1000 

dataset=ChatDataset()
train_loader = DataLoader(dataset=dataset, batch_size=batch_size, shuffle=True, num_workers=0)

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
#will use my computer's graphics card to run the model otherwise it will use the CPU^
model = NeuralNet(input_size, hidden_size, output_size).to(device) 
#the model is created from an instance of the class NeuralNet taking in said parameters^

#loss and optimiser
criterion = nn.CrossEntropyLoss()
optimiser = torch.optim.Adam(model.parameters(), lr=learning_rate)
 
for epoch in range(num_of_epochs):# training loop
    for (words, labels) in train_loader:
        words=words.to(device)
        labels = labels.to(dtype=torch.long).to(device)

        #forward
        predicted_outputs = model(words)
        loss=criterion(predicted_outputs,labels)

        #backward and optimiser step
        optimiser.zero_grad()
        loss.backward() # calculates the backwards propagation
        optimiser.step()
    if (epoch+1) %100 ==0: 
        #will output the loss every 100 epochs/cycles
        print(f'epoch {epoch+1}/{num_of_epochs}, loss={loss.item():.4f}')
print(f'final loss {epoch+1}/{num_of_epochs}, loss={loss.item():.4f}') #outputs the final loss

data = {
    "model_state": model.state_dict(),
    "input_size": input_size,
    "output_size": output_size,
    "hidden_size": hidden_size,
    "all_words": all_words,
    "tags": tags
} #dictionary which contains all the data that will be saved into a pickle file

FILE= "data.pth"
torch.save(data,FILE)#saves the data
print(f' training complete! model is saved to{FILE}')# outputs message to display save successful

