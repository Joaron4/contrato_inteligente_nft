from brownie import CompraVentaNft
from scripts.helpful_scripts import get_account
from web3 import Web3


def main():
    account = get_account()  # id="account-semillero2"
    compra_venta = CompraVentaNft[-1]
    value = compra_venta.getPrice() + 100
    creation_tx = compra_venta.createCollectible({"from": account, "value": value})
    creation_tx.wait(1)
    print("--------------------NFT creado-----------------")
