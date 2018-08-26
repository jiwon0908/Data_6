#import pandas as pd
#import numpy as np
#from app import User

#me = User('admin', 'admin@example.com')
#db.session.add(me)
#db.session.commit()
from sqlalchemy import create_engine
import pandas as pd

engine = create_engine('sqlite:///DB.db', echo=True)

def fetch_db():
    result = engine.execute("SELECT * FROM welfare_center")
    result_frame = pd.DataFrame(result.fetchall(),
                                columns=('location', 'lat', 'long', 'phone_num', 'address', 'center_url', 'target'))

    result_list = []
    for _,data in result_frame.iterrows():
        result_list.append({'location': data.location, 'lat': data.lat, 'long': data.long, 'phone_num': data.phone_num,
                       'address': data.address, 'center_url': data.center_url, 'target': data.target})
    return result_list