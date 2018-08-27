from sqlalchemy import create_engine
import pandas as pd
import re

engine = create_engine('sqlite:///DB.db', echo=True)


def get_welfare_center(center):
    result = engine.execute("select * from welfare_center where location = '{}'".format(center)).fetchall()
    result_dict = {'location': result[0][0], 'lat':  result[0][1], 'long':  result[0][2], 'phone_num':  result[0][3],
                       'address':  result[0][4], 'center_url':  result[0][5], 'target':  result[0][6], 'image':  result[0][7]}

    return result_dict

def fetch_welfare_center_program():
    center = engine.execute("SELECT * FROM welfare_center")
    center_df = pd.DataFrame(center.fetchall(),
                                columns=('location', 'lat', 'long', 'phone_num', 'address', 'center_url', 'target', 'image')) #target은 이용대상.

    center_list = []
    for _,data in center_df.iterrows():
        center_list.append({'type_point': re.findall('\S+구', data.address)[0],
                                                'name': data.location,
                                                'location_latitude': data.lat,
                                                'location_longitude': data.long,
                                                'map_image_url': data.image,
                                                'rate':'' ,
                                                'name_point': data.location,
                                                'get_directions_start_address': '',
                                                'phone': data.phone_num,
                                                'url_point': data.center_url})

    programs = engine.execute("SELECT * FROM welfare_lecture")
    program_df = pd.DataFrame(programs.fetchall(),
                                columns=('lecture_Name', 'category_L', 'category_S', 'edutime_Sta', 'edutime_End', 'edu_duration', 'location', 'fee',
                                         'eduday_Sta', 'eduday_End', 'entry_Num', 'receipt_Sta', 'receipt_End', 'day', 'ref', 'content', 'url'))

    program_list = []
    for _,data2 in program_df.iterrows():
        program_list.append({'type_point': re.findall('\S+구', center_df[center_df.location==data2.location].location[0])[0],
                                                'name': data2.location,
                                                'location_latitude': data2.lat,
                                                'location_longitude': data2.long,
                                                'map_image_url': data2.image,
                                                'rate':'' ,
                                                'name_point': data2.location,
                                                'get_directions_start_address': '',
                                                'phone': program_df[program_df.location==data2.location].phone_num[0],
                                                'url_point': data2.url})

    return center_list, program_list
