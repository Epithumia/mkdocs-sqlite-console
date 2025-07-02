# Essai

(cette page n'est pas rendue sur le site, par défaut. L'activer via mkdocs.yml pour tester les chemins relatifs au fichier md en cours)_

## Sans le plugin macro activé, ancienne syntaxe

A modifier en cas de test avec le plugin macro activé

=== "onglet 1"

    {{ sqlide titre="IDE avec initialisation et code pré-saisi" init="init1.sql" sql="code.sql" }}

=== "onglet 2"

    {{ sqlide titre="IDE avec une base binaire chargée et code pré-saisi autoexécuté" base="../bases/test.db" sql="../sql/code.sql" autoexec}}

## Avec le plugin macro activé, ancienne syntaxe

=== "onglet 1"

    {!{ sqlide titre="IDE avec initialisation et code pré-saisi" init="init1.sql" sql="code.sql" }!}

=== "onglet 2"

    {!{ sqlide titre="IDE avec une base binaire chargée et code pré-saisi autoexécuté" base="../bases/test.db" sql="../sql/code.sql" autoexec}!}

## Nouvelle syntaxe

=== "onglet 1"

    {{ sqlide("IDE avec initialisation et code pré-saisi", init="init1.sql", sql="code.sql") }}

=== "onglet 2"

    {{ sqlide("IDE avec initialisation et code pré-saisi", init="init1.sql", sql="code.sql") }}
