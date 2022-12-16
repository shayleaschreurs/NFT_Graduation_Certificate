import os
import json
from web3 import Web3
from pathlib import Path
from dotenv import load_dotenv
import streamlit as st
import io
import pandas as pd
import urllib.request

from pinata import pin_file_to_ipfs, pin_json_to_ipfs, convert_data_to_json

# cert editing imports
from PIL import Image, ImageDraw, ImageFont

# ganache
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


# pinata helper functions
def pin_certificate(certificate_name, certificate_file):
    # convert to IO
    img_byte_arr = io.BytesIO()
    certificate_file.save(img_byte_arr, format='PNG')

    # Pin the file to IPFS with Pinata
    ipfs_file_hash = pin_file_to_ipfs(img_byte_arr.getvalue())

    # Build a token metadata file for the certificate
    token_json = {
        "name": certificate_name,
        "image": ipfs_file_hash
    }
    json_data = convert_data_to_json(token_json)

    # Pin the json to IPFS with Pinata
    json_ipfs_hash = pin_json_to_ipfs(json_data)

    return json_ipfs_hash, token_json

# function for generating a certificate png


def generate_individual_certificate_png(name, completion, img):
    template = Image.open('template/certificate-template-blank.png')
    pic = Image.open(img).resize((170, 170), Image.ANTIALIAS)
    template.paste(pic, (311, 452, 481, 622))
    draw = ImageDraw.Draw(template)
    draw.text((512, 505), name, font=name_font, fill='black')
    draw.text((512, 549), completion, font=date_font, fill='#7C121C')
    return template


def generate_batch_certificate_png(name, completion):
    template = Image.open('template/certificate-template-batch.png')
    draw = ImageDraw.Draw(template)
    canvasWidth = template.size[0]
    nameWidth = draw.textsize(name, font=name_font)[0]
    dateWidth = draw.textsize(completion, font=date_font)[0]
    draw.text(((canvasWidth - nameWidth)/2, 505),
              name, font=name_font, fill='black')
    draw.text(((canvasWidth - dateWidth)/2, 549),
              completion, font=date_font, fill='#7C121C')
    return template


def generate_batch_image_certificate_png(name, completion, img):
    template = Image.open('template/certificate-template-blank.png')
    pic = Image.open(img).resize((170, 170), Image.ANTIALIAS)
    template.paste(pic, (311, 452, 481, 622))
    draw = ImageDraw.Draw(template)
    draw.text((512, 505), name, font=name_font, fill='black')
    draw.text((512, 549), completion, font=date_font, fill='#7C121C')
    return template


# Streamlit App UI
col1, col2, col3 = st.columns([1, 3, 1])
with col1:
    st.write("")
with col2:
    st.image("images/Logo.png")
with col3:
    st.write("")


st.title("Bootcamp Certificate Minter")
st.write("Choose an account to get started")
accounts = w3.eth.accounts
address = st.selectbox("Select Account", options=accounts)
st.markdown("---")

# ADD CERTIFICATE
st.markdown("## Mint Bootcamp Certificate")

tab1, tab2 = st.tabs(["Individual", "Batch (Teacher Mode)"])

# INDIVIDUAL
with tab1:
    student_name = st.text_input("Enter full name")
    completion_date = st.text_input(
        "Enter the completion date", value="December 2022")

    # Use the Streamlit `file_uploader` function create the list of digital image file types(jpg, jpeg, or png) that will be uploaded to Pinata.
    file = st.file_uploader("Upload Certificate", type=["jpg", "jpeg", "png"])

    name_font = ImageFont.truetype(
        'template_auto_generator/Open_Sans/OpenSans-Italic-VariableFont_wdth,wght.ttf', size=30)

    date_font = ImageFont.truetype(
        'template_auto_generator/Open_Sans/OpenSans-Medium.ttf', size=25)

    if st.button("Register Certificate"):
        certificate_img = generate_individual_certificate_png(
            student_name, completion_date, file)
        # Use the `pin_certificate` helper function to pin the file to IPFS
        certificate_ipfs_hash, token_json = pin_certificate(
            student_name, certificate_img)

        certificate_uri = f"ipfs://{certificate_ipfs_hash}"

        tx_hash = contract.functions.registerCertificate(
            address,
            student_name,
            completion_date,
            certificate_uri,
            token_json['image']
        ).transact({'from': address, 'gas': 1000000})
        receipt = w3.eth.waitForTransactionReceipt(tx_hash)
        st.balloons()
        st.markdown("# CONGRATULATIONS!")
        st.markdown('##### You have successfully registered your certificate!')
        st.image(certificate_img)
        st.write("Transaction receipt mined:")
        st.write(dict(receipt))
        st.write(
            "You can view the pinned metadata file with the following IPFS Gateway Link")
        st.markdown(
            f"[Certificate IPFS Gateway Link](https://ipfs.io/ipfs/{certificate_ipfs_hash})")
        st.markdown(
            f"[Certificate IPFS Image Link](https://ipfs.io/ipfs/{token_json['image']})")


# BATCH
with tab2:
    st.write(
        'Upload a CSV file with the following columns (for each student):')
    st.write('- name')
    st.write('- completion_date')
    st.write('- certificate_image_url (optional)')
    file = st.file_uploader("Upload CSV", type=["csv"])

    if st.button("Register Certificates"):
        st.write("Uploading...")
        # read csv
        df = pd.read_csv(file).fillna(value='empty')
        # iterate through each row
        for index, row in df.iterrows():
            certificate_img = None
            temp_img = None
            # generate certificate
            if row['certificate_image_url'] != 'empty':
                try:
                    temp_img = urllib.request.urlretrieve(
                        row["certificate_image_url"], 'temp_img.png')
                    certificate_img = generate_individual_certificate_png(
                        row['name'], row['completion_date'], temp_img[0])
                except:
                    temp_img = './template_auto_generator/placeholder.png'
                    certificate_img = generate_individual_certificate_png(
                        row['name'], row['completion_date'], temp_img)

            else:
                certificate_img = generate_batch_certificate_png(
                    row['name'], row['completion_date'])

            # pin certificate
            certificate_ipfs_hash, token_json = pin_certificate(
                row['name'], certificate_img)
            certificate_uri = f"ipfs://{certificate_ipfs_hash}"
            # mint certificate
            tx_hash = contract.functions.registerCertificate(
                address,
                row['name'],
                row['completion_date'],
                certificate_uri,
                token_json['image']
            ).transact({'from': address, 'gas': 1000000})
            receipt = w3.eth.waitForTransactionReceipt(tx_hash)
            st.balloons()
            st.markdown(f"# CONGRATULATIONS! {row['name']}")
            st.markdown(
                '##### You have successfully registered your certificate!')
            st.image(certificate_img)
            st.write("Transaction receipt mined:")
            st.write(dict(receipt))
            st.write(
                "You can view the pinned metadata file with the following IPFS Gateway Link")
            st.markdown(
                f"[Certificate IPFS Gateway Link](https://ipfs.io/ipfs/{certificate_ipfs_hash})")
            st.markdown(
                f"[Certificate IPFS Image Link](https://ipfs.io/ipfs/{token_json['image']})")
st.markdown("---")
