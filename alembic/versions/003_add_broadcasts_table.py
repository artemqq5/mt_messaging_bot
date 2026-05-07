"""add broadcasts table

Revision ID: b2c3d4e5f6a7
Revises: a1b2c3d4e5f6
Create Date: 2026-05-07 12:00:00.000000
"""
from alembic import op
import sqlalchemy as sa

revision = 'b2c3d4e5f6a7'
down_revision = 'a1b2c3d4e5f6'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'broadcasts',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('admin_id', sa.String(255), nullable=False),
        sa.Column('admin_name', sa.String(255), nullable=True),
        sa.Column('category', sa.String(255), nullable=False),
        sa.Column('message_text', sa.Text(), nullable=True),
        sa.Column('has_photo', sa.Boolean(), server_default='0', nullable=False),
        sa.Column('has_buttons', sa.Boolean(), server_default='0', nullable=False),
        sa.Column('sent_at', sa.DateTime(), nullable=False),
        sa.Column('groups_count', sa.Integer(), server_default='0', nullable=False),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index('ix_broadcasts_sent_at', 'broadcasts', ['sent_at'])


def downgrade() -> None:
    op.drop_index('ix_broadcasts_sent_at', table_name='broadcasts')
    op.drop_table('broadcasts')
