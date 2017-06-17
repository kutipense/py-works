#!/usr/bin/env python3
import pyperclip
import requests
import sys

def main(args):
	ext = {"py":"python3","cpp":"cpp","c":"c"}
	url = "https://paste.ubuntu.com/"
	with open(args) as f:
		file_name, syntax = sys.argv[1].rsplit("/")[-1].rsplit(".")
		
		payload = {
			"poster" : file_name,
			"syntax" : ext[syntax],
			"content" : str(f.read())
		}
		
		req = requests.post(url, data=payload)
		print(req.url)
		pyperclip.copy(str(req.url))
	return 0

if __name__=="__main__":
	sys.exit(main(sys.argv[1]))
