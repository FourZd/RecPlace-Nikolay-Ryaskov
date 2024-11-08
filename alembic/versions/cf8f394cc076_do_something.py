"""do something

Revision ID: cf8f394cc076
Revises: ff60c9d4eccf
Create Date: 2024-11-04 17:14:22.156109

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'cf8f394cc076'
down_revision = 'ff60c9d4eccf'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('movies', 'name_ru',
               existing_type=sa.VARCHAR(length=255),
               nullable=True)
    op.alter_column('movies', 'name_en',
               existing_type=sa.VARCHAR(length=255),
               nullable=True)
    
    op.execute("ALTER TABLE movies ALTER COLUMN year TYPE INTEGER USING EXTRACT(EPOCH FROM year)::integer")
    op.alter_column('movies', 'rating',
               existing_type=sa.NUMERIC(),
               nullable=True)
    op.drop_constraint('movies_user_id_fkey', 'movies', type_='foreignkey')
    op.drop_column('movies', 'user_id')
    op.create_unique_constraint(None, 'users', ['username'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'users', type_='unique')
    op.add_column('movies', sa.Column('user_id', sa.INTEGER(), autoincrement=False, nullable=False))
    op.create_foreign_key('movies_user_id_fkey', 'movies', 'users', ['user_id'], ['id'])
    op.alter_column('movies', 'rating',
               existing_type=sa.NUMERIC(),
               nullable=False)
    op.alter_column('movies', 'year',
               existing_type=sa.Integer(),
               type_=postgresql.TIMESTAMP(timezone=True),
               nullable=False)
    op.alter_column('movies', 'name_en',
               existing_type=sa.VARCHAR(length=255),
               nullable=False)
    op.alter_column('movies', 'name_ru',
               existing_type=sa.VARCHAR(length=255),
               nullable=False)
    # ### end Alembic commands ###
