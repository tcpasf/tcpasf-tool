import os
import sys

sys.path.append(os.path.dirname(__file__))
from tools.login_system import LoginSystem

if __name__ == "__main__":
    login_system = LoginSystem()
    login_system.run()
