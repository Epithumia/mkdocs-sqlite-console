import os
import re
from typing import Optional

from mkdocs.exceptions import PluginError
from mkdocs.plugins import BasePlugin
from mkdocs.structure.files import File
from mkdocs.structure.pages import Page


BASE_PATH = os.path.dirname(os.path.realpath(__file__))

LIBS_PATH = BASE_PATH + "/libs/"

CSS_PATH = BASE_PATH + "/css/"

JS_PATH = BASE_PATH + "/js/"


# "{workerinit}" was the first line of the template: removed in version > 2.0.0.
SKELETON = """
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
""".strip()     # Stripping necessary for use as macro (indentation has to be worked out...)

MACROS_TEMPLATE = "MKDOCS_SQLITE_CONSOLE_IDE_{}"



class Counter:
    def __init__(self, config):
        self.count = 0
        self.config = config
        self.spaces = {}
        self.macros_contents = {}
        self.worker_inits = []

    def insert_ide(self, macro):
        regex_titre = r".*?titre=\"(.*?)\""
        regex_init = r".*?init=[\"\']?\b([^\s]*)\b"
        regex_base = r".*?base=[\"\']?\b([^\s]*)\b"
        regex_sql = r".*?sql=[\"\']?\b([^\s]*)\b"
        regex_space = r".*?espace=[\"\']?\b([^\s]*)\b"

        params = str(macro.groups(0)[0])

        titre = "".join(re.findall(regex_titre, params))
        autoexec = "autoexec" in params
        hide = "hide" in params
        init = "".join(re.findall(regex_init, params))
        base = "".join(re.findall(regex_base, params))
        sql = "".join(re.findall(regex_sql, params))
        space = "".join(re.findall(regex_space, params))

        return self.build_sql(titre, autoexec, hide, init, base, sql, space)

    def build_sql(self, titre, autoexec, hide, init, base, sql, space):
        self.count += 1

        # handle defaults (centralizing the logic in one single place):
        autoexec = True if autoexec else ""
        hide = 'class="sqlhidden"' if hide else ""
        titre = titre or "Sql"
        init = init or ""
        base = base or "/"
        sql = sql or ""
        space = space or None

        worker = ""
        if space:
            if space not in self.spaces:
                self.spaces[space] = 0
                workerinit = 'var {worker} = new Worker(sqljs_base_path + "/js/worker.sql-wasm.js");'.format(
                    worker=space
                )
                self.worker_inits.append(workerinit)
                worker = space
            else:
                self.spaces[space] += 1
                worker = space
        if sql != "":
            try:
                with open(os.path.abspath(self.config["docs_dir"]) + "/" + sql) as f:
                    sql = f.readlines()
                    sql = "".join(sql)
                    if autoexec:
                        autoexec = sql
                        autoexec = autoexec.replace("\n", "\\n")
                        autoexec = autoexec.replace("'", "\\'")
            except OSError:
                sql = "Fichier '" + sql + "' introuvable"
        if init != "":
            try:
                with open(os.path.abspath(self.config["docs_dir"]) + "/" + init) as f:
                    init = f.readlines()
                    init = "".join(init)
                    init = init.replace("\n", "\\n")
                    init = init.replace("'", "\\'")
            except OSError:
                sql = "-- Fichier d'initialisation '" + init + "' introuvable"
                init = ""
        if base != "/":
            base_url = self.config["site_url"]
            if os.path.isfile(os.path.abspath(self.config["docs_dir"]) + "/" + base):
                base = base_url + "/" + base
                base = base.replace("//", "/")
            else:
                sql = "-- Fichier de base '" + base + "' introuvable"
                init = ""
                base = "/"
        html = SKELETON.format(
            numide=self.count,
            title=titre,
            hide=hide,
            base=base,
            sqlcode=sql,
            init=init,
            autoexec=autoexec,
            worker=worker,
            #workerinit=workerinit,      # Not inserted here anymore (version > 2.0.0)
        )
        return html

    def register_macro_content(self, html_code):
        """
        Store the html code generated from the macro call, to insert it later (in on_page_content
        hook: this avoids rendering troubles of the SQL code provided by the user, when mkdocs
        renders md to html: the user's code is in `<pre>` tags, so the line breaks have to be
        kept "as they are".
        """
        token = MACROS_TEMPLATE.format(self.count)
        self.macros_contents[token] = html_code
        return token

    def insert_macro_contents(self, html):
        """ To do _before_ resolving the older syntaxes. """
        if self.count:
            html = re.sub(
                MACROS_TEMPLATE.format('\\d+'),
                lambda m: self.macros_contents[m[0]],
                html,
            )
        return html

    def get_worker_inits(self):
        workers = " ".join(self.worker_inits)
        return f"<script>{ workers }</script>"



