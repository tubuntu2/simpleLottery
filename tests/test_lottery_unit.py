from brownie import Lottery, accounts, config, network
from scripts.deploy_lottery import deploy_lottery
from web3 import Web3
import pytest
from scripts.helpful_scripts import LOCAL_BLOCKCHAIN_ENVIRONMENTS, fund_with_link, get_account, get_contract
def test_get_entrance_fee():
    # account = accounts[0]
    # lottery = Lottery.deploy(
    #     config["networks"][network.show_active()]["eth_usd_price_feed"],
    #     {"from": account},
    #     )

    # assert lottery.getEntranceFee() > Web3.toWei (0.010, "ether")
    # assert lottery.getEntranceFee() < Web3.toWei (0.013, "ether") cmd+/ to comment or uncomment multiple lines
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()
    #Arrange
    lottery = deploy_lottery()
    expected_entrance_fee = Web3.toWei(0.025,"ether") #2000/1 = 50/x but current 4272/1 = 50/x 0.012
    entrance_fee = lottery.getEntranceFee() #for 2,000 eth/usd
    #Assert
    assert expected_entrance_fee == entrance_fee

def test_can_start_and_enter_lottery():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()
    #Arrange
    lottery = deploy_lottery()
    account = get_account()
    lottery.startLottery({"from": account})
    #Act
    lottery.enter({"from":account, "value":lottery.getEntranceFee()})
    #Assert
    assert lottery.players(0) == account

def test_can_pick_winner_correctly():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()
    #Arrange
    lottery = deploy_lottery()
    account = get_account()
    lottery.startLottery({"from": account})
    #Act
    lottery.enter({"from":account, "value":lottery.getEntranceFee()})
    lottery.enter({"from":get_account(index=1), "value":lottery.getEntranceFee()})
    lottery.enter({"from":get_account(index=2), "value":lottery.getEntranceFee()})
    fund_with_link(lottery)
    transaction = lottery.endLottery({"from": account})
    request_id = transaction.events["RequestedRandomness"]["requestId"]
    STATIC_RNG = 777
    #spooking chainlink node and sending back an RN to the contract for dev local chain testing
    get_contract ("vrf_coordinator").callBackWithRandomness(
        request_id, STATIC_RNG, lottery.address, {"from": account}
    )
    starting_balance_of_account = account.balance()
    balance_of_lottery = lottery.balance()
    #777%3=0 so that first acount is the winner
    assert lottery.recentWinner() == account
    assert lottery.balance() == 0
    assert account.balance() == starting_balance_of_account + balance_of_lottery

    

    

         