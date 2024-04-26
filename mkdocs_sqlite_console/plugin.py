import os
import re

from mkdocs.exceptions import PluginError
from mkdocs.plugins import BasePlugin
from mkdocs.structure.files import File

BASE_PATH = os.path.dirname(os.path.realpath(__file__))

LIBS_PATH = BASE_PATH + '/libs/'

CSS_PATH = BASE_PATH + '/css/'

JS_PATH = BASE_PATH + '/js/'

SKELETON = """
{workerinit}
<div id="ide{numide}" {hide}>
<label for='sqlcommands'>{title}</label>
<br>
<textarea id="sqlcommands" class="sqlcommands">{sqlcode}</textarea>
<button id="execute" class="sqlbutton execute">Exécuter</button>
<div id="error" class="sqlerror"></div>
<pre id="output" class="sqloutput"></pre>
</div>
<script>
  onElementLoaded("div#ide{numide}").then(() => {{
    const ide = document.querySelector("div#ide{numide}");
    load(ide, '{base}', '{init}', '{autoexec}', {worker});
}}).catch(() => {{}});
</script>
"""


class Counter:
    def __init__(self, config):
        self.count = 0
        self.config = config
        self.spaces = {}

    def insert_ide(self, macro):
        self.count += 1
        regex_titre = r".*?titre=\"(.*?)\""
        regex_init = r".*?init=[\"\']?\b([^\s]*)\b"
        regex_base = r".*?base=[\"\']?\b([^\s]*)\b"
        regex_sql = r".*?sql=[\"\']?\b([^\s]*)\b"
        regex_space = r".*?espace=[\"\']?\b([^\s]*)\b"
        params = str(macro.groups(0)[0])
        titre = ''.join(re.findall(regex_titre, params)) or "Sql"
        autoexec = True if 'autoexec' in params else ''
        hide = 'class="sqlhidden"' if 'hide' in params else ''
        init = ''.join(re.findall(regex_init, params)) or ''
        base = ''.join(re.findall(regex_base, params)) or '/'
        sql = ''.join(re.findall(regex_sql, params)) or ''
        space = ''.join(re.findall(regex_space, params)) or None
        worker = ''
        workerinit = ''
        if space:
            if space not in self.spaces:
                self.spaces[space] = 0
                workerinit = '<script>var {worker} = new Worker(path + "/js/worker.sql-wasm.js");</script>'.format(worker=space)
                worker = space
            else:
                self.spaces[space] += 1
                workerinit = ''
                worker = space
        if sql != '':
            try:
                with open(os.path.abspath(self.config["docs_dir"]) + '/' + sql) as f:
                    sql = f.readlines()
                    sql = ''.join(sql)
                    if autoexec:
                        autoexec = sql
                        autoexec = autoexec.replace('\n', '\\n')
                        autoexec = autoexec.replace('\'', '\\\'')
            except OSError:
                sql = "Fichier '" + sql + "' introuvable"
        if init != '':
            try:
                with open(os.path.abspath(self.config["docs_dir"]) + '/' + init) as f:
                    init = f.readlines()
                    init = ''.join(init)
                    init = init.replace('\n', '\\n')
                    init = init.replace('\'', '\\\'')
            except OSError:
                sql = "--Fichier d'initialisation '" + init + "' introuvable"
                init = ''
        if base != '/':
            base_url = self.config['site_url']
            if os.path.isfile(os.path.abspath(self.config["docs_dir"]) + '/' + base):
                base = base_url + '/' + base
                base = base.replace('//', '/')
            else:
                sql = "--Fichier de base '" + base + "' introuvable"
                init = ''
                base = '/'
        return SKELETON.format(numide=self.count, title=titre, hide=hide, base=base, sqlcode=sql, init=init, autoexec=autoexec, worker=worker, workerinit=workerinit)


# noinspection PyUnusedLocal
class SQLiteConsole(BasePlugin):

    def __init__(self, **kwargs):
        super().__init__()

    def on_page_content(self, html, page, config, files):
        import re
        if 'macros' in config['plugins'] or 'pyodide_macros' in config['plugins']:
            regex = r"(?:^|\n)\s*?<p>\s*?{!{\s*?sqlide.*?\s+?(.*?)\s*?}!}</p>(?:\n|$)"
        else:
            regex = r"(?:^|\n)\s*?<p>\s*?{{\s*?sqlide.*?\s+?(.*?)\s*?}}</p>(?:\n|$)"

        c = Counter(config)
        html = re.sub(regex, c.insert_ide, html, flags=re.MULTILINE | re.DOTALL)

        return html

    def on_post_page(self, out, page, config, **kwargs):
        base_url = config['site_url']
        codemirror = "https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.58.1/codemirror.js"
        codemirror_css = "https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.58.1/codemirror.css"
        codemirror_sql = "https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.58.1/mode/sql/sql.min.js"
        out = out.replace("</title>",
                          "</title>\n<script src=\"{}\"></script>".format(codemirror)
                          + "\n<script src=\"{}/js/sqlite_ide.js\"></script>\n".format(base_url)
                          + "\n<script src=\"{}\"></script>\n".format(codemirror_sql)
                          + "<link rel=\"stylesheet\" href=\"{}\">".format(codemirror_css)
                          + "<link rel=\"stylesheet\" href=\"{}/css/sqlite_ide.css\">".format(base_url)
                          + "<script>path=\"{}\"</script>".format(base_url))
        return out

    def on_files(self, files, config):
        files.append(File('sqlite_ide.css', CSS_PATH,
                          config['site_dir'] + '/css/', False))
        files.append(File('sqlite_ide.js', JS_PATH,
                          config['site_dir'] + '/js/', False))
        files.append(File('worker.sql-wasm.js', JS_PATH,
                          config['site_dir'] + '/js/', False))
        files.append(File('sql-wasm.wasm', JS_PATH,
                          config['site_dir'] + '/js/', False))

        return files

    def on_config(self, config, **kwargs):
        if 'site_url' not in config.keys() or config['site_url'] == '':
            raise PluginError("Le fichier de configuration doit comporter une valeur pour la clef 'site_url'")

        return config
