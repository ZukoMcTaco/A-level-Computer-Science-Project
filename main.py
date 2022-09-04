from website import create_app
#imported the function create app 

app=create_app()

if __name__=='__main__':

    app.run(host="192.168.1.200",port="5000",threaded=True,debug=True)
    #runs the website