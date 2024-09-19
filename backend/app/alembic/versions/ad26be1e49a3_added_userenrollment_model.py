""" added UserEnrollment model

Revision ID: ad26be1e49a3
Revises: 4a93345e588d
Create Date: 2024-09-19 12:21:23.823324

"""
from alembic import op
import sqlalchemy as sa
import sqlmodel.sql.sqltypes


# revision identifiers, used by Alembic.
revision = 'ad26be1e49a3'
down_revision = '4a93345e588d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('userenrollment',
    sa.Column('user_id', sa.Uuid(), nullable=False),
    sa.Column('course_id', sa.Uuid(), nullable=False),
    sa.Column('enrollment_date', sa.DateTime(), nullable=False),
    sa.Column('status', sqlmodel.sql.sqltypes.AutoString(length=64), nullable=True),
    sa.ForeignKeyConstraint(['course_id'], ['course.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['userprofile.id'], ),
    sa.PrimaryKeyConstraint('user_id', 'course_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('userenrollment')
    # ### end Alembic commands ###
