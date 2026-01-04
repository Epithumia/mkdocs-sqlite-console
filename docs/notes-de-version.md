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

### 1.0.7

- Correction d'un oubli dans pyproject.toml (dépendance manquante pour faire la documentation locale)
- Correction de typos.

### 2.0.0

- ADD - Support pour utilisation en tant que macro {{ sqlide(...) }}
- BREAKING: la syntaxe en cas de présence de mkdocs-macros-plugin change complètement. Cf. la documentation pour les changements à faire
- FIX - Compatibilité accrue avec PMT (merci @FredZinelli)
- CHANGE - Passage de SQL.js à la version 1.13.0

### 2.0.1

- FIX - les sqlides dans les admonitions repliées ??? n'étaient pas rendues correctement quand le sqlide était créés via les macros.
- FIX - les pages mélangeant les deux types de syntaxes (macros + ancienne syntaxes) pouvaient se retrouver avec des IDE non fonctionnels car les worker des espaces communs étaient insérés lors de la première insertions d'un "espace" sql, mais l'ordre des générations de code pouvait ne pas suivre l'ordre de lecture dans la page : toutes les macros d'abord, puis une seconde passe est faite pour les anciennes syntaxes.

- CHANGE - Changement de signature pour la macro, pour pouvoir utiliser qqes arguments positionnels, pour alléger les déclarations.
- CHANGE - Les macros insèrent maintenant un token dans la page, qui sera remplacé par du code html durant on_page_content (évite les problèmes de conversion md -> html de mkdocs -> FIX 1)
- CHANGE - Les workerinit sont ajoutés via on_page_context, juste sous les scripts et le css liés au sql du plugin, pour garantir qu'ils seront toujours dispo avant les sqlide de la page (FIX 2).
- CHANGE - Ajout de quelques commentaires ici et là dans le code, car la logique devient plus complexe...

- DOCS - Arguments de la macro
- DOCS - Ajout d'explication pour hide et autoexec
- DOCS - Exemple alternatif (arguments positionnels)

### 2.0.2

- FIX - MAJ automatique du rendu des IDE lors des changements d’onglets mkdocs/material.
- ADD - support pour les chemins relatifs au fichier markdown en cours (noms de fichiers sql)
- ADD - Ajouts de la logistique pour tester dans la doc
- CHANGE - Discover and add css and js files automatically
- CHANGE - Remove useless LIBS_PATH

### 2.0.3

- CHANGE - Mark as compatible with Python 3.9, update classifiers

### 2.1.0

- DEV - Add /js and /css to mkdocs watch directories

- ADD - Light/dark themes for the docs
- ADD - Hack to soften the background colors of sqlides in dark mode, without changing anything on CodeMirror side.
- ADD - Result tables are now sortable (hidden buttons)

- FIX - Unsilence errors during `load(...)` (which was a pain...)
- FIX - CSS - Gutters line numbers were going over the top menu header.

- CHANGE - Update SQLIDE class (renaming to SqlIde on the way)
- CHANGE - make `base` and `init` arguments work together.
- CHANGE - Reorganize `Counter.build_sql` so that the branches match the execution order in the JS layer.

- DOCS - Update docs with the new specs
- DOCS - Add dev tests (deactivated by default)
- DOCS - Suppress one `then`

### 2.1.1

- FIX - Missing CDN dependency

### 2.1.2

- FIX - More valid extensions for database files
