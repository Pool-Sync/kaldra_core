"""
Quick diagnostic: Show which environment variables are loaded
"""
import os

print("=" * 60)
print("Environment Variables Diagnostic")
print("=" * 60)

vars_to_check = [
    "MEDIASTACK_API_KEY",
    "GNEWS_API_KEY",
    "X_BEARER_TOKEN",
    "X_API_KEY",
    "YOUTUBE_API_KEY",
    "REDDIT_CLIENT_ID",
    "REDDIT_CLIENT_SECRET",
]

for var in vars_to_check:
    value = os.getenv(var, "NOT SET")
    
    # Check if it's a placeholder
    is_placeholder = value.startswith("COLE_") if value != "NOT SET" else False
    
    # Mask real keys for security
    if value != "NOT SET" and not is_placeholder:
        masked = value[:8] + "..." + value[-4:] if len(value) > 12 else value[:4] + "..."
        status = f"✅ SET ({masked})"
    elif is_placeholder:
        status = f"⚠️  PLACEHOLDER ({value})"
    else:
        status = "❌ NOT SET"
    
    print(f"{var:25} {status}")

print("=" * 60)
