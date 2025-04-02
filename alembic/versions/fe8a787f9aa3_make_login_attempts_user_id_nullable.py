"""make_login_attempts_user_id_nullable

Revision ID: fe8a787f9aa3
Revises: b727aa76249e
Create Date: 2025-04-02 21:19:00.593112

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'fe8a787f9aa3'
down_revision: Union[str, None] = 'b727aa76249e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
