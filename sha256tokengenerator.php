<?php
function sign_token($url_prefix, $base64_key, $algo, $expiration_time = null) {
    // Gets the Signed URL Suffix string for the Media CDN' Short token URL requests.

    $output = 'URLPrefix=' . base64_encode($url_prefix);

    if (!$expiration_time) {
        $expiration_time = new DateTime();
        $expiration_time->add(new DateInterval('PT1H')); // Default to 1 hour if not provided
    }
    $epoch_duration = $expiration_time->getTimestamp();
    $output .= '~Expires=' . $epoch_duration;

    $key = base64_decode($base64_key);
    $algo = strtolower($algo);
    if ($algo == 'sha1') {
        $signature = hash_hmac('sha1', $output, $key);
    } elseif ($algo == 'sha256') {
        $signature = hash_hmac('sha256', $output, $key);
    } else {
        throw new Exception('User input(`algo`) can be either `sha1` or `sha256`');
    }
    $output .= '~hmac=' . $signature;
    return $output;
}

// Ask user for inputs
echo "Enter the URL prefix (e.g., https://vod.cdntest.in/tearsofsteel/): ";
$up = trim(fgets(STDIN));

echo "Enter the base64 key (e.g., LGRWQgV4nlRIgjggklkhjkhljlkjkl;hkg91MuY=): ";
$bk = trim(fgets(STDIN));

echo "Enter expiration time in seconds (default is 60): ";
$expiration_seconds_input = trim(fgets(STDIN));
$expiration_seconds = $expiration_seconds_input ? intval($expiration_seconds_input) : 60;

echo "Enter the complete URL (e.g., https://vod.cdntest.in/tearsofsteel/manifest.m3u8): ";
$url_input = trim(fgets(STDIN));

// Calculate expiration time
$expiration_time = new DateTime();
$expiration_time->add(new DateInterval('PT' . $expiration_seconds . 'S'));

// Generate the signed token
$x = sign_token($up, $bk, 'sha256', $expiration_time);
$xb = strval($x);
$y = $url_input . '?hdnts=' . $xb;
echo $y . PHP_EOL;

// Make a request to the generated URL and print the response code and headers
$response = file_get_contents($y, false, stream_context_create([
    'http' => [
        'method' => 'GET',
    ]
]));

$http_response_header = isset($http_response_header) ? $http_response_header : [];

echo $response . PHP_EOL;
echo "Response Code: " . parse_response_code($http_response_header) . PHP_EOL;
echo "Response Headers:" . PHP_EOL;
foreach ($http_response_header as $header) {
    echo $header . PHP_EOL;
}

function parse_response_code($headers) {
    foreach ($headers as $header) {
        if (preg_match('/^HTTP\/\d+\.\d+\s+(\d+)/', $header, $matches)) {
            return intval($matches[1]);
        }
    }
    return 0;
}
?>
