from decimal import Decimal
from types import SimpleNamespace

from django.test import SimpleTestCase

from coupon_admin.models import Coupon


class CouponDiscountTests(SimpleTestCase):
	def test_category_percentage_uses_all_matching_cart_lines(self):
		coupon = Coupon(
			apply_to='category',
			categories=['Sneakers'],
			discount_type='percent',
			value=Decimal('10'),
		)
		cart_items = [
			SimpleNamespace(
				product=SimpleNamespace(category=SimpleNamespace(name='Sneakers')),
				line_total=Decimal('100.00'),
				quantity=1,
			),
			SimpleNamespace(
				product=SimpleNamespace(category=SimpleNamespace(name='sneakers')),
				line_total=Decimal('200.00'),
				quantity=1,
			),
			SimpleNamespace(
				product=SimpleNamespace(category=SimpleNamespace(name='Boots')),
				line_total=Decimal('500.00'),
				quantity=1,
			),
		]

		discount = coupon.calculate_discount(Decimal('800.00'), cart_items)

		self.assertEqual(discount, Decimal('30.00'))

	def test_flat_coupon_is_capped_at_total_of_eligible_lines(self):
		coupon = Coupon(
			apply_to='category',
			categories=['Sneakers'],
			discount_type='flat',
			value=Decimal('100'),
		)
		cart_items = [
			SimpleNamespace(
				product=SimpleNamespace(category=SimpleNamespace(name='Sneakers')),
				line_total=Decimal('40.00'),
				quantity=1,
			),
			SimpleNamespace(
				product=SimpleNamespace(category=SimpleNamespace(name='Boots')),
				line_total=Decimal('500.00'),
				quantity=1,
			),
		]

		discount = coupon.calculate_discount(Decimal('540.00'), cart_items)

		self.assertEqual(discount, Decimal('40.00'))

	def test_flat_coupon_applies_once_per_eligible_unit(self):
		coupon = Coupon(
			apply_to='category',
			categories=['Sneakers'],
			discount_type='flat',
			value=Decimal('10'),
		)
		cart_items = [
			SimpleNamespace(
				product=SimpleNamespace(category=SimpleNamespace(name='Sneakers')),
				line_total=Decimal('999.00'),
				quantity=1,
			),
			SimpleNamespace(
				product=SimpleNamespace(category=SimpleNamespace(name='Sneakers')),
				line_total=Decimal('1375.00'),
				quantity=1,
			),
			SimpleNamespace(
				product=SimpleNamespace(category=SimpleNamespace(name='Boots')),
				line_total=Decimal('500.00'),
				quantity=1,
			),
		]

		discount = coupon.calculate_discount(Decimal('2874.00'), cart_items)

		self.assertEqual(discount, Decimal('20.00'))
