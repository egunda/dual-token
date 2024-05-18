```sh
▒▓███████▓▒░░▒▓█▓▒░░▒▓█▓▒░░▒▓██████▓▒░░▒▓█▓▒░            ░▒▓████████▓▒░▒▓██████▓▒░░▒▓█▓▒░░▒▓█▓▒░▒▓████████▓▒░▒▓███████▓▒░  
▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░               ░▒▓█▓▒░  ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░ 
▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░               ░▒▓█▓▒░  ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░ 
▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓████████▓▒░▒▓█▓▒░               ░▒▓█▓▒░  ░▒▓█▓▒░░▒▓█▓▒░▒▓███████▓▒░░▒▓██████▓▒░ ░▒▓█▓▒░░▒▓█▓▒░ 
▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░               ░▒▓█▓▒░  ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░ 
▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░               ░▒▓█▓▒░  ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░ 
▒▓███████▓▒░ ░▒▓██████▓▒░░▒▓█▓▒░░▒▓█▓▒░▒▓████████▓▒░        ░▒▓█▓▒░   ░▒▓██████▓▒░░▒▓█▓▒░░▒▓█▓▒░▒▓████████▓▒░▒▓█▓▒░░▒▓█▓▒░ 
                                                                                                                             
      
```
# Google Media CDN Dual Token - Setup and required assets.

## Token generator Scripts for SHA256
### Python
The fiename `sha256tokengenerator.py` is a SHA256 cookieless token generator script developed in Python3. Just run `python3 sha256tokengenerator.py ` to call the script in action. It will ask you to input required data and finally will output tokenized URL. It will also make a request to the URL and show you the dump of response, response code, and response headers

### PHP
The fiename `sha256tokengenerator.php` is a SHA256 cookieless token generator script written in PHP. Just run `php sha256tokengenerator.php` to call the script in action. It will ask you to input required data and finally will output tokenized URL. It will also make a request to the URL and show you the dump of response, response code, and response headers

### NodeJS
The fiename `sha256tokengenerator.js` is a SHA256 cookieless token generator script written in NodeJS. Just run `node sha256tokengenerator.js` to call the script in action. It will ask you to input required data and finally will output tokenized URL. It will also make a request to the URL and show you the dump of response, response code, and response headers. You need to have axios package installed to run this. To install axios, use npm install axios

## Sample YAML file for setupwith SHA256
The file `vod-dual-sha256-cookieless.yaml` is a sample confif file, which you should take a reference while creating your own setup. This setup support SHA256 cookieless tokens for HLS multi-bitrate stream.
