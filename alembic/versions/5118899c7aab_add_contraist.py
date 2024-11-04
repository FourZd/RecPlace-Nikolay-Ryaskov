"""add contraist

Revision ID: 5118899c7aab
Revises: 818648ce8dc8
Create Date: 2024-11-04 22:12:58.916871

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5118899c7aab'
down_revision = '818648ce8dc8'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint('unique_user_movie', 'favorite_movies', ['user_id', 'movie_id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('unique_user_movie', 'favorite_movies', type_='unique')
    # ### end Alembic commands ###