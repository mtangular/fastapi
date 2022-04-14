"""Add foreign key to posts table

Revision ID: d71506cab5e3
Revises: 78beb23cc69a
Create Date: 2022-04-14 17:47:17.869311

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd71506cab5e3'
down_revision = '78beb23cc69a'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts',sa.Column('owner_id',sa.Integer(),nullable=False))
    op.create_foreign_key('posts_users_fk',source_table="posts",referent_table="users",local_cols=["owner_id"],remote_cols=["id"],ondelete="CASCADE")
    pass


def downgrade():
    op.drop_constraint('posts_users_fk',table_name="posts")
    op.drop_column('posts','owner_id')
    pass
