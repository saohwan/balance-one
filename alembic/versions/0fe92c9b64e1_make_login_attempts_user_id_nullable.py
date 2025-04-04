"""make_login_attempts_user_id_nullable

Revision ID: 0fe92c9b64e1
Revises: 
Create Date: 2025-04-04 14:01:30.230430

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0fe92c9b64e1'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
