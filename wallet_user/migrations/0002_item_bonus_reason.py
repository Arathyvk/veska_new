from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wallet_user', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wallettransaction',
            name='reason',
            field=models.CharField(
                choices=[
                    ('ORDER_CANCEL', 'Order Cancelled'),
                    ('ORDER_RETURN', 'Order Returned'),
                    ('ORDER_PAYMENT', 'Wallet Payment'),
                    ('ADMIN_CREDIT', 'Admin Credit'),
                    ('ADMIN_DEBIT', 'Admin Debit'),
                    ('REFERRAL', 'Referral Bonus'),
                    ('WELCOME', 'Welcome Bonus'),
                    ('ITEM_BONUS', 'Buy 4 Items Bonus'),
                    ('MANUAL', 'Manual'),
                ],
                default='MANUAL',
                max_length=20,
            ),
        ),
    ]
