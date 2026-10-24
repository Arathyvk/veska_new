from django.test import TestCase

from decimal import Decimal

from django.contrib.auth import get_user_model

from order_user.models import Order, OrderItem
from wallet_user.models import Wallet, WalletTransaction
from wallet_user.utils import credit_item_group_bonus


class ItemGroupBonusTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email='bonus@example.com',
            password='secret123',
        )
        self.order = Order.objects.create(
            user=self.user,
            full_name='Bonus User',
            phone='1234567890',
            address_line1='123 Main St',
            city='Mumbai',
            state='MH',
            pincode='400001',
            country='India',
            payment_method='stripe',
            payment_status='paid',
            status='confirmed',
        )

    def make_items(self, quantity):
        OrderItem.objects.create(
            order=self.order,
            product_name='Test item',
            product_slug='test-item',
            unit_price=Decimal('10.00'),
            quantity=quantity,
        )

    def test_awards_fifty_rupees_for_four_items(self):
        self.make_items(4)

        bonus = credit_item_group_bonus(self.order)

        wallet = Wallet.objects.get(user=self.user)
        self.assertEqual(bonus, Decimal('50.00'))
        self.assertEqual(wallet.balance, Decimal('50.00'))
        transaction = wallet.transactions.get()
        self.assertEqual(transaction.reason, WalletTransaction.REASON_ITEM_BONUS)
        self.assertEqual(transaction.order, self.order)

    def test_awards_bonus_for_each_complete_group_only_once(self):
        self.make_items(9)

        first_bonus = credit_item_group_bonus(self.order)
        second_bonus = credit_item_group_bonus(self.order)

        wallet = Wallet.objects.get(user=self.user)
        self.assertEqual(first_bonus, Decimal('100.00'))
        self.assertEqual(second_bonus, Decimal('0.00'))
        self.assertEqual(wallet.balance, Decimal('100.00'))
        self.assertEqual(wallet.transactions.count(), 1)

    def test_does_not_award_unpaid_cod_order_until_delivered(self):
        self.order.payment_method = 'cod'
        self.order.payment_status = 'pending'
        self.order.save(update_fields=['payment_method', 'payment_status'])
        self.make_items(4)

        self.assertEqual(credit_item_group_bonus(self.order), Decimal('0.00'))
        self.assertFalse(Wallet.objects.filter(user=self.user).exists())

        self.order.status = 'delivered'
        self.order.save(update_fields=['status'])
        self.assertEqual(credit_item_group_bonus(self.order), Decimal('50.00'))
        self.assertEqual(Wallet.objects.get(user=self.user).balance, Decimal('50.00'))
