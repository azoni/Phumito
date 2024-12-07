import requests
import time
import json

# OpenSea API Key
headers = {
    "accept": "application/json",
    "x-api-key": "7638682ff88840e8bcf9e522ae8854b0"
}

# Base URLs
collection_url = "https://api.opensea.io/api/v2/collections/pudgypenguins"
nft_url_template = "https://api.opensea.io/api/v2/chain/ethereum/contract/0xbd3531da5cf5857e7cfaa92426877b022e612cf8/nfts/{token_id}"

# Rate Limiter Parameters
RATE_LIMIT_SECONDS = 1  # Time to wait between requests
MAX_RETRIES = 3         # Max retries for failed requests

# File to store results
output_file = "nft_traits.txt"

def fetch_with_retries(url, headers, retries=MAX_RETRIES):
    """Fetch data from API with retry logic."""
    for attempt in range(retries):
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()  # Raise exception for HTTP errors
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching {url}: {e}")
            if attempt < retries - 1:
                print(f"Retrying... ({attempt + 1}/{retries})")
                time.sleep(2 ** attempt)  # Exponential backoff
            else:
                print("Max retries reached. Skipping.")
                return None

def main():
    # Fetch total supply
    print("Fetching total supply...")
    collection_data = fetch_with_retries(collection_url, headers)
    if not collection_data:
        print("Failed to fetch collection data. Exiting.")
        return
    
    total_supply = collection_data.get('total_supply')
    if not total_supply:
        print("Total supply not found in response. Exiting.")
        return
    
    print(f"Total supply: {total_supply}")

    # Open file for writing
    with open(output_file, "w") as file:
        for token_id in range(1, total_supply + 1):  # Iterate through token IDs
            print(f"Fetching NFT traits for Token ID: {token_id}")
            nft_url = nft_url_template.format(token_id=token_id)
            
            nft_data = fetch_with_retries(nft_url, headers)
            if not nft_data:
                print(f"Skipping Token ID {token_id} due to repeated failures.")
                continue

            traits = nft_data.get('nft', {}).get('traits', [])
            print(f"Traits for Token ID {token_id}: {traits}")

            # Write response to file
            file.write(json.dumps({
                "token_id": token_id,
                "traits": traits
            }) + "\n")
            
            # Rate limiting
            time.sleep(RATE_LIMIT_SECONDS)

    print(f"Trait data written to {output_file}.")

if __name__ == "__main__":
    main()
