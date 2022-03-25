from brownie import CompraVentaNft, config, network
from scripts.helpful_scripts import get_account, get_contract


def deploy_and_create():
    account = get_account()  # id="account-semillero2"
    compra_venta = CompraVentaNft.deploy(
        get_contract("eth_usd_price_feed").address,
        {"from": account},
        publish_source=config["networks"][network.show_active()].get("verify", False),
    )
    value = (
        compra_venta.getPrice() + 100
    )  # se envía el valor mínimo de eths, más 100(por si acaso)
    creating_tx = compra_venta.createCollectible({"from": account, "value": value})
    creating_tx.wait(1)
    print(f"Awesome, you can view your NFT at {compra_venta.address}")
    return compra_venta


def main():
    deploy_and_create()
