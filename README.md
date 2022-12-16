# U of M Fintech Bootcamp Certificate Minter
___

## Overview
The project is a certificate minter that allows institutions to issue and verify digital certificates using blockchain technology. The minter is built using a combination of Python, Solidity, and Streamlit.

Python is what we used to create the backend logic and handle interactions with the blockchain.

Solidity is what we used to create the smart contract that manages the issuance and verification of the digital certificates.

Streamlit is the framework we used to create the user interface for the minter, allowing users to easily interact with the system.

Overall, the project combines the power of blockchain technology and modern programming tools to create a secure and efficient way for institutions to issue and verify digital certificates.



## Local setup / installation
### Initial Installs
* Install Ganache and have it running locally. https://trufflesuite.com/ganache/
* If you don't have Streamlit installed yet, follow the steps provided on the Streamlit installation page. https://docs.streamlit.io/library/get-started/installation#install-streamlit-on-macoslinux
* Install Python dotenv. To do so, navigate to your terminal or gitbash and type 'pip install python-dotenv'

### Additional Setup
* Register with Pinata to obtain developer API keys. https://www.pinata.cloud/  
    -Navigate to the Developers tab after logging into Pinata to create a new key.  
    -Make sure to save your new keys to a secure place on your local computer.
    
### Download and Launch
* Download the project file named project_3 to your desktop
* Add a .env file that follows conventions in SAMPLE.env (your .env file will be gitignored)  
    -Input your API Key from Pinata into the PINATA_API_KEY variable  
    -Input your API Secret from Pinata into the PINATA_SECRET_API_KEY variable  
    -Input the Ganache URI http://127.0.0.1:7545 into the WEB3_PROVIDER_URI variable  
    -Input a public address from your Ganache into the SMART_CONTRACT_ADDRESS variable
* Navigate to the terminal or gitbash instance in which you installed Streamlit and Python dotenv
* In terminal or gitbash navigate to the project_3 file. To do so follow these steps;  
    -type 'cd desktop' then press enter  
    -type 'cd project_3' then press enter
* Use streamlit to run the app.py file within the project_3 folder. To do so type 'streamlit run app.py'. This will open a tab in your web browser to the certificate minter.

### Using the Minter
##### Navigating As A Student
* Use the 'Select Account' dropdown to choose which eth address you want to mint the certifcate to
* Enter your first and last name in the 'Enter full name' textbox
* The date of completion will automatically be filled out for you
* Upload a headshot from your computer. Make sure it is a vertical portrait photo to ensure higher quality.
* Press the 'Register Certificate' button and your certificate will be minted to your ETH address with your name and photo attached! A preview will pop up on your screen along with the transaction receipt, and IPFS links. 

##### Navigating As An Instructor
* Create a .csv file with 3 columns - Student full name, completion date, and photo url (optional)
* Navigate to the Batch(Teacher Mode) tab
* Click the 'Browse files' button and select your .csv file
* Press 'Register Certificates' and each certificate will be minted at once