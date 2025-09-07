# macOS Backup Server with Web UI

### Project Objective
This project demonstrates a solution for storing macOS backups on a server, a common need for small businesses and home labs. It features a lightweight server setup that mimics a Network Attached Storage (NAS) device and a web-based dashboard for easy management.

### Use Case
The solution provides a centralized and secure location to store backups from multiple macOS systems, offering a simple web interface for an administrator to manage user accounts and files.

---

## Technical Overview

The project is a full-stack system composed of a backend server and a single-page web application.

* **Backend:** A Python Flask application runs on an **Ubuntu Server** instance, handling all server-side logic. It communicates with the host operating system using the `subprocess` module to perform administrative tasks.
* **Samba Integration:** The server uses the open-source Samba suite to provide a network share over the SMB protocol, which is natively compatible with macOS Time Machine.
* **Frontend:** A single HTML file serves as a dashboard, using JavaScript to interact with the Flask backend via JSON API endpoints. The user interface allows for managing users, uploading/downloading files, and monitoring server status.

---

## Getting Started

### Prerequisites
To run this project, you will need a host machine (like a Mac) and virtualization software to create a virtual server.

* **Virtualization Software:** [VirtualBox](https://www.virtualbox.org/) or [Parallels Lite](https://www.parallels.com/products/lite/)
* **Server OS:** [Ubuntu Server 22.04 LTS](https://ubuntu.com/download/server)

### Setup Instructions

#### Phase 1: Server and Service Setup
1.  **Create and Configure the VM:**
    * Install **VirtualBox** and create a new virtual machine.
    * Install **Ubuntu Server 22.04 LTS** on the VM.
    * Configure the VM's network adapter to **Bridged Adapter** in its settings. This places the VM on your local network.
    * Find the VM's IP address by logging in and running `ip a`. Note this address for all future connections.

2.  **Install Necessary Services:**
    * On the Ubuntu VM, install Samba and Python with:
        ```bash
        sudo apt update
        sudo apt install samba python3-pip python3-flask openssh-server
        ```

3.  **Configure Permissions and Users:**
    * Create a user for the web application (e.g., `backup_web_app`):
        ```bash
        sudo adduser backup_web_app
        sudo mkdir -p /srv/backups/timemachine
        sudo chown -R backup_web_app:backup_web_app /srv/backups/timemachine
        sudo chmod -R 775 /srv/backups/timemachine
        ```
    * Grant passwordless `sudo` privileges for specific commands to the `backup_web_app` user. Open the `sudoers` file for editing with `sudo visudo` and add the following line at the end:
        ```
        backup_web_app ALL=(ALL) NOPASSWD: /usr/sbin/useradd, /usr/sbin/deluser, /usr/bin/smbpasswd, /usr/bin/systemctl restart smbd, /usr/bin/df, /usr/bin/ls, /usr/bin/python3, /usr/bin/tail, /usr/bin/getent
        ```

#### Phase 2: Deploy the Web Application
1.  **Transfer Files:** Copy the provided `app.py` to the `backup_web_app` user's home directory (`~`). Create a `templates` directory in the same location and place `index.html` and `login.html` inside it.
2.  **Run the Server:** Log in as `backup_web_app` and run the Flask application:
    ```bash
    python3 app.py
    ```

#### Phase 3: Access and Use the Dashboard
1.  **Open the Dashboard:** On your Mac, open a web browser and navigate to `http://<VM_IP_ADDRESS>:5000`.
2.  **Login:** Use the hardcoded credentials for the administrator:
    * **Username:** `admin`
    * **Password:** `password`
3.  **Manage Users and Files:** Use the dashboard to create new backup users, upload/download files, and view server status.

### Connecting macOS for Backups
Files can be backed up using both the web dashboard and macOS's native **Connect to Server** functionality.
1.  **Connect via Finder:** On your Mac, press `Cmd + K`. Enter the server address `smb://<VM_IP_ADDRESS>` and log in with the credentials of a user you created via the dashboard.
2.  **Configure Time Machine:** Go to `System Settings` > `General` > `Time Machine` and select `Add Backup Disk...`. The server will appear as an option.

---

## Deliverables
* **Source Code:** This repository contains the full source code for the server setup and web interface, including:
    * `app.py`: The Python Flask backend.
    * `templates/index.html`: The single-page dashboard.
    * `templates/login.html`: The admin login page.
* **Documentation:** This README file serves as the primary documentation, outlining the project's purpose, setup steps, and functionality.
