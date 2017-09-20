from datetime import  *
import uuid
from flask import Flask, jsonify,request,abort
from db import *


app = Flask(__name__)

'''
    Wh@tAPI version 0.1
    So far what it does:
    1. manage users
    2. create posts and topics
    3. manage notifications
    

'''

'''
    This method is the landing. Shows the api version, title, etc. Not necessary
    but I just thought I should put it instead of a blank page
'''
@app.route('/', methods=['GET'])
def hello_world():
    details = [{'title':'Wh@teva API'},{'version':'0.1'},{'credits':'x3l0r'}]
    return jsonify({'API details':details}), 200


'''
    Getting all the users from the database. Access method is GET.
    No filtering or ordering etc, I think I should implement those later
'''
@app.route('/users', methods=['GET'])
def getUsers():
    users = []
    user_count = User.objects.count()
    if user_count == 0:
        return jsonify({'Users':'No Users yet'}), 200   # I'm not sure why Im using response codes right now so try not to ask me
    else:
        for user in User.objects:
            users.append({'username':user.username,'email':user.email, 'avatar':user.avatar,'activationCode':user.activation_code})
        return jsonify({'users': users}), 200

'''
    Just getting a specific user
    example : http://whateva.co.zw/api/users/zeref
    should return :{
        'user':{
            'username':'zeref',
            'email':'z@z.com',
            'password':'SOMEENCRYPTEDPASSWORD',
            'avatar':'awesomeness.jpg',
            'activationCode':'SOMEACTIVATIONCODE'
        }
    }
'''
@app.route('/users/<username>', methods=['GET'])
def getUser(username):
    user = User.objects(username=username).first()
    if user is not None:
        full_user = {'username':user.username, 'email':user.email,'avatar':user.avatar,'activationCode':user.activation_code,'password':user.password}
        return jsonify({'user':full_user})
    else:
        return jsonify({'user':'No user found'})

'''
    Creating the users using a POST method
    the format for the json object should be like this:
    {
         'email':'z@z.com',
         'username':'Zeref07',
         'password':'SUPERSECRETENCRYPTEDPASSWORD',
         'avatar':'somefile.jpg',
         'activationCode':'SOMEACTIVATIONCODE'
    }
'''
@app.route('/users', methods=['POST'])
def postUser():

    user_avatar = ''
    if 'email' not in request.json:
        abort(400)

    if 'username' not in request.json:
        abort(400)

    if 'password' not in request.json:
        abort(400)


    if 'avatar'  in request.json:
        user_avatar = request.json['avatar']

    user_email = request.json['email']
    user_name = request.json['username']
    user_password = request.json['password']
    user_activationCode = uuid.uuid4().hex

    user = User(email=user_email, username=user_name, password=user_password, avatar=user_avatar,
                activation_code=user_activationCode).save()

    return jsonify({'message': 'Success!!'})

'''
    Updating the users document via API json post<or something>
    json object should  just be the same as well:
    eg. http://whateva.co.zw/api/users/zeref   --put {'username':'zeref01','email':'zd@z.com', 'avatar':'anotherpic.png'}
    {
        'user':{
            'username':'zeref01',
            'email':'zd@z.com',
            'avatar':'anotherpic.png'
        }
    }
'''
@app.route('/users/<username>', methods=['PUT'])
def updateUser(username):
    user = User.objects(username=username).first()
    user_name = user.username
    user_password = user.password
    user_email = user.email
    user_avatar = user.avatar


    if 'username' in request.json:
        user_name = request.json['username']

    if 'password' in request.json:
        user_password = request.json['password']

    if 'email' in request.json:
        user_email = request.json['email']

    if 'avatar' in request.json:
        user_avatar = request.json['avatar']

    user.username = user_name
    user.password = user_password
    user.email = user_email
    user.avatar = user_avatar

    user.save()



    user.save()
    return '', 200


