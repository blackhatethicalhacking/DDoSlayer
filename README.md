# DDoSlayer Ultimate Edition - Advanced DDoS Testing Framework

<p align="center">
<a href="https://www.blackhatethicalhacking.com"><img src="https://www.blackhatethicalhacking.com/wp-content/uploads/2022/06/BHEH_logo.png" width="300px" alt="BHEH"></a>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/release-v3.0.0-orange.svg" alt="Release">
  <img src="https://img.shields.io/badge/build-passing-brightgreen.svg" alt="Build">
  <img src="https://img.shields.io/badge/python-3.6%2B-blue.svg" alt="Python">
  <img src="https://img.shields.io/badge/platform-Linux%20%7C%20macOS-lightgrey.svg" alt="Platform">
  <img src="https://img.shields.io/badge/license-GPL--3.0-red.svg" alt="License">
  <img src="https://img.shields.io/badge/maintained-yes-green.svg" alt="Maintained">
</p>

<p align="center">
An Advanced Multi-Vector DDoS Testing Framework with AI-Powered Attack Recommendations
</p>

<p align="center">
Developed by Chris 'SaintDruG' Abou-Chabke | Black Hat Ethical Hacking
</p>

---

## What is DDoSlayer Ultimate Edition?

**DDoSlayer Ultimate Edition** is a professional-grade **Distributed Denial of Service (DDoS)** testing framework designed for authorized penetration testing and red team operations. This tool simulates sophisticated Layer 4 and Layer 7 attacks to evaluate defensive capabilities against distributed denial of service scenarios.

### What Makes This "Ultimate"?

Version 3.0 represents a complete architectural overhaul with enterprise-grade features:

- **⚡ AI-Powered Auto-Detect Mode**: Intelligent target reconnaissance with automatic attack vector recommendation
- **⚡ Rich Terminal UI**: Beautiful, neon-themed interface with real-time progress tracking
- **⚡ Advanced Analytics**: Comprehensive attack metrics with JSON/Markdown reporting
- **⚡ 10 Attack Vectors**: From basic floods to advanced CDN bypass techniques
- **⚡ Stealth Mode**: Randomized timing patterns to evade IDS/WAF detection
- **⚡ Multi-Threading**: Optimized concurrent attack execution for maximum efficiency
- **⚡ Deep Improvements**: Over 1771 Lines of Code!

---

## What's New in Version 3.0

### Revolutionary Features

#### **Auto-Detect Mode (AI-Powered)**
The flagship feature that sets DDoSlayer apart from conventional tools:

```
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ [0]Auto-Detect Mode: Detect, Analyse & Strike ┃
┃     • Scans open ports (80, 443, 8080, 8443)  ┃
┃     • Fingerprints web server & services      ┃
┃     • Detects CDN/WAF (Cloudflare, Akamai)    ┃
┃     • Identifies vulnerabilities (XML-RPC)    ┃
┃     • AI recommends optimal attack vector     ┃
┃     • Provides confidence scoring (85-95%)    ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
```

**How It Works:**
1. **Reconnaissance Phase**: Automatically scans target infrastructure
2. **Analysis Phase**: Identifies protection mechanisms and vulnerabilities  
3. **Recommendation Phase**: AI engine suggests attack with highest success probability
4. **Execution Phase**: One-click launch with optimized parameters

**Example Output:**
```
╔════════════════════════════════════════╗
║       TARGET ANALYSIS REPORT           ║
╠════════════════════════════════════════╣
║ [>] Target:        example.com         ║
║ [>] IP Address:    93.184.216.34       ║
║ [!] CDN/WAF:       Cloudflare (Active) ║
║ [+] Server:        nginx/1.18.0        ║
║ [+] Open Ports:    80, 443             ║
║ [~] Response Time: 245ms               ║
╠════════════════════════════════════════╣
║      AI RECOMMENDATION                 ║
╠════════════════════════════════════════╣
║ ► Attack:       Cache Bypass           ║
║ ► Confidence:   92%                    ║
║ ► Reason:       Cloudflare detected.   ║
║                 Cache bypass targets   ║
║                 origin server directly ║
║ ► Threads:      150 (optimized)        ║
╚════════════════════════════════════════╝
```

#### **Rich Terminal Interface**
Built with the Rich library for a premium user experience:

