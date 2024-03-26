from website import create_app
#imported the function create app 

app=create_app()

if __name__=='__main__':

    app.run(host="https://master--incredible-rugelach-e6fe4b.netlify.app",port="5000",threaded=True,debug=True)
    #runs the website
