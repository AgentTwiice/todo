"""Initial schema"""

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = "0001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.Uuid(as_uuid=True), primary_key=True),
        sa.Column("email", sa.String, nullable=False, unique=True),
        sa.Column("hashed_password", sa.String, nullable=False),
        sa.Column("created_at", sa.DateTime, nullable=False),
    )

    op.create_table(
        "calendars",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("user_id", sa.Uuid(as_uuid=True), sa.ForeignKey("users.id")),
        sa.Column("provider", sa.String, nullable=False),
        sa.Column("access_token", sa.String, nullable=False),
        sa.Column("refresh_token", sa.String),
        sa.Column("last_synced", sa.DateTime),
    )

    task_priority = sa.Enum("low", "medium", "high", name="taskpriority")
    task_status = sa.Enum("pending", "completed", "cancelled", name="taskstatus")
    task_priority.create(op.get_bind(), checkfirst=True)
    task_status.create(op.get_bind(), checkfirst=True)

    op.create_table(
        "tasks",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("user_id", sa.Uuid(as_uuid=True), sa.ForeignKey("users.id")),
        sa.Column("title", sa.String, nullable=False),
        sa.Column("description", sa.String),
        sa.Column("due_datetime", sa.DateTime),
        sa.Column("priority", task_priority, nullable=False, server_default="medium"),
        sa.Column("calendar_event_id", sa.String),
        sa.Column("status", task_status, nullable=False, server_default="pending"),
        sa.Column("created_at", sa.DateTime, nullable=False),
        sa.Column("updated_at", sa.DateTime, nullable=False),
    )


def downgrade() -> None:
    op.drop_table("tasks")
    op.drop_table("calendars")
    op.drop_table("users")
    task_priority = sa.Enum("low", "medium", "high", name="taskpriority")
    task_status = sa.Enum("pending", "completed", "cancelled", name="taskstatus")
    task_priority.drop(op.get_bind(), checkfirst=True)
    task_status.drop(op.get_bind(), checkfirst=True)
