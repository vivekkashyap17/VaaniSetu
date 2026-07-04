"""Create/update the BhashaBridge backend Hugging Face Space and deploy it.

Usage (from backend/):

    export HF_WRITE_TOKEN=hf_...        # a WRITE-scoped token
    export APP_API_KEY=<your api key>   # the X-API-Key clients must send
    # optional overrides:
    export SPACE_ID=<user>/bhashabridge-backend
    export ALLOWED_ORIGINS="*"          # tighten to your Vercel URL later
    export HF_MODEL_TOKEN=hf_...        # token used inside the Space to pull
                                        # the gated IndicTrans2 model (defaults
                                        # to HF_WRITE_TOKEN)

    python deploy/deploy_hf_space.py

It creates the Space (Docker SDK), sets config as Space variables/secrets,
and uploads app/, requirements.txt, Dockerfile and the Space README. Nothing
secret is written to the repo — everything comes from the environment.
"""

import os

from pathlib import Path

from huggingface_hub import HfApi


BACKEND_DIR = Path(__file__).resolve().parent.parent

README_PATH = BACKEND_DIR / "deploy" / "README-hf-space.md"


# Non-secret config -> Space "variables". All required by settings.py.
SPACE_VARIABLES = {
    "APP_NAME": "BhashaBridge",
    "APP_VERSION": "1.0.0",
    "DEBUG": "False",
    "HOST": "0.0.0.0",
    "PORT": "8000",
    "PROJECT_NAME": "BhashaBridge AI",
    "DATABASE_URL": "sqlite:///./bhashabridge.db",
    "TRANSLATION_MODEL": "facebook/nllb-200-distilled-600M",
    "EMBEDDING_MODEL": "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2",
    "REFINEMENT_MODEL": "google/flan-t5-base",
    "INDICTRANS2_INDIC_EN_MODEL": "ai4bharat/indictrans2-indic-en-dist-200M",
    "RATE_LIMIT": "30/minute",
}


def main():

    token = os.environ["HF_WRITE_TOKEN"]

    api_key = os.environ["APP_API_KEY"]

    allowed_origins = os.environ.get("ALLOWED_ORIGINS", "*")

    model_token = os.environ.get("HF_MODEL_TOKEN", token)

    api = HfApi(token=token)

    user = api.whoami()["name"]

    space_id = os.environ.get(
        "SPACE_ID",
        f"{user}/bhashabridge-backend"
    )

    print(f"Target Space: {space_id}")

    api.create_repo(
        repo_id=space_id,
        repo_type="space",
        space_sdk="docker",
        exist_ok=True,
        private=False,
    )

    print("Setting Space variables...")

    for key, value in SPACE_VARIABLES.items():

        api.add_space_variable(space_id, key, value)

    api.add_space_variable(space_id, "ALLOWED_ORIGINS", allowed_origins)

    print("Setting Space secrets...")

    api.add_space_secret(space_id, "API_KEY", api_key)

    api.add_space_secret(space_id, "HF_TOKEN", model_token)

    print("Uploading backend files...")

    api.upload_folder(
        repo_id=space_id,
        repo_type="space",
        folder_path=str(BACKEND_DIR),
        allow_patterns=[
            "app/**",
            "requirements.txt",
            "Dockerfile",
        ],
        commit_message="Deploy BhashaBridge backend",
    )

    api.upload_file(
        path_or_fileobj=str(README_PATH),
        path_in_repo="README.md",
        repo_id=space_id,
        repo_type="space",
        commit_message="Add Space README",
    )

    app_url = f"https://{space_id.replace('/', '-')}.hf.space"

    print("\nDone. The Space is building.")

    print(f"App URL:      {app_url}")

    print(f"Health:       {app_url}/api/v1/health")

    print(f"Settings/logs: https://huggingface.co/spaces/{space_id}")


if __name__ == "__main__":

    main()
