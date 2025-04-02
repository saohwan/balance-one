"""make_login_attempts_user_id_nullable_3th

Revision ID: 84c471388028
Revises: fe8a787f9aa3
Create Date: 2025-04-02 21:19:58.363957

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '84c471388028'
down_revision: Union[str, None] = 'fe8a787f9aa3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
