# Gitlab Snippets Manager

Gitlab Snippets Manager is a Sublime Text plugin that allows you to manage your Gitlab snippets directly from Sublime Text. With this plugin, you can list, create, update, and delete snippets without leaving your editor.

## Features

- List all snippets
- Create a new snippet
- Update an existing snippet
- Delete a snippet

## Usage

### List Snippets

To list all snippets, open the command palette (`Ctrl + Shift + P` or `Cmd + Shift + P`) and type `List Snippets`. Select the `Gitlab Snippets Manager: List Snippets` command to fetch and display a list of your snippets. You can then select a snippet from the list to copy its raw content to the clipboard.

### Create Snippet

To create a new snippet, select the text you want to create a snippet from and open the command palette. Type `Create Snippet` and select the `Gitlab Snippets Manager: Create Snippet` command. You will be prompted to enter a title, description, visibility, and file type for the snippet. Once you provide the required information, the snippet will be created on Gitlab.

### Update Snippet

To update an existing snippet, open the command palette and type `Update Snippet`. Select the `Gitlab Snippets Manager: Update Snippet` command to fetch and display a list of your snippets. Select the snippet you want to update, make the necessary changes to the content, and save the file. The plugin will automatically update the snippet on Gitlab.

### Delete Snippet

To delete a snippet, open the command palette and type `Delete Snippet`. Select the `Gitlab Snippets Manager: Delete Snippet` command to fetch and display a list of your snippets. Select the snippet you want to delete, and the plugin will prompt you to confirm the deletion. Once confirmed, the snippet will be deleted from Gitlab.

## Configuration


```json
{
  "api_endpoint": "https://gitlab.example.com/api/v4",
  "private_token": "YOUR_PRIVATE_TOKEN"
}
```

Make sure to replace `https://gitlab.example.com/api/v4` with the URL of your Gitlab instance and `YOUR_PRIVATE_TOKEN` with your actual private token.