- **Animated Progress Bars**: Real-time attack progress with live statistics
- **Professional Tables**: Clean data presentation for scan results
- **Color-Coded Output**: Intuitive color scheme (Cyan/Green/Magenta/Yellow)
- **Loading Spinners**: Visual feedback during reconnaissance
- **Perfect Box Drawing**: Works flawlessly across all terminal emulators

**Live Attack Dashboard:**
```
HTTP/2 FLOOD ━━━━━━━━━╸━━━━━━━━━ 65%
Packets: 45,832 | Rate: 763/s | Success: 98.5%
```

#### **Advanced Reporting System**
Generate professional reports in multiple formats:

**JSON Format** (Machine-Readable):
```json
{
  "attack_id": "attack_20250209_162345",
  "attack_type": "HTTP Flood",
  "results": {
    "packets_sent": 52834,
    "success_rate": 97.27,
    "avg_rate": 881,
    "peak_rate": 1245
  }
}
```

**Markdown Format** (Human-Readable):
```markdown
# DDoSlayer Attack Report
**Attack Type:** HTTP Flood
**Total Packets:** 52,834
**Success Rate:** 97.27%
**Peak Rate:** 1,245 packets/sec
```

#### ⚡ **10 Attack Vectors**

**Layer 4 Attacks:**
1. **UDP Flood** - Volumetric attack with randomized payload sizes (64-1024 bytes)
2. **SYN Flood** - TCP SYN packet flood (real packets via Scapy or TCP connect fallback)

**Layer 7 Attacks:**
3. **HTTP Flood** - High-volume HTTP/1.1 GET requests with header randomization
4. **HTTP/2 Flood** - Modern HTTP/2 protocol exploitation with session reuse
5. **Slowloris** - Connection exhaustion via slow HTTP headers (low bandwidth, high impact)
6. **Slow POST** - POST body slowdown attack (server resource exhaustion)
7. **Cache Bypass** - CDN cache evasion with randomized query strings (Cloudflare bypass)
8. **XML-RPC Flood** - WordPress/Drupal XML-RPC endpoint exploitation
9. **WebSocket Flood** - WebSocket protocol abuse (often bypasses WAF rules)
10. **CF UAM Bypass** - Cloudflare Under Attack Mode circumvention techniques

#### **Stealth Mode**
Sophisticated evasion techniques for IDS/WAF bypass:

- **Randomized Timing**: 0.1-2 second delays between requests
- **Human-Like Patterns**: Non-linear traffic distribution
- **User-Agent Rotation**: 6+ different browser signatures
- **Referer Randomization**: Mimics organic traffic sources
- **Cache Busting**: Dynamic parameter generation

**Impact:**
- Success Rate: +15-25% against protected targets
- Detection Rate: -60-70% by signature-based IDS
- Trade-off: -50% attack speed

---

## Understanding DDoS vs DoS

### What is DoS?
**Denial of Service (DoS)** is an attack from a **single source** attempting to overwhelm a target system.

### What is DDoS?
**Distributed Denial of Service (DDoS)** involves **multiple coordinated sources** attacking simultaneously, making it exponentially more powerful and harder to mitigate.

### DDoSlayer in DDoS Context
While DDoSlayer runs as a single instance, it becomes a **DDoS tool** when:
- ⚡ Deployed across **multiple machines** (VPS servers, cloud instances)
- ⚡ Coordinated with **multiple operators** in red team exercises
- ⚡ Used in **distributed testing scenarios** with orchestrated execution

**Example DDoS Deployment:**
```
Control Node (Coordinator)
    ├── VPS-1 (US East)    → DDoSlayer Instance
    ├── VPS-2 (EU West)    → DDoSlayer Instance  
    ├── VPS-3 (Asia)       → DDoSlayer Instance
    └── VPS-4 (Australia)  → DDoSlayer Instance

= Distributed attack from 4 geographic locations
= True DDoS scenario for resilience testing
```

---

## Technical Deep-Dive

### Attack Methodology Improvements (v2.0 → v3.0)

#### **UDP Flood Enhancement**
- **Old**: Fixed 1337-byte packets, single-threaded
- **New**: 64-1024 byte randomized payloads, 10-50 concurrent threads
- **Impact**: 10x throughput increase (5,000 → 50,000 packets/sec)

