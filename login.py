import os
import sys
import pickle

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from google_auth_oauthlib.flow import InstalledAppFlow
from config import CLIENT_SECRETS_FILE, TOKEN_PICKLE_FILE

SCOPES = [
    "https://www.googleapis.com/auth/youtube.upload",
    "https://www.googleapis.com/auth/youtube.force-ssl"
]

class CustomFlow(InstalledAppFlow):
    def run_local_server(self, **kwargs):
        kwargs["open_browser"] = False
        def print_and_save(msg):
            url = msg.replace("AUTH_LINK_HERE: ", "").strip()
            with open("auth_link.txt", "w", encoding="utf-8") as f:
                f.write(url)
            print(f"\n=======================================================")
            print(f"👉 EXACT_URL: {url}")
            print(f"=======================================================\n")
            sys.stdout.flush()

        kwargs["authorization_prompt_message"] = "AUTH_LINK_HERE: {url}"
        
        # Override the print behavior by wrapping stdout temporarily
        old_stdout_write = sys.stdout.write
        def custom_write(text):
            if "AUTH_LINK_HERE:" in text:
                print_and_save(text)
            else:
                old_stdout_write(text)
        sys.stdout.write = custom_write

        try:
            return super().run_local_server(**kwargs)
        finally:
            sys.stdout.write = old_stdout_write

def main():
    flow = CustomFlow.from_client_secrets_file(
        str(CLIENT_SECRETS_FILE),
        scopes=SCOPES
    )
    print("\nREADY: Server running on port 8077...")
    sys.stdout.flush()

    credentials = flow.run_local_server(
        port=8077,
        prompt="consent",
        access_type="offline"
    )
    
    with open(TOKEN_PICKLE_FILE, "wb") as token:
        pickle.dump(credentials, token)
        
    print("\n✅ SUCCESS: YouTube channel connected successfully! token.pickle saved.")
    sys.stdout.flush()

if __name__ == "__main__":
    main()
