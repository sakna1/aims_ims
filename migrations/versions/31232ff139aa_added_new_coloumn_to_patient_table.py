"""Added new column to Patient table

Revision ID: 31232ff139aa
Revises: af5ca1631b50
Create Date: 2025-12-05 23:58:04.394893

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '31232ff139aa'
down_revision = 'af5ca1631b50'
branch_labels = None
depends_on = None


def upgrade():
    # Step 1: Add column as nullable first
    with op.batch_alter_table('patients', schema=None) as batch_op:
        batch_op.add_column(sa.Column('username', sa.String(length=50), nullable=True))

    # Step 2: Fill existing rows with temporary values
    # temp_<id> ensures uniqueness
    op.execute("UPDATE patients SET username = 'temp_' || id")

    # Step 3: Alter column to NOT NULL and apply unique constraint
    with op.batch_alter_table('patients', schema=None) as batch_op:
        batch_op.alter_column('username', nullable=False)
        batch_op.create_unique_constraint('uq_patients_username', ['username'])


def downgrade():
    with op.batch_alter_table('patients', schema=None) as batch_op:
        batch_op.drop_constraint('uq_patients_username', type_='unique')
        batch_op.drop_column('username')
