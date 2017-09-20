# database classes for data storage
from mongoengine import *

connect('whateva')


class Notifications(Document):
    note_from = StringField()
    note_about = StringField()
    date_added = DateTimeField()


class User(Document):
    username = StringField(unique=True, required=True)
    password = StringField(max_length=223,required=True)
    avatar = StringField()
    email = StringField(required=True)
    activation_code = StringField()
    points = IntField()
    read_notifications = ListField(ReferenceField(Notifications))


class Topics(Document):
    title = StringField()
    subtitle = StringField()
    added_by = ReferenceField(User)
    tags = ListField(StringField())
    date_added = DateTimeField()
    background_image = StringField()

class Posts(Document):
    post_by = ReferenceField(User)
    date_posted = DateTimeField()
    topic = ReferenceField(Topics)
    post_type = StringField()
    post = StringField()
    likes = ListField(ReferenceField(User))
    dislikes = ListField(ReferenceField(User))
    flags = ListField(ReferenceField(User))

    meta = {'allow_inheritance':True}

class ImagePosts(Posts):
    imagename = StringField()
    image_type = StringField()
    save_url = StringField()

class Replies(Posts):
    replies = ListField(ReferenceField(Posts))
