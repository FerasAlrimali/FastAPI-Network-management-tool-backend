"""create users and sites table

Revision ID: d203ef2f7f91
Revises: 
Create Date: 2024-07-03 11:12:00.340086

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel
import sqlmodel.sql
import sqlmodel.sql.sqltypes

# revision identifiers, used by Alembic.
revision: str = 'd203ef2f7f91'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('sites',
                    sa.Column('id',sa.Integer(), primary_key=True),
                    sa.Column('site_name',sqlmodel.sql.sqltypes.AutoString(), nullable=False ))  
     
    op.create_table('users', sa.Column('id',sa.Integer(),primary_key=True),
                    sa.Column('username',sqlmodel.sql.sqltypes.AutoString(), nullable=False, unique=True ),
                    sa.Column('hashed_password',sqlmodel.sql.sqltypes.AutoString(), nullable=False ),
                    sa.Column('site_id',sa.Integer(),sa.ForeignKey("sites.id")),
                    sa.Column('authorization', sqlmodel.sql.sqltypes.AutoString(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_table('users')
    op.drop_table('sites')
    pass
