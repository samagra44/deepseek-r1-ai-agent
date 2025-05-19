from pdf_ingestion import process_pdf

class UploadedFile:
    """Mock class to simulate Streamlit's uploaded file object"""
    def __init__(self, file_path):
        self.file = open(file_path, "rb")
        self.name = file_path.split("\\")[-1]  # Use file name only

    def read(self):
        self.file.seek(0)
        return self.file.read()

    def close(self):
        self.file.close()


def test_pdf_processing():
    file_path = "data.pdf"  # Replace with the actual PDF path
    upload_file = UploadedFile(file_path)

    try:
        documents = process_pdf(upload_file)

        if documents:
            print(f"✅ Loaded {len(documents)} page(s) from PDF.")
            print("First 300 characters:")
            print(documents[0].page_content[:300])
            print("Metadata:", documents[0].metadata)
        else:
            print("❌ Failed to process PDF.")
    finally:
        upload_file.close()

if __name__ == "__main__":
    test_pdf_processing()
