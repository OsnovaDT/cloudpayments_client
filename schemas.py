"""Schemas for data that will be send to CloudPaymentsAPIClient"""

from marshmallow import Schema, fields


class PayerSchema(Schema):
    """Payer"""

    # Name
    FirstName = fields.Str(required=True)
    LastName = fields.Str(required=True)
    MiddleName = fields.Str()

    # Address
    Address = fields.Str(required=True)
    Street = fields.Str()
    City = fields.Str(required=True)
    Country = fields.Str(required=True)
    Postcode = fields.Integer()

    Birth = fields.Date()
    Phone = fields.Integer(required=True)


class BasePaymentSchema(Schema):
    """Base payment scheme that will be used in other payment schemes"""

    # Payer
    AccountId = fields.Str()
    Payer = fields.Nested(PayerSchema())

    # Payment
    Amount = fields.Integer(required=True)
    Currency = fields.Str()


class ChargePaymentSchema(BasePaymentSchema):
    """Payment scheme for charge API method"""

    # Payment
    IpAddress = fields.Str(required=True)
    PaymentUrl = fields.Str()
    Email = fields.Str()

    # Card owner
    Name = fields.Str()
    InvoiceId = fields.Str()

    CultureName = fields.Str()
    CardCryptogramPacket = fields.Str(required=True)
    Description = fields.Str()
