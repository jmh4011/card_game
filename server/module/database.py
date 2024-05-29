import pymysql
import bcrypt


class Database:
    def __init__(self) -> None:
        self.conn = pymysql.connect(host='127.0.0.1', user='admin', password='0000', db='card_game', charset='utf8')
        self.cur = self.conn.cursor()


    def login(self, userid, password) -> str:
        if self.cur.execute("SELECT * FROM user WHERE userid=%s AND password=%s;", (userid, password)):
            return "success"
        else:
            return "loginError"
    
    def create_account(self, userid, password) -> str:
        if self.cur.execute("SELECT * FROM user WHERE userid = %s;",(userid)):
            return "useridDuplicate"
        self.cur.execute("INSERT INTO user (userid, password, name) VALUES (%s, %s, %s);",(userid,password,'test'))
        self.conn.commit()
        return "success"
    
    def card_info(self,id:int) -> dict:
        self.cur.execute("SELECT * FROM card WHERE id=%s;",(id))
        return self.cur.fetchall()
# conn.close()