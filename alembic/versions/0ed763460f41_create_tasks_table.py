"""create tasks table

Revision ID: 0ed763460f41
Revises: bef0c961377d
Create Date: 2024-07-29 06:05:35.901729

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0ed763460f41'
down_revision: Union[str, None] = 'bef0c961377d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.create_table('tasks',sa.Column('id',sa.Integer(),primary_key=True, nullable=False),
                    sa.Column('title',sa.String(),nullable=False),
                    sa.Column('description', sa.String(),nullable=False),
                    sa.Column('status',sa.String(),nullable=False,server_default='pending'),
                    sa.Column('priority',sa.String(),nullable=False,server_default='high'),
                    sa.Column('created_at',sa.DateTime(),nullable=False),
                    sa.Column('due_date',sa.DateTime,nullable=False)
                    )
    pass


def downgrade():
    op.drop_table('tasks')
    pass