# Galerie Ponthé

## Rôle de la galerie

La galerie Ponthé est un site web géré par le club Ponthé de l'Ecole des Ponts ParisTech. Il permet aux étudiants de l'école d'accéder aux photos prises par les membres du club lors des différents évènements.

## Documentation

La galerie se compose :
- d'un backend Django
- d'un frontend React
- d'une gestion du traffic ainsi que du service des statics et des medias par l'intermédiaire de Nginx
- d'un déploiement avec gestion des dépendances entièrement géré par Docker

### Déploiement

Importer le repository git avec la commande :
```
git clone git@github.com:adcrry/gallery-website.git
```

Configurer le .env avec les variables adéquates

<ins>**NB :**</ins> Ne pas oublier de modifier la 'SECRET_KEY' ainsi que le mot de passe de la base de donnée 'DB_PASSWORD'

Lancer l'ensemble des services de la galerie (back, db, webinstaller et nginx pour le déploiement en production) à l'aide de docker compose (et  pas docker-compose !) :
```
docker compose -f docker-compose-prod.yml up --build -d
```

Lorsque le build et le lancement sont terminés, il est possible de stoper et de relancer la galerie à l'aide des commandes suivantes :
```
docker compose -f docker-compose-prod.yml start
docker compose -f docker-compose-prod.yml stop
```

Si des modifications sont appliquées notamment au niveau du Docker, il est nécessaire de reconstruire les images afin d'appliquer les modifications, pour cela, il est possible d'utiliser :
```
docker compose -f docker-compose-prod.yml up --build -d
```
OU
```
docker compose -f docker-compose-prod.yml build
docker compose -f docker-compose-prod.yml start
```
### Problèmes de déploiement

Lors du lancement des commandes précédentes, il est possible que dans certains cas, le serveur ne démarre pas.

Si vous souhaitez détecter les potentielles erreurs de déploiement, vous pouvez excécutez la commande suivante :
```
docker compose -f docker-compose-prod.yml up --build
```

1)``` Access denied to '/src/galerie/static/react/'```
Deux options sont possibles : simplement supprimer le dossier en question dans le repo, ou de manière plus brutale, donner toutes les permissions au dossier avec
```
chmod -r 777 /src/galerie/static/react/
```

2)```Tempory failure in name resolution```
Ce problème provient de la base de données qui n'arrive pas à être détécté par Django. Cela peut provenir d'un changement de l'adresse de la base de données.

La solution est souvent de supprimer le dossier ```database/``` et de relancer le déploiement.

3)```Could not connect to server: Connection refused```
Ce problème est dû à un changement du mot de passe de la base de données sans avoir supprimé le dossier ```database/```.

3)``` [emerg] host not found in upstream 'back:8000'```
Cette erreur est souvent engendrée par un problème préalable dans le déploiement. Si aucun autre problème n'est observable, la meilleure solution est de réinstaller le repo et de lancer la commande de déploiement.

### Backend

Le backend du site est développé en Python avec le framework Django. Le gestionnaire de dépendance utilisé est Poetry. Le back tourne dans un container docker et permet de servir les pages publiques contenant du code JS issue d'un bundle React. Le back sert également une API utile pour accéder aux données depuis le front.
En prod, le container back lance un serveur gunicorn qui fait le lien entre NGINX et le serveur Django Python.
Afin de faciliter le chargement de nouvelles galeries, le back contient aussi un serveur redis et celery permettant d'effectuer des tâches de mainère asynchrône. Cette fonctionnalité permet d'éviter de recevoir un timeout de NGINX lorsque l'upload est longue.

### Frontend

Le frontend du site est développé en JavaScript avec le framework React. Les fichiers JS sont, lors du lancement du container webinstaller, ajoutés dans des fichiers "bundles" qui sont placés dans le dossier ```/src/galerie/static/react/``` du back qui pourra ensuite les intégrer dans les templates html. Ces bundles contiennent l'ensemble du contenu React.

### Nginx

Lorsqu'une requête entrante est dirrigé vers ponthe.enpc.org, le serveur NGINX de Ponster la redirige vers le serveur NGINX hebergé dans un container docker qui ensuite redirigé la requête vers gunicorn ou sert directement si il s'agit de statics ou de medias. 

### Docker

L'ensemble des containers, leurs connections entre eux et leurs données persistantes sont gérés par docker compose.

Les services en prod sont les suivants :
  - base de données avec PostgreSQL
  - backend Django/Gunicorn/Redis/Celery
  - frontend ReactJS
  - gestionnaire de traffic NGINX

Concernant les volumes, les dossiers ```database/```, ```media/``` et ```backups/``` sont toujours (en dev ou prod) liés aux containers en temps réel. En dev, l'ensemble des dossiers ```back/``` et ```react/``` sont aussi liés aux containers en temps réel, ce qui permet de pouvoir update le serveur Django ou le webinstaller sans redémarrer les services. Le dossier ```/src/galerie/static/react/``` est lui toujours un volume permanent (conservé après arrêt des services), et à celà se rajoute le dossier ```/src/static``` en prod qui permet de faire le lien entre le serveur Django et NGINX pour servir les statics.

L'ensemble des variables d'environnement sont contenus dans le fichier ```.env``` que l'on peut modifier à sa convenance.

<ins>**NB :**</ins> Si la variable DB_PASSWORD est modifié assurez-vous de supprimer le dossier ```database/``` car celui-ci ne sera pas recréer !
