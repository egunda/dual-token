#Python3 script to generate sha256 tokens
import base64
import datetime
import hashlib
import hmac
import requests

def sign_token(url_prefix: str, base64_key: bytes, algo: str, expiration_time: datetime.datetime = None) -> bytes:
    """Gets the Signed URL Suffix string for the Media CDN' Short token URL requests.
    Args:
        url_prefix: URL prefix to sign as a string.
        base64_key: Secret key as a base64 encoded string.
        algo: Algorithm can be either `SHA1` or `SHA256`.
        expiration_time: Expiration time as a UTC datetime object.
    Returns:
        Returns the Signed URL appended with the query parameters based on the
        specified URL prefix and configuration.
    """
    output = b"URLPrefix=" + base64.standard_b64encode(url_prefix.encode("utf-8"))

    if not expiration_time:
        expiration_time = datetime.datetime.now() + datetime.timedelta(hours=1)
    epoch_duration = int(
        (expiration_time - datetime.datetime.utcfromtimestamp(0)).total_seconds()
    )
    output += b"~Expires=" + str(epoch_duration).encode("utf-8")
    key = base64.standard_b64decode(base64_key)
    algo = algo.lower()
    if algo == "sha1":
        signature = hmac.new(key, output, digestmod=hashlib.sha1).hexdigest()
    elif algo == "sha256":
        signature = hmac.new(key, output, digestmod=hashlib.sha256).hexdigest()
    else:
        raise ValueError("User input(`algo`) can be either `sha1` or `sha256`")
    output += b"~hmac=" + signature.encode("utf-8")
    return output

# Ask user for inputs
up = input("Enter the URL prefix (e.g., https://vod.cdntest.in/tearsofsteel/): ")
bk = input("Enter the base64 key (e.g., LGRWJKHKHKK76S7S7H7R8KHJHKJHJHGG1MuY=): ")

expiration_seconds_input = input("Enter expiration time in seconds (default is 60): ")
expiration_seconds = int(expiration_seconds_input) if expiration_seconds_input else 60

url_input = input("Enter the complete URL (e.g., https://vod.cdntest.in/tearsofsteel/manifest.m3u8): ")

date_time_str = str(datetime.datetime.now() + datetime.timedelta(seconds=expiration_seconds))
date_time_obj = datetime.datetime.strptime(date_time_str, '%Y-%m-%d %H:%M:%S.%f')
x = sign_token(up, bk.encode(), "SHA256", date_time_obj)
xb = str(x)
y = f"{url_input}?hdnts={xb[2:-1]}"
print(y)

# Make a request to the generated URL and print the response code and headers
response = requests.get(y)

# Print the response content
print(response.content)

# Print the response code
print("Response Code:", response.status_code)

# Print the response headers
print("Response Headers:")
for header, value in response.headers.items():
    print(f"{header}: {value}")