'''
    Deleting users: At the moment I do not think it is necessary, so Im putting it on hold.....
    :D
'''
@app.route('/users/<username>', methods=['DELETE'])
def removeUser(username):
    #user = User.objects(username=username).first()
    #del_user = user.drop_collection()
    abort(403)


"""
    POSTS Magic happens here <creation of topics, posts and comments>
    CRUD on topics, posts and comments along with user notifications and stuff??
"""
'''
    Get All topics saved in the db so far
'''
@app.route('/topics', methods=['GET'])
def getTopics():
    topics = []
    count = Topics.objects.count()
    if count == 0:
       abort(404)
    else:
        for topic in Topics.objects:
            topics.append({'title':topic.title,'subtitle':topic.subtitle,'dateAdded':topic.date_added,'background_image':topic.background_image,'tags':topic.tags})

        return jsonify({'topics':topics})


'''
    Get a single topic from the db
    eg whateva.co.zw/api/topics/soccer should return a json object 
    like 
    {
        {
            'title':'soccer',
            'subtitle':'soccer is awesome??',
            'dateAdded':'12-03-2009',
            'background_image':'bg.png',
            'tags':[
                'soccer','arsenal','man u'
            ]
            
        }
    
    
    }
'''
@app.route('/topics/<title>', methods=['GET'])
def getTopicByTitle(title):
    topic = Topics.objects(title=title).first()
    if topic is not None:
        json_topic = {'title':topic.title,'subtitle':topic.subtitle,'dateAdded':topic.date_added,'background_image':topic.background_image,'tags':topic.tags}
        return jsonify({'topic':json_topic})
    else:
       abort(404)


'''
    Posting/creating a topic
    topic  object structure should be as follows
    {
         {
            'title':'soccer',
            'subtitle':'soccer is awesome??',
            'dateAdded':'12-03-2009',
            'background_image':'bg.png',
            'tags':[
                'soccer','arsenal','man u'
            ]
            
        }
    
    }
'''
@app.route('/topics',methods=['POST'])
def createTopic():
    if 'title' in request.json:
        title = request.json['title']
    else:
        abort(400)

    if 'subtitle' in request.json:
        subtitle = request.json['subtitle']
    else:
        abort(400)


    date_added = datetime.now().date()
    if 'background_image' in request.json:
        background_image = request.json['background_image']
    else:
        abort(400)

    try:
        tags = request.json['tags']
    except KeyError:
        tags = []

    topic = Topics(title=title,subtitle=subtitle,date_added=date_added,background_image=background_image, tags=tags).save()

    return jsonify({'message':'Success'})


'''
  I dont think updating a topic is necessary unless someone is changing the background image or something,or updating tags?
    But I still dont think its necessary, so Im putting it on hold for now
'''
@app.route('/topics/<title>', methods=['PUT'])
def updateTopic(title):
    return jsonify({'error':'Action not allowed'})

'''
    Now we move on to posts and replies (the screwing magic -_-)
    Get all posts regardless of topic </>

'''
@app.route('/posts', methods=['GET'])
def getAllPosts():
    posts = []
    if Posts.objects.count() == 0:
        return jsonify({'posts':'None yet'})
    else:
        for post in Posts.objects:
            posts.append({'post':post.post,'post_by':post.post_by.username,'date_posted':post.date_posted,'topic':post.topic.title,'post_type':post.post_type,'likes':post.likes,'dislikes':post.dislikes, 'flags':post.flags})

        '''
         this endpoint will return an object which has the following structure
         {
            'posts':{
                'post_by':'zeref07',
                'date_posted':'23-12-1903',
                'topic':'soccer',
                'post_type':'string',
                'likes':[{
                    'username':'zeref07',
                    'email':'z@z.com',
                    'password':'SOMEENCRYPTEDSECRETPASSWORD',
                    'avatar':'',
                    'activation_code':''
                },{ 
                    'username':'madara92',
                    'email':'m@m.com',
                    'password':'SOMEENCRYPTEDSECRETPASSWORD',
                    'avatar':'',
                    'activation_code':''
                },{
                    'username':'aizen25',
                    'email':'aizen@gmail.com',
                    'password':'SOMEENCRYPTEDSECRETPASSWORD',
                    'avatar':'',
                    'activation_code':''
                }],
                'dislikes':[],
                'flags':[]
            
            }
            
         }
        '''
        return jsonify({'posts':posts})

