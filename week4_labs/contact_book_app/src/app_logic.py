# app_logic.py
import flet as ft
from database import update_contact_db, delete_contact_db, add_contact_db, get_all_contacts_db

def display_contacts(page, contacts_list_view, db_conn, search_term=""):
    """Fetches and displays all contacts in the Column using modern Cards."""
    contacts_list_view.controls.clear()
    contacts = get_all_contacts_db(db_conn, search_term)
    
    if not contacts:
        contacts_list_view.controls.append(
            ft.Container(
                content=ft.Text("No contacts found" if search_term else "No contacts yet. Add your first contact above!", 
                              size=14, color=ft.Colors.GREY_600),
                alignment=ft.alignment.center,
                height=100
            )
        )
    
    for contact in contacts:
        contact_id, name, phone, email = contact
        
        # Create a modern Card instead of simple ListTile
        contact_card = ft.Card(
            content=ft.Container(
                content=ft.Column([
                    ft.Text(name, size=16, weight=ft.FontWeight.BOLD),
                    ft.Row([
                        ft.Icon(ft.Icons.PHONE, size=16, color=ft.Colors.BLUE_400),
                        ft.Text(phone or "No phone", size=14)
                    ]) if phone else ft.Text("No phone", size=14, color=ft.Colors.GREY_500),
                    ft.Row([
                        ft.Icon(ft.Icons.EMAIL, size=16, color=ft.Colors.GREEN_400),
                        ft.Text(email or "No email", size=14)
                    ]) if email else ft.Text("No email", size=14, color=ft.Colors.GREY_500),
                    ft.Row([
                        ft.ElevatedButton(
                            "Edit",
                            icon=ft.Icons.EDIT,
                            on_click=lambda _, c=contact: open_edit_dialog(page, c, db_conn, contacts_list_view, search_term)
                        ),
                        ft.ElevatedButton(
                            "Delete",
                            icon=ft.Icons.DELETE,
                            color=ft.Colors.WHITE,
                            bgcolor=ft.Colors.RED_400,
                            on_click=lambda _, cid=contact_id, cname=name: confirm_delete_contact(page, cid, cname, db_conn, contacts_list_view, search_term)
                        ),
                    ], alignment=ft.MainAxisAlignment.END)
                ], spacing=6),
                padding=12
            ),
            elevation=2,
            margin=ft.margin.only(bottom=8)
        )
        contacts_list_view.controls.append(contact_card)
    
    page.update()

def add_contact(page, inputs, contacts_list_view, db_conn, search_field=None):
    """Adds a new contact with input validation and refreshes the list."""
    name_input, phone_input, email_input = inputs
    
    # Input Validation - Check if name is empty
    if not name_input.value or not name_input.value.strip():
        name_input.error_text = "Name cannot be empty"
        page.update()
        return
    else:
        name_input.error_text = None
    
    # Add contact to database
    add_contact_db(db_conn, name_input.value.strip(), phone_input.value, email_input.value)
    
    # Clear input fields
    for field in inputs:
        field.value = ""
    
    # Clear search if active
    search_term = ""
    if search_field:
        search_field.value = ""
    
    display_contacts(page, contacts_list_view, db_conn, search_term)
    page.update()

def confirm_delete_contact(page, contact_id, contact_name, db_conn, contacts_list_view, search_term=""):
    """Shows a compact confirmation dialog before deleting a contact."""
    
    def delete_confirmed(e):
        delete_contact_db(db_conn, contact_id)
        dialog.open = False
        display_contacts(page, contacts_list_view, db_conn, search_term)
        page.update()
    
    def cancel_delete(e):
        dialog.open = False
        page.update()
    
    dialog = ft.AlertDialog(
        modal=True,
        title=ft.Row([
            ft.Icon(ft.Icons.WARNING, color=ft.Colors.RED_400),
            ft.Text("Delete Contact")
        ]),
        content=ft.Container(
            content=ft.Text(
                f"Are you sure you want to delete '{contact_name}'?",
                size=16
            ),
            width=280,  # Compact width
            padding=ft.padding.all(10)
        ),
        actions=[
            ft.TextButton(
                "Cancel", 
                icon=ft.Icons.CANCEL,
                on_click=cancel_delete
            ),
            ft.ElevatedButton(
                "Delete", 
                icon=ft.Icons.DELETE,
                color=ft.Colors.WHITE,
                bgcolor=ft.Colors.RED_400,
                on_click=delete_confirmed
            ),
        ],
        actions_alignment=ft.MainAxisAlignment.END
    )
    
    page.overlay.append(dialog)
    dialog.open = True
    page.update()

def open_edit_dialog(page, contact, db_conn, contacts_list_view, search_term=""):
    """Opens a compact dialog to edit a contact's details."""
    contact_id, name, phone, email = contact
    
    edit_name = ft.TextField(
        label="Name", 
        value=name,
        width=280,  # Smaller width for compact dialog
        prefix_icon=ft.Icons.PERSON
    )
    edit_phone = ft.TextField(
        label="Phone", 
        value=phone,
        width=280,  # Smaller width for compact dialog
        prefix_icon=ft.Icons.PHONE
    )
    edit_email = ft.TextField(
        label="Email", 
        value=email,
        width=280,  # Smaller width for compact dialog
        prefix_icon=ft.Icons.EMAIL
    )

    def save_and_close(e):
        # Input validation for edit
        if not edit_name.value or not edit_name.value.strip():
            edit_name.error_text = "Name cannot be empty"
            page.update()
            return
        else:
            edit_name.error_text = None
        
        update_contact_db(db_conn, contact_id, edit_name.value, edit_phone.value, edit_email.value)
        dialog.open = False
        display_contacts(page, contacts_list_view, db_conn, search_term)
        page.update()

    def cancel_and_close(e):
        dialog.open = False
        page.update()

    dialog = ft.AlertDialog(
        modal=True,
        title=ft.Row([
            ft.Icon(ft.Icons.EDIT, color=ft.Colors.BLUE_400),
            ft.Text("Edit Contact")
        ]),
        content=ft.Container(
            content=ft.Column([
                edit_name, 
                edit_phone, 
                edit_email
            ], spacing=15, tight=True),  # Tight=True makes container fit content
            width=300,  # Fixed width for compact dialog
            padding=ft.padding.all(10)
        ),
        actions=[
            ft.TextButton(
                "Cancel", 
                icon=ft.Icons.CANCEL,
                on_click=cancel_and_close
            ),
            ft.ElevatedButton(
                "Save Changes", 
                icon=ft.Icons.SAVE,
                on_click=save_and_close
            ),
        ],
        actions_alignment=ft.MainAxisAlignment.END
    )
    
    page.overlay.append(dialog)
    dialog.open = True
    page.update()

def search_contacts(page, search_field, contacts_list_view, db_conn):
    """Handles real-time search filtering."""
    search_term = search_field.value
    display_contacts(page, contacts_list_view, db_conn, search_term)