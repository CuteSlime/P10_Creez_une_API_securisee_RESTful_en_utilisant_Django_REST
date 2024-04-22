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
## Mise en place de l'environement de l'api

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
  Attributes : 
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
  Attributes : 
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

 - note : vous pourrez trouver un tableau résumant [les droits CRUD ici](https://github.com/CuteSlime/P10_Creez_une_API_securisee_RESTful_en_utilisant_Django_REST/blob/main/SoftDesk_Support/Doc/P10_model-table%20de%20permission.pdf)
### Users
les informations exposé ne sont que celles autorisé au partage par les utilisateurs.

#### liste
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

autorisé : 
  - authenticated user : `GET`, `POST`
  - guest : `POST`

- requête GET.
  ```
    /api/users/
  ```
- résultat
  ```json
    "count": `int`,
    "next": `url`,
    "previous": `url`,
    "results": [
        {
            "id": `int`,
            "username": `string`,
            "can_be_contacted": `boolean`,
            "can_data_be_shared": `boolean`,
            "created_time": `date`
        },
        ...
    ]
  ```

#### détail
``` 
  /api/users/1/
```
autorisé :
  - owner: `GET`, `PUT`, `PATCH`, `DELETE`
  - authenticated user: `GET`

- requête GET.
  ```
    /api/users/1
  ```
- résultat
  ```json
    {
        "id": `int`,
        "username": `string`,
        "can_be_contacted": `boolean`,
        "can_data_be_shared": `boolean`,
        "created_time": `date`
    }
  ```
### projects
#### liste
``` 
  /api/projects/
```
  Attributes:
    - `author` _CustomUser_ _required_ – L'auteur du projet.
    - `contributors` _CustomUser_ _optional_ – La Liste des contributeurs au projet.
    - `name` _string_ _required_ – Le nom du projet.
    - `description` _string_ _required_ – La description du projet.
    - `type` _string_ _required_ – Le type du projet (choix: ‘Back-end’, ‘Front-end’, ‘iOS’, ‘Android’).
    - `created_time` _date_ _auto-generated_ – La date de creation du projet.

autorisé : 
  - Authenticated user: `GET`, `POST`

- requête GET.
  ```
    /api/projects/
  ```
- résultat
  ```json
    "count": `int`,
    "next": `url`,
    "previous": `url`,
    "results": [
        {
            "id": `int`,
            "author": `CustomUser`,
            "name": `string`,
            "description": `string`,
            "type": `string`,
            "created_time": `date`
        },
        ...
    ]
  ```
#### détail
``` 
  /api/projects/12/
```
autorisé : 
  - Project author: `GET`, `PUT`, `PATCH`, `DELETE`
  - Project contributors: `GET`

- requête GET.
  ```
    /api/projects/12/
  ```
- résultat
  ```json
    {
        "id": `int`,
        "author": `CustomUser`,
        "contributors": [`CustomUser`, ...],
        "name": `string`,
        "description": `string`,
        "type": `string`,
        "created_time": `date`
    }
  ```

### issues
#### liste
``` 
  /api/projects/12/issues/
```
  Attributs : 
    - `author` _CustomUser_ _auto-fill_ – L’auteur du ticket. 
    - `assign_to` _CustomUser_ _optional_ – Assigné à. 
    - `project` _Project_ _auto-fill_ – Le projet associé. 
    - `title` _string_ _required_ – Le titre du ticket. 
    - `description` _string_ _required_ – La description du ticket. 
    - `statue` _string_ _required_ – Le statut du ticket (choix: ‘Todo’, ‘In progress’, ‘Finished’). 
    - `priority` _string_ _required_ – La priorité du ticket (choix: ‘Low’, ‘Medium’, ‘High’). 
    - `tag string` _required_ – Le tag du ticket (choix: ‘Bug’, ‘Feature’, ‘Task’). 
    - `created_time` _date_ _auto-generated_ – La date de creation du ticket.

autorisé :
  - Project contributors, Author: `GET`, `POST`

- requête GET.
  ```
    /api/projects/12/issues/
  ```
- résultat
  ```json
    "count": `int`,
    "next": `url`,
    "previous": `url`,
    "results": [
        {
            "id": `int`,
            "author": `CustomUser`,
            "assign_to": `CustomUser`,
            "title": `string`,
            "description": `string`,
            "statue": `string`,
            "priority": `string`,
            "tag": `string`,
            "created_time": `date`
        },
        ...
  ]
  ```
#### détail
``` 
  /api/projects/12/issues/2/
```
autorisé :
  - Issue author: `GET`, `PUT`, `PATCH`, `DELETE`
  - assign_to:  `GET`, `PATCH`
  - Project contributors: `GET`

- requête GET.
  ```
    /api/projects/12/issues/
  ```
- résultat
  ```json
    {
        "id": `int`,
        "author": `CustomUser`,
        "assign_to": `CustomUser`,
        "project": `Project`,
        "title": `string`,
        "description": `string`,
        "statue": `string`,
        "priority": `string`,
        "tag": `string`,
        "created_time": `date`
    }
  ```
  
### comments
#### liste
``` 
  /api/projects/12/issues/2/comments/
```
  Attributs : 
    - `author` _CustomUser_ _auto-fill_ – L’auteur du commentaire. 
    - `issue` _Issue_ _auto-fill_ – Le ticket associé. 
    - `description` _string_ _auto-fill_ – Le commentaire.
    - `uuid` _UUID _ _auto-generated_ – L’UUID du commentaire.
    - `created_time` _date_ _auto-generated_ – La date de creation du commentaire.


- requête GET.
  ```
    /api/projects/12/issues/2/comments/
  ```
- résultat
  ```json
    "count": `int`,
    "next": `url`,
    "previous": `url`,
    "results": [
        {
            "id": `int`,
            "author": `CustomUser`,
            "description": `string`,
            "created_time": `date`
        },
        ...
    ]
  ```
autorisé : 
  - Project contributors, Issue Author, Issue assign_to: `GET`, `POST`




#### détail
``` 
  /api/projects/12/issues/2/comments/1/
```
autorisé : 
  - Project contributors, Issue Author, Issue assign_to: `GET`
  - Comment Author: `GET`, `PUT`, `PATCH`, `DELETE`

- requête GET.
  ```
    /api/projects/12/issues/2/comments/
  ```
- résultat
  ```json
      {
          "id": `int`,
          "author": `CustomUser`,
          "issue": `Issue`,
          "description": `string`,
          "uuid": `UUID`,
          "created_time": `date`
      },

  ```

---
## Avertissement
Attention toute fois dans le cas de l'utilisation de l'api browser de DRF, il vous foudras utiliser le compte admin (créer le si ce n'ai pas déjà fait), du à un bug avec django 5 empéchant le fonctionnement du logout (et donc l'imposibilité de changer de compte).
La seul possibilité devenant l'utilisation de l'admin, et donc de ce connecter avec le compte admin.
Ce bug et propre à l'api browser intégrer de DRF et ne pauseras aucun soucie pour l'utilisation de postman ou autre.
