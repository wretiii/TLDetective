# TLDetective
Enumeration tool for the registration status of an organization's domain against TLD's listed at https://data.iana.org/TLD/tlds-alpha-by-domain.txt.

## Requirements
- **Python 3.7+**: The tool is built with asyncio, which requires Python 3.7 or newer.
- **An API key from Domainr**: This tool requires a valid API key from Domainr to query domain statuses.
- **aiohttp library**: For asynchronous HTTP requests.
```bash
pip install aiohttp
```

## Usage
Before running, add your Domainr API key to the script.

Provide only the domain base name (without TLD) as an argument:

```bash
python tldetective.py -d yourdomain
```
## Output
TLDetective will enumerate all TLDs and output those with active status. Corresponding text files will also be generated for each status.
