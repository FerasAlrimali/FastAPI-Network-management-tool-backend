from datetime import datetime, date
from typing import Optional
from sqlalchemy import Column, DateTime
from sqlmodel import SQLModel, Field,Relationship
from typing import List

class Site(SQLModel,table=True):
    __tablename__ = "sites"
    
    id: int | None = Field(None,nullable=False,primary_key=True)
    site_name: str | None = Field(None, nullable=False, unique=True)
    users: List["User"] = Relationship(back_populates="site")
    devices: List["Device"] = Relationship(back_populates="site")
    vlans: List["Vlan"] = Relationship(back_populates="site")
    credentials: List["Credential"] = Relationship(back_populates="site")
    create_at: datetime = Field(default_factory=datetime.now)
    modified_at: datetime = Field(sa_column=Column(DateTime,default=datetime.now,
                                    onupdate=datetime.now, nullable=False))

class User(SQLModel,table=True):
    __tablename__ = "users"

    id: int | None = Field(None, primary_key=True, nullable=False)
    username: str | None = Field(None,nullable=False,unique=True)
    hashed_password: str | None =Field(None,nullable=False)
    site_id: int | None = Field(None,nullable=False,foreign_key="sites.id")
    site: Site | None = Relationship(back_populates="users")
    authorization: int | None =Field(None,nullable=False)
    create_at: datetime = Field(default_factory=datetime.now)
    modified_at: datetime = Field(sa_column=Column(DateTime,default=datetime.now,
                                    onupdate=datetime.now, nullable=False))

class Credential(SQLModel,table=True):
    __tablename__ = "credentials"

    id: int | None = Field(None, primary_key=True, nullable=False)
    username: str | None = Field(None,nullable=False)
    password: str | None =Field(None,nullable=False)
    site_id: int | None = Field(None,nullable=False,foreign_key="sites.id")
    site: Site | None = Relationship(back_populates="credentials")
    create_at: datetime = Field(default_factory=datetime.now)
    modified_at: datetime = Field(sa_column=Column(DateTime,default=datetime.now,
                                    onupdate=datetime.now, nullable=False))


class DeviceType(SQLModel,table=True):
    __tablename__ = "deviceTypes"

    id: int | None = Field(None, primary_key=True, nullable=False)
    device_type: str | None = Field(None,nullable=False,unique=True)
    deviceModels: List["DeviceModel"] = Relationship(back_populates="deviceType")
    create_at: datetime = Field(default_factory=datetime.now)
    modified_at: datetime = Field(sa_column=Column(DateTime,default=datetime.now,
                                    onupdate=datetime.now, nullable=False))

class DeviceModel(SQLModel,table=True):
    __tablename__ = "deviceModels"

    id: int | None = Field(None, primary_key=True, nullable=False)
    device_model: str | None = Field(None,nullable=False,unique=True)
    deviceType_id: int | None = Field(None,nullable=False,foreign_key="deviceTypes.id")
    deviceType: DeviceType | None = Relationship(back_populates="deviceModels")
    devices: List["Device"] = Relationship(back_populates="deviceModel")
    create_at: datetime = Field(default_factory=datetime.now)
    modified_at: datetime = Field(sa_column=Column(DateTime,default=datetime.now,
                                    onupdate=datetime.now, nullable=False))

class Device(SQLModel,table=True):
    __tablename__ = "devices"

    id: int | None = Field(None, primary_key=True, nullable=False)
    ip: str | None = Field(None,nullable=False)
    name: str | None = Field(None, nullable=False)
    site_id: int | None = Field(None,nullable=False,foreign_key="sites.id")
    site: Site | None = Relationship(back_populates="devices")
    deviceModel_id: int | None = Field(None,nullable=False,foreign_key="deviceModels.id")
    deviceModel: DeviceModel | None = Relationship(back_populates="devices")

class Vlan(SQLModel,table=True):
    __tablename__ = "vlans"

    id: int | None = Field(None, primary_key=True, nullable=False)
    vlan_id: str | None = Field(None,nullable=False, unique=True)
    vlan_desc: str 
    site_id: int | None = Field(None,nullable=False,foreign_key="sites.id")
    site: Site | None = Relationship(back_populates="vlans")




