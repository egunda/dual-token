import base64
import datetime
import hashlib
import hmac
import requests
import cryptography.hazmat.primitives.asymmetric.ed25519 as ed25519

def base64_encoder(value: bytes) -> str:
    """Returns a base64-encoded string compatible with Media CDN."""
    encoded_bytes = base64.urlsafe_b64encode(value)
    encoded_str = encoded_bytes.decode("utf-8")
    return encoded_str.rstrip("=")

def fix_base64_padding(base64_key: str) -> str:
    """Fixes incorrect padding in a base64-encoded string."""
    return base64_key + "=" * (-len(base64_key) % 4)

def sign_token(
    base64_key: str,
    signature_algorithm: str,
    expiration_time: datetime.datetime,
    url_prefix: str,
    headers: list,
) -> str:
    """Generates a signed URL token for Google Media CDN.

    Args:
        base64_key: Base64-encoded secret key.
        signature_algorithm: Algorithm (SHA1, SHA256, or Ed25519).
        expiration_time: Expiration time as a UTC datetime object.
        url_prefix: The URL prefix to sign.
        headers: List of headers to include in the signed token.
    
    Returns:
        A signed URL token string.
    """

    # Fix Base64 padding issue
    fixed_base64_key = fix_base64_padding(base64_key)
    decoded_key = base64.urlsafe_b64decode(fixed_base64_key)
    algo = signature_algorithm.lower()

    tokens = []
    to_sign = []

    # Add URL Prefix
    field = "URLPrefix=" + base64_encoder(url_prefix.encode("utf-8"))
    tokens.append(field)
    to_sign.append(field)

    # Add Expiration Time
    epoch_duration = expiration_time.astimezone(
        tz=datetime.timezone.utc
    ) - datetime.datetime.fromtimestamp(0, tz=datetime.timezone.utc)
    field = f"Expires={int(epoch_duration.total_seconds())}"
    tokens.append(field)
    to_sign.append(field)

    # Add custom headers
    if headers:
        header_names = []
        header_pairs = []
        for each in headers:
            header_names.append(each["name"])
            header_pairs.append(f"{each['name']}={each['value']}")
        tokens.append(f"Headers={','.join(header_names)}")
        to_sign.append(f"Headers={','.join(header_pairs)}")

    # Generate token signature
    to_sign_str = "~".join(to_sign)
    to_sign_bytes = to_sign_str.encode("utf-8")

    if algo == "ed25519":
        digest = ed25519.Ed25519PrivateKey.from_private_bytes(decoded_key).sign(to_sign_bytes)
        tokens.append("Signature=" + base64_encoder(digest))
    elif algo == "sha256":
        signature = hmac.new(decoded_key, to_sign_bytes, digestmod=hashlib.sha256).hexdigest()
        tokens.append("hmac=" + signature)
    elif algo == "sha1":
        signature = hmac.new(decoded_key, to_sign_bytes, digestmod=hashlib.sha1).hexdigest()
        tokens.append("hmac=" + signature)
    else:
        raise ValueError("Invalid `signature_algorithm`. Must be `sha1`, `sha256`, or `ed25519`.")

    return "~".join(tokens)

# Hardcoded values based on user request
url_prefix = "https://dual.vivekanurag.demo.altostrat.com/tearsofsteel/"
base64_key = "LGRWQgV4nlRABCDEFGHIJPkCiFCiS7u9gkca8b91MuY="
expiration_seconds = 60
complete_url = "https://dual.vivekanurag.demo.altostrat.com/tearsofsteel/manifest.m3u8"
custom_header_name = "stream_key"
custom_header_value = "secret"

# Format header as list of dicts
headers = [{"name": custom_header_name, "value": custom_header_value}]

# Set expiration time
expiration_time = datetime.datetime.now() + datetime.timedelta(seconds=expiration_seconds)

# Generate signed token
signed_token = sign_token(base64_key, "SHA256", expiration_time, url_prefix, headers)

# Construct the final signed URL
signed_url = f"{complete_url}?hdnts={signed_token}"

# Display the signed URL
print("\nGenerated Signed URL:")
print(signed_url)

# Make a request to the signed URL with the custom header
response = requests.get(signed_url, headers={custom_header_name: custom_header_value})

# Print the response
print("\nResponse Code:", response.status_code)
print("Response Headers:")
for header, value in response.headers.items():
    print(f"{header}: {value}")

