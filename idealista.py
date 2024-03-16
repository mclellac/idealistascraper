#!/usr/bin/env python

import argparse
import os
import requests
from bs4 import BeautifulSoup
from rich.progress import Progress
from rich.console import Console
from rich.table import Table
from urllib.parse import urljoin
import yaml

def banner():
    print("""
 ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣀⣠⠔⠉⠒⠤⣄⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢰⠺⠤⠔⠁⠀⠀⢀⣀⠀⠀⠀⠑⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⡀⢀⡰⠋⠉⠈⠉⠉⠳⠤⠔⢦⡈⢳⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢣⡜⠑⠂⠀⠀⠀⠀⠒⠄⠀⠀⣴⠃⠀⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡸⠀⢰⠄⢀⠆⠀⠰⢦⠀⠀⠀⢽⣳⣰⠇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠔⠋⢹⠄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡇⠀⠀⠠⣏⠀⠀⠀⠀⠀⠀⠀⠕⢻⡟⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⢸⠀⠀⠸⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣇⢠⡄⣀⣀⣀⠠⠴⣄⠀⠀⠀⠀⢈⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⢀⣀⣠⣧⣀⠘⠢⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠹⡌⠉⠒⣦⠖⠒⠉⠉⠀⠀⣠⠖⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⢮⠀⢀⡀⠀⠙⡆⠘⣦⣤⣀⣀⣀⠀⠀⢀⣀⣀⣙⣦⡀⠀⠀⠀⠀⠀⠠⡾⠓⢦⣄⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⢸⠉⠉⠉⠉⠚⡅⢀⡟⡄⠀⠈⠉⠉⠉⠉⠀⠀⠀⢸⠉⠳⢶⣤⣀⡤⠖⠁⢀⡞⠀⠈⠓⢤⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠈⡗⠉⠓⠒⠲⡇⢸⢁⠇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢳⠀⠀⠀⠀⣀⣠⠴⠋⠀⠀⠀⠀⠀⠈⠲⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠙⠶⢖⣒⣺⣵⣣⠊⠀⣀⣀⣀⡠⠤⠔⡿⠀⠀⠀⡞⠀⠀⠀⡞⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠣⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠈⠉⠉⠉⠀⠀⠀⠀⠀⣇⠀⠀⠀⡇⠀⠀⠀⡇⠀⠀⠀⠀⢦⣄⣀⠀⠀⠀⠀⠀⠀⢙⣆⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⠀⠀⠀⠃⠀⠀⢸⠇⠀⠀⠀⠀⣿⣿⣿⠛⢲⡄⠀⠀⢀⣼⡿⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⠀⠀⢰⠀⠀⠀⢸⠀⠀⠀⠀⢰⣿⣿⡟⢀⡞⠀⢀⣠⣿⣿⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⠦⢄⣈⠀⠀⠀⢸⠀⠀⠀⠀⣼⣿⣿⣇⡎⣠⣴⣿⣿⣿⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⡇⠀⠈⠀⠀⠀⠈⠓⠒⠒⠚⠋⠉⢸⡿⢿⣿⣿⣿⣿⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣷⢄⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣸⡇⠀⠉⡹⠻⡅⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢹⠀⠈⠉⠛⠒⠒⠒⠒⠚⣿⣿⣿⣿⣷⣀⣀⣙⣢⠇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⠄⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⣿⣿⣿⠀⠈⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠛⠛⠛⠉⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
""")

def euro_to_cad(euro_price: str) -> str:
    conversion_rate = 1.50
    cad_price = float(euro_price.replace('€', '').replace(',', '')) * conversion_rate
    return f"${cad_price:,.2f}"

