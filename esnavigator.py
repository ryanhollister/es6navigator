import sublime, sublime_plugin, os

class Es6NavigateCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        fwd = self.view.sel()[0].b
        bck = self.view.sel()[0].a
        bck_limit = self.view.line(self.view.sel()[0]).a
        fwd_limit = self.view.line(self.view.sel()[0]).b
        while self.view.substr(fwd) != "'"  :
            fwd = fwd + 1
            if fwd >= fwd_limit:
                break

        while self.view.substr(bck) != "'" :
            bck = bck - 1
            if bck < bck_limit:
                break
        
        path = self.view.substr(sublime.Region(bck+1, fwd))
        
        # relative pathing
        if (path[:2] == "./") :
            file = os.path.dirname(self.view.file_name()) + path[1:] + '.js'
            self.view.window().open_file(file)
            return


        if (path[:3] == "../") :
            file = os.path.dirname(self.view.file_name()) + '/' + path + '.js'
            self.view.window().open_file(file)
            return

        s = sublime.load_settings('es6navigator.sublime-settings')

        module_prefix = s.get('module_prefix', 'app')
        app_path = s.get('app_path', '')

        # for paths in the application
        if (path.startswith(module_prefix)):
            proj = path.lstrip(module_prefix)
            file = app_path + proj + '.js'
            print(path)
            print(app_path)
            print(proj)
            self.view.window().open_file(file)
            return

        node_modules = []
        for folder in self.view.window().folders():
            # for paths in node modules
            if os.path.exists(folder + '/node_modules'):
                if path.split('/')[0] in os.listdir(folder + '/node_modules'):
                    node_file = folder + '/node_modules/' + path + '.js'
                    em_addon = folder + '/node_modules/' + path.split('/')[0] + '/addon/' + '/'.join(path.split('/')[1:]) + '.js'
                    if os.path.exists(node_file):
                        self.view.window().open_file(node_file)
                        return
                    # for paths to ember-addons
                    elif os.path.exists(em_addon) : 
                        self.view.window().open_file(em_addon)
                        return

            # for paths in bower components
            if os.path.exists(folder + '/bower_components'):
                if path.split('/')[0] in os.listdir(folder + '/bower_components'):
                    bower_file = folder + '/bower_components/' + path + '/' + path + '.js'
                    if os.path.exists(bower_file):
                        self.view.window().open_file(bower_file)
                        return
