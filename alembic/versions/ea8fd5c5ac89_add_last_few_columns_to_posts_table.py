"""Add last few columns to posts table

Revision ID: ea8fd5c5ac89
Revises: d71506cab5e3
Create Date: 2022-04-14 18:16:16.669936

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ea8fd5c5ac89'
down_revision = 'd71506cab5e3'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts',sa.Column('published',sa.Boolean(),nullable=False,server_default='TRUE'))
    op.add_column('posts',sa.Column('created_at',sa.TIMESTAMP(timezone=True),server_default=sa.text('now()'),nullable=False))
    
    pass


def downgrade():
    op.drop_column('posts','published')
    op.drop_column('posts','created_at')
    pass
