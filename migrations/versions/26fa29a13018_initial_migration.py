"""Initial migration.

Revision ID: 26fa29a13018
Revises: 
Create Date: 2022-04-16 10:47:04.945934

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '26fa29a13018'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('Property')
    op.drop_table('user_profiles')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user_profiles',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('first_name', sa.VARCHAR(length=80), autoincrement=False, nullable=True),
    sa.Column('last_name', sa.VARCHAR(length=80), autoincrement=False, nullable=True),
    sa.Column('username', sa.VARCHAR(length=80), autoincrement=False, nullable=True),
    sa.Column('password', sa.VARCHAR(length=255), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='user_profiles_pkey'),
    sa.UniqueConstraint('username', name='user_profiles_username_key')
    )
    op.create_table('Property',
    sa.Column('id', sa.INTEGER(), server_default=sa.text('nextval(\'"Property_id_seq"\'::regclass)'), autoincrement=True, nullable=False),
    sa.Column('title', sa.VARCHAR(length=80), autoincrement=False, nullable=True),
    sa.Column('bathrooms', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('rooms', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('location', sa.VARCHAR(length=255), autoincrement=False, nullable=True),
    sa.Column('price', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('type', sa.VARCHAR(length=12), autoincrement=False, nullable=True),
    sa.Column('description', sa.VARCHAR(length=255), autoincrement=False, nullable=True),
    sa.Column('photoname', sa.VARCHAR(length=255), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='Property_pkey')
    )
    # ### end Alembic commands ###
