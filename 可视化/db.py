import pymysql

config = dict(host='localhost', user='root', password='123456',
              cursorclass=pymysql.cursors.DictCursor)
# 建立连接
conn = pymysql.Connect(**config)
# 自动确认commit True
conn.autocommit(1)
# 设置光标
cursor = conn.cursor()


# 一个根据pandas自动识别type来设定table的type
def make_table_sql(df):
    columns = df.columns.tolist()
    types = df.ftypes
    # 添加id 制动递增主键模式
    make_table = []
    for item in columns:
        if 'int' in types[item]:
            char = item + ' INT'
        elif 'float' in types[item]:
            char = item + ' FLOAT'
        elif 'object' in types[item]:
            char = item + ' VARCHAR(255)'
        elif 'datetime' in types[item]:
            char = item + ' DATETIME'
        make_table.append(char)
    return ','.join(make_table)


# csv 格式输入 mysql 中
def csv2mysql(db_name, table_name, df):
    # 创建database
    cursor.execute('CREATE DATABASE IF NOT EXISTS {}'.format(db_name))
    # 选择连接database
    conn.select_db(db_name)
    # 创建table
    cursor.execute('DROP TABLE IF EXISTS {}'.format(table_name))
    cursor.execute('CREATE TABLE {}({})'.format(table_name, make_table_sql(df)))
    # 提取数据转list 这里有与pandas时间模式无法写入因此换成str 此时mysql上格式已经设置完成
    df['date'] = df['date'].astype('str')
    values = df.values.tolist()
    # 根据columns个数
    s = ','.join(['%s' for _ in range(len(df.columns))])
    # executemany批量操作 插入数据 批量操作比逐个操作速度快很多
    cursor.executemany('INSERT INTO {} VALUES ({})'.format(table_name, s), values)


if __name__ == "__main__":
    pass
