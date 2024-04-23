# Projet "Gestion de Livres"

Ce projet vise à créer une API de gestion de livres en utilisant FastAPI, une bibliothèque web Python rapide. L'API permet de créer, lire, mettre à jour et supprimer des livres dans une base de données simulée.

## Fonctionnalités principales

- **Affichage des livres** : L'API fournit des points de terminaison pour afficher tous les livres ainsi que le nombre total de livres disponibles.
- **Ajout de nouveaux livres** : Les utilisateurs peuvent ajouter de nouveaux livres en fournissant le nom, l'auteur et l'éditeur du livre.
- **Suppression de livres** : Les livres existants peuvent être supprimés en spécifiant leur identifiant.
- **Mise à jour des livres** : Les informations d'un livre peuvent être mises à jour en fournissant son identifiant ainsi que les détails mis à jour.

## Instructions d'utilisation
1. **Activer la varible d'envirnnement** : la variable d'environnement env est présent dans le repository, pour l'activer, lancez la cmmande `.\env\Scripts\activate`
2. **Installation des dépendances** : Assurez-vous d'avoir Python installé sur votre système `python --version` que vous êtes bien sur le chemin indiqué en éxécutant `where python`. Ensuite, installez les dépendances du projet en exécutant `pip install -r requirements.txt`.

3. **Démarrage du serveur** : Lancez le serveur en exécutant `uvicorn app.main:app --reload`. Cela lancera le serveur sur `http://localhost:8000`.

4. **Utilisation de l'API** : Vous pouvez maintenant accéder à l'API en utilisant les points de terminaison fournis dans le fichier `books.py`. Par exemple, pour afficher tous les livres, visitez `http://localhost:8000/books/`la page s'affiche clair sans utiliser la documentation interactive automatique de l'API (fournie par Swagger UI), pour l'avoir visiter `http://localhost:8000/docs#/books/`.

## Les Étapes pour Utiliser les Fonctionnalités CRUD avec FastAPI

Pour utiliser les fonctionnalités CRUD (Create, Read, Update, Delete) avec FastAPI une fois que les fonctionnalités ont été créées, suivez ces étapes simples :

1. **Clonage du Dépôt :**
   ```
   git clone <URL_DU_DÉPÔT>
   ```

2. **Installation des Dépendances :**
   ```
   cd <NOM_DU_PROJET>
   pip install -r requirements.txt
   ```

3. **Démarrage du Serveur FastAPI :**
   ```
   uvicorn app.main:app --reload
   ```

4. **Exploration de la Documentation Swagger :**
   - Accédez à `http://localhost:8000/docs#/Books` dans votre navigateur pour découvrir la documentation interactive Swagger UI.
   - Consultez la documentation pour connaître les points de terminaison disponibles ainsi que les schémas des données acceptées et retournées.

5. **Utilisation des Points de Terminaison CRUD :**
   - Utilisez les différents points de terminaison pour effectuer les opérations CRUD sur les ressources du projet (livres, utilisateurs, etc.).
   - Testez les requêtes HTTP (GET, POST, PUT, DELETE) en utilisant les paramètres appropriés et en vous référant à la documentation pour les formats attendus.

6. **Validation et Tests :**
   - Validez le fonctionnement des fonctionnalités CRUD en créant, lisant, mettant à jour et supprimant des éléments du système.
   - Assurez-vous que les opérations CRUD fonctionnent comme prévu pour différents cas d'utilisation et scénarios.

7. **Partager vos Retours :**
   - Vos retours d'expérience et vos suggestions sont les bienvenus ! N'hésitez pas à partager vos impressions ou à poser des questions dans les discussions du dépôt.