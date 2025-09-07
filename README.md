# 🖥️ macOS Backup Server

A complete guide to setting up a **macOS backup server** using:
- **Ubuntu Server (VM)**
- **Samba** for Time Machine compatibility
- **Flask Web App** for management

This setup works on a VM, physical server, or NAS.

---

## 🚀 Features
- 🔄 Supports **macOS Time Machine backups**
- 📂 Shared folder access via **Finder (SMB)**
- 🌐 Web dashboard for **user & backup management**
- 🔐 Secure permissions and limited sudo rules
- 🖧 Runs on a lightweight **Ubuntu VM**

---

## 🛠️ System Requirements
- macOS (client machine)
- VirtualBox (or any hypervisor)
- Ubuntu Server 22.04 LTS (guest OS)

---

## 📦 Installation

### 1. Create the Virtual Server
1. Install **VirtualBox** (or another hypervisor).
2. Create a VM and install **Ubuntu Server 22.04 LTS**.
3. Set **Network Adapter → Bridged Adapter**.
4. Find VM IP:
   ```bash
   ip a
