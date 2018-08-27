from sqlalchemy import create_engine
import pandas as pd
import re

db_engine = create_engine('sqlite:///DB.db', echo=True)
user_engine = create_engine('sqlite:///userdata.db', echo=True)

def get_welfare_center(center):
    result = db_engine.execute("select * from welfare_center where location = '{}'".format(center)).fetchall()
    result_dict = {'location': result[0][0], 'lat': result[0][1], 'long': result[0][2], 'phone_num': result[0][3],
                   'address': result[0][4], 'center_url': result[0][5], 'target': result[0][6], 'image': result[0][7]}

    review = user_engine.execute("select * from welfare_review where location = '{}'".format(center))
    review_frame = pd.DataFrame(review.fetchall(), columns=('email', 'date', 'content', 'rating', 'name','location'))
    review_info = {}
    review_list = []
    for _, data in review_frame.iterrows():
        review_list.append(
            {'email': data.email, 'date': data.date, 'content': data.content, 'rating': data.rating,
             'name': data.name})
    review_info['review'] = review_list

    review_len = len(review_frame)
    review_info['len'] = review_len

    if review_len !=0:
        review_info['mean'] = review_frame.rating.mean()

        review_info['star5'] = len(review_frame[review_frame.rating==5])/review_len
        review_info['star4'] = len(review_frame[review_frame.rating==4])/review_len
        review_info['star3'] = len(review_frame[review_frame.rating==3])/review_len
        review_info['star2'] = len(review_frame[review_frame.rating==2])/review_len
        review_info['star1'] = len(review_frame[review_frame.rating==1])/review_len

    return (result_dict, review_info)


def fetch_welfare_center_program():
    center = db_engine.execute("SELECT * FROM welfare_center")
    center_df = pd.DataFrame(center.fetchall(),
                             columns=('location', 'lat', 'long', 'phone_num', 'address', 'center_url', 'target',
                                      'image'))  # target은 이용대상.

    center_list = []
    for _, data in center_df.iterrows():
        center_list.append({'type_point': re.findall('\S+구', data.address)[0],
                            'name': data.location,
                            'location_latitude': data.lat,
                            'location_longitude': data.long,
                            'map_image_url': data.image,
                            'rate': '',
                            'name_point': data.location,
                            'get_directions_start_address': '',
                            'phone': data.phone_num,
                            'url_point': data.center_url})

    programs = db_engine.execute("SELECT * FROM welfare_lecture")
    program_df = pd.DataFrame(programs.fetchall(),
                              columns=(
                              'lecture_Name', 'category_L', 'category_S', 'edutime_Sta', 'edutime_End', 'edu_duration',
                              'location', 'fee',
                              'eduday_Sta', 'eduday_End', 'entry_Num', 'receipt_Sta', 'receipt_End', 'day', 'ref',
                              'content', 'url'))

    program_list = []
    for _, data2 in program_df.iterrows():
        program_list.append(
            {'type_point': re.findall('\S+구', center_df[center_df.location == data2.location].location[0])[0],
             'name': data2.location,
             'location_latitude': data2.lat,
             'location_longitude': data2.long,
             'map_image_url': data2.image,
             'rate': '',
             'name_point': data2.location,
             'get_directions_start_address': '',
             'phone': program_df[program_df.location == data2.location].phone_num[0],
             'url_point': data2.url})

    return center_list, program_list
