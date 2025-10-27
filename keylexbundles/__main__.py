import argparse
from .compute_keyness import compute_keyness

def main():
    parser = argparse.ArgumentParser(description="Extract key lexical bundles between two corpora.")
    parser.add_argument("target", help="Path to folder with target corpus .txt files")
    parser.add_argument("reference", help="Path to folder with reference corpus .txt files")
    parser.add_argument("-o", "--output", default="output.csv", help="Output CSV filename (default: output.csv)")

    args = parser.parse_args()
    compute_keyness(args.target, args.reference, args.output)  
    
if __name__ == "__main__":
    main()