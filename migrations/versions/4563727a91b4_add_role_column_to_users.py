"""add role column to users

Revision ID: 4563727a91b4
Revises: b13610910fc5
Create Date: 2026-03-04 20:26:03.218192

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4563727a91b4'
down_revision: Union[str, Sequence[str], None] = 'b13610910fc5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # 1️⃣ Create the enum type first
    userroles = sa.Enum('ADMIN', 'USER', name='userroles')
    userroles.create(op.get_bind(), checkfirst=True)

    # 2️⃣ Add the column using the enum
    op.add_column('users', sa.Column('role', userroles, nullable=False))

def downgrade() -> None:
    """Downgrade schema."""
    # 1️⃣ Drop the column first
    op.drop_column('users', 'role')

    # 2️⃣ Drop the enum type
    userroles = sa.Enum('ADMIN', 'USER', name='userroles')
    userroles.drop(op.get_bind(), checkfirst=True)

