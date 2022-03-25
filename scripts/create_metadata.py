from colors.bg import backgrounds
from brownie import CompraVentaNft, network
from metadata.sample_metadata import metadata_template
from pathlib import Path
import requests
import datetime
import time
import json
import random

# ------------------------------------IMAGEN------------------------------
image_paz = (
    "https://gateway.pinata.cloud/ipfs/QmWRYFWcnvKrXEtG2BuoRKp7bjAd3V9BcofpEvmNQcLuuA"
)
date_time = time.mktime(datetime.datetime.now().timetuple())


def main():
    compra_venta = CompraVentaNft[-1]
    print(compra_venta.address)  # está bien la dirección
    # para iterar por todos los coleccionables
    number_of_advanced_collectible = compra_venta.tokenCounter()
    print(f"you've created {number_of_advanced_collectible} collectibles")
    # token id = 1,2,3,4....

    for token_id in range(number_of_advanced_collectible):
        # esto devuelve un integer 0,1,2 = razas perros
        metadata_file_name = (
            f"./metadata/{network.show_active()}/{token_id}-lesiones.json"
        )
        # importar el template de los metadatos
        collectible_metadata = metadata_template
        print(metadata_file_name)
        if Path(metadata_file_name).exists():
            print(f"{metadata_file_name} already exist")
        else:
            print(f"----------CREATING:{metadata_file_name}----------------------\n\n")
            print(f"Creating Metadata file: {metadata_file_name}")
            # ---------------------NOMBRE----------------------------
            collectible_metadata["name"] = "Paz " + str(token_id + 1) + "/20"
            # --------------------IMAGEN------------------------------
            collectible_metadata["image"] = image_paz
            # --------------------BACKGROUND--------------------------
            collectible_metadata["background_color"] = random.choice(backgrounds)
            # ---------------------TIME-----------------
            print(date_time)
            collectible_metadata["attributes"][1]["value"] = int(date_time)

            with open(metadata_file_name, "w") as file:
                json.dump(collectible_metadata, file)
            upload_to_ipfs(metadata_file_name)


def upload_to_ipfs(filepath):
    with Path(filepath).open("rb") as fp:  # rb abrir en binario
        file_binary = fp.read()
        ##subir imagen con command line ipfs
        ipfs_url = "http://127.0.0.1:5001"
        endpoint = "/api/v0/add"
        response = requests.post(ipfs_url + endpoint, files={"file": file_binary})
        print(response)
        ipfs_hash = response.json()["Hash"]
        filename = filepath.split("/")[-1:][0]
        file_uri = f"https://ipfs.io/ipfs/{ipfs_hash}?filename={filename}"
        print(file_uri)
        with open("./metadata/ipfs_url.txt", "a+", encoding="utf-8") as f:
            f.write(file_uri)
        # https://ipfs.io/ipfs/QmUPjADFGEKmfohdTaNcWhp7VGk26h5jXDA7v3VtTnTLcW?filename=st-bernard.png
        return file_uri
