"""make_login_attempts_user_id_nullable_3th

Revision ID: c485b0aad976
Revises: 84c471388028
Create Date: 2025-04-02 21:21:08.074829

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c485b0aad976'
down_revision: Union[str, None] = '84c471388028'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
