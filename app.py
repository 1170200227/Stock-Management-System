import traceback
from flask import Flask
import akshare as ak
from flask import request,g,render_template,jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine,MetaData,Table,Column,Integer,String,DateTime
from datetime import datetime
import  sqlite3
from numpy import *
import numpy as np
import time as tm

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///SRS.db'
app.config['username'] = 'zhongyu'
app.config['password'] = '666666'
app.config['count'] = '100000'
app.config['id'] = '6666'
db = SQLAlchemy(app)




def create_db():
    conn = sqlite3.connect('mytest.db')
    cursor = conn.cursor()

    user = '''create table if not exists user (id int primary key , name text, 
                                do_what text, price integer , 
                                count integer ,
                                date timestamp not null default (datetime('now','localtime')))'''
    cursor.execute(user)
    # create_user = '''insert into user (id,name,do_what,price,count)
    #             values ('6666','zhongyu','null',0,100000.00)'''
    # cursor.execute(create_user)

    stock = '''create table if not exists stock (id int primary key ,number integer,
                                    date timestamp not null default (datetime('now','localtime')))'''
    stock = '''create table if not exists stock (id int primary key references user(id), stock1 float, 
            stock2 float, stock3 float, stock4 float, stock5 float, stock6 float)'''
    cursor.execute(stock)
    # create_stock = '''insert into stock (id, stock1, stock2, stock3, stock4, stock5, stock6) 
    #             values ('6666', 0, 0, 0, 0, 0, 0)'''
    # cursor.execute(create_stock)

    conn.commit()
    print('创建成功')
#    cursor.close()
    return '用户创建成功'

def search_count():
    conn = sqlite3.connect('mytest.db')
    cursor = conn.cursor()
    find = "select count from user where id='6666'"
    count = cursor.execute(find).fetchall()
    count = list(count)[0]
    final_count = float(list(count)[0])
    return round(final_count, 2)


# 登陆
@app.route('/login/',methods=['POST','GET'])
def login():
    error = None
    if request.method == 'GET':
        if request.args.get('username') != app.config['username']:
            error = 'Invalid username'
        elif request.args.get('password') != app.config['password']:
            error = 'error password'
        else:
            print('登陆成功，请等待')
            create_db()
            return 'success'
    return error
#    return render_template('***.html')

def get_basic_price():
    value = get_value()
    code = value.get('code')
    if len(code) != 6:
        return '股票代码应为6位'
    else:
        date = ak.stock_zh_a_hist_pre_min_em(symbol=code)
        price = list(date['开盘'].to_dict().values())
        basic_price = price[price.__len__() - 1]
        return basic_price

# @app.route('/number/',methods=['POST','GET'])
def get_number():
    num = request.args.get('num')
    num = float(num)
    return num

def exchange_price():
    num = get_number()
    basic_price = get_basic_price()
    buy_price = float(basic_price) * num
    return round(buy_price, 2)

def get_stock_number(UID, code):
    con = sqlite3.connect('mytest.db')
    cur = con.cursor()
    sql = ''
    stock = ''
    a = []
    if code == '000001':
        sql = 'select stock1 from stock where id = ' + str(UID)
        stock = 'stock1'
    elif code == '000002':
        sql = 'select stock2 from stock where id = ' + str(UID)
        stock = 'stock2'
    elif code == '000003':
        sql = 'select stock3 from stock where id = ' + str(UID)
        stock = 'stock3'
    elif code == '000004':
        sql = 'select stock4 from stock where id = ' + str(UID)
        stock = 'stock4'
    elif code == '000005':
        sql = 'select stock5 from stock where id = ' + str(UID)
        stock = 'stock5'
    elif code == '000006':
        sql = 'select stock6 from stock where id = ' + str(UID)
        stock = 'stock6'
    a.append(str(cur.execute(sql).fetchall()[0][0]))
    a.append(stock)
    return a

@app.route('/getmaxmin/',methods=['POST','GET'])
def getmaxmin():
    value = get_value()
    code = value.get('code')
    # a = []
    # if len(code) != 6:
    #     return '股票代码应为6位'
    # else:
    date = ak.stock_zh_a_hist_pre_min_em(symbol=code)
    price = list(date['开盘'].to_dict().values())
    return {'min':np.amin(price), 'max':np.amax(price)}


@app.route('/buy/',methods=['POST','GET'])
def buy():
    count = float(search_count())
    price = float(exchange_price())
    if count < price:
        return 'fail'
    con = sqlite3.connect('mytest.db')
    cur = con.cursor()
    value = get_value()
    code = value.get('code')
    # id = int(value.get('code'))
    # ids = value.get('code')
    number = get_number()
    if number < 0:
        return 'fail'
    final_count = count - price
    num = get_stock_number('6666', code)
