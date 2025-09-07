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

## 🏗️ Architecture Diagram

```

```
 ┌──────────────┐
 │    macOS     │
 │  (Client)    │
 │              │
 │ Finder  🗂️   │
 │ TimeMachine ⏳ │
 └───────┬──────┘
         │ SMB
         │
 ┌───────▼─────────┐
 │   Ubuntu VM     │
 │ (Backup Server) │
 │                 │
 │  ┌───────────┐ │
 │  │  Samba    │◄┼── File Sharing
 │  └───────────┘ │
 │  ┌───────────┐ │
 │  │  Flask    │◄┼── Web Dashboard
 │  └───────────┘ │
 │                 │
 └─────────────────┘
```

````

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
````

---

### 2. Install & Configure Services

**Install packages:**

```bash
sudo apt update
sudo apt install samba python3-pip python3-flask openssh-server
```

**Create backup folder + user:**

```bash
sudo adduser backup_web_app
sudo mkdir -p /srv/backups/timemachine
sudo chown -R backup_web_app:backup_web_app /srv/backups/timemachine
sudo chmod -R 775 /srv/backups/timemachine
```

**Allow limited sudo (edit with `sudo visudo`):**

```
backup_web_app ALL=(ALL) NOPASSWD: /usr/sbin/useradd, /usr/sbin/deluser, /usr/bin/smbpasswd, /usr/bin/systemctl restart smbd, /usr/bin/df, /usr/bin/ls, /usr/bin/python3, /usr/bin/tail, /usr/bin/getent
```

**Configure Samba:**

```bash
sudo nano /etc/samba/smb.conf
```

Append:

```ini
[TimeMachineBackups]
    comment = Time Machine Backups
    path = /srv/backups/timemachine
    valid users = backup_web_app
    read only = no
    vfs objects = catia fruit streams_xattr
    fruit:aapl = yes
    fruit:time machine = yes
    fruit:model = MacSamba
```

Restart Samba:

```bash
sudo systemctl restart smbd
```

---

### 3. Deploy the Web App

1. Copy `app.py` into `backup_web_app` home directory.
2. Add a `templates/` folder with `index.html` and `login.html`.
3. Run:

   ```bash
   python3 app.py
   ```

   App runs at:

   ```
   http://<VM_IP_ADDRESS>:5000
   ```

---

## 📂 Usage

### Web Dashboard

* Open browser → `http://<VM_IP_ADDRESS>:5000`
* Default login: `admin / password`
* Manage users & monitor backups

### macOS Finder

* Finder → `Cmd + K` → enter:

  ```
  smb://<VM_IP_ADDRESS>
  ```
* Login with backup user credentials
* Drag & drop files for manual backup

### Time Machine

1. Go to **System Settings > General > Time Machine**
2. Click **Add Backup Disk…**
3. Select the Samba share
4. Enter credentials → backups start automatically 🎉

---

## ✅ To-Do / Future Enhancements

* [ ] Add HTTPS support for Flask dashboard
* [ ] Configure email alerts for failed backups
* [ ] Add monitoring via `Prometheus` or `Grafana`

---

## 📜 License

This project is open-source and available under the MIT License.
