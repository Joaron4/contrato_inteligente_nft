from scripts.helpful_scripts import get_account
from scripts.deploy import deploy_and_create
from brownie import accounts, exceptions
import pytest


def test_lower_payment():  # debe fallar
    bad_actor = accounts.add()
    compra_venta = deploy_and_create()

    with pytest.raises(
        exceptions.VirtualMachineError
    ):  # decirle que si hay un revert pasa el test
        compra_venta.createCollectible({"from": bad_actor, "value": 100})


def test_must_be_open():  # este sí pasa
    # Arange
    account = get_account()
    compra_venta = deploy_and_create()
    # Act
    tx = compra_venta.endSale({"from": account})
    tx.wait(1)

    # Assert
    with pytest.raises(exceptions.VirtualMachineError):
        compra_venta.createCollectible({"from": account})