#### **SYN Flood Evolution**
- **Old**: Basic TCP connect() simulation
- **New**: Real SYN packets via Scapy with IP spoofing capability
- **Impact**: True TCP handshake exhaustion vs. connection attempts

#### **HTTP Flood Intelligence**
- **Old**: Static headers, single connection per request
- **New**: Randomized User-Agents, cache busting, keep-alive exploitation
- **Impact**: 8x more requests per second, 95%+ success rate

### Performance Metrics

| Attack Type | Packets/Second | CPU Usage | Bandwidth Required |
|------------|----------------|-----------|-------------------|
| UDP Flood | 50,000+ | Low | High (50+ Mbps) |
| SYN Flood | 30,000+ | Medium | Medium (30+ Mbps) |
| HTTP Flood | 10,000+ | Medium | Medium (20+ Mbps) |
| HTTP/2 Flood | 8,000+ | High | Medium (25+ Mbps) |
| Slowloris | 500 conn | Low | Very Low (1 Mbps) |
| Cache Bypass | 9,000+ | Medium | Medium (20+ Mbps) |

**Testing Environment:**
- CPU: 4-core Intel Xeon
- RAM: 8GB
- Network: 1 Gbps uplink

---

## Installation

### Prerequisites
- Python 3.6 or higher
- pip3 package manager
- Linux/macOS (Windows via WSL)

### Quick Install

```bash
# Clone repository
git clone https://github.com/blackhatethicalhacking/DDoSlayer.git
cd DDoSlayer

# Install dependencies
pip3 install -r requirements.txt

# Make executable
chmod +x DDoSlayer_v3.0_ULTIMATE.py

# Run the tool
python3 DDoSlayer_v3.0_ULTIMATE.py
```

### Dependencies

**Required:**
```
termcolor>=2.3.0    # Terminal colors
requests>=2.31.0    # HTTP requests
rich>=13.7.0        # Beautiful terminal UI
```

**Optional (Enhanced Features):**
```
scapy>=2.5.0        # Real SYN flood (requires root/sudo)
dnspython>=2.4.2    # Advanced DNS analysis
```

**Install All:**
```bash
pip3 install termcolor requests rich dnspython
sudo pip3 install scapy  # Optional, requires root
```

---

## Usage Guide

### Basic Workflow

1. **Launch Tool**
```bash
python3 DDoSlayer_v3.0_ULTIMATE.py
```

2. **Choose Mode**
   - **Option 0**: Auto-Detect (AI recommendations)
   - **Options 1-10**: Manual attack selection

3. **Configure Attack**
   - Target: `example.com` or `192.168.1.100`
   - Duration: `60` (seconds)
   - Threads: `100` (default varies by attack)
   - Stealth: `y` or `n`

4. **Execute & Monitor**
   - Real-time progress tracking
   - Live statistics dashboard
   - Automatic summary generation

5. **Export Results**
   - JSON format (automation)
   - Markdown report (documentation)
   - Both formats available

### Command Examples

#### **Auto-Detect Mode (Recommended)**
```
Select option: 0
Target: example.com
Duration: 60
Stealth: n

[Automatic scanning and recommendation]
[One-click attack execution]
```

#### **Manual HTTP Flood**
```
Select option: 3
Target: https://target.com
Duration: 120
Threads: 150
Stealth: n
```

#### **Stealthy Slowloris**
```
Select option: 5
Target: vulnerable-server.com
Duration: 300
Threads: 10
Stealth: y
```

### Advanced Usage

#### **Multi-Instance DDoS**
```bash
# Terminal 1 (VPS-1)
python3 DDoSlayer_v3.0_ULTIMATE.py
# Select: HTTP Flood, threads: 200

# Terminal 2 (VPS-2)  
python3 DDoSlayer_v3.0_ULTIMATE.py
# Select: HTTP Flood, threads: 200

# Terminal 3 (VPS-3)
python3 DDoSlayer_v3.0_ULTIMATE.py
# Select: HTTP Flood, threads: 200

= 600 concurrent threads across 3 locations
= Distributed DDoS simulation
```

#### **Scripted Execution**
```bash
#!/bin/bash
# automated-test.sh

TARGET="testsite.com"
DURATION=300

echo "Starting DDoS test on $TARGET"
python3 DDoSlayer_v3.0_ULTIMATE.py << EOF
3
$TARGET
$DURATION
150
n
1
EOF
```

