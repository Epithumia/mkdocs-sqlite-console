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

!!! note "Utilisation avec `mkdocs-macros-plugin` ou Pyodide-MkDocs-Theme"

    Noter que le plugin `mkdocs-sqlite-console` doit toujours être référencé après les plugins de PMT ou des macros, dans le fichier `mkdocs.yml` :<!-- markdownlint-disable-line MD046 -->

    ```yaml
    plugins:
        - search
        - macros            # avec mkdocs-macros-plugin
        - sqlite-console
    ```

    ```yaml
    plugins:
        - search
        - pyodide_macros    # avec PMT
        - sqlite-console
    ```

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

### Paramètres

On peut afficher une console/IDE SQLite grâce à la commande `{{ sqlide paramètres }}`. Cette commande accepte quatre paramètres, tous optionnels :

- un `titre` : par exemple `titre="Exercice 1"`. Par défaut, le titre est "sql"
- un chemin vers un script SQL d'initialisation, `init` : par exemple `init=sql/init.md`
- un chemin vers une `base` SQLite : par exemple `bases/test.db`
- un chemin vers un fichier de code `sql` pré-saisi dans l'IDE : par exemple `sql="sql/code.sql"`
- si le mot clef `autoexec` est présent, alors le contenu de code sera exécuté comme si l'utilisateur avait cliqué le bouton

!!! tip "Astuce"
    A part pour le titre, les apostrophes ou guillemets sont optionnels. Ainsi, `sql="sql/code.sql"`,
    `sql='sql/code.sql'` et `sql=sql/code.sql` sont équivalents.

!!! warning "Attention"
    - le titre *doit* être entre guillemets
    - les chemins vers les fichiers sont relatifs à la racine du site
    - les chemins ne peuvent pas contenir d'espace
    - les options base et init sont mutuellement exclusives ; l'option base est prioritaire.

    Voir le cas des [utilisations en tant que macro](#as-macros), où les syntaxes diffèrent légèrement.<!-- markdownlint-disable-line MD046 -->

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

{{sqlide(titre="IDE avec une base binaire chargée et code pré-saisi autoexécuté, IDE caché" base="bases/test.db" sql="sql/code.sql" autoexec hide)}}

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

donne :

???+ sql "Bloc accordéon avec initialisation et code pré-saisi"
    {{ sqlide titre="Init + Code" init="sql/init1.sql" sql="sql/code.sql" }}

## Usage avec le plugin des macros MkDocs ou Pyodide-MkDocs-Theme { #as-macros }

`mkdocs-sqlite-console` est compatible avec l'utilisation du plugin [`mkdocs-macros-plugin`](https://mkdocs-macros-plugin.readthedocs.io/en/latest/), ainsi que le thème [Pyodide-MkDocs-Theme](https://frederic-zinelli.gitlab.io/pyodide-mkdocs-theme/).

Si l'un des deux est utilisé (avec une manipulation de configuration à faire pour le plugin des macros seul), il est alors possible de déclarer un `sqlide` via un appel de macro :

```markdown
{{ sqlide(titre="Init + Code", init="sql/init1.sql", sql="sql/code.sql") }}
```

### Syntaxes

Par rapport à l'utilisation normale du plugin, il faut :

- Ajouter les parenthèses autour des arguments,
- Ajouter des virgules entre les arguments,
- Les guillemets autour des valeurs des arguments sont alors indispensables.
- Les arguments passés sous forme de chaînes de caractères seule, dans la syntaxe originale (`autoexec`, `hide`), doivent être passés sous forme de booléens. On peut aussi utiliser des entiers pour raccourcir les déclaration : `0` ou `1`.

??? help "Signature exacte de la macro"

    Voici la déclaration exacte de la macro, et les valeurs par défaut associées aux différents arguments :

    ```python
    sqlide(
        self,
        titre='Sql',
        sql='',
        espace=None,
        *,
        base='/',
        init='',
        hide=False,
        autoexec=False,
    )
    ```

    * Les trois premiers arguments, `titre`, `sql` et `espace` sont des arguments positionnels avec des valeurs par défaut : il n'est pas obligatoire de mettre le nom de l'argument (mais dans ce cas, il faut respecter l'ordre de déclaration).

    * Les arguments après `*,` sont des arguments nommés. Ils doivent impérativement être renseignés en précisant le nom de l'argument.

    * Il est toujours possible de renseigner les noms des arguments positionnels si on le souhaite (dans ce cas, il n'est pas indispensable de respecter leur ordre dans la déclaration).

    <br>

    L'appel de l'exemple ci-dessus peut donc également se faire comme suit :


    ```markdown
    {{ sqlide("Init + Code", "sql/code.sql", init="sql/init1.sql") }}
    ```

??? tip "Anciennes syntaxes - versions 1.0.7 et antérieures"

    _Ceci décrit les anciens comportements pour utiliser `mkdocs-sqlite-console` avec le plugin des macros ou PMT activés.<!-- markdownlint-disable-line MD046 -->
    Ces méthodes restent utilisables._
    { style="color:#FFAA00" }

    Le plugin `macros` utilise les doubles accolades pour définir ses propres blocs de code, ce qui empêche ce plugin de
    fonctionner normalement. En conséquence, quand le plugin macros est détecté, la syntaxe change et l'IDE SQLite est
    chargée avec la syntaxe suivante :

    ```markdown
    {!{ sqlide paramètres }!}
    ```

    Par exemple, l'appel :

    ```markdown
    {{ sqlide titre="..." init="sql/init1.sql" sql="sql/code.sql" }}
    ```

    ...devait alors s'écrire :

    `{!{ sqlide titre="..." init="sql/init1.sql" sql="sql/code.sql" }!}`

### Activation

#### `Pyodide-MkDocs-Theme`

Le thème gère tout automatiquement, à partir de sa version 4.4.6.

Les versions antérieures nécessitent d'utiliser les anciennes syntaxes de déclaration des `sqlide`, ou de mettre en place la logistique décrite ci-dessous pour `mkdocs-macros-plugin`.

#### `mkdocs-macros-plugin`

Dans le cas de l'utilisation du plugin des macros seul, il est nécessaire d'enregistrer la macro depuis votre fichier/module de macros personnalisées.

Par défaut, il s'agit du fichier `main.py` :

```python

def define_env(env):

    # Vos macros personnalisées ici:
    ...

    # Enregistrement de la macro sqlide:
    sql_plugin = env._conf.plugins['sqlite-console']
    env.macro(sql_plugin.sqlide)
```

## Erreurs

Le plugin détectera les fichiers non existants :

```markdown
{{sqlide titre="Erreur fichier base manquant" base=bases/basem.db sql=sql/code1.sql }}

```

{{sqlide titre="Erreur fichier base manquant" base=bases/basem.db sql=sql/code1.sql }}

```markdown
{{sqlide titre="Erreur fichier sql manquant" init=sql/initm.sql sql=sql/codem.sql }}
```

{{sqlide titre="Erreur fichier sql manquant" init=sql/initm.sql sql=sql/codem.sql }}
