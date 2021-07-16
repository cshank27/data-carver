#!/usr/bin/env python3

#Clayton Shank

import sys
import hashlib
import os

def carve(bin_file_input):
    current_start_location = None
    current_type = None
    total_count = {"jpg" : 0, "png" : 0, "pdf" : 0}
    #checks for folder with last name if not it creates the directory
    folder = "shank"
    if not os.path.exists(folder):
        os.makedirs('shank')
    try:
        #opens the file and looks for start of file jpg's
        with open(bin_file_input, "rb") as f:
            carve_file = f.read()
            for i in range(len(carve_file)):
                if carve_file[i] == 0xFF and carve_file[i+1] == 0xD8 and carve_file[i+2] == 0xFF:
                    current_start_location = i
                    current_type = "jpg"
                    continue
                if carve_file[i] == 0x89 and carve_file[i+1] == 0x50 and carve_file[i+2] == 0x4E and carve_file[i+3] == 0x47 and carve_file[i+4] == 0x0D and carve_file[i+5] == 0x0A and carve_file[i+6] == 0x1A and carve_file[i+7] == 0x0A:
                    current_start_location = i
                    current_type = "png"
                    continue
                if carve_file[i] == 0x25 and carve_file[i+1] == 0x50 and carve_file[i+2] == 0x44 and carve_file[i+3] == 0x46:
                    current_start_location = i
                    current_type = "pdf"
                    continue
                #finds the EOF of jpg then writes that to a file
                if current_start_location is not None and current_type == "jpg":
                    if carve_file[i] == 0xFF and carve_file[i+1] == 0xD9:
                        #incorporates the full end marker
                        carved_bytes = carve_file[current_start_location : i+2]
                        filename = folder + "/shankjpg" + str(total_count["jpg"]) + ".jpg"
                        total_count["jpg"] += 1
                        with open(filename, "wb") as g:
                            g.write(carved_bytes)
                        print(f"File name: {filename}, File type: jpg, File size: {i+2 - current_start_location}, Start offset: {hex(current_start_location)}" )
                        current_start_location = None
                        continue
                if current_start_location is not None and current_type == "png":
                    if carve_file[i] == 0x49 and carve_file[i+1] == 0x45 and carve_file[i+2] == 0x4E and carve_file[i+3] == 0x44 and carve_file[i+4] == 0xAE and carve_file[i+5] == 0x42 and carve_file[i+6] == 0x60 and carve_file[i+7] == 0x82:
                        #incorporates the full end marker
                        carved_bytes = carve_file[current_start_location : i+8]
                        filename = folder + "/shankpng" + str(total_count["png"]) + ".png"
                        total_count["png"] += 1
                        with open(filename, "wb") as g:
                            g.write(carved_bytes)
                        print(f"File name: {filename}, File type: png, File size: {i+8 - current_start_location}, Start offset: {hex(current_start_location)}" )
                        current_start_location = None
                        continue
                if current_start_location is not None and current_type == "pdf":
                    if carve_file[i] == 0x0A and carve_file[i+1] == 0x25 and carve_file[i+2] == 0x25 and carve_file[i+3] == 0x45 and carve_file[i+4] == 0x4F and carve_file[i+5] == 0x46 or carve_file[i] == 0x0A and carve_file[i+1] == 0x25 and carve_file[i+2] == 0x25 and carve_file[i+3] == 0x45 and carve_file[i+4] == 0x4F and carve_file[i+5] == 0x46 or carve_file[i] == 0x0D and carve_file[i+1] == 0x0A and carve_file[i+2] == 0x25 and carve_file[i+3] == 0x25 and carve_file[i+4] == 0x45 and carve_file[i+5] == 0x4F and carve_file[i+6] == 0x46 and carve_file[i+7] == 0x0D and carve_file[i+8] == 0x0A or carve_file[i] == 0x0D and carve_file[i+1] == 0x25 and carve_file[i+2] == 0x25 and carve_file[i+3] == 0x45 and carve_file[i+4] == 0x4F and carve_file[i+5] == 0x46 and carve_file[i+6] == 0x0D:
                        #incorporates the full end marker
                        carved_bytes = carve_file[current_start_location : i+8]
                        filename = folder + "/shankpdf" + str(total_count["pdf"]) + ".pdf"
                        total_count["pdf"] += 1
                        with open(filename, "wb") as g:
                            g.write(carved_bytes)
                        print(f"File name: {filename}, File type: pdf, File size: {i+8 - current_start_location}, Start offset: {hex(current_start_location)}" )
                        current_start_location = None
                        continue
        carved_hashes = []
        for filename in os.listdir(folder):
            carved_hashes.append(hashlib.md5(open("shank/" + filename,'rb').read()).hexdigest())
        with open ("shank/hashes.txt", "w") as f:
            for hash in carved_hashes:
                f.write(hash + "\n")
        #get hashes put in a list once done open a text file and write out
        #
    except IOError:
        print("invalid file path")

if __name__ == "__main__":
    bin_file_input = input('Enter the binary file name: ')
    carve(bin_file_input)