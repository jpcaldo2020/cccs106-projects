"""Weather Application using Flet v0.28.3 - With 5-Day Forecast Feature"""

import flet as ft
import asyncio
from datetime import datetime
from weather_service import WeatherService
from config import Config


class WeatherApp:
    """Main Weather Application class with 5-day forecast."""
    
    def __init__(self, page: ft.Page):
        self.page = page
        self.weather_service = WeatherService()
        self.search_history = []
        self.current_theme = "light"
        self.current_city = ""  # Store current city for forecast
        self.setup_page()
        self.build_ui()
    
    def setup_page(self):
        """Configure page settings."""
        self.page.title = Config.APP_TITLE
        self.page.theme_mode = ft.ThemeMode.LIGHT
        self.page.padding = 20
        
        # Window properties
        self.page.window.width = Config.APP_WIDTH
        self.page.window.height = 700  # Increased height for forecast
        self.page.window.resizable = False
        self.page.window.center()
        
        # Enable hidden scrolling
        self.page.scroll = ft.ScrollMode.HIDDEN
    
    def get_theme_colors(self):
        """Get colors based on current theme."""
        if self.current_theme == "light":
            return {
                "bg": ft.Colors.WHITE,
                "title": ft.Colors.BLUE_700,
                "input_border": ft.Colors.BLUE_400,
                "input_bg": ft.Colors.WHITE,
                "input_text": ft.Colors.BLACK,
                "input_label": ft.Colors.BLUE_600,
                "button_bg": ft.Colors.BLUE_700,
                "button_text": ft.Colors.WHITE,
                "location_button_bg": ft.Colors.GREEN_700,
                "container_bg": ft.Colors.BLUE_50,
                "card_bg": ft.Colors.WHITE,
                "text_primary": ft.Colors.BLACK,
                "text_secondary": ft.Colors.GREY_700,
                "temp_color": ft.Colors.BLUE_900,
                "icon_color": ft.Colors.BLUE_700,
                "error_color": ft.Colors.RED_700,
                "dropdown_bg": ft.Colors.WHITE,
                "divider": ft.Colors.BLUE_200,
                "tab_bg": ft.Colors.BLUE_100,
                "suggestion_hover": ft.Colors.GREY_100,
            }
        elif self.current_theme == "dark":
            return {
                "bg": "#121212",
                "title": ft.Colors.BLUE_300,
                "input_border": ft.Colors.BLUE_700,
                "input_bg": "#1e1e1e",
                "input_text": ft.Colors.WHITE,
                "input_label": ft.Colors.BLUE_400,
                "button_bg": ft.Colors.BLUE_800,
                "button_text": ft.Colors.WHITE,
                "location_button_bg": ft.Colors.GREEN_800,
                "container_bg": "#1e1e1e",
                "card_bg": "#2d2d2d",
                "text_primary": ft.Colors.WHITE,
                "text_secondary": ft.Colors.GREY_400,
                "temp_color": ft.Colors.BLUE_300,
                "icon_color": ft.Colors.BLUE_400,
                "error_color": ft.Colors.RED_300,
                "dropdown_bg": "#1e1e1e",
                "divider": ft.Colors.BLUE_900,
                "tab_bg": "#2d2d2d",
                "suggestion_hover": "#3d3d3d",
            }
        else:  # pink
            return {
                "bg": "#fff0f5",
                "title": ft.Colors.PINK_700,
                "input_border": ft.Colors.PINK_300,
                "input_bg": ft.Colors.WHITE,
                "input_text": ft.Colors.PINK_900,
                "input_label": ft.Colors.PINK_600,
                "button_bg": ft.Colors.PINK_400,
                "button_text": ft.Colors.WHITE,
                "location_button_bg": ft.Colors.PINK_500,
                "container_bg": "#ffe4f0",
                "card_bg": ft.Colors.WHITE,
                "text_primary": ft.Colors.PINK_900,
                "text_secondary": ft.Colors.PINK_700,
                "temp_color": ft.Colors.PINK_800,
                "icon_color": ft.Colors.PINK_600,
                "error_color": ft.Colors.RED_700,
                "dropdown_bg": ft.Colors.WHITE,
                "divider": ft.Colors.PINK_200,
                "tab_bg": "#ffe4f0",
                "suggestion_hover": "#ffe4f0",
            }
    
    def build_ui(self):
        """Build the user interface."""
        colors = self.get_theme_colors()
        
        # Set page background
        self.page.bgcolor = colors["bg"]
        
        # Title
        self.title = ft.Text(
            "Weather App",
            size=32,
            weight=ft.FontWeight.BOLD,
            color=colors["title"],
        )
        
        # Theme toggle button
        self.theme_button = ft.IconButton(
            icon=ft.Icons.SUNNY,
            icon_color=colors["icon_color"],
            tooltip="Change theme (Light/Dark/Pink)",
            on_click=self.cycle_theme,
        )
        
        # Title row with theme button
        self.title_row = ft.Row(
            [self.title, self.theme_button],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        )
        
        # Search suggestions container
        self.suggestions_column = ft.Column(spacing=0, visible=False)
        
        # City input field
        self.city_input = ft.TextField(
            label="Enter city name",
            label_style=ft.TextStyle(color=colors["input_label"]),
            text_style=ft.TextStyle(color=colors["input_text"]),
            hint_text="e.g., London, Tokyo, New York",
            hint_style=ft.TextStyle(color=colors["text_secondary"]),
            border_color=colors["input_border"],
            focused_border_color=colors["icon_color"],
            bgcolor=colors["input_bg"],
            prefix_icon=ft.Icons.LOCATION_CITY,
            autofocus=True,
            on_submit=self.on_search,
            on_change=self.on_input_change,
            on_focus=self.on_input_focus,
            on_blur=self.on_input_blur,
        )
        
        # Input container
        self.input_container = ft.Container(
            content=ft.Stack([
                ft.Column([self.city_input, self.suggestions_column], spacing=0),
            ]),
            width=800,
        )
        
        # Search button
        self.search_button = ft.ElevatedButton(
            "Get Weather",
            icon=ft.Icons.SEARCH,
            on_click=self.on_search,
            style=ft.ButtonStyle(
                color=colors["button_text"],
                bgcolor=colors["button_bg"],
            ),
        )
        
        # Location button
        self.location_button = ft.ElevatedButton(
            "Use My Location",
            icon=ft.Icons.MY_LOCATION,
            on_click=self.on_location_search,
            style=ft.ButtonStyle(
                color=colors["button_text"],
                bgcolor=colors["location_button_bg"],
            ),
        )
        
        # Button row
        self.button_row = ft.Row(
            [self.search_button, self.location_button],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=10,
        )
        
        # Tabs for Current Weather and Forecast
        self.weather_tab = ft.Tab(
            text="Current",
            icon=ft.Icons.WB_SUNNY,
        )
        
        self.forecast_tab = ft.Tab(
            text="5-Day Forecast",
            icon=ft.Icons.CALENDAR_MONTH,
        )
        
        self.tabs = ft.Tabs(
            selected_index=0,
            tabs=[self.weather_tab, self.forecast_tab],
            on_change=self.on_tab_change,
            visible=False,
        )
        
        # Weather containers
        self.weather_container = ft.Container(visible=False)
        self.forecast_container = ft.Container(visible=False)
        
        # Error message
        self.error_message = ft.Text("", color=colors["error_color"], visible=False)
        
        # Loading indicator
        self.loading = ft.ProgressRing(visible=False, color=colors["icon_color"])
        
        # Main column
        self.main_column = ft.Column(
            [
                self.title_row,
                ft.Divider(height=20, color=ft.Colors.TRANSPARENT),
                self.input_container,
                self.button_row,
                ft.Divider(height=20, color=ft.Colors.TRANSPARENT),
                self.loading,
                self.error_message,
                self.tabs,
                self.weather_container,
                self.forecast_container,
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=10,
            scroll=ft.ScrollMode.HIDDEN,
        )
        
        # Add to page
        self.page.add(self.main_column)
    
    def cycle_theme(self, e):
        """Cycle through light -> dark -> pink themes."""
        if self.current_theme == "light":
            self.current_theme = "dark"
            self.theme_button.icon = ft.Icons.DARK_MODE
        elif self.current_theme == "dark":
            self.current_theme = "pink"
            self.theme_button.icon = ft.Icons.FAVORITE
        else:
            self.current_theme = "light"
            self.theme_button.icon = ft.Icons.SUNNY
        
        self.update_all_colors()
        self.page.update()
    
    def update_all_colors(self):
        """Update all UI colors including forecast."""
        colors = self.get_theme_colors()
        
        self.page.bgcolor = colors["bg"]
        self.title.color = colors["title"]
        self.theme_button.icon_color = colors["icon_color"]
        
        self.city_input.border_color = colors["input_border"]
        self.city_input.focused_border_color = colors["icon_color"]
        self.city_input.bgcolor = colors["input_bg"]
        self.city_input.label_style = ft.TextStyle(color=colors["input_label"])
        self.city_input.text_style = ft.TextStyle(color=colors["input_text"])
        
        self.search_button.style = ft.ButtonStyle(
            color=colors["button_text"], bgcolor=colors["button_bg"]
        )
        self.location_button.style = ft.ButtonStyle(
            color=colors["button_text"], bgcolor=colors["location_button_bg"]
        )
        
        self.error_message.color = colors["error_color"]
        self.loading.color = colors["icon_color"]
        
        # Update weather container colors if visible
        if self.weather_container.visible and self.weather_container.content:
            self.update_weather_colors()
        
        # Update forecast container colors if visible
        if self.forecast_container.visible and self.forecast_container.content:
            self.update_forecast_colors()
    
    def on_tab_change(self, e):
        """Handle tab changes."""
        if e.control.selected_index == 0:  # Current Weather
            self.weather_container.visible = True
            self.forecast_container.visible = False
        else:  # Forecast
            self.weather_container.visible = False
            self.forecast_container.visible = True
        self.page.update()
    
    def on_search(self, e):
        """Handle search."""
        self.page.run_task(self.get_weather_and_forecast)
    
    def on_location_search(self, e):
        """Handle location search."""
        self.page.run_task(self.get_location_weather)
    
    def on_input_change(self, e):
        """Handle input changes."""
        search_text = self.city_input.value.strip().lower()
        
        if not search_text or len(self.search_history) == 0:
            self.suggestions_column.visible = False
            self.page.update()
            return
        
        matching_cities = [
            city for city in self.search_history if search_text in city.lower()
        ]
        
        if matching_cities:
            self.show_suggestions(matching_cities)
        else:
            self.suggestions_column.visible = False
            self.page.update()
    
    def on_input_focus(self, e):
        """Show all suggestions on focus."""
        if not self.city_input.value.strip() and len(self.search_history) > 0:
            self.show_suggestions(self.search_history)
    
    def on_input_blur(self, e):
        """Hide suggestions on blur."""
        async def hide_after_delay():
            await asyncio.sleep(0.2)
            self.suggestions_column.visible = False
            self.page.update()
        
        self.page.run_task(hide_after_delay)
    
    def show_suggestions(self, cities: list):
        """Display suggestions."""
        colors = self.get_theme_colors()
        suggestions_list = ft.Column(spacing=0)
        
        for city in cities:
            suggestion_btn = ft.Container(
                content=ft.Row(
                    [
                        ft.Icon(ft.Icons.HISTORY, size=16, color=colors["text_secondary"]),
                        ft.Text(city, color=colors["text_primary"], size=14),
                    ],
                    spacing=10,
                ),
                bgcolor=colors["card_bg"],
                padding=10,
                on_click=lambda e, c=city: self.select_suggestion(c),
                on_hover=lambda e: self.on_suggestion_hover(e),
                border=ft.border.only(bottom=ft.BorderSide(1, colors["divider"])),
            )
            suggestions_list.controls.append(suggestion_btn)
        
        suggestion_container = ft.Container(
            content=suggestions_list,
            bgcolor=colors["card_bg"],
            border=ft.border.all(1, colors["input_border"]),
            border_radius=5,
        )
        
        self.suggestions_column.controls = [suggestion_container]
        self.suggestions_column.visible = True
        self.page.update()
    
    def on_suggestion_hover(self, e):
        """Handle hover."""
        colors = self.get_theme_colors()
        e.control.bgcolor = colors["suggestion_hover"] if e.data == "true" else colors["card_bg"]
        self.page.update()
    
    def select_suggestion(self, city: str):
        """Select suggestion."""
        self.city_input.value = city
        self.suggestions_column.visible = False
        self.page.update()
        self.page.run_task(self.get_weather_and_forecast)
    
    async def get_weather_and_forecast(self):
        """Fetch both current weather and forecast."""
        city = self.city_input.value.strip()
        
        if not city:
            self.show_error("Please enter a city name")
            return
        
        self.loading.visible = True
        self.error_message.visible = False
        self.tabs.visible = False
        self.weather_container.visible = False
        self.forecast_container.visible = False
        self.suggestions_column.visible = False
        self.page.update()
        
        try:
            # Fetch both current weather and forecast
            weather_data, forecast_data = await asyncio.gather(
                self.weather_service.get_weather(city),
                self.weather_service.get_forecast(city)
            )
            
            self.current_city = city
            self.add_to_history(city)
            
            # Display both
            await self.display_weather(weather_data)
            await self.display_forecast(forecast_data)
            
            # Show tabs
            self.tabs.visible = True
            self.tabs.selected_index = 0
            self.weather_container.visible = True
            self.forecast_container.visible = False
            
        except Exception as e:
            self.show_error(str(e))
        
        finally:
            self.loading.visible = False
            self.page.update()
    
    async def get_location_weather(self):
        """Get weather for current location."""
        self.loading.visible = True
        self.error_message.visible = False
        self.tabs.visible = False
        self.weather_container.visible = False
        self.forecast_container.visible = False
        self.page.update()
        
        try:
            import httpx
            
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.get("https://ipapi.co/json/")
                data = response.json()
                city = data.get('city', 'Unknown')
                
                weather_data, forecast_data = await asyncio.gather(
                    self.weather_service.get_weather(city),
                    self.weather_service.get_forecast(city)
                )
                
                self.current_city = city
                self.add_to_history(city)
                
                await self.display_weather(weather_data)
                await self.display_forecast(forecast_data)
                
                self.tabs.visible = True
                self.tabs.selected_index = 0
                self.weather_container.visible = True
                self.forecast_container.visible = False
                
        except Exception as e:
            self.show_error(f"Could not get your location: {str(e)}")
        
        finally:
            self.loading.visible = False
            self.page.update()
    
    def add_to_history(self, city: str):
        """Add city to history."""
        if city not in self.search_history:
            self.search_history.insert(0, city)
            self.search_history = self.search_history[:10]
    
    async def display_weather(self, data: dict):
        """Display current weather."""
        colors = self.get_theme_colors()
        
        city_name = data.get("name", "Unknown")
        country = data.get("sys", {}).get("country", "")
        temp = data.get("main", {}).get("temp", 0)
        feels_like = data.get("main", {}).get("feels_like", 0)
        humidity = data.get("main", {}).get("humidity", 0)
        pressure = data.get("main", {}).get("pressure", 0)
        cloudiness = data.get("clouds", {}).get("all", 0)
        description = data.get("weather", [{}])[0].get("description", "").title()
        icon_code = data.get("weather", [{}])[0].get("icon", "01d")
        wind_speed = data.get("wind", {}).get("speed", 0)
        
        # Store references to text elements for theme updates
        self.weather_city_text = ft.Text(
            f"{city_name}, {country}",
            size=24,
            weight=ft.FontWeight.BOLD,
            color=colors["text_primary"],
        )
        
        self.weather_desc_text = ft.Text(
            description, 
            size=20, 
            italic=True, 
            color=colors["text_secondary"]
        )
        
        self.weather_temp_text = ft.Text(
            f"{temp:.1f}°C",
            size=48,
            weight=ft.FontWeight.BOLD,
            color=colors["temp_color"],
        )
        
        self.weather_feels_text = ft.Text(
            f"Feels like {feels_like:.1f}°C", 
            size=16, 
            color=colors["text_secondary"]
        )
        
        self.weather_divider = ft.Divider(color=colors["divider"])
        
        # Create info cards and store references
        self.weather_info_cards = [
            self.create_info_card(ft.Icons.WATER_DROP, "Humidity", f"{humidity}%", colors),
            self.create_info_card(ft.Icons.AIR, "Wind", f"{wind_speed} m/s", colors),
            self.create_info_card(ft.Icons.COMPRESS, "Pressure", f"{pressure}hPa", colors),
            self.create_info_card(ft.Icons.CLOUD, "Clouds", f"{cloudiness}%", colors),
        ]
        
        self.weather_container.content = ft.Container(
            content=ft.Column(
                [
                    self.weather_city_text,
                    ft.Row(
                        [
                            ft.Image(
                                src=f"https://openweathermap.org/img/wn/{icon_code}@2x.png",
                                width=100,
                                height=100,
                            ),
                            self.weather_desc_text,
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                    ),
                    self.weather_temp_text,
                    self.weather_feels_text,
                    self.weather_divider,
                    ft.Container(
                        content=ft.Column(
                            [
                                ft.Row(
                                    [self.weather_info_cards[0], self.weather_info_cards[1]],
                                    alignment=ft.MainAxisAlignment.CENTER,
                                    spacing=15,
                                ),
                                ft.Row(
                                    [self.weather_info_cards[2], self.weather_info_cards[3]],
                                    alignment=ft.MainAxisAlignment.CENTER,
                                    spacing=15,
                                ),
                            ],
                            spacing=15,
                        ),
                        width=350,
                    ),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=10,
            ),
            bgcolor=colors["container_bg"],
            border_radius=15,
            padding=20,
            border=ft.border.all(2, colors["input_border"]),
        )
        
        self.page.update()
    
    def update_weather_colors(self):
        """Update weather display colors dynamically."""
        colors = self.get_theme_colors()
        
        # Update container
        if self.weather_container.content:
            self.weather_container.content.bgcolor = colors["container_bg"]
            self.weather_container.content.border = ft.border.all(2, colors["input_border"])
        
        # Update text colors
        if hasattr(self, 'weather_city_text'):
            self.weather_city_text.color = colors["text_primary"]
        if hasattr(self, 'weather_desc_text'):
            self.weather_desc_text.color = colors["text_secondary"]
        if hasattr(self, 'weather_temp_text'):
            self.weather_temp_text.color = colors["temp_color"]
        if hasattr(self, 'weather_feels_text'):
            self.weather_feels_text.color = colors["text_secondary"]
        if hasattr(self, 'weather_divider'):
            self.weather_divider.color = colors["divider"]
        
        # Update info cards
        if hasattr(self, 'weather_info_cards'):
            for card in self.weather_info_cards:
                card.bgcolor = colors["card_bg"]
                card.border = ft.border.all(1, colors["input_border"])
                # Update card content colors
                if card.content and isinstance(card.content, ft.Column):
                    for item in card.content.controls:
                        if isinstance(item, ft.Icon):
                            item.color = colors["icon_color"]
                        elif isinstance(item, ft.Text):
                            if item.size == 12:
                                item.color = colors["text_secondary"]
                            elif item.size == 16:
                                item.color = colors["text_primary"]
    
    async def display_forecast(self, data: dict):
        """Display 5-day forecast."""
        colors = self.get_theme_colors()
        
        # Process forecast data - group by date
        forecast_list = data.get("list", [])
        daily_forecasts = {}
        
        for item in forecast_list:
            dt = datetime.fromtimestamp(item["dt"])
            date_key = dt.strftime("%Y-%m-%d")
            
            if date_key not in daily_forecasts:
                daily_forecasts[date_key] = {
                    "temps": [],
                    "conditions": [],
                    "icons": [],
                    "date": dt,
                }
            
            daily_forecasts[date_key]["temps"].append(item["main"]["temp"])
            daily_forecasts[date_key]["conditions"].append(
                item["weather"][0]["description"]
            )
            daily_forecasts[date_key]["icons"].append(
                item["weather"][0]["icon"]
            )
        
        # Get first 5 days
        sorted_dates = sorted(daily_forecasts.keys())[:5]
        forecast_cards = []
        
        # Store forecast cards for theme updates
        self.forecast_cards_list = []
        
        for date_key in sorted_dates:
            day_data = daily_forecasts[date_key]
            high_temp = max(day_data["temps"])
            low_temp = min(day_data["temps"])
            
            # Most common condition
            condition = max(set(day_data["conditions"]), key=day_data["conditions"].count).title()
            
            # Most common icon
            icon = max(set(day_data["icons"]), key=day_data["icons"].count)
            
            # Format date
            day_name = day_data["date"].strftime("%A")
            date_str = day_data["date"].strftime("%b %d")
            
            # Create text elements with references
            day_name_text = ft.Text(
                day_name,
                size=16,
                weight=ft.FontWeight.BOLD,
                color=colors["text_primary"],
            )
            
            date_str_text = ft.Text(
                date_str,
                size=12,
                color=colors["text_secondary"],
            )
            
            condition_text = ft.Text(
                condition,
                size=12,
                color=colors["text_secondary"],
                text_align=ft.TextAlign.CENTER,
            )
            
            high_temp_text = ft.Text(
                f"↑{high_temp:.0f}°",
                size=14,
                weight=ft.FontWeight.BOLD,
                color=colors["temp_color"],
            )
            
            low_temp_text = ft.Text(
                f"↓{low_temp:.0f}°",
                size=14,
                color=colors["text_secondary"],
            )
            
            # Create forecast card
            card = ft.Container(
                content=ft.Column(
                    [
                        day_name_text,
                        date_str_text,
                        ft.Image(
                            src=f"https://openweathermap.org/img/wn/{icon}.png",
                            width=60,
                            height=60,
                        ),
                        condition_text,
                        ft.Row(
                            [high_temp_text, low_temp_text],
                            alignment=ft.MainAxisAlignment.CENTER,
                            spacing=10,
                        ),
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=5,
                ),
                bgcolor=colors["card_bg"],
                border_radius=10,
                padding=15,
                width=140,
                border=ft.border.all(1, colors["input_border"]),
            )
            
            # Store references for theme updates
            self.forecast_cards_list.append({
                'container': card,
                'day_name': day_name_text,
                'date_str': date_str_text,
                'condition': condition_text,
                'high_temp': high_temp_text,
                'low_temp': low_temp_text,
            })
            
            forecast_cards.append(card)
        
        # Create title text with reference
        self.forecast_title_text = ft.Text(
            "5-Day Weather Forecast",
            size=20,
            weight=ft.FontWeight.BOLD,
            color=colors["text_primary"],
        )
        
        self.forecast_divider = ft.Divider(color=colors["divider"])
        
        # Display forecast cards in a scrollable row
        self.forecast_container.content = ft.Container(
            content=ft.Column(
                [
                    self.forecast_title_text,
                    self.forecast_divider,
                    ft.Row(
                        forecast_cards,
                        alignment=ft.MainAxisAlignment.CENTER,
                        wrap=True,
                        spacing=10,
                        run_spacing=10,
                    ),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=15,
            ),
            bgcolor=colors["container_bg"],
            border_radius=15,
            padding=20,
            border=ft.border.all(2, colors["input_border"]),
        )
        
        self.page.update()
    
    def update_forecast_colors(self):
        """Update forecast display colors dynamically."""
        colors = self.get_theme_colors()
        
        # Update main container
        if self.forecast_container.content:
            self.forecast_container.content.bgcolor = colors["container_bg"]
            self.forecast_container.content.border = ft.border.all(2, colors["input_border"])
        
        # Update title and divider
        if hasattr(self, 'forecast_title_text'):
            self.forecast_title_text.color = colors["text_primary"]
        if hasattr(self, 'forecast_divider'):
            self.forecast_divider.color = colors["divider"]
        
        # Update all forecast cards
        if hasattr(self, 'forecast_cards_list'):
            for card_refs in self.forecast_cards_list:
                # Update container
                card_refs['container'].bgcolor = colors["card_bg"]
                card_refs['container'].border = ft.border.all(1, colors["input_border"])
                
                # Update text colors
                card_refs['day_name'].color = colors["text_primary"]
                card_refs['date_str'].color = colors["text_secondary"]
                card_refs['condition'].color = colors["text_secondary"]
                card_refs['high_temp'].color = colors["temp_color"]
                card_refs['low_temp'].color = colors["text_secondary"]
    
    def create_info_card(self, icon, label, value, colors):
        """Create info card."""
        return ft.Container(
            content=ft.Column(
                [
                    ft.Icon(icon, size=30, color=colors["icon_color"]),
                    ft.Text(label, size=12, color=colors["text_secondary"]),
                    ft.Text(
                        value,
                        size=16,
                        weight=ft.FontWeight.BOLD,
                        color=colors["text_primary"],
                    ),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=5,
            ),
            bgcolor=colors["card_bg"],
            border_radius=10,
            padding=15,
            width=150,
            border=ft.border.all(1, colors["input_border"]),
        )
    
    def show_error(self, message: str):
        """Show error message."""
        colors = self.get_theme_colors()
        self.error_message.value = f"❌ {message}"
        self.error_message.color = colors["error_color"]
        self.error_message.visible = True
        self.weather_container.visible = False
        self.forecast_container.visible = False
        self.tabs.visible = False
        self.page.update()


def main(page: ft.Page):
    """Main entry point."""
    WeatherApp(page)


if __name__ == "__main__":
    ft.app(target=main)