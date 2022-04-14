"""create posts table

Revision ID: ce574065a10e
Revises: 
Create Date: 2022-04-14 16:44:37.983487

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ce574065a10e'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('posts',sa.Column('id',sa.Integer(),primary_key=True,nullable=False),sa.Column('title',sa.String(),nullable=False))
    pass


def downgrade():
    op.drop_table('posts')
    pass
