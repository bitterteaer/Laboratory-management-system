"""empty message

Revision ID: b41c920adbd5
Revises: 
Create Date: 2022-07-24 10:15:40.978975

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b41c920adbd5'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('register_requests',
    sa.Column('id_register_requests', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('username', sa.String(length=45), nullable=False),
    sa.Column('password', sa.String(length=45), nullable=False),
    sa.Column('name', sa.String(length=45), nullable=False),
    sa.Column('phone', sa.String(length=45), nullable=False),
    sa.Column('role', sa.String(length=45), nullable=False),
    sa.Column('power', sa.Integer(), nullable=False),
    sa.Column('grade', sa.String(length=45), nullable=False),
    sa.PrimaryKeyConstraint('id_register_requests'),
    sa.UniqueConstraint('username')
    )
    op.create_table('user',
    sa.Column('id_user', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('username', sa.String(length=45), nullable=False),
    sa.Column('password', sa.String(length=45), nullable=False),
    sa.Column('name', sa.String(length=45), nullable=False),
    sa.Column('phone', sa.String(length=45), nullable=False),
    sa.Column('role', sa.String(length=45), nullable=False),
    sa.Column('power', sa.Integer(), nullable=False),
    sa.Column('grade', sa.String(length=45), nullable=False),
    sa.PrimaryKeyConstraint('id_user'),
    sa.UniqueConstraint('username')
    )
    op.create_table('big_data',
    sa.Column('id_big_data', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('filename', sa.String(length=45), nullable=False),
    sa.Column('path', sa.String(length=200), nullable=False),
    sa.Column('time', sa.String(length=45), nullable=False),
    sa.Column('who_can_see', sa.Integer(), nullable=False),
    sa.Column('id_user', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['id_user'], ['user.id_user'], ),
    sa.PrimaryKeyConstraint('id_big_data')
    )
    op.create_table('data',
    sa.Column('id_data', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('title', sa.String(length=45), nullable=False),
    sa.Column('content', sa.Text(), nullable=False),
    sa.Column('appendix', sa.String(length=200), nullable=False),
    sa.Column('time', sa.String(length=45), nullable=False),
    sa.Column('id_user', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['id_user'], ['user.id_user'], ),
    sa.PrimaryKeyConstraint('id_data')
    )
    op.create_table('device',
    sa.Column('id_device', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(length=45), nullable=False),
    sa.Column('pic', sa.String(length=200), nullable=False),
    sa.Column('time', sa.String(length=45), nullable=False),
    sa.Column('id_user', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['id_user'], ['user.id_user'], ),
    sa.PrimaryKeyConstraint('id_device')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('device')
    op.drop_table('data')
    op.drop_table('big_data')
    op.drop_table('user')
    op.drop_table('register_requests')
    # ### end Alembic commands ###
