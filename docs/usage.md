# Utilisation

## Activer le plugin

Ajouter dans votre fichier `mkdocs.yml`:
```yaml
plugins:
  - search
  - sqlite-console
```

!!! note 
    Si vous n'avez aucune entrée dans la section `plugins` de votre fichier de configuration, 
    vous voudrez sans doute ajouter le plugin `search`. MkDocs l'active par défaut s'il n'y a pas 
    d'autres `plugins`, et dans le cas contraire, MkDocs demande de l'activer explicitement.

Si vous voulez déployer votre site (à l'aide de `mkdocs build` ou `mkdocs gh-deploy`), il faut également ajouter à votre
fichier `mkdocs.yml` une ligne du type
```yaml
site_url: https://monsite.url/chemin
```
Par exemple, ce site est configuré avec
```yaml
site_url: https://epithumia.github.io/mkdocs-sqlite-console
```

!!! error "site_url"
    Si vous n'avez pas défini la variable `site_url` dans votre fichier `mkdocs.yml`, les commandes 
    `mkdocs build` et `mkdocs gh-deploy` ne fonctionneront pas et signaleront la nécessité de le faire.

## Afficher la console/IDE

On peut afficher une console/IDE SQLite grâce à la commande `{{ sqlide paramètres }}`. Cette commande accepte quatre paramètres, tous optionnels :

- un *titre* : par exemple `titre="Exercice 1"`. Par défaut, le titre est "sql"
- un chemin vers un script SQL d'initialisation *init* : par exemple `init=sql/init.md`
- un chemin vers une *base* SQLite : par exemple `bases/test.db`
- un chemin vers un fichier de code *sql* pré-saisi dans l'IDE : par exemple `sql="sql/code.sql"`
- si le mot clef *autoexec* est présent, alors le contenu de code sera exécuté comme si l'utilisateur avit cliqué le bouton

!!! tip "Astuce"
    A part pour le titre, les apostrophes ou guillemets sont optionnels. Ainsi, `sql="sql/code.sql"`,
    `sql='sql/code.sql'` et `sql=sql/code.sql` sont équivalents.

!!! warning "Attention"
    - le titre *doit* être entre guillemets
    - les chemins vers les fichiers sont relatifs à la racine du site
    - les chemins ne peuvent pas contenir d'espace
    - les options base et init sont mutuellement exclusives ; l'option base est prioritaire. 

### Quelques exemples

#### Affichage basique

Pour afficher un IDE avec du code SQL d'initialisation et du code pré-saisi :
```markdown
{{ sqlide titre="IDE avec initialisation et code pré-saisi" init="sql/init1.sql" sql="sql/code.sql" }}
```

On obtient l'affichage ci-dessous :

{{ sqlide titre="IDE avec initialisation et code pré-saisi" init="sql/init1.sql" sql="sql/code.sql" }}

On peut aussi charger une base directement :

```markdown
{{sqlide titre="IDE avec une base binaire chargée et code pré-saisi autoexécuté" base="bases/test.db" sql="sql/code.sql" autoexec}}
```

{{sqlide titre="IDE avec une base binaire chargée et code pré-saisi autoexécuté" base="bases/test.db" sql="sql/code.sql" autoexec}}

#### Cacher l'IDE

Si l'on ne veut que le résultat de la requête sans pour autant afficher l'IDE, il suffit d'ajouter l'option *hide* :

```markdown
{{sqlide titre="IDE avec une base binaire chargée et code pré-saisi autoexécuté, IDE caché" base="bases/test.db" sql="sql/code.sql" autoexec hide}}
```

{{sqlide titre="IDE avec une base binaire chargée et code pré-saisi autoexécuté, IDE caché" base="bases/test.db" sql="sql/code.sql" autoexec hide}}

!!! warning "Titre"
    Attention, le titre n'est plus affiché dans ce cas.

#### Base partagée entre plusieurs consoles

Il est possible de donner un argument supplémentaire pour partager une base entre plusieurs consoles/IDE :

```markdown
{{ sqlide titre="IDE avec initialisation dans l'espace bdd1" init="sql/init1.sql" espace="bdd1" }}

{{ sqlide titre="IDE sans initialisation, avec code pré-saisi, dans l'espace bdd1" sql="sql/code.sql" espace=bdd1}}
```

{{ sqlide titre="IDE avec initialisation dans l'espace bdd1" init="sql/init1.sql" espace="bdd1" }}

{{ sqlide titre="IDE sans initialisation, avec code pré-saisi, dans l'espace bdd1" sql="sql/code.sql" espace=bdd1}}

#### Utilisation dans les *admonitions* de mkdocs-material

On peut appeler le code à l'intérieur d'une admonition :

```markdown
!!! sql "Bloc admonition avec initialisation et code pré-saisi"
    {{ sqlide titre="Init + Code" init="sql/init1.sql" sql="sql/code.sql" }}
```

donne :

!!! sql "Bloc admonition avec initialisation et code pré-saisi"
    {{ sqlide titre="Init + Code" init="sql/init1.sql" sql="sql/code.sql" }}

```markdown
???+ sql "Bloc accordéon avec initialisation et code pré-saisi"
    {{ sqlide titre="Init + Code" init="sql/init1.sql" sql="sql/code.sql" }}
```
donne

???+ sql "Bloc accordéon avec initialisation et code pré-saisi"
    {{ sqlide titre="Init + Code" init="sql/init1.sql" sql="sql/code.sql" }}


!!! bug
    Les blocs ne s'affichent pas correctement dans les admonitions qui sont repliées par défaut :
    ```markdown
    ??? sql "Bloc admonition avec initialisation et code pré-saisi"
        {{ sqlide titre="Init + Code" init="sql/init1.sql" sql="sql/code.sql" }}
    ```
    Il faut cliquer sur le champ de texte pour que l'IDE s'affiche (incorrectement).
    ??? sql "Bloc admonition avec initialisation et code pré-saisi"
        {{ sqlide titre="Init + Code" init="sql/init1.sql" sql="sql/code.sql" }}

### Usage avec le plugin [macros](https://mkdocs-macros-plugin.readthedocs.io/en/latest/)

Le plugin macros utilise les doubles accolades pour définir ses propres blocs de code, ce qui empêche ce plugin de 
fonctionner normalement. En conséquence, quand le plugin macros est détecté, la syntaxe change et l'IDE SQLite est
chargée avec la syntaxe suivante :
```markdown
{!{ sqlide paramètres }!}
```
Par exemple `{!{ sqlide titre="IDE avec initialisation et code pré-saisi" init="sql/init1.sql" sql="sql/code.sql" }!}`
affichera :

{{ sqlide titre="IDE avec initialisation et code pré-saisi" init="sql/init1.sql" sql="sql/code.sql" }}

### Erreurs

Le plugin détectera les fichiers non existants :

```markdown
{{sqlide titre="Erreur fichier base manquant" base=bases/basem.db sql=sql/code1.sql }}

```

{{sqlide titre="Erreur fichier base manquant" base=bases/basem.db sql=sql/code1.sql }}

```markdown
{{sqlide titre="Erreur fichier sql manquant" init=sql/initm.sql sql=sql/codem.sql }}
```

{{sqlide titre="Erreur fichier sql manquant" init=sql/initm.sql sql=sql/codem.sql }}
