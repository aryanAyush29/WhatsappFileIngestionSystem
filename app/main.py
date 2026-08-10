from fastapi import FastAPI, UploadFile, File, HTTPException, Body
from app.media_downloader import get_media_url, download_media
from app.file_manager import (
    get_today_folder,
    is_allowed_file,
    generate_safe_filename
)


app = FastAPI()


@app.get("/")
def home():
    return {
        "message": "WhatsApp File Downloader API is running"
    }


@app.post("/test-upload")
async def test_upload(file: UploadFile = File(...)):

    # Step 1: Check whether a file was provided
    if not file.filename:
        raise HTTPException(
            status_code=400,
            detail="No file provided"
        )

    # Step 2: Validate file type
    if not is_allowed_file(file.filename):
        raise HTTPException(
            status_code=400,
            detail="File type not allowed. Only .xlsx, .xls and .csv files are accepted."
        )

    # Step 3: Create today's folder
    today_folder = get_today_folder()

    # Step 4: Generate a unique filename
    safe_filename = generate_safe_filename(file.filename)

    # Step 5: Create complete file path
    file_path = today_folder / safe_filename

    # Step 6: Save the file
    with open(file_path, "wb") as buffer:

        while content := await file.read(1024 * 1024):
            buffer.write(content)

    return {
        "status": "success",
        "original_filename": file.filename,
        "saved_filename": safe_filename,
        "saved_to": str(file_path)
    }
def process_document(media_id, filename):
    """
    Process a WhatsApp document.

    1. Get the temporary media URL from Meta.
    2. Create today's download folder.
    3. Generate a safe filename.
    4. Create the final file path.
    5. Download the file.
    6. Return the saved file path.
    """

    # Step 1: Get temporary media URL
    media_url = get_media_url(media_id)

    print("Media URL received")

    # Step 2: Create today's folder
    today_folder = get_today_folder()

    # Step 3: Generate a safe filename
    safe_filename = generate_safe_filename(filename)

    # Step 4: Create complete file path
    output_path = today_folder / safe_filename

    print("File will be saved to:", output_path)

    # Step 5: Download the file
    download_media(media_url, output_path)

    print("File downloaded successfully")

    # Step 6: Return the saved path
    return output_path

@app.post("/webhook")
async def webhook(data: dict = Body(...)):

    print("Received webhook:")
    print(data)

    entry = data.get("entry", [])

    if not entry:
        return {
            "status": "ignored",
            "reason": "No entry found"
        }

    changes = entry[0].get("changes", [])

    if not changes:
        return {
            "status": "ignored",
            "reason": "No changes found"
        }

    value = changes[0].get("value", {})

    messages = value.get("messages", [])

    if not messages:
        return {
            "status": "ignored",
            "reason": "No messages found"
        }

    message = messages[0]

    message_type = message.get("type")

    if message_type != "document":
        return {
            "status": "ignored",
            "reason": "Message is not a document"
        }

    sender = message.get("from")
    message_id = message.get("id")

    document = message.get("document", {})

    media_id = document.get("id")
    filename = document.get("filename")
    mime_type = document.get("mime_type")

    if not media_id:
        return {
                "status": "error",
                "reason": "Document does not contain a media ID"
        }

    try:
        saved_path = process_document(media_id, filename)
        print("Document processed. Output path:", saved_path)
    except Exception as e:
        print("Error processing document:", e)
        return {
            "status": "error",
            "reason": "Failed to process document",
            "detail": str(e)
        }

    print("----- DOCUMENT INFORMATION -----")
    print("Sender:", sender)
    print("Message ID:", message_id)
    print("Media ID:", media_id)
    print("Filename:", filename)
    print("MIME Type:", mime_type)

    return {
        "status": "success",
        "message_type": message_type,
        "sender": sender,
        "message_id": message_id,
        "media_id": media_id,
        "filename": filename,
        "mime_type": mime_type
    }