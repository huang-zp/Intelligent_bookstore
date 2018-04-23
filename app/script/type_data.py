import os
from app.models import Type
from app.engines import db

FILE_PATH = os.path.dirname(os.path.dirname(os.path.dirname(__file__))) + '/app/resources/' + 'booktype.txt'


tag_list = []
with open(FILE_PATH, 'r') as f:
    for line in f:
        tag_list.append(line.strip())

for tag in tag_list:
    type = Type()
    type.title = tag
    db.session.add(type)

db.session.commit()