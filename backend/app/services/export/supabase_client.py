import os
from supabase import create_client, Client
from app.core.config import settings

try:
    supabase: Client = create_client(settings.supabase_url, settings.supabase_secret_key)
except AttributeError:
    print("WARNING: SUPABASE_URL or SUPABASE_KEY not found in settings.")
    supabase = None

def upload_pdf_to_supabase(file_path: str, destination_path: str, bucket_name: str) -> str:
    if not supabase:
        raise Exception("Supabase client is not configured.")

    try:
        with open(file_path, 'rb') as f:
            res = res = supabase.storage.from_(bucket_name).upload(
                path=destination_path,
                file=f,
                file_options={"content-type": "application/pdf"}
            )

            public_url = supabase.storage.from_(bucket_name).get_public_url(destination_path)
            return public_url
    
    except Exception as e:
        print({f"Error uploading to supabase"})
        print(repr(e))
        raise e