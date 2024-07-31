"""update7

Revision ID: c3c9f53010b7
Revises: 9d8288314fad
Create Date: 2024-07-29 14:50:40.535858

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c3c9f53010b7'
down_revision: Union[str, None] = '9d8288314fad'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('role_permission_role_id_fkey', 'role_permission', type_='foreignkey')
    op.drop_constraint('role_permission_permission_id_fkey', 'role_permission', type_='foreignkey')
    op.create_foreign_key(None, 'role_permission', 'roles', ['role_id'], ['id'], ondelete='CASCADE')
    op.create_foreign_key(None, 'role_permission', 'permissions', ['permission_id'], ['id'], ondelete='CASCADE')
    op.drop_constraint('role_users_role_id_fkey', 'role_users', type_='foreignkey')
    op.drop_constraint('role_users_user_id_fkey', 'role_users', type_='foreignkey')
    op.create_foreign_key(None, 'role_users', 'users', ['user_id'], ['id'], ondelete='CASCADE')
    op.create_foreign_key(None, 'role_users', 'roles', ['role_id'], ['id'], ondelete='CASCADE')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'role_users', type_='foreignkey')
    op.drop_constraint(None, 'role_users', type_='foreignkey')
    op.create_foreign_key('role_users_user_id_fkey', 'role_users', 'users', ['user_id'], ['id'])
    op.create_foreign_key('role_users_role_id_fkey', 'role_users', 'roles', ['role_id'], ['id'])
    op.drop_constraint(None, 'role_permission', type_='foreignkey')
    op.drop_constraint(None, 'role_permission', type_='foreignkey')
    op.create_foreign_key('role_permission_permission_id_fkey', 'role_permission', 'permissions', ['permission_id'], ['id'])
    op.create_foreign_key('role_permission_role_id_fkey', 'role_permission', 'roles', ['role_id'], ['id'])
    # ### end Alembic commands ###
