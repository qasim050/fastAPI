import pytest
from calc import Cum, BankAccount

@pytest.fixture
def zero_bank_account():
    return BankAccount()

@pytest.fixture
def bank_account():
    return BankAccount(50)

@pytest.mark.parametrize("num1 , num2 , resulte",[
    (3,4,7),
    (5,4,9),
    (6,4,10)
])
def test_clac(num1,num2,resulte):
    
    assert Cum(num1,num2) == resulte
    
def test_bank(bank_account):
    assert bank_account.balance == 50

def test_bank_default_amount(zero_bank_account):
    assert zero_bank_account.balance == 0

def test_withdraw(bank_account):
    bank_account.withdraw(20)
    assert bank_account.balance == 30

def test_deposit(bank_account):
    bank_account.deposit(30)
    assert bank_account.balance == 80
    
def test_interest(bank_account):
    bank_account.collect_interest()
    assert round(bank_account.balance) == 55
    
@pytest.mark.parametrize("deposit , withdraw , resulte",[
    (100,20,80),
    (500,200,300),
    (200,100,100)
])
def test_bank_transection(zero_bank_account,deposit,withdraw,resulte):
    zero_bank_account.deposit(deposit)
    zero_bank_account.withdraw(withdraw)

    assert zero_bank_account.balance == resulte
    
def test_insufficient_funds(bank_account):
    with pytest.raises(Exception):
        bank_account.withdraw(200)