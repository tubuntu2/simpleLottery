from brownie import Lottery, accounts, config, network, RandomNumberConsumer
from scripts.deploy_lottery import deploy_lottery
from web3 import Web3
import pytest,time
from scripts.helpful_scripts import LOCAL_BLOCKCHAIN_ENVIRONMENTS, fund_with_link, get_account, get_contract

def test_can_pick_winner():
    account =get_account()
    random = RandomNumberConsumer.deploy(
        {"from": account},
        publish_source=config["networks"][network.show_active()].get("verify",False)
        )
    tx = fund_with_link(random.address)
    tx.wait(1)
    print(f"{random.randomResult()} is first random")
    random.getRandomNumber()
    time.sleep(60)
    print(f"{random.randomResult()} is second random")

def main():
    test_can_pick_winner()
