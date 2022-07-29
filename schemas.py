"""Schemas for data that will be send to CloudPaymentsAPIClient"""

from marshmallow import Schema, fields


class PayerSchema(Schema):
    """Payer"""

    # Name
    FirstName = fields.String(required=True)
    LastName = fields.String(required=True)
    MiddleName = fields.String()

    # Address
    Address = fields.String(required=True)
    Street = fields.String()
    City = fields.String(required=True)
    Country = fields.String(required=True)
    Postcode = fields.Integer()

    Phone = fields.Integer(required=True)


class BasePaymentSchema(Schema):
    """Base payment scheme that will be used in other payment schemes"""

    # Payer
    AccountId = fields.Str(required=True)
    Payer = fields.Nested(PayerSchema())

    # Payment
    Amount = fields.Integer(required=True)
    Currency = fields.String()


class ChargeTokenPaymentSchema(BasePaymentSchema):
    """Payment scheme for charge API method"""

    Token = fields.String(required=True)
    InvoiceId = fields.String()
    Description = fields.String()
    IpAddress = fields.String()
    Email = fields.String()
