require 'base64'
require 'openssl'
require 'time'
require 'net/http'
require 'uri'

# Function to fix Base64 padding
def fix_base64_padding(base64_key)
  padding = (4 - base64_key.length % 4) % 4
  base64_key + "=" * padding
end

# Function to Base64 encode
def base64_encoder(value)
  Base64.urlsafe_encode64(value).gsub(/=+$/, '') # Remove padding
end

# Function to generate the signed token
def sign_token(base64_key, algorithm, expiration_time, url_prefix, headers)
  fixed_base64_key = fix_base64_padding(base64_key)
  decoded_key = Base64.urlsafe_decode64(fixed_base64_key)

  tokens = []
  to_sign = []

  # Add URL Prefix
  url_prefix_encoded = base64_encoder(url_prefix)
  tokens << "URLPrefix=#{url_prefix_encoded}"
  to_sign << "URLPrefix=#{url_prefix_encoded}"

  # Add Expiration Time
  expires_epoch = expiration_time.to_i
  tokens << "Expires=#{expires_epoch}"
  to_sign << "Expires=#{expires_epoch}"

  # Add custom headers
  if headers.any?
    header_names = headers.map { |h| h[:name] }
    header_pairs = headers.map { |h| "#{h[:name]}=#{h[:value]}" }

    tokens << "Headers=#{header_names.join(',')}"
    to_sign << "Headers=#{header_pairs.join(',')}"
  end

  # Generate signature
  to_sign_str = to_sign.join("~")

  if algorithm.downcase == "sha256"
    signature = OpenSSL::HMAC.hexdigest("SHA256", decoded_key, to_sign_str)
    tokens << "hmac=#{signature}"
  else
    raise "Invalid algorithm: Only SHA256 is supported"
  end

  tokens.join("~")
end

# Hardcoded values as requested
url_prefix = "https://dual.vivekanurag.demo.altostrat.com/tearsofsteel/"
base64_key = "LGRWQgV4nABCDEFGHIJFKPkCiFCiS7u9gkca8b91MuY"
expiration_seconds = 60
complete_url = "https://dual.vivekanurag.demo.altostrat.com/tearsofsteel/manifest.m3u8"
custom_header_name = "stream_key"
custom_header_value = "secret"

# Format header as array of hashes
headers = [{ name: custom_header_name, value: custom_header_value }]

# Set expiration time
expiration_time = Time.now + expiration_seconds

# Generate signed token
signed_token = sign_token(base64_key, "SHA256", expiration_time, url_prefix, headers)

# Construct final signed URL
signed_url = "#{complete_url}?hdnts=#{signed_token}"

# Display signed URL
puts "\nGenerated Signed URL:"
puts signed_url

# Make a request to the signed URL with the custom header
uri = URI(signed_url)
request = Net::HTTP::Get.new(uri)
request[custom_header_name] = custom_header_value

response = Net::HTTP.start(uri.host, uri.port, use_ssl: uri.scheme == "https") do |http|
  http.request(request)
end

# Print the response
puts "\nResponse Code: #{response.code}"
puts "Response Headers:"
response.each_header { |header, value| puts "#{header}: #{value}" }

