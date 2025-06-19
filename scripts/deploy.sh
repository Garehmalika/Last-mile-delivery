#!/bin/bash
# Script de déploiement pour Last Mile Delivery - Production

set -e  # Arrêter en cas d'erreur

# Couleurs pour les messages
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
PROJECT_NAME="last-mile-delivery"
COMPOSE_FILE="docker-compose.prod.yml"
ENV_FILE=".env.production"
BACKUP_DIR="/backup"
LOG_FILE="/var/log/deploy.log"

# Fonctions utilitaires
log() {
    echo -e "${GREEN}[$(date +'%Y-%m-%d %H:%M:%S')] $1${NC}" | tee -a $LOG_FILE
}

error() {
    echo -e "${RED}[ERROR] $1${NC}" | tee -a $LOG_FILE
    exit 1
}

warning() {
    echo -e "${YELLOW}[WARNING] $1${NC}" | tee -a $LOG_FILE
}

info() {
    echo -e "${BLUE}[INFO] $1${NC}" | tee -a $LOG_FILE
}

# Vérification des prérequis
check_prerequisites() {
    log "Vérification des prérequis..."
    
    # Docker
    if ! command -v docker &> /dev/null; then
        error "Docker n'est pas installé"
    fi
    
    # Docker Compose
    if ! command -v docker-compose &> /dev/null; then
        error "Docker Compose n'est pas installé"
    fi
    
    # Fichier de configuration
    if [ ! -f "$ENV_FILE" ]; then
        error "Fichier $ENV_FILE introuvable"
    fi
    
    # Espace disque
    AVAILABLE_SPACE=$(df -BG . | awk 'NR==2 {print $4}' | sed 's/G//')
    if [ "$AVAILABLE_SPACE" -lt 5 ]; then
        error "Espace disque insuffisant (minimum 5GB requis)"
    fi
    
    log "Prérequis vérifiés avec succès"
}

# Sauvegarde des données
backup_data() {
    log "Sauvegarde des données..."
    
    # Créer le répertoire de sauvegarde
    mkdir -p $BACKUP_DIR/$(date +%Y%m%d_%H%M%S)
    BACKUP_PATH=$BACKUP_DIR/$(date +%Y%m%d_%H%M%S)
    
    # Sauvegarde de la base de données
    if docker-compose -f $COMPOSE_FILE ps postgres | grep -q "Up"; then
        info "Sauvegarde de PostgreSQL..."
        docker-compose -f $COMPOSE_FILE exec -T postgres pg_dump -U postgres lastmile_db > $BACKUP_PATH/database_backup.sql
    fi
    
    # Sauvegarde des modèles ML
    if [ -d "models" ]; then
        info "Sauvegarde des modèles ML..."
        cp -r models $BACKUP_PATH/
    fi
    
    # Sauvegarde des logs
    if [ -d "logs" ]; then
        info "Sauvegarde des logs..."
        cp -r logs $BACKUP_PATH/
    fi
    
    log "Sauvegarde complétée dans $BACKUP_PATH"
}

# Construire les images
build_images() {
    log "Construction des images Docker..."
    
    # Pull des images de base
    docker-compose -f $COMPOSE_FILE pull
    
    # Construction des images custom
    docker-compose -f $COMPOSE_FILE build --no-cache
    
    log "Images construites avec succès"
}

# Tests de santé
health_check() {
    log "Vérification de la santé des services..."
    
    local max_attempts=30
    local attempt=0
    
    while [ $attempt -lt $max_attempts ]; do
        if curl -f http://localhost/health &> /dev/null; then
            log "Service API opérationnel"
            break
        fi
        
        attempt=$((attempt + 1))
        info "Tentative $attempt/$max_attempts - En attente..."
        sleep 10
    done
    
    if [ $attempt -ge $max_attempts ]; then
        error "Le service n'a pas démarré correctement"
    fi
    
    # Test des autres services
    if curl -f http://localhost:3000 &> /dev/null; then
        log "Grafana opérationnel"
    else
        warning "Grafana n'est pas accessible"
    fi
}

# Déploiement principal
deploy() {
    log "Début du déploiement en production..."
    
    # Arrêt des services existants
    log "Arrêt des services existants..."
    docker-compose -f $COMPOSE_FILE down --remove-orphans
    
    # Nettoyage des volumes orphelins
    docker volume prune -f
    
    # Démarrage des services
    log "Démarrage des services..."
    docker-compose -f $COMPOSE_FILE --env-file $ENV_FILE up -d
    
    # Attendre que tous les services soient opérationnels
    log "Attente du démarrage des services..."
    sleep 30
    
    # Vérification de santé
    health_check
    
    log "Déploiement complété avec succès"
}

# Rollback en cas de problème
rollback() {
    warning "Rollback en cours..."
    
    # Arrêter les services actuels
    docker-compose -f $COMPOSE_FILE down
    
    # Restaurer depuis la dernière sauvegarde
    LATEST_BACKUP=$(ls -t $BACKUP_DIR | head -n1)
    if [ -n "$LATEST_BACKUP" ]; then
        log "Restauration depuis $LATEST_BACKUP"
        
        # Restaurer la base de données
        if [ -f "$BACKUP_DIR/$LATEST_BACKUP/database_backup.sql" ]; then
            docker-compose -f $COMPOSE_FILE up -d postgres
            sleep 20
            docker-compose -f $COMPOSE_FILE exec -T postgres psql -U postgres -d lastmile_db < $BACKUP_DIR/$LATEST_BACKUP/database_backup.sql
        fi
        
        # Restaurer les modèles
        if [ -d "$BACKUP_DIR/$LATEST_BACKUP/models" ]; then
            cp -r $BACKUP_DIR/$LATEST_BACKUP/models ./
        fi
    fi
    
    warning "Rollback terminé"
}

# Nettoyage des anciennes sauvegardes
cleanup() {
    log "Nettoyage des anciennes sauvegardes..."
    find $BACKUP_DIR -type d -mtime +30 -exec rm -rf {} \; 2>/dev/null || true
    docker system prune -f
    log "Nettoyage terminé"
}

# Affichage de l'aide
show_help() {
    echo "Usage: $0 [OPTION]"
    echo ""
    echo "Options:"
    echo "  deploy      Déployer l'application en production"
    echo "  rollback    Effectuer un rollback"
    echo "  backup      Sauvegarder les données"
    echo "  health      Vérifier la santé des services"
    echo "  cleanup     Nettoyer les anciennes données"
    echo "  logs        Afficher les logs"
    echo "  help        Afficher cette aide"
}

# Affichage des logs
show_logs() {
    docker-compose -f $COMPOSE_FILE logs -f --tail=100
}

# Menu principal
case "$1" in
    deploy)
        check_prerequisites
        backup_data
        build_images
        deploy
        cleanup
        ;;
    rollback)
        rollback
        ;;
    backup)
        backup_data
        ;;
    health)
        health_check
        ;;
    cleanup)
        cleanup
        ;;
    logs)
        show_logs
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        error "Option invalide. Utilisez '$0 help' pour voir les options disponibles."
        ;;
esac

log "Script terminé avec succès"