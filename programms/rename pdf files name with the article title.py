import os
import re
import PyPDF2
from tkinter import Tk, filedialog
from pathlib import Path

def get_user_folder():
    """Get folder path with explicit error handling"""
    try:
        root = Tk()
        root.withdraw()
        folder = filedialog.askdirectory(title="Select folder with PDFs")
        root.destroy()
        if not folder:
            print("✖ No folder selected!")
            return None
        if not os.path.exists(folder):
            print(f"✖ Folder doesn't exist: {folder}")
            return None
        return folder
    except Exception as e:
        print(f"✖ Folder selection failed: {str(e)}")
        return None

def extract_title(pdf_path):
    """Simplified but reliable title extraction"""
    try:
        print(f"\nOpening: {pdf_path.name}")
        with open(pdf_path, 'rb') as f:
            pdf = PyPDF2.PdfReader(f)
            
            # Try metadata first
            if pdf.metadata and pdf.metadata.get('/Title'):
                title = pdf.metadata['/Title']
                if title:
                    print(f"Found metadata title: {title[:60]}...")
                    return title
            
            # Analyze first page text
            if len(pdf.pages) > 0:
                text = pdf.pages[0].extract_text()
                if text:
                    print("First page text preview:")
                    print(text[:200].replace('\n', ' ') + "...")
                    
                    # Find the most title-like line
                    lines = [line.strip() for line in text.split('\n') if line.strip()]
                    for line in lines:
                        if (20 < len(line) < 200 and ' ' in line and not line.isupper()):
                            if not any(x in line.lower() for x in ['doi:', 'http', 'copyright', 'page ', 'figure ']):
                                print(f"Selected title candidate: {line}")
                                return line
    except Exception as e:
        print(f"⚠ Error reading {pdf_path.name}: {str(e)}")
    return None

def clean_filename(title):
    """Make safe filenames with clear transformations"""
    if not title:
        return "Untitled"
    clean = re.sub(r'[<>:"/\\|?*]', '', title)
    clean = clean[:100].strip()
    print(f"Cleaned filename: {clean}")
    return clean

def rename_pdfs(folder):
    """Main function with step-by-step logging"""
    print(f"\n🔍 Scanning: {folder}")
    pdfs = list(Path(folder).glob('*.pdf'))
    print(f"Found {len(pdfs)} PDFs")
    
    if not pdfs:
        print("✖ No PDFs found in folder!")
        return False
    
    for pdf in pdfs:
        try:
            print(f"\n➤ Processing: {pdf.name}")
            title = extract_title(pdf)
            
            if not title:
                print("⚠ Couldn't extract title - skipping")
                continue
                
            new_name = f"{clean_filename(title)}.pdf"
            new_path = pdf.with_name(new_name)
            
            if new_path.exists():
                if new_path.samefile(pdf):
                    print("✓ Already correctly named")
                    continue
                else:
                    print("⚠ Duplicate detected - adding number")
                    for i in range(1, 100):
                        new_name = f"{clean_filename(title)} ({i}).pdf"
                        new_path = pdf.with_name(new_name)
                        if not new_path.exists():
                            break
            
            pdf.rename(new_path)
            print(f"✅ Renamed to: {new_name}")
            
        except Exception as e:
            print(f"✖ Failed to process {pdf.name}: {str(e)}")
    
    print("\n✔ All files processed!")
    return True

if __name__ == "__main__":
    print("=== PDF Renamer ===")
    print("Please select a folder containing PDFs")
    
    folder = get_user_folder()
    if folder:
        rename_pdfs(folder)
    
    input("\nPress Enter to exit...")