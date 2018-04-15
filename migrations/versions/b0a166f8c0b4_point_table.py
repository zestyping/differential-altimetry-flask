"""Point table

Revision ID: b0a166f8c0b4
Revises: 75d735462929
Create Date: 2018-04-15 17:03:23.230504

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b0a166f8c0b4'
down_revision = '75d735462929'
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
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('point')
    op.drop_index(op.f('ix_user_username'), table_name='user')
    op.drop_index(op.f('ix_user_email'), table_name='user')
    op.drop_table('user')
    op.drop_table('sensor')
    # ### end Alembic commands ###
