import requests

def shorten_url(long_url):
    """
    Sends a long URL to the is.gd API and returns the shortened version.
    """
    base_url = "https://is.gd/create.php"
    
    # Define the request parameters required by the API
    payload = {
        "format": "json",
        "url": long_url
    }
    
    try:
        print("🔗 Contacting shortening API stream...")
        # Send a GET request to the API
        response = requests.get(base_url, params=payload)
        
        # Check if the network request was successful (HTTP Status Code 200)
        if response.status_code == 200:
            data = response.json()
            
            # If the API successfully shrunk the link
            if "shorturl" in data:
                return data["shorturl"]
            elif "errormessage" in data:
                return f"❌ API Error: {data['errormessage']}"
        else:
            return f"❌ Server Connection Error: HTTP {response.status_code}"
            
    except requests.exceptions.RequestException as e:
        return f"❌ Network Connection Failed: {e}"

def main():
    print("✂️ Welcome to the CLI URL Shortener Engine ✂️")
    print("-" * 45)
    
    # Get user input link
    long_url = input("Enter or paste your long URL link here:\n➔ ").strip()
    
    if not long_url:
        print("❌ Error: You must enter a valid URL link string.")
        return
        
    # Run the shortener logic
    short_url = shorten_url(long_url)
    
    print("-" * 45)
    print(f"🎉 Result: {short_url}")
    print("-" * 45)

if __name__ == "__main__":
    main()
  
