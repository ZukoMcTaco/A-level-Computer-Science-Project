class Chatbox{
    //This is the class contains all the methods and variables which are used to update the chatbot website.
    constructor(){
        this.args ={
            openButton: document.querySelector(".chatbox__button"),
            chatBox: document.querySelector(".convo_box"),
            sendButton: document.querySelector(".send_button")
        }
        this.state =false;
        this.messages=[];

    }
    display(){
        /*method that will listen for the enter key and send button and will send the inputs back to the chatbot algorithm using
        the onsendbutton method*/
        const{chatBox, sendButton}=this.args;
        sendButton.addEventListener('click', ()=> this.onSendButton(chatBox))
        const node = document.querySelector('.input');
        node.addEventListener("keyup",({key}) =>{
            if (key=="Enter") {
                this.onSendButton(chatBox)
            }
        })  
    }
    onSendButton(chatBox){
        /*Method that uses the fetch promise api to do a post request onto the api endpoint of /predict
        then once the promise is resolved the response of the request is converted into a javascript object
        which displays the message onto the screen and will display the corresponding image and colour.
        If there's an error, it will display: "Error"
        */
        var textField = document.querySelector(".input");
        let text1 = textField.value
        if (text1 ===""){
            return;
        }
        let msg1 = { name: "You: " ,message: text1}
        this.messages.push(msg1);
        fetch('http://192.168.1.200:5000/predict',{
            method: 'POST',
            body: JSON.stringify({message: text1}),
            mode: 'cors', //cross origin resource sharing
            headers: {
                'Counter-Type': 'application/json'
            },
        })
        .then( r=> r.json())
        .then(r =>{
            let image= document.getElementById("image")
            let msg2 ={name:"Felicia", message: r.answer};
            let image_box=document.getElementById("image_box");
            this.messages.push(msg2);
            this.updateChatText(chatbox)
            textField.value=''
            if (r.bot_mood==="sad"){
                image.src="/static/felicia_sad.png"
                image_box.style.backgroundColor="lightblue"
            }
            else if(r.bot_mood==="angry"){
                image.src="/static/felicia_angry.png"
                image_box.style.backgroundColor="red"
            }
            else if(r.bot_mood==="happy"){
                image.src="/static/felicia_happy.png"
                image_box.style.backgroundColor="green"
            }
        }).catch((error) =>{
            console.error('Error',error);
            this.updateChatText(chatbox)
            textField.value=''
        }
        )
    }
    updateChatText(chatbox){
        /*This Method will go through each message that is sent that is stored in the message array
        and if its name is "Felicia" then it will add html to the variable "html" 
        with her name as well as the bot's response to the user
        otherwise if it isn't then it will store "You: " with the user's input in the html variable.
        The html variable is injected into the contents of the div with an id of "convo_box"
        */
        var html='';
        this.messages.slice().reverse().forEach(function(item,){
            if (item.name ==="Felicia")
            {
                html += "<div class='messages__item messages__item-visitor'> Felicia: " + item.message + "</div>"
            }
            else
            {
                html +='<div class="messages__item messages__item--operator"> You: ' + item.message + "</div>"
            }
        });
        const chatmessage = document.querySelector("#convo_box");
        chatmessage.innerHTML =html;
    }
}
const chatbox = new Chatbox();/* new instance of Chatbox created */
chatbox.display();/* method display run*/