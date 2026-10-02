from decimal import Decimal

from django.test import TestCase

from users.models import ReferralCode, ReferralTransaction, User
from users.utils import apply_referral_for_new_user
from wallet_user.models import Wallet, WalletTransaction


class ReferralBonusTests(TestCase):
    def setUp(self):
        self.referrer = User.objects.create_user(
            email='referrer@example.com',
            password='test-password',
            first_name='Referrer',
        )
        self.referred_user = User.objects.create_user(
            email='referred@example.com',
            password='test-password',
            first_name='Referred',
        )
        self.referral_code = ReferralCode.objects.create(
            user=self.referrer,
            code='REFERRER100',
        )

    def test_signup_credits_both_wallets_once_without_an_offer(self):
        self.assertTrue(
            apply_referral_for_new_user(self.referred_user, self.referral_code.code)
        )
        apply_referral_for_new_user(self.referred_user, self.referral_code.code)

        referrer_wallet = Wallet.objects.get(user=self.referrer)
        referred_wallet = Wallet.objects.get(user=self.referred_user)
        self.assertEqual(referrer_wallet.balance, Decimal('100.00'))
        self.assertEqual(referred_wallet.balance, Decimal('50.00'))
        self.assertEqual(
            list(referrer_wallet.transactions.values_list('reason', 'transaction_type', 'amount')),
            [(WalletTransaction.REASON_REFERRAL, WalletTransaction.CREDIT, Decimal('100.00'))],
        )
        self.assertEqual(
            list(referred_wallet.transactions.values_list('reason', 'transaction_type', 'amount')),
            [(WalletTransaction.REASON_WELCOME, WalletTransaction.CREDIT, Decimal('50.00'))],
        )
        self.assertEqual(
            ReferralTransaction.objects.filter(referred_user=self.referred_user).count(),
            1,
        )
        self.referral_code.refresh_from_db()
        self.assertEqual(self.referral_code.total_referrals, 1)
        self.assertEqual(self.referral_code.total_earnings, Decimal('100.00'))
