""" added CourseAuthorLink table and added foreign key to Course and Author table 

Revision ID: 6ceec85f8711
Revises: 4d0bc1b4e389
Create Date: 2024-09-03 07:32:48.728533

"""
from alembic import op
import sqlalchemy as sa
import sqlmodel.sql.sqltypes


# revision identifiers, used by Alembic.
revision = '6ceec85f8711'
down_revision = '4d0bc1b4e389'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('courseauthorlink',
    sa.Column('course_id', sa.Uuid(), nullable=False),
    sa.Column('author_id', sa.Uuid(), nullable=False),
    sa.ForeignKeyConstraint(['author_id'], ['author.id'], ),
    sa.ForeignKeyConstraint(['course_id'], ['course.id'], ),
    sa.PrimaryKeyConstraint('course_id', 'author_id')
    )
    op.drop_column('course', 'author')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('course', sa.Column('author', sa.VARCHAR(length=64), autoincrement=False, nullable=False))
    op.drop_table('courseauthorlink')
    # ### end Alembic commands ###
