#!/bin/bash

BACKUP_DIR="./backups/$(date +%Y%m%d_%H%M%S)"
RETENTION_DAYS=7

echo "💾 Début de la sauvegarde..."

# Création du répertoire de sauvegarde
mkdir -p $BACKUP_DIR

# Sauvegarde de la base de données
echo "📊 Sauvegarde de la base de données..."
docker-compose -f docker-compose.prod.yml exec -T postgres pg_dump \
    -U ${DB_USER} ${DB_NAME} | gzip > $BACKUP_DIR/database.sql.gz

# Sauvegarde des données Redis
echo "📝 Sauvegarde du cache Redis..."
docker-compose -f docker-compose.prod.yml exec -T redis redis-cli \
    --rdb /data/dump.rdb BGSAVE
docker cp $(docker-compose -f docker-compose.prod.yml ps -q redis):/data/dump.rdb \
    $BACKUP_DIR/redis_dump.rdb

# Sauvegarde des fichiers de configuration
echo "⚙️  Sauvegarde des configurations..."
cp -r ./nginx $BACKUP_DIR/
cp docker-compose.prod.yml $BACKUP_DIR/
cp .env $BACKUP_DIR/

# Nettoyage des anciennes sauvegardes
echo "🧹 Nettoyage des anciennes sauvegardes..."
find ./backups -type d -mtime +$RETENTION_DAYS -exec rm -rf {} +

echo "✅ Sauvegarde terminée: $BACKUP_DIR"