# BI-project-winx-club

created by: [Agnieszka Kulesz](https://github.com/agatherat), [Michella Miłecka](https://github.com/michellamilecka), [Alicja Lendzioszek](https://github.com/alicjalendzioszek), [Hania Gibus](https://github.com/haniagibus)

## Project description
The project for the subject "E-Business 2024/2025," consists of two stages in which students are tasked with creating an online store based on PrestaShop software.

## Prerequisites
1. Install [Docker](https://docs.docker.com/engine/install/)
2. Clone repository: `git clone https://github.com/agatherat/BI-project-winx-club.git`
3. [Create self-signed SSL certificate](#create-self-signed-ssl-certificate-for-windows)

## How to run
1. 

## Setup and Configuration Tips


## Setup and Configuration Tips
### Dependencies 
- PrestaShop [1.7.8](https://github.com/PrestaShop/PrestaShop/releases/download/1.7.8.11/prestashop_1.7.8.11.zip)
- Python 3.11
- Java 

### Create self-signed SSL certificate _(for Windows)_
_**Prerequisites:** WSL (Windows Subsystem for Linux)_

1. Run the following command in **WSL** to create a self-signed SSL certificate (`localhost.crt`) and private key (`localhost.key`):
```shell
openssl req -x509 -out localhost.crt -keyout localhost.key -newkey rsa:2048 -nodes -sha256 -subj '/CN=localhost'
```
2. Move SSL certificate and private key files to project tree in `./certs/`
3. To ensure your browser trusts the self-signed certificate, import it into the Windows certificate store using **PowerShell**:
```powershell
Import-Certificate -FilePath 'path\to\cert\localhost.crt' -CertStoreLocation Cert:\CurrentUser\Root\
```
