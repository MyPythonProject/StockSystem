"""装饰器路由"""
import time
from application import urls
import re
import pymysql

def route(path):
    # path 向装饰器内部传递的参数    path    index.py
    # {"index.py": index函数引用}

    def function_out(func):    # func index函数的引用

        urls.route_dict[path] = func

        # 装饰器内层函数
        def function_in():
            # 调用原函数并且执行
            return func()

        return function_in

    return function_out


@route("/index.py")
# 1、route("/index.py")  ---> function_out 引用
# 2、@function_out
#     index = function_out(index)
#     index()  --->  function_in
def index():
    """处理 index.py 请求"""
    # 1、打开本地网页文件
    with open("templates/index.html", "r", encoding='UTF-8') as file:
        # 2、读取文件内容
        content = file.read()


        # 创建连接
        conn = pymysql.connect(host="localhost", user="root", password="tao", database="stock_db")
        # 创建游标对象
        cur = conn.cursor()
        # 通过游标执行查询
        cur.execute("select * from info")
        # 获取查询结果
        # ((...), (), ()...)
        # data_from_mysql = str(cur.fetchall())
        data_from_mysql = ""
        # 遍历列表元组(得到每一行信息)
        for line in cur.fetchall():
            str = """
            <tr>
                    <td>%s</td>
                    <td>%s</td>
                    <td>%s</td>
                    <td>%s</td>
                    <td>%s</td>
                    <td>%s</td>
                    <td>%s</td>
                    <td>%s</td>
                    <td><input type="button" value="添加" id="toAdd" name="toAdd" systemidvaule="000007"></td>
            </tr>
            """ % line
            # 拼接html格式的字符串
            data_from_mysql += str
        # 关闭操作
        cur.close()
        conn.close()


        # 正则进行替换
        content = re.sub("{%content%}", data_from_mysql, content)

    # 返回文件内容
    return content


@route("/center.py")
def center():
    """处理 center.py 请求"""
    with open("templates/center.html", "r", encoding="UTF-8") as file:
        content = file.read()

        conn = pymysql.connect(host="localhost", user="root", password="tao", database="stock_db")
        cur = conn.cursor()
        cur.execute("select i.code,i.short,i.chg,i.turnover,i.price,i.highs,f.note_info from info i, focus f where i.id = f.id")
        data_from_center = ""

        for line in cur.fetchall():
            str = """
            <tr>
                    <td>%s</td>
                    <td>%s</td>
                    <td>%s</td>
                    <td>%s</td>
                    <td>%s</td>
                    <td>%s</td>
                    <td>%s</td>
                    <td><a type="button" class="btn btn-default btn-xs" href="/update/000007.html"> <span class="glyphicon glyphicon-star" aria-hidden="true"></span> 修改 </a></td>
                    <td><input type="button" value="删除" id="toDel" name="toDel" systemidvaule="000007"></td>
            </tr>
            """ % line
            data_from_center += str
        content = re.sub("{%content%}", data_from_center, content)

    return content
