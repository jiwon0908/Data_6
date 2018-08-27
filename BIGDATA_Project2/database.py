from sqlalchemy import create_engine
import pandas as pd
import random
import re
import datetime
from concurrent import futures


db_engine = create_engine('sqlite:///DB.db', echo=True)
user_engine = create_engine('sqlite:///userdata.db', echo=True)


def insert_welfare_review(email, content, rating, name, location):
    date = datetime.datetime.now().date()
    sql = "insert into welfare_review values('{}','{}','{}',{},'{}','{}')".format(email, date, content, rating, name,
                                                                                  location)

    user_engine.execute(sql)



def get_welfare_center(center):
    result = db_engine.execute("select * from welfare_center where location = '{}'".format(center)).fetchall()
    result_dict = {'location': result[0][0], 'lat': result[0][1], 'long': result[0][2], 'phone_num': result[0][3],
                   'address': result[0][4], 'center_url': result[0][5], 'target': result[0][6], 'image': result[0][7]}

    review = user_engine.execute("select * from welfare_review where location = '{}'".format(center))
    review_frame = pd.DataFrame(review.fetchall(), columns=('email', 'date', 'content', 'rating', 'name', 'location'))
    review_info = {}
    review_list = []
    for _, data in review_frame.iterrows():
        review_list.append(
            {'email': data.email, 'date': data.date, 'content': data.content, 'rating': data.rating,
             'name': data.name})
    review_info['review'] = review_list

    review_len = len(review_frame)
    review_info['len'] = review_len

    if review_len != 0:
        review_info['mean'] = round(review_frame.rating.mean(),1)
        review_info['star5'] = len(review_frame[review_frame.rating == 5]) / review_len * 100
        review_info['star4'] = len(review_frame[review_frame.rating == 4]) / review_len * 100
        review_info['star3'] = len(review_frame[review_frame.rating == 3]) / review_len * 100
        review_info['star2'] = len(review_frame[review_frame.rating == 2]) / review_len * 100
        review_info['star1'] = len(review_frame[review_frame.rating == 1]) / review_len * 100

    return (result_dict, review_info)


def get_review(email, order):
    review = user_engine.execute("select date, content, rating, name, location from welfare_review where email='{}' order by date {}".format(email, "desc" if order else ""))
    review_frame = pd.DataFrame(review.fetchall(), columns=('date', 'content', 'rating', 'name', 'location'))

    name = user_engine.execute("select username from user where email='{}'".format(email)).fetchall()[0][0]

    review_info = {}
    review_info['email'] = email
    review_info['name'] = name

    def get_location_img(location):
        img_url = db_engine.execute("select image from welfare_center where location='{}'".format(location)).fetchall()[0]
        return pd.DataFrame({'location':location, 'image':img_url})

    executor = futures.ThreadPoolExecutor(max_workers=5)
    return_list = [executor.submit(get_location_img, location) for location in review_frame.location.unique()]
    futures.wait(return_list)

    img_df = pd.DataFrame()
    for result in return_list:
        img_df = img_df.append(result.result(), ignore_index=True)
    review_frame = review_frame.merge(img_df, how='left', on='location')

    review_list = []
    for _, data in review_frame.iterrows():
        review_list.append(
            {'date': data.date, 'content': data.content, 'rating': data.rating,'location': data.location, 'image':data.image})
    review_info['review'] = review_list


    return review_info


def get_my_page(email):
    review_len = user_engine.execute("select count(*) from welfare_review where email='{}'".format(email)).fetchall()[0][0]
    print(review_len)

    data = {}
    data['email'] = email
    data['review_len'] = review_len

    return data


def register_wish(email, center, lecture, category, flag):
    if flag == True:
        sql = "insert into lecture_wish values('{}','{}','{}','{}')".format(email, lecture, center, category)
        db_engine.execute(sql)
    else:
        sql = "delete from lecture_wish where email='{}' and center='{}' and lecture='{}'".format(email,center,lecture)
        db_engine.execute(sql)


def remove_wish(email, lecture, center):
    sql = "delete from lecture_wish where email='{}' and lecture='{}' and center = '{}'".format(email, lecture, center)
    db_engine.execute(sql)


def get_wish(email):
    wish_datas = db_engine.execute("select a.category_L, a.url, b.lecture, b.center, b.category from (select * from welfare_lecture) "
                                  "as a inner join (select * from lecture_wish where email='{}') as b "
                                  "on a.lecture_Name = b.lecture and a.location=b.center".format(email))
    wish_datas = pd.DataFrame(wish_datas.fetchall(), columns=('category_L','url', 'lecture', 'center', 'category'))

    result_dict = {}
    result_dict['email'] = email
    result_list = []
    program_photo_num = {'A': 1, 'B': 5, 'C': 1, 'D': 5, 'E': 1, 'F': 5, 'G': 1, 'H': 1}
    for _, wish_data in wish_datas.iterrows():
        data = {}
        if wish_data.category == "indoor":
            data['category'] = "실내프로그램"
        elif wish_data.category == "activity":
            data['category'] = "야외프로그램"
        data['lecture'] = wish_data.lecture
        data['center'] = wish_data.center
        data['url'] = wish_data.url
        data['image'] = 'static/img/program/'+str(wish_data.category_L)+str(random.randrange(0,program_photo_num[wish_data.category_L]))+'.jpg'
        result_list.append(data)
    result_dict['wish'] = result_list
    result_dict['len'] = len(result_list)

    return result_dict


