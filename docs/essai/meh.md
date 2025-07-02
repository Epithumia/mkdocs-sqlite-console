_(cette page n'est pas rendue sur le site, par défaut. L'activer via mkdocs.yml pour tester les chemins relatifs au fichier md en cours)_

{!{ sqlide titre="IDE avec initialisation et code pré-saisi" init="init1.sql" sql="code.sql" }!}

{!{ sqlide titre="IDE avec une base binaire chargée et code pré-saisi autoexécuté" base="../bases/test.db" sql="../sql/code.sql" autoexec}!}


=== "onglet 1"

    {{ sqlide("IDE avec initialisation et code pré-saisi", init="init1.sql", sql="code.sql") }}


=== "onglet 2"

    {{ sqlide("IDE avec initialisation et code pré-saisi", init="init1.sql", sql="code.sql") }}
