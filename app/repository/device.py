from sqlalchemy import update, delete,or_, text,func, column,literal_column
from sqlalchemy.sql import select
from app.conf import db, commit_rollback
from app.model.models import DeviceModel,Device,DeviceType
import math
from app.repository.utils import convert_columns,convert_filter,convert_sort
from app.schema import PageResponse,DeviceCreate
from fastapi import HTTPException, status
from fastapi_filters.ext.sqlalchemy import apply_filters
class DeviceRepository:

    @staticmethod
    async def create(create_form: DeviceCreate):
        db.add(Device(
                    ip=create_form.ip,name=create_form.name,
                    site_id=create_form.site_id,deviceModel_id=create_form.deviceModel_id
        ))
        await commit_rollback()
    
    @staticmethod
    async def update(device_id: int, update_form: DeviceCreate):
        query = update(Device).where(Device.id == device_id)\
                        .values(**update_form.dict()).execution_options(synchronize_session='fetch')
        await db.execute(query)
        await commit_rollback()

    @staticmethod
    async def delete(device_id: int):
        query = delete(Device).where(Device.id == device_id)
        await db.execute(query)
        await commit_rollback()

    @staticmethod
    async def get_by_device_type_and_site_id(
        site_id: int,
        device_type: str,
        page: int = 1,
        limit: int = 10,
        columns: str = None,
        sort: str = None,
        filter: str = None
):
        query = select(Device.ip,Device.id,Device.name,DeviceType.device_type,DeviceModel.device_model)\
                                    .join(DeviceModel,DeviceModel.id == Device.deviceModel_id)\
                                    .join(DeviceType,DeviceType.id == DeviceModel.deviceType_id)\
                                        .where(DeviceType.device_type == device_type , Device.site_id == site_id )
        if columns is not None and columns != "all":
            query.select(*convert_columns(columns,DeviceModel))

        if filter is not None and filter != "null":
            query = query.filter(or_(*convert_filter(filter,DeviceModel)))

        if sort is not None and sort != "null":
            query = query.order_by(text(convert_sort(sort)))

        offset_page = page - 1
        query = query.offset(offset_page * limit).limit(limit)
        count_query = select(func.count(1)).select_from(Device).join(Device.deviceModel).join(DeviceModel.deviceType).where(DeviceType.device_type == device_type and Device.site_id == site_id )
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
    async def get_all_by_site_id(
        site_id: int,
        page: int = 1,
        limit: int = 10,
        columns: str = None,
        sort: str = None,
        filter: str = None
        ):
        query = select(Device.ip,Device.id,Device.name,DeviceType.device_type,DeviceModel.device_model)\
                                    .join(DeviceModel,DeviceModel.id == Device.deviceModel_id)\
                                    .join(DeviceType,DeviceType.id == DeviceModel.deviceType_id)\
                                    .where(Device.site_id == site_id )
        
        if columns is not None and columns != "all":
            query.select(*convert_columns(columns,Device))

        if filter is not None and filter != "null":
            query = query.filter(or_(*convert_filter(filter,Device)))

        if sort is not None and sort != "null":
            query = query.order_by(text(convert_sort(sort)))

        offset_page = page - 1
        query = query.offset(offset_page * limit).limit(limit)
        count_query = select(func.count(1)).select_from(Device).where(Device.site_id == site_id)
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
    
        
    async def get_switches_by_site_id(site_id: int):
        query = select(Device.ip,Device.name,DeviceType.device_type)\
                                    .join(Device.deviceModel)\
                                    .join(DeviceModel.deviceType)\
                                    .where(Device.site_id == site_id, DeviceType.device_type == "Switch")
        
        # result
        result = (await db.execute(query)).fetchall()
        content = [r._mapping for r in result]
        #print(result[0]._mapping) to print_filtered_data
        #print(result)
        return content

    @staticmethod
    async def test(filters):
        query = select(Device.ip,Device.id,Device.name,DeviceType.device_type,DeviceModel.device_model)\
            .join(Device.deviceModel)\
                .join(DeviceModel.deviceType)
        query = apply_filters(query, filters)
        result =  (await db.execute(query)).fetchall()
        return [r._mapping for r in result]