"""initial

Revision ID: cff1ba19a08d
Revises: 
Create Date: 2023-07-28 19:31:28.098943

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'cff1ba19a08d'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('app_name', sa.String(), nullable=True),
    sa.Column('token', sa.Uuid(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_users_app_name'), 'users', ['app_name'], unique=True)
    op.create_index(op.f('ix_users_id'), 'users', ['id'], unique=False)
    op.create_table('cards',
    sa.Column('id', sa.Uuid(), nullable=False),
    sa.Column('card_number', sa.String(), nullable=True),
    sa.Column('cvv', sa.String(), nullable=True),
    sa.Column('owner', sa.String(), nullable=True),
    sa.Column('payment_system', sa.String(), nullable=True),
    sa.Column('trusted_app_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['trusted_app_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_cards_card_number'), 'cards', ['card_number'], unique=True)
    op.create_index(op.f('ix_cards_cvv'), 'cards', ['cvv'], unique=False)
    op.create_index(op.f('ix_cards_id'), 'cards', ['id'], unique=False)
    op.create_table('transactions',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('src_card_id', sa.Uuid(), nullable=True),
    sa.Column('dst_card_id', sa.Uuid(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('status', sa.String(), nullable=True),
    sa.Column('amount_usd', sa.Float(), nullable=True),
    sa.ForeignKeyConstraint(['dst_card_id'], ['cards.id'], ),
    sa.ForeignKeyConstraint(['src_card_id'], ['cards.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_transactions_dst_card_id'), 'transactions', ['dst_card_id'], unique=False)
    op.create_index(op.f('ix_transactions_id'), 'transactions', ['id'], unique=False)
    op.create_index(op.f('ix_transactions_src_card_id'), 'transactions', ['src_card_id'], unique=False)
    op.create_index(op.f('ix_transactions_status'), 'transactions', ['status'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_transactions_status'), table_name='transactions')
    op.drop_index(op.f('ix_transactions_src_card_id'), table_name='transactions')
    op.drop_index(op.f('ix_transactions_id'), table_name='transactions')
    op.drop_index(op.f('ix_transactions_dst_card_id'), table_name='transactions')
    op.drop_table('transactions')
    op.drop_index(op.f('ix_cards_id'), table_name='cards')
    op.drop_index(op.f('ix_cards_cvv'), table_name='cards')
    op.drop_index(op.f('ix_cards_card_number'), table_name='cards')
    op.drop_table('cards')
    op.drop_index(op.f('ix_users_id'), table_name='users')
    op.drop_index(op.f('ix_users_app_name'), table_name='users')
    op.drop_table('users')
    # ### end Alembic commands ###