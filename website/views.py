from flask import Blueprint, render_template, request
from flask_login import login_required, current_user
import requests
import json
import socket
import random

views = Blueprint("views", __name__)

@views.route('/Video/<video>')
def video_page(video):
    print (video)
    # expect the mongo deployment to be in the same server for now
    ServerIP=request.host.split(':')[0]    
    url = 'http://54.86.116.7/myflix/videos?filter={"video.uuid":"'+video+'"}' #MONGO
    print(ServerIP)
    headers = {"Authorization": "Basic YWRtaW46c2VjcmV0"}
    #request
    payload = json.dumps({ })
    print (request.endpoint)
    response = requests.get(url)
    print (url)
    if response.status_code != 200:
      print("Unexpected response: {0}. Status: {1}. Message: {2}".format(response.reason, response.status, jResp['Exception']['Message']))
      return "Unexpected response: {0}. Status: {1}. Message: {2}".format(response.reason, response.status, jResp['Exception']['Message'])
    jResp = response.json()
    print (type(jResp))
    print (jResp)
    videofile, video, pic=('','','')
    for index in jResp:
        for key in index:
           if (key !="_id"):
              print (index[key])
              for key2 in index[key]:
                  print (key2,index[key][key2])
                  if (key2=="Name"):
                      video=index[key][key2]
                  if (key2=="file"):
                      videofile=index[key][key2]
                  if (key2=="pic"):
                      pic=index[key][key2]
    return render_template('video.html', name=video,file=videofile,pic=pic)


@views.route("/")
@login_required
def home():
    print("hello")
    # expect the mongo deployment to be in the same server for now
    ServerIP=request.host.split(':')[0]    
    url = "http://54.86.116.7/myflix/videos" #MONGO
    #print(os.environ['AUTH'])
    headers = {"Authorization": "Basic YWRtaW46c2VjcmV0"}
    payload = json.dumps({ })

    response = requests.get(url)
    print (response)
    # exit if status code is not ok
    print (response)
    print (response.status_code)
    if response.status_code != 200:
      print("Unexpected response: {0}. Status: {1}. Message: {2}".format(response.reason, response.status, jResp['Exception']['Message']))
      return "Unexpected response: {0}. Status: {1}. Message: {2}".format(response.reason, response.status, jResp['Exception']['Message'])
    jResp = response.json()
    print (type(jResp))
    html = '''<!DOCTYPE html>
              <html lang="en">
          
              <head>
                  <meta charset="utf-8">
                  <meta name="viewport" content="width=device-width,initial-scale=1">
                  <title>Home Page</title>
                  <link rel="stylesheet" href="/static/css/bootstrap.min.css">
                  <link rel="stylesheet" type="text/css" href="/static/css/my-login.css">
                  <meta name="viewport" content="width=device-width, initial-scale=1.0">
                  <title>Thumbnail Example</title>
                  <style>
                      img {
                          width: 200px; /* set your desired width */
                          height: 150px; /* set your desired height */
                          object-fit: cover; /* This property ensures that the image covers the entire box without distorting its aspect ratio */
                      }
                 </style>
                 
                 <title>Text Container</title>
                 <style>
                       body {
                            margin: 0;
                            padding: 0;
                            font-family: Arial, sans-serif;
                        }
                    
                        .container {
                            position: fixed;
                            top: 10px;
                            right: 10px;
                            width: 200px; /* Adjust the width as needed */
                            height: 100px; /* Adjust the height as needed */
                            padding: 10px;
                            background-color: #f0f0f0;
                            border: 1px solid #ccc;
                            border-radius: 5px;
                            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
                            font-size: 13px;
                        }
                  </style>
              </head>'''
    html+= '''<nav class="navbar navbar-expand-lg navbar-dark bg-dark">
                 <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbar">
                     <span class="navbar-toggler-icon"></span>
                 </button>
                 <div class="collapse navbar-collapse" id="navbar">
                     <div class="navbar-nav">
                         <a class="nav-item nav-link" id="home" href="/">Home</a>
                         <a class="nav-item nav-link" id="logout" href="/logout">Logout</a>
                     </div>
                 </div>
             </nav>'''
    
    html += "<h2> "+ current_user.name +"'s Videos</h2>"
    for index in jResp:
       print (json.dumps(index))
       print ("----------------")
       for key in index:

           if (key !="_id" and key != "_etag"):
              print (index[key])
              for key2 in index[key]:
                  print (key2,index[key][key2])
                  if (key2=="Name"):
                      name=index[key][key2]
                  if (key2=="thumb"):
                      thumb=index[key][key2]
                  if (key2=="uuid"):
                      uuid=index[key][key2]
              html=html+'<h3>'+name+'</h3>'

              # ServerIP=request.host.split(':')[0]
              html=html+'<a href="http://'+ServerIP+':5000'+'/Video/'+uuid+'">' #back to flask
              html=html+'<img src="http://34.197.43.106/pics/'+thumb+'">' #nginx
              html=html+"</a>"
              print("=======================")
              
    # expect the tfrecomm deployment to be in the same server for now
    HOST = "34.233.156.40"
    PORT = 81  # The port used by the server
    received_data = ""
    for i in range(5):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((HOST, PORT))
                s.sendall(str(random.randint(1,6000)).encode())
                received_data = s.recv(1024).decode()
        except Exception as e:
            print(f"Attempt {i+1} failed: {str(e)}")
        else:
            break
            
    
    html += ''' 
    <body>

    <div class="container">
    <h5>Recommendations</h5>
    '''
    #    <p>This is the text inside the container. You can put any text or content here.</p>
    #    <p>Feel free to modify this code to suit your needs.</p>
    for line in received_data.split('\n'):
        html+= '<p>'+line+'</p>'
    # html += received_data
    
    html+= '''
    </div>

    </body>
    </html>
    '''
    

    return html

#    return render_template("home.html", user=current_user)
