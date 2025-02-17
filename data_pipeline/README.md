# README for the data_pipeline

## Connection a Scaleway via boto3 pour stockage cloud

Il faut créer un fichier .env dans le dossier data_pipeline/config avec les secrets ci dessous pour que la connection fonctionne.

```text
SCW_ACCESS_KEY={ACCESS_KEY}
SCW_SECRET_KEY={SECRET_KEY}
REGION_NAME={REGION_NAME}
BUCKET_NAME={BUCKET_NAME}
```
Vous trouverez un example avec le fichier [.env.example](config/.env.example)
