from scripts.helpful_scripts import get_account, local_blockchain_enviroments
from scripts.deploy import deploy_and_create
from brownie import network, accounts, exceptions
import pytest


def test_can_change_price():
    # Arange
    account = get_account()
    compra_venta = deploy_and_create()
    precio_inicial = compra_venta.getPrice()
    # Arange
    entrance_fee = 10
    tx = compra_venta.updatePrice({"value": entrance_fee})  # 10 dólares
    tx.wait(1)
    precio_final = compra_venta.getPrice()
    # Assert
    print(precio_inicial)
    assert precio_inicial != precio_final
