"""Add reading table

Revision ID: d41e78b08d5f
Revises: 24cb19a6af7f
Create Date: 2018-04-15 21:49:10.802769

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd41e78b08d5f'
down_revision = '24cb19a6af7f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('sensor',
    sa.Column('sensor_id', sa.String(length=64), nullable=False),
    sa.Column('fixed', sa.Boolean(), nullable=True),
    sa.Column('lat', sa.Float(), nullable=True),
    sa.Column('lon', sa.Float(), nullable=True),
    sa.Column('alt', sa.Float(), nullable=True),
    sa.PrimaryKeyConstraint('sensor_id')
    )
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=64), nullable=True),
    sa.Column('email', sa.String(length=120), nullable=True),
    sa.Column('password_hash', sa.String(length=128), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_user_email'), 'user', ['email'], unique=True)
    op.create_index(op.f('ix_user_username'), 'user', ['username'], unique=True)
    op.create_table('point',
    sa.Column('id', sa.String(length=64), nullable=False),
    sa.Column('sensor_id', sa.String(length=64), nullable=True),
    sa.Column('time', sa.DateTime(), nullable=True),
    sa.Column('lat', sa.Float(), nullable=True),
    sa.Column('lon', sa.Float(), nullable=True),
    sa.Column('lat_lon_sd', sa.Float(), nullable=True),
    sa.Column('alt', sa.Float(), nullable=True),
    sa.Column('alt_sd', sa.Float(), nullable=True),
    sa.ForeignKeyConstraint(['sensor_id'], ['sensor.sensor_id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('reading',
    sa.Column('id', sa.String(length=64), nullable=False),
    sa.Column('sensor_id', sa.String(length=64), nullable=True),
    sa.Column('calibration', sa.Boolean(), nullable=True),
    sa.Column('time', sa.DateTime(), nullable=True),
    sa.Column('duration', sa.Float(), nullable=True),
    sa.Column('lat', sa.Float(), nullable=True),
    sa.Column('lon', sa.Float(), nullable=True),
    sa.Column('lat_lon_sd', sa.Float(), nullable=True),
    sa.Column('uncal_pressure', sa.Float(), nullable=True),
    sa.Column('uncal_pressure_sd', sa.Float(), nullable=True),
    sa.Column('uncal_temperature', sa.Float(), nullable=True),
    sa.Column('uncal_temperature_sd', sa.Float(), nullable=True),
    sa.Column('sample_count', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['sensor_id'], ['sensor.sensor_id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('reading')
    op.drop_table('point')
    op.drop_index(op.f('ix_user_username'), table_name='user')
    op.drop_index(op.f('ix_user_email'), table_name='user')
    op.drop_table('user')
    op.drop_table('sensor')
    # ### end Alembic commands ###
