""" added CourseChapter model

Revision ID: 800d833aa70e
Revises: c417ded569db
Create Date: 2024-09-18 10:29:12.756461

"""
from alembic import op
import sqlalchemy as sa
import sqlmodel.sql.sqltypes


# revision identifiers, used by Alembic.
revision = '800d833aa70e'
down_revision = 'c417ded569db'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('coursechapter',
    sa.Column('id', sa.Uuid(), nullable=False),
    sa.Column('title', sqlmodel.sql.sqltypes.AutoString(length=128), nullable=False),
    sa.Column('content', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    sa.Column('order', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    sa.Column('course_id', sa.Uuid(), nullable=False),
    sa.ForeignKeyConstraint(['course_id'], ['course.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('coursechapter')
    # ### end Alembic commands ###
