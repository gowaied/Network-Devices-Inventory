# Network Device Inventory & Backup Automation

A Python-based automation tool that uses **Netmiko** to connect to multiple Cisco IOS devices, retrieve critical system information, and store them in an organized local directory structure.

## 🚀 Features
- **Secure Authentication**: Uses `getpass` to ensure passwords and secrets are never hardcoded in the script.
- **Automated Directory Management**: Dynamically creates folders for each device using the `os` module.
- **Robust Error Handling**: Handles `NetMikoAuthenticationException` and `NetMikoTimeoutException` to prevent the script from crashing during connectivity issues.
- **Inventory Collection**: Automatically captures:
    - `show ip int br | ex un` (Active Interfaces)
    - `show version` (System Version)
    - `show start` (Startup Configuration)
 
## 📋 How to Use

  - Clone this repository.

  - Update the all_devices dictionary in the script with your device hostnames and IP addresses.

  - Run the script:
      - python script_name.py
  
  - Enter your SSH password and Enable secret when prompted.

## 🛠️ Prerequisites
- Python 3.x
- Netmiko library

You can install the required library via pip:
```bash
pip install netmiko
