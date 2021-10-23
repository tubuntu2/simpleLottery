from brownie import Lottery,config,network
from scripts.helpful_scripts import get_account,get_contract,fund_with_link
import time

def deploy_lottery():
    account = get_account()
    #get_contract() chooses the online net contract or the mock concracts based on network used(eg.Rinkeby or Local Ganache)
    lottery = Lottery.deploy(
        get_contract("eth_usd_price_feed").address,
        get_contract("vrf_coordinator").address,
        get_contract("link_token").address,
        config["networks"][network.show_active()]["fee"],
        config["networks"][network.show_active()]["keyhash"],
        {"from": account},
        publish_source=config["networks"][network.show_active()].get("verify",False)
        )
    print ("Deployed lottery")
    return lottery

def start_lottery():
    account = get_account()
    lottery = Lottery[-1]
    starting_tx = lottery.startLottery({"from": account})
    starting_tx.wait(1)
    print("Lottery started")

def enter_lottery():
    account=get_account()
    lottery = Lottery[-1]
    value = lottery.getEntranceFee()+100000000 #extra to make sure it passes
    tx = lottery.enter({"from": account, "value" : value})
    tx.wait(1)
    print(f"{account.address}You entered the lottery")

def end_lottery():
    account = get_account()
    lottery = Lottery[-1]
    #fund contract then end lottery
    tx = fund_with_link(lottery.address)
    tx.wait(1)
    ending_transaction = lottery.endLottery({"from": account}) #endLottery calls fulfillRandomness which gets randome number and selects winner and pays them 
    ending_transaction.wait(1)
    time.sleep(180) #wait for callback from Chainlink node, also, import time for this
    print(f"{lottery.recentWinner()} is the new winner!")



def main():
    deploy_lottery()
    start_lottery()
    enter_lottery()
    end_lottery()