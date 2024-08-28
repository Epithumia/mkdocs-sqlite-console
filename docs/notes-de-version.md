# Historique des versions

## 1.0.0

- Version initiale.

## 1.0.1

- Correction de problèmes de chemins.
- Documentation complétée.

### 1.0.1a

- Inclusion des fichiers css/\* et js/\* dans l'installation.

## 1.0.2

- Cohabitation possible avec le plugin `macros`.
- La commande `mkdocs build` requiert explicitement que `site_url` soit configuré.

## 1.0.3

- Possibilité de partager un worker entre plusieurs IDE pour exécuter différentes séquences sur la même BDD.

## 1.0.4

- Possibilité d'autoexécuter le code sql pré-saisi dans la console.

### 1.0.4b

- Petite modification d'un message pour clarifier que la requête n'e renvoie pas de résultat.

### 1.0.4c

- Modification de l'injection des scripts/CSS pour que le CSS puisse être customisé.

## 1.0.5

- Possibilité de cacher l'IDE pour ne garder que les résultats des requêtes

### 1.0.5a

- Correction d'un problème d'affichage si pyodide-mkdocs est utilisé.

### 1.0.5b

- Dirty Fix (merci F. Zinelli) pour rendre le plugin compatible avec [pyodide-mkdocs-theme](https://frederic-zinelli.gitlab.io/pyodide-mkdocs-theme/).

### 1.0.6

- Publié sur PyPi
