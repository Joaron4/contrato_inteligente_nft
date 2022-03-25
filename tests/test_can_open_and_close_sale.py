from scripts.helpful_scripts import get_account


from scripts.deploy import deploy_and_create
from brownie import accounts, exceptions
import pytest


def test_can_close_sale():
    # Arange
    account = get_account()
    compra_venta = deploy_and_create()
    # act
    compra_venta.endSale({"from": account})
    # assert
    assert compra_venta.saleState() != 0


def test_only_owner_can_end():
    bad_actor = accounts.add()
    compra_venta = deploy_and_create()

    with pytest.raises(
        exceptions.VirtualMachineError
    ):  # decirle que si hay un revert pasa el test
        compra_venta.endSale({"from": bad_actor})


def test_can_open_sale():
    # Arange
    account = get_account()
    compra_venta = deploy_and_create()
    # act
    tx = compra_venta.endSale({"from": account})
    closed = compra_venta.saleState()
    tx.wait(1)
    tx2 = compra_venta.startSale({"from": account})
    tx2.wait(1)
    open = compra_venta.saleState()
    # assert
    assert open != closed


def test_only_owner_can_start():
    bad_actor = accounts.add()
    compra_venta = deploy_and_create()

    with pytest.raises(
        exceptions.VirtualMachineError
    ):  # decirle que si hay un revert pasa el test
        compra_venta.startSale({"from": bad_actor})


def test_cannot_start_if_target():  # Si apsa el test epro no funciona
    account = get_account()
    compra_venta = deploy_and_create()
    for i in range(21):
        tx = compra_venta.createCollectible({"from": account})
        tx.wait(1)
    with pytest.raises(exceptions.VirtualMachineError):  # verificar error
        compra_venta.startSale({"from": account})
