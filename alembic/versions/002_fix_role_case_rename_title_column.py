"""fix role case and rename title_gruop

Revision ID: a1b2c3d4e5f6
Revises: d8cd90ead460
Create Date: 2026-05-01 16:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = 'a1b2c3d4e5f6'
down_revision: Union[str, Sequence[str], None] = 'd8cd90ead460'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Fix admin role case: 'admin' -> 'ADMIN', 'admin_*' -> 'ADMIN_*'
    op.execute("UPDATE admins SET role = UPPER(role) WHERE role = LOWER(role)")
    op.alter_column(
        'admins', 'role',
        existing_type=sa.String(length=255),
        server_default='ADMIN',
        existing_nullable=True,
    )


def downgrade() -> None:
    op.execute("UPDATE admins SET role = LOWER(role) WHERE role = UPPER(role)")
    op.alter_column(
        'admins', 'role',
        existing_type=sa.String(length=255),
        server_default='admin',
        existing_nullable=True,
    )
