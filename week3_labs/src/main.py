import flet as ft
import mysql.connector
from db_connection import connect_db

async def main(page: ft.Page):
    # Configure the page
    page.window.center()
    page.window.frameless = True
    page.title = "User Login"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.window.height = 350
    page.window.width = 400
    page.bgcolor = ft.Colors.AMBER_ACCENT
    
    # Create UI controls
    # Login Title
    login_title = ft.Text(
        "User Login",
        size=20,
        weight=ft.FontWeight.BOLD,
        font_family="Arial",
        text_align=ft.TextAlign.CENTER,
        color=ft.Colors.BLACK
    )
    
    # Username Input Field (without prefix icon)
    username_field = ft.TextField(
        label="User name",
        hint_text="Enter your user name",
        width=300,
        autofocus=True,
        disabled=False,
        bgcolor=ft.Colors.LIGHT_BLUE_ACCENT,
        color=ft.Colors.BLACK,
        label_style=ft.TextStyle(color=ft.Colors.BLACK),
        border_color=ft.Colors.BLACK
    )
    
    # Username helper text
    username_helper = ft.Text(
        "This is your unique identifier",
        size=12,
        color=ft.Colors.BLACK,
        text_align=ft.TextAlign.LEFT
    )
    
    # Password Input Field (without prefix icon)
    password_field = ft.TextField(
        label="Password",
        hint_text="Enter your password",
        width=300,
        disabled=False,
        password=True,
        can_reveal_password=True,
        bgcolor=ft.Colors.LIGHT_BLUE_ACCENT,
        color=ft.Colors.BLACK,
        label_style=ft.TextStyle(color=ft.Colors.BLACK),
        border_color=ft.Colors.BLACK
    )
    
    # Password helper text
    password_helper = ft.Text(
        "This is your secret key",
        size=12,
        color=ft.Colors.BLACK,
        text_align=ft.TextAlign.LEFT
    )
    
    # Login Logic Function
    async def login_click(e):
        # Create Dialogs for Feedback
        success_dialog = ft.AlertDialog(
            title=ft.Text("Login Successful"),
            content=ft.Container(
                content=ft.Text(f"Welcome, {username_field.value}!", text_align=ft.TextAlign.CENTER),
                alignment=ft.alignment.center
            ),
            actions=[ft.ElevatedButton("OK", on_click=lambda e: close_dialog(success_dialog))],
            icon=ft.Icon(ft.Icons.CHECK_CIRCLE, color=ft.Colors.GREEN)
        )
        
        failure_dialog = ft.AlertDialog(
            title=ft.Text("Login Failed"),
            content=ft.Container(
                content=ft.Text("Invalid username or password", text_align=ft.TextAlign.CENTER),
                alignment=ft.alignment.center
            ),
            actions=[ft.ElevatedButton("OK", on_click=lambda e: close_dialog(failure_dialog))],
            icon=ft.Icon(ft.Icons.ERROR, color=ft.Colors.RED)
        )
        
        invalid_input_dialog = ft.AlertDialog(
            title=ft.Text("Input Error"),
            content=ft.Container(
                content=ft.Text("Please enter username and password", text_align=ft.TextAlign.CENTER),
                alignment=ft.alignment.center
            ),
            actions=[ft.ElevatedButton("OK", on_click=lambda e: close_dialog(invalid_input_dialog))],
            icon=ft.Icon(ft.Icons.INFO, color=ft.Colors.BLUE)
        )
        
        database_error_dialog = ft.AlertDialog(
            title=ft.Text("Database Error"),
            content=ft.Container(
                content=ft.Text("An error occurred while connecting to the database", text_align=ft.TextAlign.CENTER),
                alignment=ft.alignment.center
            ),
            actions=[ft.ElevatedButton("OK", on_click=lambda e: close_dialog(database_error_dialog))]
        )
        
        def close_dialog(dialog):
            dialog.open = False
            page.update()
        
        # Validation and Database Logic
        # Check if username or password are empty
        if not username_field.value or not password_field.value:
            page.overlay.append(invalid_input_dialog)
            invalid_input_dialog.open = True
            page.update()
            return
        
        try:
            # Establish database connection
            connection = connect_db()
            cursor = connection.cursor()
            
            # Execute parameterized SQL query to prevent SQL injection
            query = "SELECT * FROM users WHERE username = %s AND password = %s"
            cursor.execute(query, (username_field.value, password_field.value))
            
            # Fetch the result
            result = cursor.fetchone()
            
            # Close the database connection
            cursor.close()
            connection.close()
            
            # Check if user was found
            if result:
                page.overlay.append(success_dialog)
                success_dialog.open = True
            else:
                page.overlay.append(failure_dialog)
                failure_dialog.open = True
            
            page.update()
            
        except mysql.connector.Error as e:
            print(f"Database error: {e}")
            page.overlay.append(database_error_dialog)
            database_error_dialog.open = True
            page.update()
    
    # Login Button (white background)
    login_button = ft.ElevatedButton(
        text="Login",
        on_click=login_click,
        width=100,
        icon=ft.Icons.LOGIN,
        bgcolor=ft.Colors.WHITE,
        color=ft.Colors.BLACK,
        icon_color=ft.Colors.BLACK
    )
    
    # Add all controls to the page with proper layout
    page.add(
        ft.Container(height=10),  # Top spacing
        login_title,
        ft.Container(height=10),  # Spacing after title
        
        # Username section with icon outside and proper alignment
        ft.Container(
            content=ft.Row(
                [
                    ft.Icon(ft.Icons.PERSON, color=ft.Colors.BLACK, size=20),
                    ft.Column(
                        [
                            username_field,
                            username_helper
                        ],
                        spacing=3,
                        alignment=ft.MainAxisAlignment.START
                    )
                ],
                spacing=15,
                alignment=ft.MainAxisAlignment.CENTER
            ),
            alignment=ft.alignment.center,
            margin=ft.margin.only(left=10)
        ),
        
        ft.Container(height=10),  # Spacing between fields
        
        # Password section with icon outside and proper alignment
        ft.Container(
            content=ft.Row(
                [
                    ft.Icon(ft.Icons.PASSWORD, color=ft.Colors.BLACK, size=20),
                    ft.Column(
                        [
                            password_field,
                            password_helper
                        ],
                        spacing=3,
                        alignment=ft.MainAxisAlignment.START
                    )
                ],
                spacing=15,
                alignment=ft.MainAxisAlignment.CENTER
            ),
            alignment=ft.alignment.center,
            margin=ft.margin.only(left=10)
        ),
        
        ft.Container(height=10),  # Spacing before button
        
        # Login button centered horizontally
        ft.Container(
            content=login_button,
            alignment=ft.alignment.top_right,
            margin=ft.margin.only(right=20, bottom=20) 
        )
    )

# Start the Flet app
ft.app(target=main)