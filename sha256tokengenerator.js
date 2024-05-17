const crypto = require('crypto');
const axios = require('axios');
const readline = require('readline');

// Function to sign the token
function signToken(urlPrefix, base64Key, algo, expirationTime = null) {
    let output = 'URLPrefix=' + Buffer.from(urlPrefix).toString('base64');

    if (!expirationTime) {
        expirationTime = Math.floor(Date.now() / 1000) + 3600; // Default to 1 hour if not provided
    }

    output += '~Expires=' + expirationTime;

    const key = Buffer.from(base64Key, 'base64');
    const hmac = crypto.createHmac(algo.toLowerCase(), key);
    hmac.update(output);
    const signature = hmac.digest('hex');

    output += '~hmac=' + signature;
    return output;
}

// Function to prompt user input
function askQuestion(query) {
    const rl = readline.createInterface({
        input: process.stdin,
        output: process.stdout,
    });

    return new Promise(resolve => rl.question(query, answer => {
        rl.close();
        resolve(answer);
    }));
}

(async () => {
    const up = await askQuestion("Enter the URL prefix (e.g., https://vod.cdntest.in/tearsofsteel/): ");
    const bk = await askQuestion("Enter the base64 key (e.g., LGRWJKHKHKK76S7S7H7R8KHJHKJHJHGG1MuY=): ");
    let expirationSeconds = await askQuestion("Enter expiration time in seconds (default is 60): ");
    expirationSeconds = expirationSeconds ? parseInt(expirationSeconds) : 60;
    const urlInput = await askQuestion("Enter the complete URL (e.g., https://vod.cdntest.in/tearsofsteel/manifest.m3u8): ");

    // Calculate expiration time
    const expirationTime = Math.floor(Date.now() / 1000) + expirationSeconds;

    // Generate the signed token
    const x = signToken(up, bk, 'sha256', expirationTime);
    const y = `${urlInput}?hdnts=${x}`;
    console.log(y);

    try {
        // Make a request to the generated URL and print the response code and headers
        const response = await axios.get(y);

        // Print the response content
        console.log(response.data);

        // Print the response code
        console.log("Response Code:", response.status);

        // Print the response headers
        console.log("Response Headers:");
        for (const [header, value] of Object.entries(response.headers)) {
            console.log(`${header}: ${value}`);
        }
    } catch (error) {
        if (error.response) {
            // Print the response code and headers if the request was made and the server responded with a status code
            console.log("Response Code:", error.response.status);
            console.log("Response Headers:");
            for (const [header, value] of Object.entries(error.response.headers)) {
                console.log(`${header}: ${value}`);
            }
        } else {
            // Print error message if there was an issue with making the request
            console.error("Error:", error.message);
        }
    }
})();
