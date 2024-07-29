import os

# Gets the directory path of the current file
basedir = '/home/ubuntu/CY6740-Project'

class Config:
    SECRET_KEY = 'b\x1e\xfa\x8d\xb3\xf5\x0e\x8f\xf6\xe7\xdc\xd0\xd7\xa7\x1b\xc8\xcd\x91\x1c\x11\xbc\xf8\x9a'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'application.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
