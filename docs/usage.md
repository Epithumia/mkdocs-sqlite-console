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


## Afficher la console/IDE

On peut afficher une console/IDE SQLite grâce à la commande `{{ sqlide paramètres }}`. Cette commande accepte quatre paramètres, tous optionnels :

- un *titre* : par exemple `titre="Exercice 1"`. Par défaut, le titre est "sql"
- un chemin vers un script SQL d'initialisation *init* : par exemple `init=sql/init.md`
- un chemin vers une *base* SQLite : par exemple `bases/test.db`
- un chemin vers un fichier de code *sql* pré-saisi dans l'IDE : par exemple `sql="sql/code.sql"`

!!! tip "Astuce"
    A part pour le titre, les apostrophes ou guillemets sont optionnels. Ainsi, `sql="sql/code.sql"`,
    `sql='sql/code.sql'` et `sql=sql/code.sql` sont équivalents.

!!! warning "Attention"
    - le titre *doit* être entre guillemets
    - les chemins vers les fichiers sont relatifs à la racine du site
    - les chemins ne peuvent pas contenir d'espace

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
{{sqlide titre="IDE avec une base binaire chargée et code pré-saisi" base="bases/test.db" sql="sql/code.sql" }}
```

{{sqlide titre="IDE avec une base binaire chargée et code pré-saisi" base="bases/test.db" sql="sql/code.sql" }}

#### Utilisation dans les *admonitions* de mkdocs-materiel

On peut appeler le code à l'intérieur d'un admonition :

```markdown
!!! sql "Bloc accordéon avec initialisation et code pré-saisi"
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

```markdown
!!! sql "Bloc adminition avec initialisation et code pré-saisi"
    {{ sqlide titre="Init + Code" init="sql/init1.sql" sql="sql/code.sql" }}
```

!!! bug
    Les blocs ne s'affichent pas correctement dans les adminitions qui sont repliées par défaut:
    ```markdown
    ??? sql "Bloc admonition avec initialisation et code pré-saisi"
        {{ sqlide titre="Init + Code" init="sql/init1.sql" sql="sql/code.sql" }}
    ```
    Il faut cliquer sur le champ de texte pour que l'IDE s'affiche (incorrectement).
    ??? sql "Bloc admonition avec initialisation et code pré-saisi"
        {{ sqlide titre="Init + Code" init="sql/init1.sql" sql="sql/code.sql" }}

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
