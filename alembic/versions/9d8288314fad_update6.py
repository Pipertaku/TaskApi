"""update6

Revision ID: 9d8288314fad
Revises: cd8b53dec810
Create Date: 2024-07-29 14:45:12.655843

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9d8288314fad'
down_revision: Union[str, None] = 'cd8b53dec810'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('role_permission', 'role_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.alter_column('role_permission', 'permission_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.alter_column('role_users', 'role_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.alter_column('role_users', 'user_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('role_users', 'user_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.alter_column('role_users', 'role_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.alter_column('role_permission', 'permission_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.alter_column('role_permission', 'role_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    # ### end Alembic commands ###
