import os
import threading
import subprocess
from kaggle.api.kaggle_api_extended import KaggleApi

DATASET_NAME = "ko-vi-fpcb-translator"
REPO_PATH = os.getcwd()

# Kaggle API 인증 정보 설정
os.environ['KAGGLE_USERNAME'] = "yakdoljo"
os.environ['KAGGLE_KEY'] = "7959e4a5f973e51fb68a28d3b6375828"

def download_dataset():
    api = KaggleApi()
    api.authenticate()
    api.dataset_download_files(DATASET_NAME, path=REPO_PATH, unzip=True)
    print("Dataset download completed")

def push_to_github():
    while True:
        files = os.listdir(REPO_PATH)
        if files:
            subprocess.run(["git", "add", "."])
            subprocess.run(["git", "commit", "-m", f"Update Kaggle dataset: {DATASET_NAME}"])
            subprocess.run(["git", "push", "origin", "main"])
            print("Changes pushed to GitHub")
        if not download_thread.is_alive():
            break

# 다운로드 쓰레드
download_thread = threading.Thread(target=download_dataset)

# 푸시 쓰레드
push_thread = threading.Thread(target=push_to_github)

# 다운로드 쓰레드 시작
download_thread.start()

# 푸시 쓰레드 시작
push_thread.start()

# 두 쓰레드가 완료될 때까지 대기
download_thread.join()
push_thread.join()
