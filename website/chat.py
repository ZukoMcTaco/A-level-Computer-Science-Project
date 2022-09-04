import random
import json
from urllib import response
import torch
from .model import NeuralNet
from .nltk_utils import bag_of_words, tokenise
#libraries imported ^

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
#will use my computer's graphics card to run the model otherwise it will use the CPU^

with open("website/intents.json", "r") as f:
    intents =json.load(f) #json file containing the responses is loaded
FILE ="website/data.pth"

data=torch.load(FILE) 

input_size=data["input_size"]
output_size=data["output_size"]
hidden_size=data["hidden_size"]
all_words=data["all_words"]
tags=data["tags"]
model_state=data["model_state"]
#required variables are taken from the data file

model = NeuralNet(input_size, hidden_size, output_size).to(device) 
#the model is created from an instance of the class NeuralNet taking in said parameters^

model.load_state_dict(model_state)
model.eval() #evaluates the model

#print("Felicia: Welcome, Master! What would you like to do today!")
gibberish_probability=0.4948996305465698 #constant value that is used to detect if a response is illogical
#intents["intents"][0]["state"] ---> gets the state



def get_response(user_input):
    "Module that gets the response of the user and returns the chatbot's response as well as the chatbot's mood"
    bot_contents=[]#local list that will contain the response and the bot mood variable
    user_input=tokenise(user_input)#user input is tokenised
    X= bag_of_words(user_input,all_words)#a bag of words is created
    X=X.reshape(1,X.shape[0])
    X = torch.from_numpy(X).to(device)
    output=model(X) #X is inputted into the model
    _, predicted = torch.max(output, dim=1)
    tag=tags[predicted.item()]
    #print(predicted.item())

    bot_status=intents["intents"][predicted.item()]["state"]
    #takes the same indexed item to make the bot status the same as the one assigned to the appropriate tag


    probability = torch.softmax(output,dim=1)
    actual_probability=probability[0][predicted.item()]
    #print(actual_probability.item())



    if actual_probability.item()==gibberish_probability:
        #if user inputs gibberish, the algorithm will return the following
        bot_contents.append("I don't quite understand master :(")
        bot_contents.append(bot_status)#bot status set
        return bot_contents
    elif actual_probability.item() >0.75:
        #if the probablity of the response is greater than 0.75 it will output the response
    
        for intent in intents["intents"]:
            if tag==intent["tag"]:
                bot_contents.append(random.choice(intent["responses"]))#appends the response of the chatbot
                bot_contents.append(bot_status)#appends the bot's status
                return bot_contents #outputs the bot's response
    else:
        bot_contents.append("I don't quite understand master :(")#appends I don't understand to bot contents list
        bot_contents.append(bot_status)#appends the bot's status
        return bot_contents#returns bot's response and bot's mood
