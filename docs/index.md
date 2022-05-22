# Welcome to MkDocs

For full documentation visit [mkdocs.org](https://www.mkdocs.org).

## Commands

* `mkdocs new [dir-name]` - Create a new project.
* `mkdocs serve` - Start the live-reloading docs server.
* `mkdocs build` - Build the documentation site.
* `mkdocs -h` - Print help message and exit.

## Project layout

    mkdocs.yml    # The configuration file.
    docs/
        index.md  # The documentation homepage.
        ...       # Other markdown pages, images and other files.

1. A
2. B


{{ sqlide titre="IDE avec initialisation et code pré-saisi" init="sql/init1.sql" sql="sql/code.sql" }}

???+ sql "Bloc accordéon avec initialisation et code pré-saisi"
    {{ sqlide titre="Init + Code" init="sql/init1.sql" sql="sql/code.sql" }}

!!! sql "Bloc admonition avec initialisation et code pré-saisi"
    {{ sqlide titre="Init + Code" init="sql/init1.sql" sql="sql/code.sql" }}

{{sqlide titre="IDE avec une base binaire chargée et code pré-saisi" base="bases/test.db" sql="sql/code.sql" }}

{{sqlide titre="Erreur fichier base manquant" base=bases/basem.db sql=sql/code1.sql }}

{{sqlide titre="Erreur fichier sql manquant" init=sql/initm.sql sql=sql/codem.sql }}
