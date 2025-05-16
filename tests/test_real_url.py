from url_ingestion import process_web

def test_real_url():
    url = "https://en.wikipedia.org/wiki/Python_(programming_language)"
    documents = process_web(url)

    if documents:
        print(f"✅ Loaded {len(documents)} document(s).")
        print("First 500 characters of content:")
        print(documents[0].page_content[:500])
        print("Metadata:", documents[0].metadata)
    else:
        print("❌ Failed to load documents.")

if __name__ == "__main__":
    test_real_url()