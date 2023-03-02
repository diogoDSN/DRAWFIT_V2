
mkdir .certificates
cd .certificates

# Create root certificate
openssl req -new -nodes -text -out drawfit.csr -keyout drawfit.key -subj "/CN=drawfit"
chmod og-rwx drawfit.key

openssl x509 -req -in drawfit.csr -text -days 3650 \
  -extfile /etc/ssl/openssl.cnf -extensions v3_ca \
  -signkey drawfit.key -out drawfit.crt

rm drawfit.csr

# Create db certificate

openssl req -new -nodes -text -out drawfit_db.csr \
  -keyout drawfit_db.key -subj "/CN=drawfit_db"
chmod og-rwx drawfit_db.key

openssl x509 -req -in drawfit_db.csr -text -days 3000 \
  -CA drawfit.crt -CAkey drawfit.key -CAcreateserial \
  -out drawfit_db.crt

rm drawfit_db.csr
