import requests
import zipfile
import io
import certifi

def update_certifi():
    # URL to download the Dell certificates zip file
    url = "https://pki.dell.com//Dell%20Technologies%20PKI%202018%20B64_PEM.zip"
    print("Downloading Dell certificates zip from:", url)
    response = requests.get(url)
    # Use raise_for_status() for concise error checking
    response.raise_for_status()
    print("Downloaded certificate zip, size:", len(response.content), "bytes")

    # Determine the location of the certifi bundle
    cert_path = certifi.where()
    print("Certifi bundle path:", cert_path)

    # Define the names of the certificates within the zip file
    dell_root_cert_name = "Dell Technologies Root Certificate Authority 2018.pem"
    dell_issuing_cert_name = "Dell Technologies Issuing CA 101_new.pem"

    # Append the certificates directly from the zip archive in memory.
    print("Appending Dell certificates to certifi bundle...")
    try:
        with zipfile.ZipFile(io.BytesIO(response.content)) as z:
            # Read certificate contents directly from the zip file in memory
            # Ensure decoding from bytes to string (assuming UTF-8)
            root_cert_content = z.read(dell_root_cert_name).decode('utf-8')
            issuing_cert_content = z.read(dell_issuing_cert_name).decode('utf-8')

            # Append the certificates to the certifi bundle
            # (Make sure you have backup of certifi bundle if needed.)
            with open(cert_path, "a") as bundle:
                bundle.write("\n")
                bundle.write(root_cert_content)
                bundle.write("\n") # Ensure newline after first cert
                bundle.write(issuing_cert_content)
                bundle.write("\n") # Ensure newline after second cert

        print("Dell certificates successfully added to certifi bundle.")

    except KeyError as e:
        # Handle case where expected certificate file is not in the zip
        print(f"Error: Certificate file '{e}' not found in the zip archive.")
    except Exception as e:
        # Handle other potential errors during processing
        print(f"An error occurred during certificate appending: {e}")


update_certifi()