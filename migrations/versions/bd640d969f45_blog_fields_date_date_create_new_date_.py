"""Blog fields: date -> date_create, new date_updated

Revision ID: bd640d969f45
Revises: 116e8a98400c
Create Date: 2023-02-03 13:37:14.483383

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'bd640d969f45'
down_revision = '116e8a98400c'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table('blog', schema=None) as batch_op:
        batch_op.add_column(sa.Column('date_updated', sa.DateTime(), nullable=True))
        batch_op.alter_column('date', new_column_name='date_created')


def downgrade():
    with op.batch_alter_table('blog', schema=None) as batch_op:
        batch_op.drop_column('date_updated')
        batch_op.alter_column('date_created', new_column_name='date')