---

## Screenshots

### Main Menu
<img width="1906" height="1079" alt="mainmenu" src="https://github.com/user-attachments/assets/23b12f28-994d-4b95-8e89-896ed930ba7b" />
*Professional neon-themed interface with 10 attack options*

### Auto-Detect Scanning
<img width="1906" height="1079" alt="detect 1" src="https://github.com/user-attachments/assets/684a35dd-6ee3-4f1d-a800-68471eda4fd1" />
*Real-time reconnaissance with animated progress bars*

### Analysis Report
<img width="1906" height="1079" alt="detect 2" src="https://github.com/user-attachments/assets/716b961c-032c-425d-9051-7a21e3b0aa28" />
*Detailed target analysis with AI recommendations*

### Live Attack Dashboard
<img width="1906" height="1079" alt="liveattack" src="https://github.com/user-attachments/assets/7046131a-7872-4e99-8851-382d2637771a" />
*Real-time metrics: packets sent, rate, success percentage*

### Attack Summary
<img width="1906" height="1079" alt="attack summary" src="https://github.com/user-attachments/assets/c952524a-1b04-4020-b2f0-2b6be877f084" />
*Comprehensive statistics with peak performance metrics*

### Export Reports in JSON or Markdown
<img width="1906" height="832" alt="report" src="https://github.com/user-attachments/assets/8fb9fb04-5bcc-47a3-b349-d849468834f0" />
*Generate reports to include in your Assessments*

## Demo Preview

https://github.com/user-attachments/assets/67185129-e33d-4a8a-891e-b9bfc023d790

---

## Defensive Considerations

### Detection Signatures

**What Blue Teams Will See:**

1. **UDP Flood**
   - Abnormal UDP traffic spike
   - Random payload patterns
   - Multiple source ports

2. **SYN Flood**
   - Half-open TCP connections
   - SYN packet volume anomaly
   - Incomplete handshakes

3. **HTTP Flood**
   - High request rate from single/multiple IPs
   - Unusual User-Agent patterns
   - Cache query parameter variations

4. **Slowloris**
   - Long-duration connections
   - Incomplete HTTP headers
   - Connection pool exhaustion

### Mitigation Recommendations

- **Rate Limiting**: Implement per-IP request throttling
- **SYN Cookies**: Enable TCP SYN cookie protection
- **WAF Rules**: Deploy application-layer filtering
- **CDN Protection**: Use services like Cloudflare, Akamai
- **Connection Limits**: Set max connections per IP
- **Behavioral Analysis**: Deploy anomaly detection systems

---

## Testing Best Practices

### Authorized Testing Only

✅ **DO:**
- Obtain written permission (NDA/contract)
- Test in isolated lab environments
- Use against owned infrastructure
- Document all activities
- Follow scope limitations

❌ **DON'T:**
- Test without authorization
- Attack production systems without approval
- Exceed agreed-upon intensity
- Test third-party infrastructure
- Ignore rate limits or warnings

### Recommended Test Scenarios

1. **Baseline Testing**
   - Start with low thread count (10-20)
   - Short duration (30-60 seconds)
   - Monitor target response

2. **Gradual Escalation**
   - Increase threads incrementally
   - Extend duration gradually
   - Document breaking points

3. **Defense Validation**
   - Trigger IDS/IPS alerts
   - Test WAF effectiveness
   - Verify rate limiting

4. **Recovery Testing**
   - Stop attack, measure recovery time
   - Check service availability
   - Validate logging/alerting

---

## 🔬 Research & Development

### Planned Features (v3.1+)

- [ ] **Proxy Chain Support**: Route traffic through SOCKS5/HTTP proxies
- [ ] **Attack Profiles**: Save/load custom attack configurations  
- [ ] **Distributed Mode**: Native multi-instance coordination
- [ ] **API Integration**: RESTful API for automation
- [ ] **ML-Enhanced Detection**: Machine learning for target analysis
- [ ] **Custom Payload Scripts**: Lua scripting for attack customization
- [ ] **Network Graphing**: Visual representation of attack distribution
- [ ] **DNS Amplification**: Reflective amplification attacks

### Contributing

We welcome contributions! Areas of interest:
- New attack vectors
- Evasion techniques
- Performance optimizations
- UI/UX improvements
- Documentation enhancements

