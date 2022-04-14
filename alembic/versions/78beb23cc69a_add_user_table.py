"""Add user table

Revision ID: 78beb23cc69a
Revises: 2be927e31af0
Create Date: 2022-04-14 17:24:03.857015

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '78beb23cc69a'
down_revision = '2be927e31af0'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('users',
                    sa.Column('id',sa.Integer(),nullable=False),
                    sa.Column('email',sa.String(),nullable=False),
                    sa.Column('password',sa.String(),nullable=False),
                    sa.Column('created_at',sa.TIMESTAMP(timezone=True),server_default=sa.text('now()'),nullable=False),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('email')
                    )
    pass


def downgrade():
    op.drop_table('users')
    pass
