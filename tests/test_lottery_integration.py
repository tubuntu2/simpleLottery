from brownie import Lottery, accounts, config, network
from scripts.deploy_lottery import deploy_lottery
from web3 import Web3
import pytest,time
from scripts.helpful_scripts import LOCAL_BLOCKCHAIN_ENVIRONMENTS, fund_with_link, get_account, get_contract

def test_can_pick_winner():
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS: #remove not since we deploy to rinkeby
        pytest.skip()
    #Arrange
    lottery = deploy_lottery()
    account = get_account()
    lottery.startLottery({"from": account})
    #Act
    lottery.enter({"from":account, "value": lottery.getEntranceFee()})
    lottery.enter({"from":account, "value": lottery.getEntranceFee()})
    print (f"{lottery.players(0)} is first player")
    print (f"{lottery.players(1)} is second player")
    fund_with_link(lottery)
    lottery.endLottery({"from":account})
    request_id = transaction.events["RequestedRandomness"]["requestId"]
    STATIC_RNG = 777
    #spooking chainlink node and sending back an RN to the contract for dev local chain testing
    get_contract ("vrf_coordinator").callBackWithRandomness(
        request_id, STATIC_RNG, lottery.address, {"from": account}
    )
    #time.sleep(60)
    assert lottery.recentWinner() == account
    assert lottery.balance == 0