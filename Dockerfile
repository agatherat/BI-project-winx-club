# Wybierz obraz bazowy z PrestaShop
FROM prestashop/prestashop:1.7.8

# Instalacja zależności, jeśli są potrzebne (np. MySQL Client, jeśli chcemy zainstalować bazę danych)
RUN apt-get update && apt-get install -y \
    mysql-client \
    && rm -rf /var/lib/apt/lists/*

# Kopiowanie plików aplikacji PrestaShop do kontenera
COPY ./html /var/www/html

# Kopiowanie kopii zapasowej bazy danych do kontenera
COPY ./backup.sql /tmp/backup.sql

# Ustawienie odpowiednich uprawnień dla plików
RUN chown -R www-data:www-data /var/www/html

# Konfiguracja bazy danych
# Wykonanie importu bazy danych (tylko jeśli backup.sql jest dostępny)
RUN mysql -h mysql -u root -p$MYSQL_ROOT_PASSWORD -e "CREATE DATABASE IF NOT EXISTS prestashop;"
RUN mysql -h mysql -u root -p$MYSQL_ROOT_PASSWORD prestashop < /tmp/backup.sql

# Expose port 80 (standardowy port HTTP)
EXPOSE 80

# Uruchomienie Apache w tle
CMD ["apache2-foreground"]
