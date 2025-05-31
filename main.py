# Logistique pour tester en local avec l'utilisation de mkdocs-macros-plugin.
#
# Nécessite d'installer le plugin dans le venv et de configurer mkdocs.yml.plugins.macros


def define_env(env):
    env.macro(env._conf.plugins['sqlite-console'].sqlide)
