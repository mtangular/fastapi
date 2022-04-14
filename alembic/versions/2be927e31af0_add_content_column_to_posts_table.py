"""Add content column to posts table

Revision ID: 2be927e31af0
Revises: ce574065a10e
Create Date: 2022-04-14 16:45:31.919487

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2be927e31af0'
down_revision = 'ce574065a10e'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts',sa.Column('content',sa.String(),nullable=False))


def downgrade():
    op.drop_column('posts','content')
    pass
