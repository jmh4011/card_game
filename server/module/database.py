import pymysql
import bcrypt


class db:
    def __init__(self) -> None:
        self.conn = pymysql.connect(host='127.0.0.1', user='admin', password='0000,', db='card_game', charset='utf8')
        self.cur = self.conn.cursor()


    def login(self) -> bool:
        pass
    
    def create_account(self, name, password) -> bool:
        if self.cur.execute(f"SELECT * FROM user WHERE name = {name};"):
            return False
        self.cur.execute(f"INSERT INTO user (name, passwold) VALUES ({name}, {password});")
        return True




# # 4. 데이터 입력하기 - 1이 나오면 잘 되는 것
# cur.execute("INSERT INTO userTable VALUES('hong', '홍지윤', 'hong@naver.com', 1996)")
# cur.execute("INSERT INTO userTable VALUES('kim', '김태연', 'kim@daum.com', 2011)")
# cur.execute("INSERT INTO userTable VALUES('star', '별사랑', 'star@paran.com', 1990)")
# cur.execute("INSERT INTO userTable VALUES('yang', '양지은', 'yang@gmail.com', 1993)")

# # 5. 입력한 데이터 저장하기
# conn.commit()

# # 6. MySQL 연결 종료하기
# conn.close()