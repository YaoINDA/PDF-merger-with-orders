#!/usr/bin/env python3
"""
PDF Combiner Script

This script combines all PDF files found in a master folder and its subfolders into a single PDF file.
The files are processed in alphabetical order by folder name and then by file name.

Usage:
    python pdf_combiner.py [--source_folder FOLDER] [--output_folder FOLDER]

Parameters:
    --source_folder: The master folder containing PDFs to combine (default: current directory)
    --output_folder: The folder to save the combined PDF (default: ./output)
"""

import os
import argparse
from PyPDF2 import PdfMerger
import re

def natural_sort_key(s):
    """
    Sort strings with numerical parts naturally
    For example: "file1.pdf" comes before "file10.pdf"
    """
    return [int(c) if c.isdigit() else c.lower() for c in re.split(r'(\d+)', s)]

def combine_pdfs(source_folder='.', output_folder='output'):
    """
    Combines all PDF files in source_folder and its subfolders into a single PDF.
    
    Args:
        source_folder: The master folder containing PDFs (default: current directory)
        output_folder: The folder to save the combined PDF (default: ./output)
    """
    # Create output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
        print(f"Created output folder: {output_folder}")
    
    # Create PDF merger object
    merger = PdfMerger()
    
    # Get all subfolders including the source folder itself
    all_folders = []
    for root, dirs, files in os.walk(source_folder):
        all_folders.append(root)
    
    # Sort folders alphabetically
    all_folders.sort(key=natural_sort_key)
    
    # Count of PDFs added
    pdf_count = 0
    
    # Process each folder
    for folder in all_folders:
        # Get all PDF files in the current folder
        pdf_files = [f for f in os.listdir(folder) if f.lower().endswith('.pdf')]
        
        # Sort PDF files alphabetically
        pdf_files.sort(key=natural_sort_key)
        
        # Add each PDF to the merger
        for pdf_file in pdf_files:
            pdf_path = os.path.join(folder, pdf_file)
            try:
                merger.append(pdf_path)
                pdf_count += 1
                print(f"Added: {pdf_path}")
            except Exception as e:
                print(f"Error adding {pdf_path}: {e}")
    
    # Save the result if PDFs were found
    if pdf_count > 0:
        output_path = os.path.join(output_folder, 'combined_pdf.pdf')
        merger.write(output_path)
        merger.close()
        print(f"\nSuccessfully combined {pdf_count} PDF files into: {output_path}")
    else:
        print("\nNo PDF files found in the specified folders.")

def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Combine PDF files from a master folder and its subfolders.')
    parser.add_argument('--source_folder', default='.', help='Master folder containing PDFs to combine (default: current directory)')
    parser.add_argument('--output_folder', default='output', help='Folder to save the combined PDF (default: ./output)')
    
    args = parser.parse_args()
    
    print(f"Starting PDF combination from: {args.source_folder}")
    combine_pdfs(args.source_folder, args.output_folder)

if __name__ == "__main__":
    main()