
# 🐳 Setting Up Valmont with Docker, PostGIS, and GeoServer

Follow these steps to install Docker, set up your environment, restore the Valmont database, and run the GeoServer app.

---

## 📥 1. Install Docker on your server

Follow the official guide to install Docker on Ubuntu:  
👉 [Official Docker Install Guide](https://docs.docker.com/engine/install/ubuntu/)

To run Docker commands **without typing `sudo`** every time, follow this DigitalOcean guide:  
👉 [Run Docker Without Sudo](https://www.digitalocean.com/community/tutorials/how-to-install-and-use-docker-on-ubuntu-20-04#step-2-executing-the-docker-command-without-sudo-optional)

---
## 2. Install Caddy Server on your server

Follow the official guide to [install Caddyserver on Ubuntu](https://caddyserver.com/docs/install)

## 3. Clone the project repository into your server:

```bash
git clone https://github.com/geoafrikana/valmont-recovery.git && cd valmont-recovery
```

## Note the absolute path of the project in your server:
```bash
pwd
```

## 📦 3. Upload workspace and raster backup files
Download the database, workspace and raster backups from [Google Drive](https://colab.research.google.com/drive/1_9mgDJHgBAK5PuApDJEIfZMnwKtsT6Lt?usp=sharing) to your local computer. Then upload them to your project folder on your server.
```bash
scp /local/path/to/valmont_workspace_backup.zip username@server_ip:<absolute_project_path>/valmont_workspace_backup.zip
scp /local/path/to/raster.zip username@server_ip:<absolute_project_path>/raster.zip
scp /local/path/to/db.sql username@server_ip:<absolute_project_path>/db.sql
```

### 4. Unzip the project on the server:
Back to the server, return to the project directory and unzip the workspace backup and raster data.

```bash
unzip valmont_workspace_backup.zip -d valmont_workspace_backup
unzip raster.zip -d raster
```
⚠️ Warning:
Depending on how the ZIP file was created, the first command may result in nested folders, like:

```bash
./valmont_workspace_backup/valmont_workspace_backup/
```

This structure will break the GeoServer restore process, as it expects the actual workspace contents directly inside ./valmont_workspace_backup.

✅ Check the folder after unzipping. If nested, flatten it using:
```bash
mv valmont_workspace_backup/valmont_workspace_backup/* valmont_workspace_backup/
rmdir valmont_workspace_backup/valmont_workspace_backup
```

---

## 🔐 5. Configure Environment Variables
Create a .env file in your project folder and populate it with the right values according to .env.template
Then explicitly export the variables to ensure they're available.

```bash
source .env
```

## 🐳 6. Start Services with Docker Compose

Run the `docker-compose` script to:

- Start the PostGIS database
- Load the backup data
- Start the GeoServer application

```bash
docker compose up -d
```

---

## 🔑 7. Secure Your Database

### Connect to the PostGIS shell and change the user password (optional but **recommended**):

```bash
psql -U $db_user -d $db_name -h localhost -c "ALTER USER ${db_user} WITH PASSWORD 'mysuperstrongpassword';"
```

> Replace `mysuperstrongpassword` with your own secure password.

---

## 8. Start the Caddy server

```bash
caddy run --config $(pwd)/Caddyfile
```
Note that the above command will run Caddy in the foreground. To run it in the background, use nohup, screen for better still, systemd.

## 🌍 9. Access GeoServer

Open GeoServer in your browser:

```bash
http://server_ip:8080/geoserver
```
or
```bash
https://your_domain_name/geoserver
```

## 🔧 10. Update PostGIS Credentials in GeoServer

### - Login credentials:
- **Username:** `$geoserver_user` (from your `.env` file)
- **Password:** `$geoserver_admin_password` (from your `.env` file)

> ⚠️ On first login, **change the master password** as recommended by GeoServer.

---

1. In GeoServer, go to **Data → Stores**.
2. Click on the `valmontp` store.
3. Update the password to the new PostGIS password you chose in `step 5` above or the default password in `$db_password`.
4. Click **Apply**, then **Save**.

If you see **no error message**, the password is correct.

---
Next, update the PostGIS host configuration in Geoserver.
Since both containers are in the same Docker network, they can reference each other by their container names.

In the new GeoServer instance:
- Go to **Data → Stores → valmontp**
- Change the **host** field to `postgis`
- Click **Apply**, then **Save** 

# Troubleshooting

1. Workspace data is outdated: The above instruction uses the last restored data from the corrupt Digital Ocean droplet. Contact admin for permissions to the monthly backups on OVH.
2. Geoserver not available in browser: check your firewall configuration and ensure you have allowed port 80 and 443 or http and https
2. Check Docker logs for issues.
