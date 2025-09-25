import pytest 
from app.calculations import add, subtract, multiply, divide, BankAccount, InsufficientFunds

@pytest.fixture
def zero_bank_account():
    print("Creating a bank account with zero balance")
    return BankAccount()

@pytest.fixture
def bank_account():
    print("Creating a bank account with 50 balance")
    return BankAccount(50)


@pytest.mark.parametrize("num1, num2, expected", [
    (5, 3, 8),
    (10, -2, 8),
    # (0, 0, 0),
    # (-1, 1, 0)
])
def test_add(num1, num2, expected):
    print("Testing add function")
    assert add(num1, num2)

def test_subtract():
    print("Testing subtract function")
    assert subtract(5, 3) == 2

def test_multiply():
    print("Testing multiply function")
    assert multiply(5, 3) == 15  

def test_divide():
    print("Testing divide function")
    assert divide(6, 3) == 2
    try:
        divide(5, 0)
    except ValueError as e:
        assert str(e) == "Cannot divide by zero"

def test_bank_account(zero_bank_account):
    print("Testing BankAccount class")
    assert zero_bank_account.get_balance() == 0

    zero_bank_account.deposit(50)
    assert zero_bank_account.get_balance() == 50

    # try:
    #     zero_bank_account.deposit(-20)
    # except ValueError as e:
    #     assert str(e) == "Deposit amount must be positive"

    zero_bank_account.withdraw(30)
    assert zero_bank_account.get_balance() == 20

    # try:
    #     zero_bank_account.withdraw(200)
    # except ValueError as e:
    #     assert str(e) == "Insufficient funds"

    # try:
    #     zero_bank_account.withdraw(-10)
    # except ValueError as e:
    #     assert str(e) == "Withdrawal amount must be positive"

    zero_bank_account.collect_interest(0.1)
    assert zero_bank_account.get_balance() == 22.0

    # try:
    #     zero_bank_account.collect_interest(-0.05)
    # except ValueError as e:
    #     assert str(e) == "Interest rate must be non-negative"

@pytest.mark.parametrize("deposited, withdrew, expected", [
    (100, 50, 50),
    (200, 150, 50),
    (300, 100, 200)
])
def test_bank_transaction(zero_bank_account, deposited, withdrew, expected):
    zero_bank_account.deposit(deposited)
    zero_bank_account.withdraw(withdrew)
    assert zero_bank_account.get_balance() == expected

def test_insufficient_funds(bank_account):
    with pytest.raises(InsufficientFunds):
        bank_account.withdraw(200)