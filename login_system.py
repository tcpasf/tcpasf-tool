import os
import time
import getpass
import re
import datetime
from colorama import init, Fore, Style

from database import (
    initialize_database, authenticate_user, create_user,
    get_all_users, update_user_status, update_user_expiration,
    delete_user
)
from ascii_art import (
    tcpasf_login_ascii, print_gradient_text, clear_screen,
    spinner_animation, typing_animation, progress_bar,
    display_system_info, animated_login_attempt
)
from ip_tools import ip_tools_menu
from fivem_tools import fivem_tools_menu
from discord_tools import discord_tools_menu

init(autoreset=True)

class LoginSystem:
    def __init__(self):
        clear_screen()
        spinner_animation(2, "Initializing system")
        initialize_database()
        progress_bar(2, 40, "Loading security modules")
        self.current_user = None
        self.is_admin = False

    def display_welcome(self):
        clear_screen()
        spinner_animation(1, "Preparing interface")
        print(tcpasf_login_ascii())
        display_system_info()
        typing_animation("\nWelcome to TCPASF Advanced Login System", 0.01)
        print("\n" + "=" * 60 + "\n")

    def display_menu(self):
        self.display_welcome()
        print(f"{Fore.CYAN}[1]{Style.RESET_ALL} Login")
        print(f"{Fore.CYAN}[2]{Style.RESET_ALL} Exit")
        print("\n" + "=" * 60 + "\n")

    def get_valid_input(self, prompt, validation_func, error_message):
        while True:
            user_input = input(prompt)
            if validation_func(user_input):
                return user_input
            print(f"{Fore.RED}{error_message}{Style.RESET_ALL}")

    def validate_username(self, username):
        return 3 <= len(username) <= 20 and re.match(r'^[a-zA-Z0-9_]+$', username)

    def validate_password(self, password):
        return len(password) >= 8

    def login(self):
        self.display_welcome()
        typing_animation("=== User Login ===", 0.02, Fore.CYAN)
        print()

        username = input(f"{Fore.CYAN}Username: {Style.RESET_ALL}")
        password = getpass.getpass(f"{Fore.CYAN}Password: {Style.RESET_ALL}")

        # Show animated login attempt
        animated_login_attempt(username)

        success, message, is_admin = authenticate_user(username, password)

        if success:
            self.current_user = username
            self.is_admin = is_admin

            # Show loading animation
            if self.is_admin:
                progress_bar(2, 30, "Loading admin interface")
            else:
                progress_bar(2, 30, "Loading user interface")

            if self.is_admin:
                self.admin_dashboard()
            else:
                self.user_dashboard()
        else:
            # Show failed login animation
            animated_login_attempt(username, success=False, duration=1)
            print(f"{Fore.RED}{message}{Style.RESET_ALL}")
            time.sleep(2)

    def user_dashboard(self):
        while self.current_user:
            clear_screen()
            spinner_animation(1, "Loading dashboard")
            print(tcpasf_login_ascii())
            display_system_info()
            typing_animation(f"\nWelcome, {self.current_user}!", 0.02, Fore.GREEN)
            print("\n" + "=" * 60 + "\n")

            typing_animation("Available Options:", 0.01, Fore.YELLOW)
            print(f"{Fore.CYAN}[1]{Style.RESET_ALL} View Profile")
            print(f"{Fore.CYAN}[2]{Style.RESET_ALL} IP Tools")
            print(f"{Fore.CYAN}[3]{Style.RESET_ALL} FiveM Tools")
            print(f"{Fore.CYAN}[4]{Style.RESET_ALL} Discord Tools")
            print(f"{Fore.CYAN}[5]{Style.RESET_ALL} Change Password")
            print(f"{Fore.CYAN}[6]{Style.RESET_ALL} Logout")
            print("\n" + "=" * 60 + "\n")

            choice = input(f"{Fore.CYAN}Select an option: {Style.RESET_ALL}")

            if choice == '1':
                spinner_animation(1, "Loading profile")
                self.view_profile()
            elif choice == '2':
                spinner_animation(1, "Loading IP tools")
                ip_tools_menu()
            elif choice == '3':
                spinner_animation(1, "Loading FiveM tools")
                fivem_tools_menu()
            elif choice == '4':
                spinner_animation(1, "Loading Discord tools")
                discord_tools_menu()
            elif choice == '5':
                spinner_animation(1, "Loading password settings")
                self.change_password()
            elif choice == '6':
                spinner_animation(1, "Logging out")
                self.logout()
            else:
                print(f"{Fore.RED}Invalid option. Please try again.{Style.RESET_ALL}")
                time.sleep(1)

    def admin_dashboard(self):
        while self.current_user:
            clear_screen()
            spinner_animation(1, "Loading admin dashboard")
            print(tcpasf_login_ascii())
            display_system_info()
            typing_animation(f"\nWelcome, {self.current_user} (Admin)!", 0.02, Fore.GREEN)
            print("\n" + "=" * 60 + "\n")

            typing_animation("Admin Controls:", 0.01, Fore.YELLOW)
            print(f"{Fore.CYAN}[1]{Style.RESET_ALL} User Management")
            print(f"{Fore.CYAN}[2]{Style.RESET_ALL} IP Tools")
            print(f"{Fore.CYAN}[3]{Style.RESET_ALL} FiveM Tools")
            print(f"{Fore.CYAN}[4]{Style.RESET_ALL} Discord Tools")
            print(f"{Fore.CYAN}[5]{Style.RESET_ALL} Change Password")
            print(f"{Fore.CYAN}[6]{Style.RESET_ALL} Logout")
            print("\n" + "=" * 60 + "\n")

            choice = input(f"{Fore.CYAN}Select an option: {Style.RESET_ALL}")

            if choice == '1':
                spinner_animation(1, "Loading user management")
                self.user_management_menu()
            elif choice == '2':
                spinner_animation(1, "Loading IP tools")
                ip_tools_menu()
            elif choice == '3':
                spinner_animation(1, "Loading FiveM tools")
                fivem_tools_menu()
            elif choice == '4':
                spinner_animation(1, "Loading Discord tools")
                discord_tools_menu()
            elif choice == '5':
                spinner_animation(1, "Loading password settings")
                self.change_password()
            elif choice == '6':
                spinner_animation(1, "Logging out")
                self.logout()
            else:
                print(f"{Fore.RED}Invalid option. Please try again.{Style.RESET_ALL}")
                time.sleep(1)

    def user_management_menu(self):
        """Menu for user management options."""
        while True:
            clear_screen()
            print(tcpasf_login_ascii())
            print(f"\n{Fore.CYAN}╔══════════════════════════════════════════╗{Style.RESET_ALL}")
            print(f"{Fore.CYAN}║           USER MANAGEMENT MENU           ║{Style.RESET_ALL}")
            print(f"{Fore.CYAN}╚══════════════════════════════════════════╝{Style.RESET_ALL}")

            print(f"{Fore.CYAN}[1]{Style.RESET_ALL} View All Users")
            print(f"{Fore.CYAN}[2]{Style.RESET_ALL} Create New User")
            print(f"{Fore.CYAN}[3]{Style.RESET_ALL} Ban/Unban User")
            print(f"{Fore.CYAN}[4]{Style.RESET_ALL} Set User Expiration")
            print(f"{Fore.CYAN}[5]{Style.RESET_ALL} Delete User")
            print(f"{Fore.CYAN}[6]{Style.RESET_ALL} Back to Admin Dashboard")

            choice = input(f"\n{Fore.CYAN}Select an option: {Style.RESET_ALL}")

            if choice == '1':
                spinner_animation(1, "Loading user database")
                self.view_all_users()
            elif choice == '2':
                spinner_animation(1, "Loading user creation form")
                self.create_new_user()
            elif choice == '3':
                spinner_animation(1, "Loading user status management")
                self.manage_user_status()
            elif choice == '4':
                spinner_animation(1, "Loading expiration settings")
                self.set_user_expiration()
            elif choice == '5':
                spinner_animation(1, "Loading user deletion")
                self.delete_user_menu()
            elif choice == '6':
                break
            else:
                print(f"{Fore.RED}Invalid option. Please try again.{Style.RESET_ALL}")
                time.sleep(1)

    def view_profile(self):
        clear_screen()
        print(tcpasf_login_ascii())
        print(f"\n{Fore.CYAN}=== User Profile ==={Style.RESET_ALL}\n")
        print(f"{Fore.CYAN}Username:{Style.RESET_ALL} {self.current_user}")
        print(f"{Fore.CYAN}Account Status:{Style.RESET_ALL} Active")

        print("\n" + "=" * 60 + "\n")
        input(f"{Fore.CYAN}Press Enter to continue...{Style.RESET_ALL}")

    def change_password(self):
        clear_screen()
        print(tcpasf_login_ascii())
        print(f"\n{Fore.CYAN}=== Change Password ==={Style.RESET_ALL}\n")

        print(f"{Fore.YELLOW}Password change functionality would be implemented here.{Style.RESET_ALL}")
        print("\n" + "=" * 60 + "\n")
        input(f"{Fore.CYAN}Press Enter to continue...{Style.RESET_ALL}")

    def logout(self):
        self.current_user = None
        print(f"{Fore.GREEN}Logged out successfully.{Style.RESET_ALL}")
        time.sleep(1)

    def view_all_users(self):
        clear_screen()
        print(tcpasf_login_ascii())
        print(f"\n{Fore.CYAN}=== All Users ==={Style.RESET_ALL}\n")

        users = get_all_users()

        if not users:
            print(f"{Fore.YELLOW}No users found.{Style.RESET_ALL}")
        else:
            print(f"{Fore.CYAN}{'Username':<20} {'Admin':<10} {'Status':<10} {'Expiration':<15} {'Created':<20}{Style.RESET_ALL}")
            print("-" * 75)

            for user in users:
                username = user['username']
                is_admin = "Yes" if user['is_admin'] else "No"
                status = user['status']
                expiration = user['expiration_date'] if user['expiration_date'] else "Never"
                created = user['created_at'][:19]  # Truncate to remove milliseconds

                print(f"{username:<20} {is_admin:<10} {status:<10} {expiration:<15} {created:<20}")

        print("\n" + "=" * 60 + "\n")
        input(f"{Fore.CYAN}Press Enter to continue...{Style.RESET_ALL}")

    def create_new_user(self):
        clear_screen()
        print(tcpasf_login_ascii())
        print(f"\n{Fore.CYAN}=== Create New User ==={Style.RESET_ALL}\n")

        username = self.get_valid_input(
            f"{Fore.CYAN}Username: {Style.RESET_ALL}",
            self.validate_username,
            "Username must be 3-20 characters and contain only letters, numbers, and underscores."
        )

        password = self.get_valid_input(
            f"{Fore.CYAN}Password: {Style.RESET_ALL}",
            self.validate_password,
            "Password must be at least 8 characters long."
        )

        confirm_password = getpass.getpass(f"{Fore.CYAN}Confirm Password: {Style.RESET_ALL}")

        if password != confirm_password:
            print(f"{Fore.RED}Passwords do not match.{Style.RESET_ALL}")
            time.sleep(2)
            return

        is_admin_input = input(f"{Fore.CYAN}Make user an admin? (y/n): {Style.RESET_ALL}").lower()
        is_admin = is_admin_input == 'y'

        expiration_input = input(f"{Fore.CYAN}Set expiration (days, 0 for none): {Style.RESET_ALL}")
        expiration_days = None

        if expiration_input.isdigit():
            expiration_days = int(expiration_input)
            if expiration_days <= 0:
                expiration_days = None

        success, message = create_user(username, password, is_admin, expiration_days)

        if success:
            print(f"{Fore.GREEN}{message}{Style.RESET_ALL}")
        else:
            print(f"{Fore.RED}{message}{Style.RESET_ALL}")

        time.sleep(2)

    def manage_user_status(self):
        clear_screen()
        print(tcpasf_login_ascii())
        print(f"\n{Fore.CYAN}=== Ban/Unban User ==={Style.RESET_ALL}\n")

        users = get_all_users()

        if not users:
            print(f"{Fore.YELLOW}No users found.{Style.RESET_ALL}")
            time.sleep(2)
            return

        print(f"{Fore.CYAN}{'ID':<5} {'Username':<20} {'Status':<10}{Style.RESET_ALL}")
        print("-" * 35)

        for i, user in enumerate(users, 1):
            if user['username'] != self.current_user:  # Don't show current admin user
                print(f"{i:<5} {user['username']:<20} {user['status']:<10}")

        print("\n" + "=" * 60 + "\n")

        user_id = input(f"{Fore.CYAN}Enter user ID to manage (0 to cancel): {Style.RESET_ALL}")

        if not user_id.isdigit() or int(user_id) <= 0 or int(user_id) > len(users):
            return

        selected_user = users[int(user_id) - 1]
        username = selected_user['username']
        current_status = selected_user['status']

        print(f"\n{Fore.CYAN}Selected user: {username} (Current status: {current_status}){Style.RESET_ALL}")

        if current_status == 'banned':
            action = input(f"{Fore.CYAN}Unban this user? (y/n): {Style.RESET_ALL}").lower()
            new_status = 'active' if action == 'y' else 'banned'
        else:
            action = input(f"{Fore.CYAN}Ban this user? (y/n): {Style.RESET_ALL}").lower()
            new_status = 'banned' if action == 'y' else current_status

        if new_status != current_status:
            success, message = update_user_status(username, new_status)

            if success:
                print(f"{Fore.GREEN}{message}{Style.RESET_ALL}")
            else:
                print(f"{Fore.RED}{message}{Style.RESET_ALL}")

        time.sleep(2)

    def set_user_expiration(self):
        clear_screen()
        print(tcpasf_login_ascii())
        print(f"\n{Fore.CYAN}=== Set User Expiration ==={Style.RESET_ALL}\n")

        users = get_all_users()

        if not users:
            print(f"{Fore.YELLOW}No users found.{Style.RESET_ALL}")
            time.sleep(2)
            return

        print(f"{Fore.CYAN}{'ID':<5} {'Username':<20} {'Expiration':<15}{Style.RESET_ALL}")
        print("-" * 40)

        for i, user in enumerate(users, 1):
            if user['username'] != self.current_user:  # Don't show current admin user
                expiration = user['expiration_date'] if user['expiration_date'] else "Never"
                print(f"{i:<5} {user['username']:<20} {expiration:<15}")

        print("\n" + "=" * 60 + "\n")

        user_id = input(f"{Fore.CYAN}Enter user ID to set expiration (0 to cancel): {Style.RESET_ALL}")

        if not user_id.isdigit() or int(user_id) <= 0 or int(user_id) > len(users):
            return

        selected_user = users[int(user_id) - 1]
        username = selected_user['username']
        current_expiration = selected_user['expiration_date'] if selected_user['expiration_date'] else "Never"

        print(f"\n{Fore.CYAN}Selected user: {username} (Current expiration: {current_expiration}){Style.RESET_ALL}")

        expiration_input = input(f"{Fore.CYAN}Set new expiration (days, 0 for none): {Style.RESET_ALL}")

        if not expiration_input.isdigit():
            print(f"{Fore.RED}Invalid input. Please enter a number.{Style.RESET_ALL}")
            time.sleep(2)
            return

        expiration_days = int(expiration_input)
        if expiration_days <= 0:
            expiration_days = None

        success, message = update_user_expiration(username, expiration_days)

        if success:
            print(f"{Fore.GREEN}{message}{Style.RESET_ALL}")
        else:
            print(f"{Fore.RED}{message}{Style.RESET_ALL}")

        time.sleep(2)

    def delete_user_menu(self):
        """Menu for deleting users."""
        clear_screen()
        print(tcpasf_login_ascii())
        print(f"\n{Fore.CYAN}=== Delete User ==={Style.RESET_ALL}\n")

        users = get_all_users()

        if not users:
            print(f"{Fore.YELLOW}No users found.{Style.RESET_ALL}")
            time.sleep(2)
            return

        print(f"{Fore.CYAN}{'ID':<5} {'Username':<20} {'Admin':<10} {'Status':<10}{Style.RESET_ALL}")
        print("-" * 50)

        displayed_users = []
        for user in users:
            if user['username'] != self.current_user:  # Don't show current admin user
                displayed_users.append(user)
                is_admin = "Yes" if user['is_admin'] else "No"
                print(f"{len(displayed_users):<5} {user['username']:<20} {is_admin:<10} {user['status']:<10}")

        if not displayed_users:
            print(f"{Fore.YELLOW}No other users to delete.{Style.RESET_ALL}")
            time.sleep(2)
            return

        print("\n" + "=" * 60 + "\n")

        user_id = input(f"{Fore.CYAN}Enter user ID to delete (0 to cancel): {Style.RESET_ALL}")

        if not user_id.isdigit() or int(user_id) <= 0 or int(user_id) > len(displayed_users):
            return

        selected_user = displayed_users[int(user_id) - 1]
        username = selected_user['username']

        print(f"\n{Fore.RED}WARNING: You are about to delete user: {username}{Style.RESET_ALL}")
        print(f"{Fore.RED}This action cannot be undone!{Style.RESET_ALL}")

        confirm = input(f"\n{Fore.CYAN}Type 'DELETE' to confirm: {Style.RESET_ALL}")

        if confirm != "DELETE":
            print(f"{Fore.YELLOW}User deletion cancelled.{Style.RESET_ALL}")
            time.sleep(2)
            return

        success, message = delete_user(username)

        if success:
            print(f"{Fore.GREEN}{message}{Style.RESET_ALL}")
        else:
            print(f"{Fore.RED}{message}{Style.RESET_ALL}")

        time.sleep(2)

    def run(self):
        clear_screen()
        spinner_animation(2, "Starting TCPASF Security System")
        progress_bar(3, 50, "Initializing components")

        while True:
            self.display_menu()
            choice = input(f"{Fore.CYAN}Select an option: {Style.RESET_ALL}")

            if choice == '1':
                self.login()
            elif choice == '2':
                clear_screen()
                spinner_animation(1, "Preparing to exit")
                print(tcpasf_login_ascii())
                typing_animation("\nThank you for using TCPASF Login System. Goodbye!", 0.02, Fore.GREEN)
                progress_bar(2, 30, "Shutting down")
                clear_screen()
                break
            else:
                print(f"{Fore.RED}Invalid option. Please try again.{Style.RESET_ALL}")
                time.sleep(1)
