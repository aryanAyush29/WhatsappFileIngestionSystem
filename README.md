# Project Context: WhatsApp File Ingestion

Paste this whole document at the start of a new Claude chat to resume exactly where we left off.

## What this project is

A FastAPI service that receives WhatsApp document messages via a webhook, downloads the
actual file from Meta's Graph API, and saves it locally in a date-organized folder.

**Project path:** `C:\Users\Ankit\Desktop\Everest\whatsappFileIngestion\`

## File structure

```
whatsappFileIngestion/
├── app/
│   ├── __init__.py
│   ├── main.py              (FastAPI app, webhook route, process_document())
│   ├── media_downloader.py  (Meta Graph API calls: get_media_url, download_media)
│   └── file_manager.py      (folder creation, safe filenames, file-type checks)
├── downloads/
│   └── YYYY-MM-DD/          (date-based folders for saved files)
├── venv/
├── .env                     (GRAPH_API_VERSION, WHATSAPP_ACCESS_TOKEN, WHATSAPP_PHONE_NUMBER_ID — currently EMPTY)
├── .gitignore
└── requirements.txt
```

## Module responsibilities

| Module | Responsibility |
|---|---|
| `main.py` | FastAPI endpoints, coordinates the processing workflow |
| `media_downloader.py` | Talks to Meta Graph API, downloads WhatsApp media |
| `file_manager.py` | Creates date-based folders, generates safe filenames, validates file types |
| `.env` | Configuration and credentials (not committed to source control) |

## Current pipeline (fully built and tested, except real Meta credentials)

```
WhatsApp Document Message
        ↓
FastAPI Webhook (/webhook)
        ↓
Validate media_id present
        ↓
process_document(media_id, filename)
        ↓
get_media_url(media_id) → Meta Graph API
        ↓
get_today_folder() → today's download folder
        ↓
generate_safe_filename() → collision-safe filename
        ↓
download_media(media_url, output_path)
        ↓
Return saved file path
```

The webhook wraps `process_document()` in try/except — any failure returns a clean JSON
error instead of crashing the server.

`get_media_url()` validates that `GRAPH_API_VERSION` and `WHATSAPP_ACCESS_TOKEN` are set
before attempting a request, and raises a clear `ValueError` if not (instead of sending a
malformed request to Meta).

## Status

| Component | Status |
|---|---|
| FastAPI application | ✅ Completed |
| Test file upload (`/test-upload`) | ✅ Completed |
| Webhook endpoint | ✅ Completed |
| Webhook document parsing | ✅ Completed |
| Media ID extraction | ✅ Completed |
| `process_document()` full pipeline | ✅ Completed & tested |
| Error handling (webhook try/except + config validation) | ✅ Completed |
| Media downloader module | ✅ Created, integrated |
| File manager | ✅ Completed |
| Meta/WhatsApp credentials | ⏳ Pending |
| Real WhatsApp media download (end-to-end) | ⏳ Pending Meta access |

## How it was verified (without real credentials)

Sent a simulated webhook payload via PowerShell (`Invoke-RestMethod`) with a fake `media_id`
(`MEDIA_ID_TEST_123`) and filename `Mumbai.xlsx`. Confirmed:
- Webhook parses the payload correctly
- `process_document()` runs the full pipeline
- With empty `.env`, `get_media_url()` raises a clean `ValueError` explaining what's missing
- The server stays alive and returns structured JSON errors — no crashes

Dev environment note: using **PowerShell** on Windows, not cmd — `curl` in PowerShell is
aliased to `Invoke-WebRequest`, so use `curl.exe` explicitly or native `Invoke-RestMethod`
syntax, not Linux/cmd-style curl commands with `^` continuations.

## Next step (where to pick up)

**Set up real Meta/WhatsApp Business API credentials.** This is the one thing blocking a true
end-to-end test. Needed in `.env`:

- `GRAPH_API_VERSION` (e.g. `v19.0` — the Graph API version string)
- `WHATSAPP_ACCESS_TOKEN` (from the Meta Developer app / WhatsApp product)
- `WHATSAPP_PHONE_NUMBER_ID` (from the WhatsApp Business phone number setup)

I already have a Meta Developer account created. Need help creating/configuring the
WhatsApp product on it, generating an access token, and finding the phone_number_id.

After credentials are in place:
1. Re-run the same PowerShell test — should now succeed or hit a *different*, more specific
   Meta error (invalid media ID, since `MEDIA_ID_TEST_123` still isn't real).
2. Test with an actual WhatsApp message sent to the configured number to trigger a real webhook.
3. Then: harden `download_media()` for real-world edge cases (timeouts, large files, bad URLs).
4. Update the Word doc after real end-to-end success.

## Instruction for the assistant reading this

Continue step-by-step, one small change at a time, the way this project has been built so
far — explain what's changing and why, give exact code to paste, and confirm before moving
to the next step. Don't skip ahead or bundle multiple changes at once.





WHATSAPP FILE INGESTION PROJECT
===============================

Project Location:
C:\Users\Ankit\Desktop\Everest\whatsappFileIngestion

1. Open VS Code.

2. Open the project folder:
   whatsappFileIngestion

3. Open Terminal.

4. Navigate to project:
   cd "C:\Users\Ankit\Desktop\Everest\whatsappFileIngestion"

5. Activate virtual environment:
   .\venv\Scripts\Activate.ps1

6. Start FastAPI:
   uvicorn app.main:app --reload

7. Open Swagger:
   http://127.0.0.1:8000/docs

8. Test:
   GET /
   POST /test-upload
   POST /webhook

9. Stop server when finished:
   Ctrl + C
