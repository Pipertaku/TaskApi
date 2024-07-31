"""create forign key table

Revision ID: af675c032e39
Revises: 0ed763460f41
Create Date: 2024-07-29 06:06:40.896251

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'af675c032e39'
down_revision: Union[str, None] = '0ed763460f41'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None



def upgrade():
    op.add_column('tasks', sa.Column('user_id',sa.Integer(),nullable=False))
    op.create_foreign_key('user_task_fk',source_table='tasks',referent_table='users',local_cols=['user_id'],remote_cols=['id'],ondelete='CASCADE')
    
    pass


def downgrade():
    op.drop_column('tasks','user_id')
    op.drop_constraint('user_task_fk','tasks')
    pass

