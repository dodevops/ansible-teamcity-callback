# Ansible Callback Plugin for Teamcity

## Introduction

This [Ansible](https://ansible.com) [callback plugin]() formats the output of an Ansible playbook, so that it can be better interpreted by TeamCity.

## Why?

Because Ansible logs in Teamcity look like this:

![Log without this plugin](log_view_without.png)

## Usage

You have different options of using this plugin:

* In your playbook repository:
  * Create a folder named callback_plugins directly where your playbook lives
  * Download the [file teamcity.py]() and place it in inside the callback_plugins directory
* Somewhere else:
  * Download the [plugin](), unzip it and place the folder somewhere accessible
  * Use the following environment variable to tell Ansible where to find your plugin:\
    `export ANSIBLE_CALLBACK_PLUGINS=<path of your plugin>`

Set the following environment variable to use the plugin:

    export ANSIBLE_STDOUT_CALLBACK=teamcity

Then run your playbook.