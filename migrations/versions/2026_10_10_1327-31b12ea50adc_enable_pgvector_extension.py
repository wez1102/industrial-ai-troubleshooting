"""enable pgvector extension

Revision ID: 31b12ea50adc
Revises:
Create Date: 2026-10-10 13:27:11.045875

"""

from collections.abc import Sequence

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "31b12ea50adc"
down_revision: str | Sequence[str] | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """
    Upgrade schema.
    """
    op.execute("CREATE EXTENSION IF NOT EXISTS vector")


def downgrade() -> None:
    """
    Downgrade schema.
    """
    op.execute("DROP EXTENSION IF EXISTS vector")
