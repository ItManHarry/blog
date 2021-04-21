from alembic import op
import sqlalchemy as sa
from datetime import datetime

def upgrade():
    op.add_column('student', sa.Column('timestamp', sa.DateTime(), nullable=True,default=datetime.utcnow))

if __name__ == '__main__':
    upgrade()