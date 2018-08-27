from sqlalchemy import create_engine

engine = create_engine('sqlite:///DB.db', echo=True)


def get_welfare_center(center):
    result = engine.execute("select * from welfare_center where location = '{}'".format(center)).fetchall()
    result_dict = {'location': result[0][0], 'lat':  result[0][1], 'long':  result[0][2], 'phone_num':  result[0][3],
                       'address':  result[0][4], 'center_url':  result[0][5], 'target':  result[0][6], 'image':  result[0][7]}

    return result_dict




#import pandas as pd
#import numpy as np
#from app import User

#me = User('admin', 'admin@example.com')
#db.session.add(me)
#db.session.commit()

