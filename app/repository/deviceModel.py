from sqlalchemy import update, delete,or_, text,func, column,literal_column
from sqlalchemy.sql import select
from app.conf import db, commit_rollback
from app.model.models import DeviceModel,DeviceType
import math
from app.repository.utils import convert_columns,convert_filter,convert_sort
from app.schema import PageResponse,DeviceModelCreate
from fastapi import HTTPException, status

class DeviceModelRepository:

    @staticmethod
    async def create(create_form: DeviceModelCreate):
        db.add(DeviceModel(
                    device_model=create_form.device_model,deviceType_id=create_form.deviceType_id
        ))
        await commit_rollback()
    
    @staticmethod
    async def update(deviceModel_id: int, update_form: DeviceModelCreate):
        query = update(DeviceModel).where(DeviceModel.id == deviceModel_id)\
                        .values(**update_form.dict()).execution_options(synchronize_session='fetch')
        await db.execute(query)
        await commit_rollback()

    @staticmethod
    async def delete(deviceModel_id: int):
        query = delete(DeviceModel).where(DeviceModel.id == deviceModel_id)
        await db.execute(query)
        await commit_rollback()

    @staticmethod
    async def get_by_device_type(
        device_type: str,
        page: int = 1,
        limit: int = 10,
        columns: str = None,
        sort: str = None,
        filter: str = None
):
        query = select(DeviceModel.device_model, DeviceModel.id)\
                                    .join(DeviceType,DeviceType.id == DeviceModel.deviceType_id)\
                                        .where(DeviceType.device_type == device_type)
        if columns is not None and columns != "all":
            query.select(*convert_columns(columns,DeviceModel))

        if filter is not None and filter != "null":
            query = query.filter(or_(*convert_filter(filter,DeviceModel)))

        if sort is not None and sort != "null":
            query = query.order_by(text(convert_sort(sort)))

        offset_page = page - 1
        query = query.offset(offset_page * limit).limit(limit)
        count_query = select(func.count(1)).select_from(DeviceModel)
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
    async def get_all(
        page: int = 1,
        limit: int = 10,
        columns: str = None,
        sort: str = None,
        filter: str = None
        ):
        query = select(DeviceModel.id, DeviceModel.device_model, DeviceType.device_type)\
                                    .join(DeviceType,DeviceType.id == DeviceModel.deviceType_id)
        
        if columns is not None and columns != "all":
            query.select(*convert_columns(columns,DeviceModel))

        if filter is not None and filter != "null":
            query = query.filter(or_(*convert_filter(filter,DeviceModel)))

        if sort is not None and sort != "null":
            query = query.order_by(text(convert_sort(sort)))

        offset_page = page - 1
        query = query.offset(offset_page * limit).limit(limit)
        count_query = select(func.count(1)).select_from(DeviceModel)
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
    
        