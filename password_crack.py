#!/usr/bin/python

import sys
import os
import argparse
import zipfile


def file_checks(zipfile, words):
    # Gets the file extension
    zipfiletype = os.path.splitext(zipfile)[-1].lower()
    wordsfiletype = os.path.splitext(words)[-1].lower()

    # Making sure the filetypes are correct
    if zipfiletype != ".zip":
        print("Argument 1 needs to be a zip file")
        sys.exit()
    elif not os.path.exists(zipfile):
        print("Argument 1 path does not exist!")
        sys.exit()

    if wordsfiletype != ".txt":
        print("Argument 2 needs to be a txt file")
        sys.exit()
    elif not os.path.exists(words):
        print("Argument 2 path does not exist!")
        sys.exit()


def crack(zipdir, wordlist, output_dir):
    found = False
    try:
        # If there's a ~, just convert it to the user's home dir
        if "~" in output_dir:
            new_output = output_dir.replace("~", os.environ['HOME'])
        else:
            new_output = output_dir
    except TypeError:
        # Output is None
        new_output = output_dir
    
    for word in wordlist:
        # Iterates through every word, tries to extract the zip using that word
        try:
            with zipfile.ZipFile(zipdir) as zip_ref:
                zip_ref.extractall(new_output, pwd=word.encode())
                found = True
                return word
        except RuntimeError:
            pass
    # If we couldn't find the password, we want to let main() know
    if not found:
        return None


def main():
    # Adding all the args
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "encrypted_dir", help="Directory of your encrypted zip file")
    parser.add_argument("wordlist_dir", help="Directory of your wordlist")
    parser.add_argument("--output", help="Where you want the unencrypted directory to be located")
    args = parser.parse_args()

    zipfile = args.encrypted_dir
    words = args.wordlist_dir
    output = args.output

    file_checks(zipfile, words)

    word_list = []
    with open(words) as f:
        for line in f:
            # :-1 removes \n from each line
            if "\n" in line:
                # Adds the word to the array
                word_list.append(line[:-1])
            else:
                word_list.append(line)

    found_word = crack(zipfile, word_list, output)
    
    if found_word is None:
        print("Password not found in wordlist!")
    else:
        # Tell user what the password was, and where to find the unzipped directory
        print("Cracked! The password is {}, and the dir is extracted {}".format(found_word, "to {}".format(output) if output else "in your working directory!"))


if __name__ == "__main__":
    main()
