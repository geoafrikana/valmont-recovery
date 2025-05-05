
# 🐳 Setting Up Valmont with Docker, PostGIS, and GeoServer

Follow these steps to install Docker, set up your environment, restore the Valmont database, and run the GeoServer app.

---

## 📥 1. Install Docker

Follow the official guide to install Docker on Ubuntu:  
👉 [Official Docker Install Guide](https://docs.docker.com/engine/install/ubuntu/)

To run Docker commands **without typing `sudo`** every time, follow this DigitalOcean guide:  
👉 [Run Docker Without Sudo](https://www.digitalocean.com/community/tutorials/how-to-install-and-use-docker-on-ubuntu-20-04#step-2-executing-the-docker-command-without-sudo-optional)

---
## 2. Install Caddy Server

Follow the official guide to [install Caddyserver on Ubuntu](https://caddyserver.com/docs/install)

## 📦 3. Upload and Extract Project Files

### Upload the zip file to your server:

```bash
scp /local/path/to/valmont.zip username@server_ip:/destination/path/valmont.zip
```

### 4. Unzip the project on the server:

```bash
unzip valmont.zip -d valmont && cd valmont/
```

---

## 🔐 5. Configure Environment Variables

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
caddy run --config /path/to/Caddyfile
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
