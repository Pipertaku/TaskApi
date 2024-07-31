"""create user table

Revision ID: bef0c961377d
Revises: 
Create Date: 2024-07-29 06:04:15.305431

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'bef0c961377d'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade():
    op.create_table('users',sa.Column('id',sa.Integer(), nullable=False,primary_key=True),
                    sa.Column('firstname',sa.String(),nullable=False),
                    sa.Column('lastname',sa.String(),nullable=False),
                    sa.Column('age',sa.Integer,nullable=False),
                    sa.Column('sex',sa.String(),nullable=False,server_default='male'),
                    sa.Column('password',sa.String(),nullable=False),
                    sa.Column('email',sa.String,nullable=False, unique=True))
    
    pass

def downgrade():
    op.drop_table('users')
    pass