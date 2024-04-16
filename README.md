# P10_Creez_une_API_securisee_RESTful_en_utilisant_Django_REST

Projet numéro10 du parcour OpenClassrooms "développeur d'application python"


---
## dépendance
Le projet utilise pipenv pour gérer l'environement virtuel et les dépendances.
celui ci peut être installer ainsi :
```bash
  pip install pipenv
```
Le projet a été créé en utilisant 
- Python 3.12.
- django 5
- django rest framework 3.15.

les package suplémentaire sont : 
- djangorestframework-simplejwt
- drf-nested-routers


---
## installer le projet (Windows)

- Commencer par cloner le projet avec git clone

- A la racine du projet (la ou ce trouve le .git) créer votre environement virtuel :
    ```
    pipenv shell
    ```
  la même commande activera celui-ci si il existe déjà.

- Installer toute les dépendances :
    ``` 
    pipenv install
    ```
    
- allez au dossier de l'application :
    ```
    cd SoftDesk_Support
    ```
- vous pouvez désormais lancer le projet avec la commande : 
  ```
    py manage.py runserver
  ```

L'api peut désormais être utilisé. 


---
##mise en place de l'environement de l'api

tout les chemin d'api commence par l'adresse du serveur django suivit de `/api/`
exemple :
```
  http://localhost:8000/api/
```

pour utiliser l'api il faut tout d'abord créer un compte utilisateur 
- requête POST.
  ```
    /api/users/
  ```
  attribut : 
    - `username` _string_ _required_ -- nom de l'utilisateur.
    - `password` _string_ _required_ -- mot de passe de l'utilisateur.
    - `age` _integer_ _required_ -- age de l'utilisateur (doit avoir 16 ans et plus).
    - `mail` _string_ _optional_ -- adresse mail de l'utilisateur.
    - `can_be_contacted` _boolean_ _optional_ -- l'utilisateur accepte t'il d'être contacté ? non par défaut.
    - `can_data_be_shared` _boolean_ _optional_ -- l'utilisateur accepte t'il de partager ses information ? non par défaut.

pour acceder à l'api il faut avoir un token
- requête POST.
  ```
    /api/token/
  ```
  attribut : 
    - `username` _string_ _required_ -- nom de l'utilisateur.
    - `password` _string_ _required_ -- mot de passe de l'utilisateur.
- résultat
  ```json
    {
      "refresh": "HEADER:(ALGORITHM & TOKEN TYPE).PAYLOAD:(DATA).VERIFY SIGNATURE",
      "access": "HEADER:(ALGORITHM & TOKEN TYPE).PAYLOAD:(DATA).VERIFY SIGNATURE"
    }
  ```

celui ci peut ensuite être renouvelé via le refresh
- requête POST.
  ```
    /api/token/refresh/
  ```
  attribut : 
    - `refresh` _string_ _required_ -- le token `refresh` de la requête précédente.
- résultat
  ```json
    {
      "access": "HEADER:(ALGORITHM & TOKEN TYPE).PAYLOAD:(DATA).VERIFY SIGNATURE"
    }
  ```

ce token doit être fournie dans le header de chaque requête en guise d'`authorization`


---
## Utilisation de l'api
### Users
#### liste
``` 
  /api/users/
```
autorisé : `GET`, `POST`

#### détail
``` 
  /api/users/1/
```
autorisé : `GET`, `PUT`, `PATCH`, `DELETE`

### projects
#### liste
``` 
  /api/projects/
```
autorisé : `GET`, `POST`

#### détail
``` 
  /api/projects/12/
```
autorisé : `GET`, `PUT`, `PATCH`, `DELETE`

### issues
#### liste
``` 
  /api/projects/12/issues/
```
autorisé : `GET`, `POST`

#### détail
``` 
  /api/projects/12/issues/2/
```
autorisé : `GET`, `PUT`, `PATCH`, `DELETE`

### comments
#### liste
``` 
  /api/projects/12/issues/2/comments/
```
autorisé : `GET`, `POST`

#### détail
``` 
  /api/projects/12/issues/2/comments/1/
```
autorisé : `GET`, `PUT`, `PATCH`, `DELETE`


---
## Avertissement
Attention toute fois dans le cas de l'utilisation de l'api browser de DRF, il vous foudras utiliser le compte admin (créer le si ce n'ai pas déjà fait), du à un bug avec django 5 empéchant le fonctionnement du logout (et donc l'imposibilité de changer de compte).
La seul possibilité devenant l'utilisation de l'admin, et donc de ce connecter avec le compte admin.
Ce bug et propre à l'api browser intégrer de DRF et ne pauseras aucun soucie pour l'utilisation de postman ou autre.
