from sqlalchemy import update, delete,or_, text,func, column,literal_column
from sqlalchemy.sql import select
from app.conf import db, commit_rollback
from app.model.models import Credential, Site
import math
from app.repository.utils import convert_columns,convert_filter,convert_sort
from app.schema import PageResponse,CredentialCreate
from fastapi import HTTPException, status

class CredentialRepository:

    @staticmethod
    async def create(create_form: CredentialCreate):
        db.add(Credential(
            username=create_form.username,password=create_form.password,
            site_id=create_form.site_id
        ))
        await commit_rollback()
    
    @staticmethod
    async def get_by_site_id(site_id: int):
        query = select(Credential.username, Credential.password)\
                                    .where(Credential.site_id == site_id)
        return (await db.execute(query)).first()
    
    
    @staticmethod
    async def update(credential_id: int, update_form: CredentialCreate):
        query = update(Credential)\
                        .where(Credential.id == credential_id)\
                        .values(**update_form.dict()).execution_options(synchronize_session='fetch')
        await db.execute(query)
        await commit_rollback()

    @staticmethod
    async def delete(credential_id: int):
        query = delete(Credential).where(Credential.id == credential_id)
        await db.execute(query)
        await commit_rollback()

    @staticmethod
    async def get_all(
        page: int = 1,
        limit: int = 10,
        columns: str = None,
        sort: str = None,
        filter: str = None

        ):
        query = select(Credential.id, Credential.username, Credential.password,Credential.site_id)
        
        if columns is not None and columns != "all":
            query.select(*convert_columns(columns,Credential))

        if filter is not None and filter != "null":
            query = query.filter(or_(*convert_filter(filter,Credential)))

        if sort is not None and sort != "null":
            query = query.order_by(text(convert_sort(sort)))

        offset_page = page - 1
        query = query.offset(offset_page * limit).limit(limit)
        count_query = select(func.count(1)).select_from(Credential)
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
    
        