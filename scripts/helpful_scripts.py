from brownie import accounts, config, network, MockV3Aggregator, Contract
from web3 import Web3

forked_local_enviroments = ["mainnet-fork,mainnet-fork-dev"]
local_blockchain_enviroments = ["development", "ganache-local"]

decimals = 8
start_price = 3 * 10**8  # eth price

OPENSEA_URL = "https://testnets.opensea.io/assets/{}/{}"

# ----------------------Obtener cuentas----------------------


def get_account(index=None, id=None):
    if index:
        return accounts[index]
    if id:
        return accounts.load(id)

    if (
        network.show_active() in local_blockchain_enviroments
        or network.show_active() in forked_local_enviroments
    ):
        return accounts[0]

    return accounts.add(config["wallets"]["from_key"])


# ------------------------MOCKS--------------------------------
contract_to_mock = {"eth_usd_price_feed": MockV3Aggregator}


def get_contract(contract_name):

    contract_type = contract_to_mock[contract_name]
    if network.show_active() in local_blockchain_enviroments:
        if len(contract_type) <= 0:  # si el mock es igual o menor a 0 cree un mock
            deploy_mocks()
        contract = contract_type[-1]
    else:
        contract_address = config["networks"][network.show_active()][contract_name]
        contract = Contract.from_abi(
            contract_type._name, contract_address, contract_type.abi
        )
    return contract


def deploy_mocks():

    print(f"The active network is {network.show_active()}")
    print("---------------Deploying mocks-----------------")
    account = get_account()
    print("Deploying Mock LinkToken...")
    if len(MockV3Aggregator) <= 0:  # los contratos son arrays con los ctos desplegados
        eth_toUsd = MockV3Aggregator.deploy(
            decimals, Web3.toWei(start_price, "ether"), {"from": get_account()}
        )  # valores cto (uint8 _decimals, int256 _initialAnswer)
    print(f"Link Token deployed to {eth_toUsd.address}")

    print("------------All done!-------------")
