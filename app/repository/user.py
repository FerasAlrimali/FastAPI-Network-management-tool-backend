from sqlalchemy import update, delete,or_, text,func, column,literal_column
from sqlalchemy.sql import select
from app.conf import db, commit_rollback
from app.model.models import User, Site
import math
from app.repository.utils import convert_columns,convert_filter,convert_sort
from app.schema import PageResponse,UserCreate
from fastapi import HTTPException, status
from ..utils import get_password_hash

class UserRepository:
    @staticmethod

    async def create(create_form: UserCreate):
        db.add(
            User(
                username=create_form.username.lower(),
                hashed_password=get_password_hash(create_form.hashed_password),
                site_id=create_form.site_id,
                authorization=create_form.authorization
            ))
        await commit_rollback()
    
    @staticmethod
    async def get_by_name(username: str):
        query = select(User).where(User.username == username)
        return (await db.execute(query)).scalar_one_or_none()
    
    @staticmethod
    async def update(user_id:int,update_form: UserCreate):
        hashed_pw = get_password_hash(update_form.hashed_password)
        update_form.hashed_password = hashed_pw
        query = update(User).where(User.id == user_id)\
        .values(**update_form.dict())\
        .execution_options(synchronize_session='fetch')
        await db.execute(query)
        await commit_rollback()

    @staticmethod
    async def delete(user_id: int):

        query = delete(User).where(User.id == user_id)
        await db.execute(query)
        await commit_rollback()

    @staticmethod
    async def get_all(page: int = 1,
                      limit: int = 10,
                      columns: str = None,
                      sort: str = None,
                      filter: str = None
    ):
        query = select(User.username,User.id,User.authorization,Site.site_name,User.site_id)\
                                                    .join(Site, Site.id == User.site_id)
        
        if columns is not None and columns != "all":
            query.select(*convert_columns(columns,User))

        if filter is not None and filter != "null":
            query = query.filter(or_(*convert_filter(filter,User)))

        if sort is not None and sort != "null":
            query = query.order_by(text(convert_sort(sort)))

        offset_page = page - 1
        query = query.offset(offset_page * limit).limit(limit)
        count_query = select(func.count(1)).select_from(User)
        total_records = (await db.execute(count_query)).scalar() or 0
        total_page = math.ceil(total_records/limit)

        # result
        result = (await db.execute(query)).fetchall()
        content = [r._mapping for r in result]
        #print(result[0]._mapping) to print_filtered_data
        #print(result)
        return PageResponse(
                page_number = page,
                page_size = limit,
                total_pages = total_page,
                total_records = total_records,
                content = content
        )

    @staticmethod
    async def test(filters):
        return