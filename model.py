from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, UnicodeText, Float, DateTime, PrimaryKeyConstraint

from re import sub
from decimal import Decimal

Base = declarative_base()

class SymbolEODEntry(Base):
    __tablename__ = 'EOD'

    date = Column(DateTime, nullable=False)
    symbol = Column(UnicodeText, nullable=False)

    account_name = Column(UnicodeText, nullable=False)

    quantity = Column(Float, nullable=False)

    last_price = Column(Float, nullable=False)
    last_price_change = Column(Float, nullable=False)

    current_value = Column(Float, nullable=False)
    today_dollar = Column(Float)
    today_percent = Column(Float)
    total_dollar = Column(Float, nullable=False)
    total_percent = Column(Float, nullable=False)

    cost_basis_per_share = Column(Float, nullable=False)
    cost_basis_total = Column(Float, nullable=False)

    __table_args__ = (
        PrimaryKeyConstraint(
            date,
            symbol),
        {})

    def __init__(self, date, row):
        self.date = date
        self.symbol = row["Symbol"]

        self.account_name = row["Account Name/Number"]

        self.quantity = float(row["Quantity"])

        self.last_price = Decimal(sub(r'[^\d.]', '', row["Last Price"]))
        self.last_price_change = Decimal(sub(r'[^\d.]', '', row["Last Price Change"]))

        self.current_value = Decimal(sub(r'[^\d.]', '', row["Current Value"]))

        if "--" not in row["Today's Gain/Loss Dollar"]:
            self.today_dollar = Decimal(sub(r'[^\d.]', '', row["Today's Gain/Loss Dollar"]))
        if "--" not in row["Today's Gain/Loss Percent"]:
            self.today_percent = row["Today's Gain/Loss Percent"].strip('%')

        if "--" not in row["Total Gain/Loss Dollar"]:
            self.total_dollar = Decimal(sub(r'[^\d.]', '', row["Total Gain/Loss Dollar"]))
        if "--" not in row["Total Gain/Loss Percent"]:
            self.total_percent = row["Total Gain/Loss Percent"].strip('%')

        if "--" not in row["Cost Basis Per Share"]:
            self.cost_basis_per_share = Decimal(sub(r'[^\d.]', '', row["Cost Basis Per Share"]))
        if "--" not in row["Cost Basis Total"]:
            self.cost_basis_total = Decimal(sub(r'[^\d.]', '', row["Cost Basis Total"]))
