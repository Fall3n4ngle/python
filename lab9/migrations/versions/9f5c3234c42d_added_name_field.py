"""added name field

Revision ID: 9f5c3234c42d
Revises: d833be7e077b
Create Date: 2023-11-02 11:10:51.005532

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9f5c3234c42d'
down_revision = 'd833be7e077b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('feedback', schema=None) as batch_op:
        batch_op.add_column(sa.Column('name', sa.String(length=40), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('feedback', schema=None) as batch_op:
        batch_op.drop_column('name')

    # ### end Alembic commands ###
