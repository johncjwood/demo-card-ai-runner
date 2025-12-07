import os
import shutil

code_folder = "/code/"

demo_app = os.path.join(code_folder, "demo-card-app")
demo_app_orig = os.path.join(code_folder, "demo-card-app-orig")

if os.path.exists(demo_app):
    shutil.rmtree(demo_app)

if os.path.exists(demo_app_orig):
    shutil.copytree(demo_app_orig, demo_app)
