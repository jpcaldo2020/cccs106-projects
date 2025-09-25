# main.py
import flet as ft
from database import init_db
from app_logic import display_contacts, add_contact, search_contacts

def main(page: ft.Page):
    page.title = "Contact Book"
    page.vertical_alignment = ft.MainAxisAlignment.START
    page.window.width = 400
    page.window.height = 600
    page.scroll = ft.ScrollMode.AUTO  # Enable page-level scrolling
    
    # Initialize database connection
    db_conn = init_db()
    
    # Theme toggle state
    is_dark_mode = False
    
    def toggle_theme(e):
        nonlocal is_dark_mode
        is_dark_mode = not is_dark_mode
        page.theme_mode = ft.ThemeMode.DARK if is_dark_mode else ft.ThemeMode.LIGHT
        
        # Update theme button text and icon
        if is_dark_mode:
            theme_button.text = "Light Mode"
            theme_button.icon = ft.Icons.LIGHT_MODE
        else:
            theme_button.text = "Dark Mode"
            theme_button.icon = ft.Icons.DARK_MODE
        
        page.update()
    
    # Theme toggle button with icon
    theme_button = ft.ElevatedButton(
        text="Dark Mode",
        icon=ft.Icons.DARK_MODE,
        on_click=toggle_theme
    )
    
    # Create input fields with icons
    name_input = ft.TextField(
        label="Name", 
        width=350,
        prefix_icon=ft.Icons.PERSON,
        border_radius=10,
        filled=True
    )
    phone_input = ft.TextField(
        label="Phone", 
        width=350,
        prefix_icon=ft.Icons.PHONE,
        border_radius=10,
        filled=True
    )
    email_input = ft.TextField(
        label="Email", 
        width=350,
        prefix_icon=ft.Icons.EMAIL_ROUNDED,
        border_radius=10,
        filled=True
    )
    inputs = (name_input, phone_input, email_input)
    
    # Search field for filtering contacts with icon
    search_field = ft.TextField(
        label="Search contacts...",
        width=350,
        prefix_icon=ft.Icons.SEARCH,
        border_radius=10,
        filled=True,
        on_change=lambda e: search_contacts(page, search_field, contacts_list_view, db_conn)
    )
    
    # Create contacts list view with proper scrolling
    contacts_list_view = ft.Column(
        spacing=5,
        scroll=ft.ScrollMode.AUTO,  # Enable scrolling for contacts
        height=250,  # Fixed height to enable scrolling
    )
    
    # Create add button with icon
    add_button = ft.ElevatedButton(
        text="Add Contact",
        icon=ft.Icons.ADD_CIRCLE,
        on_click=lambda e: add_contact(page, inputs, contacts_list_view, db_conn, search_field)
    )
    
    # Add all components to the page with proper scrolling
    main_column = ft.Column([
        ft.Row([
            ft.Text("Contact Book", size=20, weight=ft.FontWeight.BOLD),
            theme_button
        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
        ft.Divider(),
        ft.Text("Enter Contact Details:", size=18, weight=ft.FontWeight.BOLD),
        name_input,
        phone_input,
        email_input,
        add_button,
        ft.Divider(),
        ft.Text("Search & Filter:", size=18, weight=ft.FontWeight.BOLD),
        search_field,
        ft.Divider(),
        ft.Text("Contacts:", size=18, weight=ft.FontWeight.BOLD),
        ft.Container(
            content=contacts_list_view,
            border=ft.border.all(1, ft.Colors.GREY_300),
            border_radius=10,
            padding=10,
            height=250,  # Fixed height container for scrolling
        ),
    ])
    
    # Add scroll to the main column
    page.add(
        ft.Container(
            content=main_column,
            expand=True
        )
    )
    
    # Display existing contacts
    display_contacts(page, contacts_list_view, db_conn)

if __name__ == "__main__":
    ft.app(target=main)