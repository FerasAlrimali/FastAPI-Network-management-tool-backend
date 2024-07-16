from sqlalchemy import update, delete,or_, text,func, column,literal_column
from sqlalchemy.sql import select
from app.conf import db, commit_rollback
from app.model.models import DeviceType
import math
from app.repository.utils import convert_columns,convert_filter,convert_sort
from app.schema import PageResponse,DeviceTypeCreate
from fastapi import HTTPException, status

class DeviceTypeRepository:

    @staticmethod
    async def create(create_form: DeviceTypeCreate ):
        db.add(DeviceType(
            device_type=create_form.device_type
        ))
        await commit_rollback()

    @staticmethod
    async def update(deviceType_id: int, update_form: DeviceTypeCreate):
        query = update(DeviceType).where(DeviceType.id == deviceType_id)\
                                  .values(**update_form.dict())\
                                  .execution_options(synchronize_session='fetch')
        await db.execute(query)
        await commit_rollback()

    @staticmethod
    async def delete(deviceType_id: int):
        query = delete(DeviceType).where(DeviceType.id == deviceType_id)
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
        query = select(DeviceType.id, DeviceType.device_type)
        
        if columns is not None and columns != "all":
            query.select(*convert_columns(columns,DeviceType))

        if filter is not None and filter != "null":
            query = query.filter(or_(*convert_filter(filter,DeviceType)))

        if sort is not None and sort != "null":
            query = query.order_by(text(convert_sort(sort)))

        offset_page = page - 1
        query = query.offset(offset_page * limit).limit(limit)
        count_query = select(func.count(1)).select_from(DeviceType)
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
    