from brownie import network, CompraVentaNft
from scripts.helpful_scripts import OPENSEA_URL, get_account

metadata = (
    open("./metadata/ipfs_url.txt", "r", encoding="utf-8")
    .read()
    .replace("https:", "####https:")
    .split("####")
)[1:]


def main():
    print(f"Working on {network.show_active()}")
    compra_venta = CompraVentaNft[-1]
    # --------------contar nfts----------------------
    number_of_collectibles = compra_venta.tokenCounter()  # número tokens
    print(f"You have {number_of_collectibles} tokenIds")
    for token_id in range(number_of_collectibles):
        print(metadata[token_id])
        if not compra_venta.tokenURI(token_id).startswith(
            "https://"
        ):  # si el token uri no empieza con https poaila
            print(f"Setting tokenURI of {token_id}")
            set_tokenURI(token_id, compra_venta, metadata[token_id])


def set_tokenURI(token_id, nft_contract, tokenURI):
    account = get_account()
    tx = nft_contract.setTokenURI(token_id, tokenURI, {"from": account})
    tx.wait(1)
    print(
        f"Awesome! You can view your NFT at {OPENSEA_URL.format(nft_contract.address, token_id)}"
    )
    print("Please wait up to 20 minutes, and hit the refresh metadata button")
