# mkdocs-sqlite-console

Mkdocs-SQLite-Console est un plugin pour MkDocs, qui permet d'afficher un IDE SQL (SQLite) permettant d'exécuter du code.
Le public visé est essentiellement les enseignants et étudiants : les premiers pourront ainsi placer du code que les
seconds pourront exécuter et ainsi voir le résultat de leur requête.

## Installation

Installer le plugin avec pip :

`pyhton3 -m pip install git+https://github.com/Epithumia/mkdocs-sqlite-console.git`

Pour accéder à la documentation :

```shell
git clone git+https://github.com/Epithumia/mkdocs-sqlite-console.git
cd mkdocs-sqlite-console
pyhton3 -m pip install .[docs]
mkdocs build
```

Puis dans le dossier `docs`, activer le plugin dans votre fichier `mkdocs.yml`:
```yaml
plugins:
  - search
  - sqlite-console
```

> **Note:** Si vous n'avez aucune entrée dans la section `plugins` de votre fichier de configuration, 
> vous voudrez sans doute ajouter le plugin `search`. MkDocs l'active par défaut s'il n'y a pas 
> d'autres `plugins`, et dans le cas contraire, MkDocs demande de l'activer explicitement.

Plus d'informations sur les plugins se trouvent dans la [documentation MkDocs][mkdocs-plugins].

## Usage

Voir la section [Guide d'utilisation](https://epithumia.github.io/mkdocs-sqlite-console/usage/)

## Licence

Voir [LICENCE](LICENSE)

## Voir aussi

Plus d'informations sur les templates [here][mkdocs-template].

Plus d'informations sur les blocs [here][mkdocs-block].

[mkdocs-plugins]: http://www.mkdocs.org/user-guide/plugins/
[mkdocs-template]: https://www.mkdocs.org/user-guide/custom-themes/#template-variables
[mkdocs-block]: https://www.mkdocs.org/user-guide/styling-your-docs/#overriding-template-blocks
