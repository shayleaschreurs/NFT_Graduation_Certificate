# TODO: write streamlit app
import os
import json
from web3 import Web3
from pathlib import Path
from dotenv import load_dotenv
import streamlit as st
### ganache
load_dotenv()

w3 = Web3(Web3.HTTPProvider(os.getenv("WEB3_PROVIDER_URI")))


def load_contract():
    with open(Path('./contracts/compiled/bootcampcertificate_abi.json')) as f:
        certificate_abi = json.load(f)
        
    contract_address = os.getenv('SMART_CONTRACT_ADDRESS')
    
    contract = w3.eth.contract(
        address=contract_address,
        abi=certificate_abi
    )
    
    return contract

contract = load_contract()


### pinata helper functions
def pin_certificate(certificate_name, certificate_file):
    # Pin the file to IPFS with Pinata
    ipfs_file_hash = pin_file_to_ipfs(certificate_file.getvalue())

    # Build a token metadata file for the certificate
    token_json = {
        "name": certificate_name,
        "image": ipfs_file_hash
    }
    json_data = convert_data_to_json(token_json)

    # Pin the json to IPFS with Pinata
    json_ipfs_hash = pin_json_to_ipfs(json_data)

    return json_ipfs_hash, token_json


st.title("Bootcamp Certificate Minter")
st.write("Choose an account to get started")
accounts = w3.eth.accounts
address = st.selectbox("Select Account", options=accounts)
st.markdown("---")

### ADD CERTIFICATE

st.markdown("## Mint Bootcamp Certificate")
student_name = st.text_input("Enter full name")
completion_date = st.text_input("Enter the completion date")

# Use the Streamlit `file_uploader` function create the list of digital image file types(jpg, jpeg, or png) that will be uploaded to Pinata.
file = st.file_uploader("Upload Certificate", type=["jpg", "jpeg", "png"])

if st.button("Register Certificate"):
    # Use the `pin_certificate` helper function to pin the file to IPFS
    certificate_ipfs_hash, token_json = pin_certificate(student_name, file)

    certificate_uri = f"ipfs://{certificate_ipfs_hash}"

    tx_hash = contract.functions.registerCertificate(
        address,
        student_name,
        completion_date,
        int(initial_appraisal_value),
        certificate_uri,
        token_json['image']
    ).transact({'from': address, 'gas': 1000000})
    receipt = w3.eth.waitForTransactionReceipt(tx_hash)
    st.write("Transaction receipt mined:")
    st.write(dict(receipt))
    st.write("You can view the pinned metadata file with the following IPFS Gateway Link")
    st.markdown(f"[Certificate IPFS Gateway Link](https://ipfs.io/ipfs/{certificate_ipfs_hash})")
    st.markdown(f"[Certificate IPFS Image Link](https://ipfs.io/ipfs/{token_json['image']})")

st.markdown("---")
