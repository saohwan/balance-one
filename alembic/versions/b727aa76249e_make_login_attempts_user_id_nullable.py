"""make_login_attempts_user_id_nullable

Revision ID: b727aa76249e
Revises: 78176c135f33
Create Date: 2025-04-02 21:18:23.041962

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b727aa76249e'
down_revision: Union[str, None] = '78176c135f33'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
