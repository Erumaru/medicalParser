from os import listdir
import os
from os.path import isfile, join
import sys


def convert_pdfs_to_txt(path):
	samples_path = "%s/samples" % path
	print(samples_path)
	os.system("mkdir text_files")
	allFiles = [f for f in listdir(samples_path) if isfile(join(samples_path, f))]

	for index, file in enumerate(allFiles):
		if file.endswith('.pdf'):
			f = os.path.splitext(file)[0]
			print(f)
			print("pdf2txt.py -o text_files/%d.txt %s/%s" % (index, samples_path, file))
			os.system("pdf2txt.py -o text_files/%d.txt %s/%s" % (index, samples_path, file))



def parse_abstructs(path):
	txt_path = "%s/text_files" % path
	print(txt_path)
	os.system("mkdir abstract")
	os.system("mkdir abstract/ru")
	os.system("mkdir abstract/en")

	allFiles = [f for f in listdir(txt_path) if isfile(join(txt_path, f))]
	fileNumber = 1

	for index, file in enumerate(allFiles):
		if file.endswith('.txt'):
			list = open("%s/%s" % (txt_path, file), 'r').read().splitlines() 
			for lineIndex, line in enumerate(list):
				if line == 'РЕЗЮМЕ':
					newAbstract = []
					for abstractLine in list[lineIndex + 1:]:
						if "РМЖ." in abstractLine: 
							newAbstract.append(abstractLine)
							break
						else:
							newAbstract.append(abstractLine)
					os.system("touch abstract/ru/%04d.txt" % fileNumber)
					txtFile = open("abstract/ru/%04d.txt" % fileNumber, "w")
					txtFile.write('\n'.join(newAbstract))
					txtFile.close()
				elif line == 'ABSTRACT':
					newAbstract = []
					for abstractLine in list[lineIndex + 1:]:
						if "RMJ." in abstractLine: 
							newAbstract.append(abstractLine)
							break
						else:
							newAbstract.append(abstractLine)
					os.system("touch abstract/en/%04d.txt" % fileNumber)
					txtFile = open("abstract/en/%04d.txt" % fileNumber, "w")
					txtFile.write('\n'.join(newAbstract))
					txtFile.close()
					fileNumber += 1


def parse_title(path):
	txt_path = "%s/text_files" % path
	print(txt_path)
	os.system("mkdir titles")

	allFiles = [f for f in listdir(txt_path) if isfile(join(txt_path, f))]
	fileNumber = 1

	for index, file in enumerate(allFiles):
		if file.endswith('.txt'):
			list = open("%s/%s" % (txt_path, file), 'r').read().splitlines() 
			for lineIndex, line in enumerate(list):
				if line == 'РЕЗЮМЕ':
					newTitle = []
					numberOfEmptyLines = 0
					for abstractLine in list[lineIndex - 1::-1]:
						if abstractLine == '': 
							numberOfEmptyLines += 1
							if numberOfEmptyLines == 4:
								break
						else:
							newTitle.append(abstractLine)
					newTitle.reverse()
					os.system("touch titles/%04d.txt" % fileNumber)
					txtFile = open("titles/%04d.txt" % fileNumber, "w")
					txtFile.write('\n'.join(newTitle))
					txtFile.close()
					fileNumber += 1


def findArticle(line, path):

	txt_files = [f for f in listdir(path) if isfile(join(path, f))]
	ok = False 
	body = []

	for index, file in enumerate(txt_files):
		file_data_lines = open("%s/%s" % (path, file)).read().splitlines()

		for line_index, file_line in enumerate(file_data_lines):
			if line == file_line:
				for body_line in file_data_lines[line_index + 1:]:
					if body_line == 'Литература':
						return body
					if 'Список литературы' in file_line:
						return body
					else:
						body.append(body_line)			

	print("$$$$$$$$$$$")

	return None


def parse_body(path): 
	txt_path = "%s/text_files" % path
	print(txt_path)
	abstract_path = "%s/abstract/en" % path
	os.system("mkdir articles")

	absctract_files = [f for f in listdir(abstract_path) if isfile(join(abstract_path, f))]
	created_file_number = 1

	for index, file in enumerate(absctract_files):
		if file.endswith('.txt'):
			list = open("%s/%s" % (abstract_path, file), 'r').read().splitlines() 
			last = list[-1]
			body = findArticle(last, txt_path)
			print()
			if body != None:
				os.system("touch articles/%04d.txt" % created_file_number)
				txtFile = open("articles/%04d.txt" % created_file_number, "w")
				txtFile.write('\n'.join(body))
				txtFile.close()
				created_file_number += 1


def test(path): 
	txt_path = "%s/text_files" % path
	txt_files = [f for f in listdir(txt_path) if isfile(join(txt_path, f))]
	for index, file in enumerate(txt_files):
		file_data_lines = open("%s/%s" % (txt_path, file)).read().splitlines()
		for line_index, file_line in enumerate(file_data_lines):
			if 'Список литературы Вы можете найти на сайте http://www.rmj.ru' in file_line:
				print("OH NO")

path = sys.argv[1]



#convert_pdfs_to_txt(path)
#parse_abstructs(path)
#parse_title(path)
parse_body(path)



