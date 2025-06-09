"""
Logistique pour tester en local avec l'utilisation de mkdocs-macros-plugin.

Nécessite d'installer le plugin dans le venv et d'ajouter le plugin macros
dans mkdocs.yml:plugins.
"""

def define_env(env):
    sql_plugin = env._conf.plugins['sqlite-console']
    env.macro(sql_plugin.sqlide)