**How to Contribute:**
1. Fork the repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request

---

## Comparison with Other Tools

| Feature | DDoSlayer v3.0 | LOIC | HOIC | SlowHTTPTest |
|---------|----------------|------|------|--------------|
| AI Auto-Detect | ✅ | ❌ | ❌ | ❌ |
| Layer 4 Attacks | ✅ | ✅ | ❌ | ❌ |
| Layer 7 Attacks | ✅ (8 types) | ✅ (1 type) | ✅ (1 type) | ✅ (3 types) |
| Stealth Mode | ✅ | ❌ | ❌ | ✅ |
| Rich UI | ✅ | ❌ | ❌ | ❌ |
| Report Generation | ✅ (JSON+MD) | ❌ | ❌ | ❌ |
| CDN Bypass | ✅ | ❌ | ❌ | ❌ |
| Multi-Threading | ✅ (10-200) | ✅ | ✅ | ✅ |
| Active Development | ✅ | ❌ | ❌ | ⚠️ |

---

## Compatibility

### Tested Platforms

✅ **Linux Distributions:**
- Kali Linux 2023.x
- Parrot Security OS 5.x
- Ubuntu 20.04+
- Debian 11+
- Arch Linux

✅ **macOS:**
- macOS Monterey (12.x)
- macOS Ventura (13.x)
- macOS Sonoma (14.x)

⚠️ **Windows:**
- Windows 10/11 (via WSL2)
- Native support limited

### Hardware Requirements

**Minimum:**
- CPU: Dual-core processor
- RAM: 2GB
- Network: 10 Mbps
- Storage: 100MB

**Recommended:**
- CPU: Quad-core+ processor
- RAM: 4GB+
- Network: 100 Mbps+
- Storage: 500MB

**Optimal (Enterprise Testing):**
- CPU: 8+ cores
- RAM: 8GB+
- Network: 1 Gbps+
- Storage: 1GB

---

## 📜 License

This project is licensed under the **GNU General Public License v3.0** - see the [LICENSE](LICENSE) file for details.

**Summary:**
- ✅ Commercial use allowed (with proper authorization)
- ✅ Modification and distribution permitted
- ✅ Patent use granted
- ⚠️ Liability and warranty disclaimed
- ⚠️ Must disclose source code changes

---

## ⚠️ Legal Disclaimer

### READ CAREFULLY BEFORE USE

This tool is provided **exclusively for educational purposes** and **authorized security testing**. The authors and contributors are **NOT responsible** for any misuse or damage caused by this software.

#### Acceptable Use

✅ **AUTHORIZED USE ONLY:**
- Penetration testing with signed contracts
- Red team exercises with documented authorization
- Security research in controlled lab environments
- Educational demonstrations with proper consent
- Defensive security training on owned infrastructure

#### Prohibited Use

❌ **STRICTLY FORBIDDEN:**
- Unauthorized access to systems or networks
- Attacking infrastructure without written permission
- Malicious intent or causing harm
- Violating local, state, or federal laws
- Circumventing security measures without authorization

#### Legal Consequences

Unauthorized DDoS attacks are **CRIMINAL OFFENSES** in most jurisdictions:

- **United States**: Computer Fraud and Abuse Act (CFAA) - Up to 10 years imprisonment
- **United Kingdom**: Computer Misuse Act 1990 - Up to 10 years imprisonment
- **European Union**: Directive 2013/40/EU - Criminal prosecution
- **Australia**: Cybercrime Act 2001 - Up to 10 years imprisonment

**Civil Liability:**
- Lawsuits for damages and losses
- Financial restitution (potentially millions)
- Permanent criminal record

### Required Documentation

Before using this tool, ensure you have:

1. ✅ **Written Authorization** from system owner
2. ✅ **Signed NDA** with clear scope definition
3. ✅ **Engagement Letter** defining test parameters
4. ✅ **Liability Insurance** (for professional consultants)
5. ✅ **Incident Response Plan** for unexpected issues

### Ethical Guidelines

- **Transparency**: Clearly communicate intentions and methods
- **Proportionality**: Use minimum force necessary for testing objectives
- **Responsibility**: Take ownership of all actions and consequences
- **Disclosure**: Report findings responsibly to affected parties
- **Respect**: Honor the trust placed in you by clients and community

