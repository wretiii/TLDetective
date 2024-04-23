import argparse
import aiohttp
import asyncio

API_KEY = "your-API-key"  # Add Domainr API key

async def download_tlds(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                text = await response.text()
                return [line.strip() for line in text.split('\n') if not line.startswith('#')]
            else:
                raise Exception(f"Failed to download TLD list from {url}")

def generate_full_domains(domain_name, tlds):
    return [f"{domain_name}.{tld.lower()}" for tld in tlds]

async def fetch_status(session, domain, url_base):
    headers = {
        "X-RapidAPI-Key": API_KEY,
        "X-RapidAPI-Host": "domainr.p.rapidapi.com"
    }
    url = f"{url_base}?domain={domain.lower()}"
    async with session.get(url, headers=headers) as response:
        if response.status == 200:
            data = await response.json()
            status_list = data.get('status', [])
            if status_list and isinstance(status_list, list):
                summary = status_list[0].get('summary', 'Unknown status format')
            else:
                summary = 'Unknown status format'
            return (domain.lower(), summary)
        else:
            return (domain.lower(), 'Failed to fetch data')

async def check_domains(domains):
    url_base = "https://domainr.p.rapidapi.com/v2/status"
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_status(session, domain, url_base) for domain in domains]
        results = await asyncio.gather(*tasks)
    return results

def save_results_by_status(results, domain_name):
    status_dict = {}
    for domain, status in results:
        formatted_status = status.replace(' ', '-').lower()
        if formatted_status not in status_dict:
            status_dict[formatted_status] = []
        status_dict[formatted_status].append(domain)

    for status, domains in status_dict.items():
        file_name = f"{domain_name}-{status}.txt"
        with open(file_name, 'w') as file:
            for domain in domains:
                file.write(f"{domain.lower()}\n")
        print(f"Results for {status.replace('-', ' ')} domains saved to {file_name}")

async def main():
    parser = argparse.ArgumentParser(description='Domain Checker')
    parser.add_argument('-d', '--domain-name', required=True, help='Domain name without the top-level domain (e.g., example)')
    args = parser.parse_args()
    domain_name = args.domain_name.lower()

    tlds = await download_tlds('https://data.iana.org/TLD/tlds-alpha-by-domain.txt')
    full_domains = generate_full_domains(domain_name, tlds)

    print("Enumerating all TLDs from https://data.iana.org/TLD/tlds-alpha-by-domain.txt.")
    
    results = await check_domains(full_domains)

    active_domains = [domain for domain, status in results if status.lower() == "active"]
    if active_domains:
        print("The following domains are active:")
        for domain in active_domains:
            print(domain.lower())

    save_results_by_status(results, domain_name)

if __name__ == '__main__':
    asyncio.run(main())
