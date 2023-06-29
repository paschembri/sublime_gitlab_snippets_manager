# -*- coding: utf-8 -*-
import sublime
import sublime_plugin
import json
import urllib


class ListSnippetsCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        # Get the API endpoint and PRIVATE-TOKEN from the settings
        settings = sublime.load_settings(
            'GitlabSnippetsManager.sublime-settings'
        )
        api_endpoint = settings.get('api_endpoint')
        private_token = settings.get('private_token')

        # Make a GET request to the Snippets API
        url = "{api_endpoint}/snippets".format(api_endpoint=api_endpoint)
        headers = {'PRIVATE-TOKEN': private_token}
        request = urllib.request.Request(url, headers=headers)
        response = urllib.request.urlopen(request)

        if response.status == 200:
            snippets = json.loads(response.read().decode())
            snippet_names = [snippet['title'] for snippet in snippets]
            sublime.active_window().show_quick_panel(
                snippet_names,
                lambda index: self.on_snippet_selected(index, snippets),
            )
            sublime.status_message(
                'Fetched {} snippets'.format(len(snippet_names))
            )
        else:
            sublime.error_message('Failed to list snippets')

    def on_snippet_selected(self, index, snippets):
        if index != -1:
            # Snippet selected, copy raw content to clipboard
            settings = sublime.load_settings(
                'GitlabSnippetsManager.sublime-settings'
            )
            api_endpoint = settings.get('api_endpoint')
            selected_snippet = snippets[index]
            raw_url = "{api_endpoint}/snippets/{id}/raw".format(
                api_endpoint=api_endpoint, id=selected_snippet['id']
            )

            # Make a GET request to the Snippets API
            private_token = settings.get('private_token')
            headers = {'PRIVATE-TOKEN': private_token}

            request = urllib.request.Request(raw_url, headers=headers)
            response = urllib.request.urlopen(request)
            raw_content = response.read().decode()
            sublime.set_clipboard(raw_content)
            sublime.status_message('Raw content copied to clipboard')


class CreateSnippetCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        # Get the API endpoint and PRIVATE-TOKEN from the settings
        settings = sublime.load_settings(
            'GitlabSnippetsManager.sublime-settings'
        )
        api_endpoint = settings.get('api_endpoint')
        private_token = settings.get('private_token')

        # Get the selected text
        selected_text = self.view.substr(self.view.sel()[0])

        # Prompt the user for snippet details
        sublime.active_window().show_input_panel(
            'Snippet Title:', '', self.on_snippet_title_entered, None, None
        )

        # Store the selected text in a class variable for later use
        self.selected_text = selected_text

        # Store the API endpoint and PRIVATE-TOKEN in class variables for later use
        self.api_endpoint = api_endpoint
        self.private_token = private_token

    def on_snippet_title_entered(self, snippet_title):
        # Store the snippet title in a class variable for later use
        self.snippet_title = snippet_title

        # Prompt the user for snippet description
        sublime.active_window().show_input_panel(
            'Snippet Description:',
            '',
            self.on_snippet_description_entered,
            None,
            None,
        )

    def on_snippet_description_entered(self, snippet_description):
        # Store the snippet description in a class variable for later use
        self.snippet_description = snippet_description

        # Prompt the user for snippet visibility
        visibility_options = ['private', 'internal', 'public']
        sublime.active_window().show_quick_panel(
            visibility_options, self.on_snippet_visibility_selected
        )

    def on_snippet_visibility_selected(self, visibility_index):
        visibility_options = ['private', 'internal', 'public']
        self.snippet_visibility = visibility_options[visibility_index]

        type_options = ['file.py', 'file.js', 'file.md', 'file.txt']
        sublime.active_window().show_quick_panel(
            type_options, self.on_snippet_type_selected
        )

    def on_snippet_type_selected(self, type_index):
        type_options = ['file.py', 'file.js', 'file.md', 'file.txt']
        self.filename = type_options[type_index]

        # Make a POST request to the Snippets API to create a new snippet
        settings = sublime.load_settings(
            'GitlabSnippetsManager.sublime-settings'
        )
        api_endpoint = settings.get('api_endpoint')
        private_token = settings.get('private_token')
        url = "{api_endpoint}/snippets".format(api_endpoint=api_endpoint)
        headers = {
            'PRIVATE-TOKEN': private_token,
            'Content-Type': 'application/json',
        }
        data = {
            'title': self.snippet_title,
            'description': self.snippet_description,
            'visibility': self.snippet_visibility,
            'files': [
                {'content': self.selected_text, 'file_path': self.filename}
            ],
        }
        req = urllib.request.Request(
            url, data=json.dumps(data).encode(), headers=headers, method='POST'
        )
        response = urllib.request.urlopen(req)

        if response.status == 201:
            sublime.status_message('Snippet created successfully')
        else:
            sublime.error_message('Failed to create snippet')


class DeleteSnippetCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        # Get the API endpoint and PRIVATE-TOKEN from the settings
        settings = sublime.load_settings(
            'GitlabSnippetsManager.sublime-settings'
        )
        api_endpoint = settings.get('api_endpoint')
        private_token = settings.get('private_token')

        # Make a GET request to the Snippets API
        url = "{api_endpoint}/snippets".format(api_endpoint=api_endpoint)
        headers = {'PRIVATE-TOKEN': private_token}
        request = urllib.request.Request(url, headers=headers)
        response = urllib.request.urlopen(request)

        if response.status == 200:
            snippets = json.loads(response.read().decode())
            snippet_names = [snippet['title'] for snippet in snippets]
            sublime.active_window().show_quick_panel(
                snippet_names,
                lambda index: self.on_snippet_selected(index, snippets),
            )
            sublime.status_message(
                'Fetched {} snippets'.format(len(snippet_names))
            )
        else:
            sublime.error_message('Failed to list snippets')

    def on_snippet_selected(self, index, snippets):
        if index != -1:
            # Snippet selected, delete the snippet
            settings = sublime.load_settings(
                'GitlabSnippetsManager.sublime-settings'
            )
            api_endpoint = settings.get('api_endpoint')
            selected_snippet = snippets[index]
            delete_url = "{api_endpoint}/snippets/{id}".format(
                api_endpoint=api_endpoint, id=selected_snippet['id']
            )

            # Make a DELETE request to the Snippets API
            private_token = settings.get('private_token')
            headers = {'PRIVATE-TOKEN': private_token}

            request = urllib.request.Request(
                delete_url, headers=headers, method='DELETE'
            )
            response = urllib.request.urlopen(request)

            if response.status == 204:
                sublime.status_message('Snippet deleted successfully')
            else:
                sublime.error_message('Failed to delete snippet')


class UpdateSnippetCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        # Get the API endpoint and PRIVATE-TOKEN from the settings
        settings = sublime.load_settings(
            'GitlabSnippetsManager.sublime-settings'
        )
        api_endpoint = settings.get('api_endpoint')
        private_token = settings.get('private_token')

        # Make a GET request to the Snippets API
        url = "{api_endpoint}/snippets".format(api_endpoint=api_endpoint)
        headers = {'PRIVATE-TOKEN': private_token}
        request = urllib.request.Request(url, headers=headers)
        response = urllib.request.urlopen(request)

        if response.status == 200:
            snippets = json.loads(response.read().decode())
            snippet_names = [snippet['title'] for snippet in snippets]
            sublime.active_window().show_quick_panel(
                snippet_names,
                lambda index: self.on_snippet_selected(index, snippets),
            )
            sublime.status_message(
                'Fetched {} snippets'.format(len(snippet_names))
            )
        else:
            sublime.error_message('Failed to list snippets')

    def on_snippet_selected(self, index, snippets):
        if index != -1:
            # Snippet selected, prompt the user for new content

            selected_text = self.view.substr(self.view.sel()[0])
            self.update_snippet(index, snippets, selected_text)

    def update_snippet(self, index, snippets, new_content):
        # Get the selected snippet and its ID
        selected_snippet = snippets[index]
        snippet_id = selected_snippet['id']

        # Get the API endpoint and PRIVATE-TOKEN from the settings
        settings = sublime.load_settings(
            'GitlabSnippetsManager.sublime-settings'
        )
        api_endpoint = settings.get('api_endpoint')
        private_token = settings.get('private_token')

        # Create the update payload
        update_payload = {
            'files': [
                {
                    'action': 'update',
                    'file_path': selected_snippet['files'][0]['path'],
                    'content': new_content,
                }
            ],
        }

        # Make a PUT request to the Snippets API to update the snippet
        update_url = "{api_endpoint}/snippets/{snippet_id}".format(
            api_endpoint=api_endpoint, snippet_id=snippet_id
        )
        headers = {
            'PRIVATE-TOKEN': private_token,
            'Content-Type': 'application/json',
        }
        req = urllib.request.Request(
            update_url,
            data=json.dumps(update_payload).encode(),
            headers=headers,
            method='PUT',
        )
        response = urllib.request.urlopen(req)

        if response.status == 200:
            sublime.status_message('Snippet updated successfully')
        else:
            sublime.error_message('Failed to update snippet')
