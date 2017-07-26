"""Database Relationships

Revision ID: 17cd0780a403
Revises: 72e776999d4b
Create Date: 2017-07-26 15:21:42.873150

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '17cd0780a403'
down_revision = '72e776999d4b'
branch_labels = None
depends_on = None


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('user-activity', 'activity', type_='foreignkey')
    op.drop_constraint('group-activity', 'activity', type_='foreignkey')
    op.drop_column('activity', 'user_id')
    op.drop_column('activity', 'group_id')
    op.drop_constraint('activity-schedule', 'activity_schedule', type_='foreignkey')
    op.drop_constraint('user-comment', 'comment', type_='foreignkey')
    op.drop_constraint('activity-comment', 'comment', type_='foreignkey')
    op.drop_column('comment', 'user_id')
    op.drop_column('comment', 'activity_id')
    op.drop_constraint('following-user', 'follow', type_='foreignkey')
    op.drop_constraint('follower-user', 'follow', type_='foreignkey')
    op.drop_constraint('user-membership', 'membership', type_='foreignkey')
    op.drop_constraint('group-member', 'membership', type_='foreignkey')
    op.drop_constraint('user-user_activity', 'user_activity', type_='foreignkey')
    op.drop_constraint('activity-user_activity', 'user_activity', type_='foreignkey')
    # ### end Alembic commands ###


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_foreign_key('activity-user_activity', 'user_activity', 'activity', ['activity_id'], ['id'], onupdate='CASCADE', ondelete='CASCADE')
    op.create_foreign_key('user-user_activity', 'user_activity', 'user', ['user_id'], ['id'], onupdate='CASCADE', ondelete='CASCADE')
    op.create_foreign_key('group-member', 'membership', 'interest_group', ['group_id'], ['id'], onupdate='CASCADE', ondelete='CASCADE')
    op.create_foreign_key('user-membership', 'membership', 'user', ['user_id'], ['id'], onupdate='CASCADE', ondelete='CASCADE')
    op.create_foreign_key('follower-user', 'follow', 'user', ['user_id'], ['id'], onupdate='CASCADE', ondelete='CASCADE')
    op.create_foreign_key('following-user', 'follow', 'user', ['following_id'], ['id'], onupdate='CASCADE', ondelete='CASCADE')
    op.add_column('comment', sa.Column('activity_id', mysql.INTEGER(display_width=11), autoincrement=False, nullable=False))
    op.add_column('comment', sa.Column('user_id', mysql.INTEGER(display_width=11), autoincrement=False, nullable=False))
    op.create_foreign_key('activity-comment', 'comment', 'activity', ['activity_id'], ['id'], onupdate='CASCADE', ondelete='CASCADE')
    op.create_foreign_key('user-comment', 'comment', 'user', ['user_id'], ['id'], onupdate='CASCADE', ondelete='CASCADE')
    op.create_foreign_key('activity-schedule', 'activity_schedule', 'activity', ['activity_id'], ['id'], onupdate='CASCADE', ondelete='CASCADE')
    op.add_column('activity', sa.Column('group_id', mysql.INTEGER(display_width=11), autoincrement=False, nullable=False))
    op.add_column('activity', sa.Column('user_id', mysql.INTEGER(display_width=11), autoincrement=False, nullable=False))
    op.create_foreign_key('group-activity', 'activity', 'interest_group', ['group_id'], ['id'], onupdate='CASCADE', ondelete='CASCADE')
    op.create_foreign_key('user-activity', 'activity', 'user', ['user_id'], ['id'], onupdate='CASCADE', ondelete='CASCADE')
    # ### end Alembic commands ###