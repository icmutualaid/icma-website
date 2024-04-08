#!/usr/bin/env bash


# Set up the Python virtual environment
python3 -m venv .venv
pip3 install -e .


# Create the database
echo "Installing the blog database..."
flask --app blog init-db
echo "...done"


# Create the admin user
echo; read -p "Enter the administrator's username: " admin_user
while true; do
    read -sp "Enter the administrator's password: " admin_pass; echo
    read -sp "Confirm the administrator password: " admin_pass_confirm; echo
    [ "$admin_pass" = "$admin_pass_confirm" ] && break
    echo "Passwords do not match."
done
echo "Creating the blog admin user..."
flask --app blog create-user "$admin_pass" "$admin_pass_confirm"
echo "...done"