def get_wishlist(email):
    sql = "select c.location, c.lat, c.long, c.phone_num, c.address, c.center_url, c.target, c.image " \
          "from (select * from welfare_center) " \
          "as c inner join " \
          "(select b.lecture, b.center from (select * from welfare_lecture) " \
          "as a inner join " \
          "(select * from lecture_wish where email='{}') as b " \
          "on a.lecture_Name = b.lecture and a.location=b.center) as d " \
          "on c.location = d.center".format(email)
    center_df = pd.DataFrame(db_engine.execute(sql).fetchall(),
                             columns=('location', 'lat', 'long', 'phone_num', 'address', 'center_url', 'target',
                                      'image'))


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

    sql = "select a.lecture_Name, a.category_L, a.category_S, a.edutime_Sta, a.edutime_End, " \
          "a.edu_duration, a.location, a.fee, a.eduday_Sta, a.eduday_End, a.entry_Num," \
          " 'a.receipt_Sta', 'a.receipt_End', a.day, a.ref,a.content, a.url " \
          "from (select * from welfare_lecture) " \
          "as a inner join " \
          "(select * from lecture_wish where email='{}') as b " \
          "on a.lecture_Name = b.lecture and a.location=b.center".format(email)

    programs = db_engine.execute(sql)
    program_df = pd.DataFrame(programs.fetchall(),
                              columns=(
                                  'lecture_Name', 'category_L', 'category_S', 'edutime_Sta', 'edutime_End',
                                  'edu_duration',
                                  'location', 'fee',
                                  'eduday_Sta', 'eduday_End', 'entry_Num', 'receipt_Sta', 'receipt_End', 'day', 'ref',
                                  'content', 'url'))

    result_dict = {}
    result_dict['len'] = len(program_df)
    program_list = []
    program_photo_num = {'A':1, 'B':5, 'C':1, 'D':5, 'E':1, 'F':5, 'G':1, 'H':1} # static/img/program에 들어있는 각 대분류별 사진 개수
    for _,data2 in program_df.iterrows():
        row_index = center_df[center_df.location==data2.location].index[0]
        program_list.append({'type_point': re.findall('\S+구', center_df.loc[row_index, 'address'])[0],
                                                'name': data2.location,
                                                'location_latitude': center_df.loc[row_index, 'lat'],
                                                'location_longitude': center_df.loc[row_index, 'long'],
                                                'map_image_url': 'static/img/program/'+str(data2.category_L)+str(random.randrange(0,program_photo_num[data2.category_L]))+'.jpg',
                                                'rate':'' ,
                                                'name_point': data2.location,
                                                'get_directions_start_address': '',
                                                'phone': center_df.loc[row_index, 'phone_num'],
                                                'url_point': data2.url,
                                                'center_url': 'center-detail?welfare='+data2.location,
                                                 'edu_name': data2.lecture_Name,
                                                 'edu_start': str(data2.edutime_Sta)[:5],
                                                 'edu_end': str(data2.edutime_End)[:5],
                                                 'edu_duration': int(data2.edu_duration),
                                                 'edu_fee': data2.fee,
                                                 'edu_day': data2.day,
                                                 'edu_ref': data2.ref,
                                                 'edu_content': data2.content,
                                                 'edu_category': [data2.category_L, data2.category_S],
                                                 'edu_entrynum': data2.entry_Num,
                             })

        result_dict['program_list'] = program_list

    return center_list, result_dict


def fetch_welfare_center_program(email):
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
                                  'lecture_Name', 'category_L', 'category_S', 'edutime_Sta', 'edutime_End',
                                  'edu_duration',
                                  'location', 'fee',
                                  'eduday_Sta', 'eduday_End', 'entry_Num', 'receipt_Sta', 'receipt_End', 'day', 'ref',
                                  'content', 'url'))

    wish_program = db_engine.execute("select email, lecture, center from lecture_wish where email='{}' and category='indoor'".format(email))
    wish_program = pd.DataFrame(wish_program.fetchall(), columns=('email','lecture_Name','location'))
    wish_program = program_df.merge(wish_program, on=['lecture_Name', 'location'], right_index=True)
    program_df['wish_flag'] = "wish_bt"
    program_df.loc[wish_program.index.tolist(), 'wish_flag'] = "wish_bt liked"

    program_list = []
    program_photo_num = {'A':1, 'B':5, 'C':1, 'D':5, 'E':1, 'F':5, 'G':1, 'H':1} # static/img/program에 들어있는 각 대분류별 사진 개수
    for _,data2 in program_df.iterrows():
        row_index = center_df[center_df.location==data2.location].index[0]
        program_list.append({'type_point': re.findall('\S+구', center_df.loc[row_index, 'address'])[0],
                                                'name': data2.location,
                                                'location_latitude': center_df.loc[row_index, 'lat'],
                                                'location_longitude': center_df.loc[row_index, 'long'],
                                                'map_image_url': 'static/img/program/'+str(data2.category_L)+str(random.randrange(0,program_photo_num[data2.category_L]))+'.jpg',
                                                'rate':'' ,
                                                'name_point': data2.location,
                                                'get_directions_start_address': '',
                                                'phone': center_df.loc[row_index, 'phone_num'],
                                                'url_point': data2.url,
                                                'center_url': 'center-detail?welfare='+data2.location,
                                                 'edu_name': data2.lecture_Name,
                                                 'edu_start': str(data2.edutime_Sta)[:5],
                                                 'edu_end': str(data2.edutime_End)[:5],
                                                 'edu_duration': int(data2.edu_duration),
                                                 'edu_fee': data2.fee,
                                                 'edu_day': data2.day,
                                                 'edu_ref': data2.ref,
                                                 'edu_content': data2.content,
                                                 'edu_category': [data2.category_L, data2.category_S],
                                                 'edu_entrynum': data2.entry_Num,
                                                 'wish_flag' : data2.wish_flag
                             })

    return center_list, program_list

# 보여주는 페이지의 순서 정렬
def define_listing():
    return "col-md-6 isotope-item " + random.choice(['popular', 'latest'])


