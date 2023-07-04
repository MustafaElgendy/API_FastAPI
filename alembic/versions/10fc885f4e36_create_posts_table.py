"""create posts table

Revision ID: 10fc885f4e36
Revises: 
Create Date: 2023-07-04 06:45:07.880558

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '10fc885f4e36'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('posts',sa.Column('id',sa.Integer(),nullable=True,primary_key=True),
                    sa.Column('title',sa.String(),nullable=False))
    pass


def downgrade() -> None:
    op.drop_table('posts')
    pass
