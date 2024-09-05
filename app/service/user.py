import string
from datetime import date
from typing import Optional

from fastapi import Form, requests
from sqlalchemy import insert, select, and_
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
import re
from typing import Dict

from sqlalchemy.sql.functions import random

from app.model.users import Users
from app.schema.user import NewUser



def get_user_data(
        userid: str = Form(...),
        passwd: str = Form(...),
        name: str = Form(...),
        email: str = Form(...),
        birth: date = Form(...),
        phone: str = Form(...),
        captcha: str = Form(...),
        business_id: Optional[str] = Form(None),
        businessno: Optional[str] = Form(None)
):
    return NewUser(
        userid=userid,
        passwd=passwd,
        name=name,
        email=email,
        birth=birth,
        phone=phone,
        captcha=captcha,
        business_id=business_id,
        businessno=businessno
    )



class UserService:
    @staticmethod
    def insert_user(db: Session, user: NewUser):
        try:
            stmt = insert(Users).values(
                userid=user.userid,
                passwd=user.passwd,
                name=user.name,
                email=user.email,
                birth=user.birth,
                phone=user.phone
            )
            result = db.execute(stmt)
            db.commit()
            return result
        except SQLAlchemyError as ex:
            print(f'▶▶▶ insert_user 오류발생: {str(ex)}')
            db.rollback()

    @staticmethod
    def insert_business_user(db: Session, user: NewUser, BusinessUser=None):
        try:
            if not user.business_id or not user.businessno:
                print("Business ID or Business Number is missing")
                return None

            # 자체 유효성 검사 수행 (API 대신 직접 검증)
            if not UserService.is_valid_business_number(user.businessno):
                print("Invalid business number format")
                return None

            stmt = insert(BusinessUser).values(
                business_id=user.business_id,
                business_pwd=user.passwd,
                business_name=user.name,
                business_email=user.email,
                business_phone=user.phone,
                business_birth=user.birth,
                business_uploadno=user.businessno
            )
            result = db.execute(stmt)
            db.commit()
            return result
        except SQLAlchemyError as ex:
            print(f'Error occurred during database operation: {str(ex)}')
            db.rollback()


    @staticmethod
    def save_user(db: Session, user: NewUser):
        if user.business_id and user.businessno:
            result = UserService.insert_business_user(db, user)
            if result is None:
                print("Database insert operation failed or no rows affected.")
        else:
            result = UserService.insert_user(db, user)
            if result is None:
                print("Database insert operation failed or no rows affected.")
        return result


    @staticmethod
    def check_captcha(user):
        req_url = 'https://www.google.com/recaptcha/api/siteverify'
        params = {
            'secret': '6LeKoCsqAAAAAOGQbslqQCwHU6shGBsPfmajiVh5',
            'response': user.captcha
        }

        res = requests.get(req_url, params=params)
        result = res.json()
        print('check => ', result)

        return result['success']

    @staticmethod
    def login_member(db: Session, data):
        try:
            find_login = and_(Users.userid == data.get('userid'),
                              Users.passwd == data.get('passwd'))
            stmt = select(Users).where(find_login).where(Users.status == None) # 이부분만 추가
            result = db.execute(stmt).scalars().first()


            return result
        except SQLAlchemyError as ex:
            print(f' ▶▶▶ login_member 오류 발생 : {str(ex)}')
            db.rollback()
            return None


    @staticmethod
    def check_userid_exists(db, userid):
        try:
            stmt= select(Users).where(Users.userid == userid)
            result = db.execute(stmt).scalars().first()
            return result is not None # 아이디가 존재하면 True, 아니면 False 반환


        except SQLAlchemyError as ex:
            print(f'▶▶▶ check_userid_exists 오류 발생 : {str(ex)}')
            db.rollback()
            return False



    @staticmethod
    def validate_business_number(business_no: str) -> Dict:
        """
        Validate the business number format.

        Args:
            business_no (str): The business number to validate.

        Returns:
            Dict: A dictionary with validation result.
        """
        # 사업자 등록 번호 형식 검증 (10자리 숫자)
        pattern = re.compile(r'^\d{3}-\d{2}-\d{5}$')

        # 형식에 맞는지 확인
        if pattern.match(business_no):
            # 추가적인 검증 로직이 필요할 경우 여기에 추가
            # 예를 들어, 특정 패턴의 유효성을 추가적으로 검증할 수 있습니다.
            return {"valid": True}
        else:
            return {"valid": False}




    @staticmethod
    def check_business_number(business_number: str) -> bool:
        """
        사업자 등록 번호의 유효성을 확인하는 메서드.
        자체 검증 로직을 사용하여 API 호출을 하지 않습니다.
        """
        try:
            # 사업자 등록 번호 형식 검증
            is_valid_format = UserService.validate_business_number_format(business_number)

            # 형식이 유효한 경우에는 True를 반환
            if is_valid_format:
                return True

            # 형식이 유효하지 않은 경우에는 False를 반환
            return False

        except Exception as ex:
            print(f'▷▷▷ check_business_number 오류 발생 : {str(ex)}')
            return False


    @staticmethod
    def is_valid_business_number(business_number: str) -> bool:
        # 비즈니스 번호의 형식을 직접 검사하는 함수
        # 간단한 형식 검증 예시 (길이와 숫자 확인)
        if len(business_number) == 10 and business_number.isdigit():
            return True
        return False


    @staticmethod
    def get_masked_password(user: Users) -> str:
        """비밀번호의 첫 번째 자리를 마스킹하고 나머지 부분은 모두 표시합니다."""
        password = user.passwd
        if len(password) > 1:
            masked_password = '*' + password[1:]
        else:
            # 비밀번호가 한 자리 이하인 경우, 전체 비밀번호를 반환
            masked_password = '*' * len(password)
        return masked_password