def scrape_idealista(url: str) -> list[dict]:
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36',
            'Accept-Language': 'en-US,en;q=0.9',
        }
        all_homes = []
        with Progress() as progress:
            task = progress.add_task("[green]Collecting: Please stand by...", total=None)
            current_url = url
            while current_url:
                response = requests.get(current_url, headers=headers)
                response.raise_for_status()
                soup = BeautifulSoup(response.content, 'html.parser')
                
                listings = soup.find_all('article', class_='item')
                for listing in listings:
                    title = listing.find('a', class_='item-link').text.strip()
                    price_euro = listing.find('span', class_='item-price').text.strip()
                    price_cad = euro_to_cad(price_euro)
                    details = listing.find('span', class_='item-detail').text.strip()
                    link_path = listing.find('a', class_='item-link')['href']
                    link = urljoin(url, link_path)
                    photo_div = listing.find('div', class_='picture')
                    photo_url = None
                    if photo_div:
                        img_tag = photo_div.find('img')
                        if img_tag:
                            photo_url = img_tag.get('src')
   
                    home_info = {
                        'Title': title,
                        'Price (Euro)': price_euro,
                        'Price (CAD)': price_cad,
                        'Details': details,
                        'Link': link,
                        'Photo': photo_url
                    }
                    all_homes.append(home_info)
                
                progress.advance(task)
                
                next_link = soup.find('a', rel='nofollow', class_='icon-arrow-right-after', string='Next')
                current_url = urljoin(url, next_link['href']) if next_link else None

        return all_homes
    except KeyboardInterrupt:
            print("\nProgram terminated by user.")
            exit()
    except requests.exceptions.RequestException as e:
        print("Failed to fetch data:", e)
        return []

def read_config() -> str:
    with open("config.yaml", "r") as config_file:
        config = yaml.safe_load(config_file)
        return config["url"]

def generate_html(homes: list[dict]):
    # Build the HTML table manually
    html_table = "<table>"
    html_table += "<tr>"
    html_table += "<th>No.</th>"
    html_table += "<th>Title</th>"
    html_table += "<th>Price (Euro)</th>"
    html_table += "<th>Price (CAD)</th>"
    html_table += "<th>Details</th>"
    html_table += "<th>Photo</th>"
    html_table += "<th>Link</th>"
    html_table += "</tr>"

    for idx, home in enumerate(homes, start=1):
        html_table += "<tr>"
        html_table += f"<td>{idx}</td>"
        html_table += f"<td>{home['Title']}</td>"
        html_table += f"<td>{home['Price (Euro)']}</td>"
        html_table += f"<td>{home['Price (CAD)']}</td>"
        html_table += f"<td>{home['Details']}</td>"
        html_table += f"<td><img src='{home['Photo']}' alt='{home['Title']}' width='100'></td>"
        html_table += f"<td><a href='{home['Link']}'>Link</a></td>"
        html_table += "</tr>"

    html_table += "</table>"

    # Write the HTML content to the file
    os.makedirs("html", exist_ok=True)
    with open("html/index.html", "w") as html_file:
        html_file.write("<!DOCTYPE html>\n<html>\n<head>\n")
        html_file.write("<style>table {border-collapse: collapse; width: 100%;} th, td {border: 1px solid #ddd; padding: 8px; color: #333;} th {padding-top: 12px; padding-bottom: 12px; text-align: left; background-color: #f2f2f2; color: black;}</style>\n")
        html_file.write("</head>\n<body>\n")
        html_file.write(html_table)
        html_file.write(html_table)
        html_file.write("</body>\n</html>\n")


if __name__ == "__main__":
    banner()
    parser = argparse.ArgumentParser(description="Scrape homes from Idealista.")
    parser.add_argument("--generate-html", action="store_true", help="Generate HTML file with results.")
    args = parser.parse_args()
    
    url = read_config()
    homes = scrape_idealista(url)
    
    if homes:
        console = Console()
                
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("No.", style="cyan")
        table.add_column("Title", style="green")
        table.add_column("Price (Euro)", style="yellow")
        table.add_column("Price (CAD)", style="yellow")
        table.add_column("Details", style="magenta")
        table.add_column("Link", style="blue")
        
        for idx, home in enumerate(homes, start=1):
            table.add_row(
                str(idx),
                home['Title'],
                home['Price (Euro)'],
                home['Price (CAD)'],
                home['Details'],
                home['Link']
            )
        
        console.print(table)
        
        if args.generate_html:
            generate_html(homes)
            console.print("HTML file: [magenta]html[/magenta]/[blue]index.html[/blue] generated successfully.", style="bold green")