#    insert = 'update user set count=? where  id=6666'
    cur.execute('update user set count=? where  id=6666',tuple([final_count]))
    UID = '6666'
    stock = "update stock set " + num[1] + "=" + str(number + float(num[0])) + " where id = " + UID
    cur.execute(stock)
    # stock_id = get_stock_id()
    # if int(ids) not in stock_id:
    #     cur.execute('insert into stock(id,number) values (?,?)',(id,number))
    # else:
    #     num = get_stock_num(ids)
    #     numbers = num + number
    #     cur.execute('delete from stock where id={}'.format(ids))
    #     cur.execute('insert into stock (id,number )  values (?,?)', (id, numbers))
    con.commit()
#   find = "select count from user where id='6666'"
#    count = cur.execute(find).fetchall()
#    print(list(count)[0])
#    cur.close()
    return 'successful buy!!!'

#   获取股票id
def get_stock_id():
    con = sqlite3.connect('mytest.db')
    cur = con.cursor()
    find_id = 'select id from stock'
    stock_ids = cur.execute(find_id).fetchall()
    new_id = [int(x) for i in stock_ids for x in i]
    return new_id

# 获取股票数量
def get_stock_num(id):
    con = sqlite3.connect('mytest.db')
    cur = con.cursor()
    num = cur.execute("select number from stock where id ={}".format(id)).fetchall()
    num = [int(x) for i in num for x in i][0]
    return num

@app.route('/sale/',methods=['POST','GET'])
def sale():
    value = get_value()
    code = value.get('code')
    num = get_stock_number('6666', code)
    number = get_number()
    if number < 0:
        return 'fail'
    if number > float(num[0]):
        return 'fail'
    
    con = sqlite3.connect('mytest.db')
    cur = con.cursor()
    # value = get_value()
    # id = value.get('code')
    # number = get_number()
    count = search_count()
    price = exchange_price()
    final_count = count + price
    cur.execute('update user set count=? where  id=6666', tuple([final_count]))
    UID = '6666'
    stock = "update stock set " + num[1] + "=" + str(float(num[0]) - number) + " where id = " + UID
    cur.execute(stock)
    con.commit()

#     new_id =get_stock_id()


#     if int(id)  in new_id :
#         #  获取对应的股票数量num
#         num = get_stock_num(id)

#         count = search_count()
#         price = exchange_price()
#         final_count = count - price
#         if num >= number:
#             update_number = num - number
#             #    insert = 'update user set count=? where  id=6666'
#             # 修改user的count
#             cur.execute('update user set count=? where  id=6666', tuple([final_count]))

# #            cur.execute("update stock " + "set number={}".format(update_number) + "where id={}".format(stock_id))
# #            cur.execute('update stock set number=? where id={}'.format(stock_id),value(update_number))
# #           修改stock的number
#             cur.execute('delete from stock where id={}'.format(id))
#             cur.execute('insert into stock (id,number )  values (?,?)', (id,update_number))

#             con.commit()
#         else:
#             return '数量不足，请重新输入'
#     else:
#         return '您未持有该股票，请先购买'
#    find = "select count from user where id='6666'"
#    count = cur.execute(find).fetchall()
#    print(list(count)[0])
#    cur.close()
    return 'successful sale!!!'

@app.route('/getcount/', methods=['POST','GET'])
def getcount():
    return str(search_count())

@app.route('/getstock/', methods=['POST','GET'])
def getstock():
    value = get_value()
    code = value.get('code')
    return get_stock_number('6666', code)[0]

@app.route('/getstockprice/', methods=['POST','GET'])
def getstockprice():
    value = get_value()
    code = value.get('code')
    basic_price = float(get_basic_price())
    price = float(get_stock_number('6666', code)[0]) * basic_price
    return str(round(price, 2))

context =  {}

def get_value():
    code = request.args.get('code')
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    return {'code':code,
                'start_date':start_date,
                'end_date':end_date}

@app.route('/today/', methods=['POST','GET'])
# 当日股价，开始时间为当日9：15，共256条数据
def TodayPrice():
    value = get_value()
    code = value.get('code')
    if len(code) != 6:
        return '股票代码应为6位'
    else:
        date = ak.stock_zh_a_hist_pre_min_em(symbol=code)
        price = date[['时间','开盘']].to_dict(orient='records')
    # 获取最新的值,供后续用户买 与 卖
    #    new_value = list(price.values())[0]
        return jsonify(price)

@app.route('/history/',methods=['POST','GET'])
def HistoryPrice():
    value = get_value()
    code = value.get('code')
    start_date = value.get('start_date')
    end_date = value.get('end_date')
    if len(code) != 6:
        return '股票代码应为6位'
    if start_date >= end_date:
        return '开始日期不能晚于结束日期'
    else:
        history = ak.stock_zh_a_hist(symbol=code,start_date=start_date,end_date=end_date,period='daily',adjust='')
        price = history[['日期','开盘','收盘','最高','最低']].to_dict(orient='records')
        price = np.array(price).tolist()

    return jsonify(price)


if __name__ == '__main__':
    app.run()
