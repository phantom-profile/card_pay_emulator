"""initial

Revision ID: 59206b022c77
Revises:
Create Date: 2023-07-29 16:34:01.141607

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '59206b022c77'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('app_name', sa.String(), nullable=False),
        sa.Column('token', sa.Uuid(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_users_app_name'), ['app_name'], unique=True)
        batch_op.create_index(batch_op.f('ix_users_id'), ['id'], unique=False)

    op.create_table(
        'cards',
        sa.Column('id', sa.Uuid(), nullable=False),
        sa.Column('card_number', sa.String(), nullable=False),
        sa.Column('cvv', sa.String(), nullable=False),
        sa.Column('owner', sa.String(), nullable=False),
        sa.Column('payment_system', sa.String(), nullable=False),
        sa.Column('trusted_app_id', sa.Integer(), nullable=False),
        sa.Column('bank_name', sa.String(), nullable=False),
        sa.ForeignKeyConstraint(['trusted_app_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('card_number', 'cvv', name='card_number_cvv_index')
    )
    with op.batch_alter_table('cards', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_cards_card_number'), ['card_number'], unique=True)
        batch_op.create_index(batch_op.f('ix_cards_cvv'), ['cvv'], unique=False)
        batch_op.create_index(batch_op.f('ix_cards_id'), ['id'], unique=False)

    op.create_table(
        'transactions',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('src_card_id', sa.Uuid(), nullable=False),
        sa.Column('dst_card_id', sa.Uuid(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('status', sa.String(), nullable=False),
        sa.Column('amount_usd', sa.Float(), nullable=False),
        sa.ForeignKeyConstraint(['dst_card_id'], ['cards.id'], ),
        sa.ForeignKeyConstraint(['src_card_id'], ['cards.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('transactions', schema=None) as batch_op:
        batch_op.create_index(
            batch_op.f('ix_transactions_dst_card_id'), ['dst_card_id'], unique=False
        )
        batch_op.create_index(
            batch_op.f('ix_transactions_id'), ['id'], unique=False
        )
        batch_op.create_index(
            batch_op.f('ix_transactions_src_card_id'), ['src_card_id'], unique=False
        )
        batch_op.create_index(
            batch_op.f('ix_transactions_status'), ['status'], unique=False
        )

    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('transactions', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_transactions_status'))
        batch_op.drop_index(batch_op.f('ix_transactions_src_card_id'))
        batch_op.drop_index(batch_op.f('ix_transactions_id'))
        batch_op.drop_index(batch_op.f('ix_transactions_dst_card_id'))

    op.drop_table('transactions')
    with op.batch_alter_table('cards', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_cards_id'))
        batch_op.drop_index(batch_op.f('ix_cards_cvv'))
        batch_op.drop_index(batch_op.f('ix_cards_card_number'))

    op.drop_table('cards')
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_users_id'))
        batch_op.drop_index(batch_op.f('ix_users_app_name'))

    op.drop_table('users')
    # ### end Alembic commands ###