'''
    get specific posts mainly by topic(actually by topic ^_^)
'''
@app.route('/posts/<topic_title>/<int:num_results>', methods=['GET'])
def getPostsByTitle(topic_title, num_results):
    topic = Topics.objects(title=topic_title).first()
    posts = []
    if topic is not None:
        for post in Posts.objects(topic=topic)[:num_results]:
            posts.append({'post':post.post,'post_by':post.post_by.username,'date_posted':post.date_posted,'topic':post.topic.title,'post_type':post.post_type,'likes':post.likes,'dislikes':post.dislikes, 'flags':post.flags})
            """
                return same M.O. --no changes here, the object is the same as the /posts endpoint
            """
        return jsonify({'posts':posts})
    else:
        abort(404)

'''
    Posting Images

@app.route('/posts/<topic_title>/images', methods=['POST'])
def postImageField(topic_title):
    topic = Topics.objects(title=topic_title).first()
    post = []
    if topic is not None:
        #do something here
        
        return jsonify({'message':'success'})

    else:
        return jsonify({'message':'no such topic'})
        
'''

'''
    create a post from the title topic
    SO we first obtain the title of the topic then use it to create a post. That way a post is linked to a specific topic
'''
@app.route('/posts', methods=['POST'])
def createPost():
    topic = None
    if 'topic' in request.json:
        topic = Topics.objects(title=request.json['topic']).first()

    user = None
    if 'username' in request.json:
        user = User.objects(username=request.json['username']).first()


    message = ''
    if topic is not None and user is not None:
       today = datetime.now().date()
       post = Posts(date_posted=today,post=request.json['post'])
       post.post_by = user  #User(username=user.username, email=user.email,password=user.password)
       post.topic = topic          #Topics(title=topic.title, subtitle=topic.subtitle)
       post.save()

       '''
        Basically what we really need to create a post is the post, username and topic, so you should create a json object with 
        those parameters eg:
        {
            'topic':'soccer',
            'username':'zeref07',
            'post':'Yippee, Liverpool got thrashed again yesterday'
        
        }
       '''
       message = 'Success'
    else:
       message = 'No such topic or user'

       '''
        Not returning a json object since its useless to return a json object everytime someone posts something
        So I'll just return a message that says either success or fail
       '''
    return jsonify({'post':message})

'''
    Notifications magic goes here
    First we'll start with unread notifications
'''
@app.route('/notifications/<username>', methods=['GET'])
def getNotificationsUnread(username):
    user = User.objects(username=username).first()
    read_list = user.read_notifications
    all_notes = Notifications.objects()
    unread_notes = []
    for note in all_notes:
        if note in read_list:
            pass
        else:
            unread_notes.append({'from':note.note_from, 'about':note.note_about,'date':note.date_added})
    return jsonify({'notifications':unread_notes})






'''
     What else is left???
     1. posting replies
     2. saving image posts
     3. updating topic tags
     
     What I don't think is required or necessary
     1. updating and deleting posts and topics
     2. deleting users
'''


'''
    Error handling methods down here
'''
'''Start with an error 500 because its the one I've been getting like a lot ^_^ '''
@app.errorhandler(500)
def error_occured(e):
    return jsonify({'error':str(e)})

@app.errorhandler(404)
def notFound(e):
    return jsonify({'error':str(e)})

@app.errorhandler(403)
def noAllowed(e):
    return jsonify({'error':'Action not allowed =>' +str(e)})

@app.errorhandler(400)
def badRequest(e):
    return jsonify({'error':'Bad Request -- '+str(e)})


if __name__ == '__main__':
    app.run()