# noinspection PyUnusedLocal
class SQLiteConsole(BasePlugin):

    def __init__(self, **kwargs):
        super().__init__()

        self.has_instant_nav = False
        """ Is theme.features.navigation.instant option active or not? """

        self.macros = None
        """ PMT:pyodide_macros or mkdocs-macros-plugin:macros or None """

        self.ressources = {}  # dict[page_url,Counter]
        """ Tracking pages vs counters, to spot where the additional files need to be included """

    def on_config(self, config, **kwargs):
        if "site_url" not in config.keys() or config["site_url"] == "":
            raise PluginError(
                "Le fichier de configuration doit comporter une valeur pour la clef 'site_url'"
            )

        self.has_instant_nav = "navigation.instant" in config["theme"]["features"]

        plugins = config["plugins"]
        self.macros = plugins.get("pyodide_macros") or plugins.get("macros")

        return config

    def on_files(self, files, config):
        files.append(
            File("sqlite_ide.css", CSS_PATH, config["site_dir"] + "/css/", False)
        )
        files.append(File("sqlite_ide.js", JS_PATH, config["site_dir"] + "/js/", False))
        files.append(
            File("worker.sql-wasm.js", JS_PATH, config["site_dir"] + "/js/", False)
        )
        files.append(File("sql-wasm.wasm", JS_PATH, config["site_dir"] + "/js/", False))
        return files

    def on_pre_page(self, page, config, files):
        self.counter_for(page, set_counter=Counter(config))

    def on_page_content(self, html, page, config, files):
        # NOTE: regex are working on the interpreted markdown, so searching for `<p>...</p>` to
        #       not match calls that are in code blocks, in the documentation.

        c = self.counter_for(page)
        if self.macros:
            # Insert code coming from the macro use itself (done now to avoid rendering troubles
            # when converting md 6> html after the macro content was inserted):
            # To apply BEFORE using the old syntax logistic (relies on c.count value).god cod
            html = c.insert_macro_contents(html)

            # Still apply the "old way", for backward compatibility.
            # If used as an actual macro, this won't find anything to update in the page.
            regex = r"(?:^|\n)\s*?<p>\s*?{!{\s*?sqlide.*?\s+?(.*?)\s*?}!}</p>(?:\n|$)"
        else:
            regex = r"(?:^|\n)\s*?<p>\s*?{{\s*?sqlide.*?\s+?(.*?)\s*?}}</p>(?:\n|$)"

        if c:
            html = re.sub(regex, c.insert_ide, html, flags=re.MULTILINE | re.DOTALL)

        return html

    def on_page_context(self, ctx, page:Page, config, **kwargs):

        c = self.counter_for(page)
        sql_scripts = ""
        is_page_with_sql_ides = bool(c and c.count)

        # When using navigation.instant, the scripts are loaded once only and have to always
        # be included in every page (because one doesn't know where the user will land first).
        # If no navigation.instant, they have to be inserted in all pages using sql IDEs.
        if self.has_instant_nav or is_page_with_sql_ides:

            base_url = config["site_url"]
            codemirror = (
                "https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.58.1/codemirror.js"
            )
            codemirror_css = "https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.58.1/codemirror.css"
            codemirror_sql = "https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.58.1/mode/sql/sql.min.js"

            sql_scripts = f"""\
<script src="{ codemirror }"></script>
<script src="{ base_url }/js/sqlite_ide.js"></script>
<script src="{ codemirror_sql }"></script>
<link rel="stylesheet" href="{ codemirror_css }">
<link rel="stylesheet" href="{ base_url }/css/sqlite_ide.css">
<script>sqljs_base_path="{ base_url }"</script>
"""

        # If some sqlides are used in the page, insert the workers logistic:
        # NOTES:
        #   1. This depends on the page content, and is not related to navigation.instant
        #   2. The workers have to be inserted once per page, depending on the number of "spaces"
        #   3. They have to be inserted _after_ the sql scripts...
        #   4. ...but _before_ any SQL IDE in the html.
        if is_page_with_sql_ides:
            sql_scripts += c.get_worker_inits()

        # Mutate the page content with all the required logistic if any:
        if sql_scripts:
            page.content = sql_scripts + page.content

    def counter_for(self, page, *, set_counter: Counter = None) -> Optional[Counter]:
        key = page and page.url
        if set_counter is not None:
            self.ressources[key] = set_counter
        else:
            return self.ressources.get(key)

    def sqlide(
        self,
        titre=None,
        sql=None,
        espace=None,
        *,
        base=None,
        init=None,
        hide=None,
        autoexec=None,
    ):
        """
        Can be registered as a mkdocs macro (through the macro module, or automatically
        when using Pyodide-MkDocs-Theme).
        """
        # (actual default values are handled in Counter.build_sql)
        c = self.counter_for(self.macros.page)
        html_code = c.build_sql(titre, autoexec, hide, init, base, sql, espace)
        return c.register_macro_content(html_code)
