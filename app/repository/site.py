from sqlalchemy import update, delete,or_, text,func, column,literal_column
from sqlalchemy.sql import select
from app.conf import db, commit_rollback
from app.model.models import Site
import math
from app.repository.utils import convert_columns,convert_filter,convert_sort
from app.schema import PageResponse, SiteCreate
from fastapi import HTTPException, status

class SiteRepository:
    @staticmethod
    async def create(create_form: SiteCreate):
        db.add(Site(site_name = create_form.site_name))
        await commit_rollback()
        
    @staticmethod
    async def update(site_id: int, update_form: SiteCreate):
        query = update(Site)\
            .where(Site.id == site_id)\
            .values(**update_form.dict())\
            .execution_options(synchronize_session='fetch')
        await db.execute(query)
        await commit_rollback()
    
    @staticmethod
    async def delete(site_id: int):
        query = delete(Site).where(Site.id == site_id)
        await db.execute(query)
        await commit_rollback()

    @staticmethod
    async def get(
        page: int = 1,
        limit: int = 0,
        columns: str = None,
        sort: str = None,
        filter: str = None
    ):
        query = select(Site.site_name,Site.id)
            
        if columns is not None and columns != "all":
            query = select(*convert_columns(columns,Site))
        
        if filter is not None and filter != "null":
            query = query.filter(or_(*convert_filter(filter)))

        if sort is not None and sort != "null":
            query = query.order_by(text(convert_sort(sort)))

        offset_page = page - 1
        query = query.offset(offset_page * limit).limit(limit)
        count_query = select(func.count(1)).select_from(Site)
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