---

## Support & Community

### Get Help

- **Documentation**: [Wiki](https://github.com/blackhatethicalhacking/DDoSlayer/wiki)
- **Issues**: [GitHub Issues](https://github.com/blackhatethicalhacking/DDoSlayer/issues)
- **Discussions**: [GitHub Discussions](https://github.com/blackhatethicalhacking/DDoSlayer/discussions)

### Follow Us

- **Website**: [blackhatethicalhacking.com](https://www.blackhatethicalhacking.com)
- **YouTube**: [BHEH Channel](https://www.youtube.com/channel/UC7-AsunT7zO-ny5-U8glqkw)
- **LinkedIn**: [BHEH Company](https://www.linkedin.com/company/black-hat-ethical-hacking/)
- **Twitter**: [@secur1ty1samyth](https://twitter.com/secur1ty1samyth)

### Sponsor This Project

If DDoSlayer has helped your security testing:

- ⭐ Star this repository
- 🍴 Fork and contribute
- 📢 Share with the community
- ☕ [Buy us a coffee](https://www.buymeacoffee.com/bheh)

---

## 🏆 Acknowledgments

### Special Thanks

- **Chris 'SaintDruG' Abou-Chabke** - Lead Developer
- **Black Hat Ethical Hacking Team** - Testing & Feedback
- **Open Source Community** - Libraries and inspiration
- **Beta Testers** - Early adoption and bug reports

### Built With

- [Python](https://www.python.org/) - Core language
- [Rich](https://github.com/Textualize/rich) - Terminal UI
- [Requests](https://requests.readthedocs.io/) - HTTP library
- [Scapy](https://scapy.net/) - Packet manipulation
- [DNSPython](https://www.dnspython.org/) - DNS toolkit

---

## Official Merchandise

<h2 align="center">
  <a href="https://store.blackhatethicalhacking.com/" target="_blank">BHEH Official Merch Store</a>
</h2>

<p align="center">
Gear up with our exclusive offensive security apparel! Our collection features premium t-shirts, hoodies, and drinkware designed for the ethical hacking community. Rep your dedication to cybersecurity with bold designs that showcase your passion for red teaming and penetration testing.
</p>

<p align="center">
  <img src="https://github.com/blackhatethicalhacking/blackhatethicalhacking/blob/main/Merch_Promo.gif" width="540px" height="540px">
</p>

---

## 📈 Changelog

### Version 3.0.0 (2025-02-13) - Ultimate Edition

**Major Features:**
- AI-powered Auto-Detect Mode with attack recommendations
- Rich terminal UI with animated progress bars
- Advanced reporting (JSON/Markdown export)
- 8 new attack vectors (total: 10)
- Stealth mode with IDS/WAF evasion
- Multi-threading optimization (up to 200 threads)

**Improvements:**
- Complete codebase refactor (Python 3.6+)
- Enhanced error handling and recovery
- Intelligent protocol detection (HTTP/HTTPS)
- Real-time attack statistics dashboard
- Professional documentation and screenshots

**Bug Fixes:**
- Fixed UDP payload size randomization
- Resolved HTTP/2 protocol detection issues
- Corrected SSL warning suppression
- Fixed progress bar rendering on all terminals

### Version 2.0.0 (2023-01-15)

- Added 3 attack types (UDP, SYN, HTTP)
- Error handling improvements
- Time-based attack duration
- Basic colorization

### Version 1.2.0 (2022-08-20)

- Python 3 migration
- Added colored output
- Duration parameter support

### Version 1.0.0 (2022-06-10)

- Initial release
- Basic HTTP flood functionality

---

<p align="center">
  <b>DDoSlayer Ultimate Edition v3.0</b><br>
  <i>Professional DDoS Testing for the Modern Era</i><br><br>
  Made with ❤️ by <a href="https://www.blackhatethicalhacking.com">Black Hat Ethical Hacking</a><br>
  <sub>Stay Ethical. Test Authorized. Hack Responsibly.</sub>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/⚡-Powered%20by%20Python-blue.svg" alt="Python">
  <img src="https://img.shields.io/badge/🛡️-Security%20Testing-red.svg" alt="Security">
  <img src="https://img.shields.io/badge/🎯-DDoS%20Simulation-orange.svg" alt="DDoS">
</p>
