FROM prestashop/prestashop:1.7.8

COPY certs/localhost.crt /etc/ssl/certs/localhost.crt
COPY certs/localhost.key /etc/ssl/private/localhost.key

RUN a2enmod ssl && a2ensite default-ssl && \
    sed -i 's|SSLCertificateFile.*|SSLCertificateFile /etc/ssl/certs/localhost.crt|' /etc/apache2/sites-available/default-ssl.conf && \
    sed -i 's|SSLCertificateKeyFile.*|SSLCertificateKeyFile /etc/ssl/private/localhost.key|' /etc/apache2/sites-available/default-ssl.conf

EXPOSE 443
