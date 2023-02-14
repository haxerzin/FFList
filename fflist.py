from __future__ import print_function
from os import scandir, walk, system
from argparse import ArgumentParser
from pathlib import Path
import asyncio
import platform

# saving all the gathered filepaths into list
total_files = []

global printout

# get os name
def get_os_name() -> str:
	return platform.system()


# clear screen
def sclear() -> None:
	plt = get_os_name()
	if plt == "Windows":
		system('cls')
	elif plt in ["Linux", "Darwin"]:
		system('clear')


# convert names to path
async def convert_to_path(dirpath: str):
	dirpath.encode('unicode escape')
	p = Path(dirpath)
	return p


# progress bar
async def pbar(progress, total: float) -> None:
	try:
		percent = 100 * (progress / float(total))
		bar = '+' * int(percent) + '-' * (100 - int(percent))
		print(f"\r|{bar}| {percent:.2f}%", end="\r")
	except ZeroDivisionError as e:
		print(f"No Folders Found\n\nERROR: {e}")


# read lines from files
def readfilelines(filepath: str) -> []:
	try:
		with open(filepath, 'r') as f:
			lines = [x.rstrip() for x in f.readlines()]
		return lines
	except Exception as e:
		raise e


# print output
async def print_output():
	sclear()
	fpath = str(Path.cwd()) + "/files.txt"
	fpath = await convert_to_path(fpath)
	print(readfilelines(fpath))


# save the list into file
async def save_files() -> None:
	ffolder = str(Path.cwd()) + "/files.txt"
	filepath = await convert_to_path(ffolder)
	with open(filepath, 'w') as f:
		for file in total_files:
			try:
				f.write(f"{file}\n")
			except Exception as e:
				pass
	if printout == True:
		await print_output()


# get the files from folder
async def get_files(dirpath: str) -> []:
	files = []
	f_obj = scandir(path=dirpath)
	for entry in f_obj:
		if entry.is_file() and entry.name != None:
			ffolder = f"{dirpath}\\{entry.name}"
			fpath = await convert_to_path(ffolder)
			files.append(fpath)
	return files


# total appender
async def total_appender(dirpath: str) -> None:
	total_lists = []
	total_lists.append(await get_files(dirpath))
	for lst in total_lists:
		for file in lst:
			total_files.append(file)


# init
async def init(init_dir: str, isDeep: bool) -> None:
	sclear()
	init_dir = await convert_to_path(init_dir)
	print(f"Gathering FileSystem Directories from {init_dir}..")
	dirs_raw = []
	match isDeep:
		case True:
			filenum = 0
			try:
				for x in walk(init_dir):
					dirs_raw.append(x[0])
					filenum	+= 1
					if filenum % 100 == 0:
						print(f"Folders Gathered: {filenum}")
			except Exception as e:
				raise e
		case False:
			try:
				dirs_raw = [x[0] for x in walk(init_dir)]
			except Exception as e:
				raise e
	print(f"Gathering files in {len(dirs_raw)} directories..")
	await pbar(0, len(dirs_raw))
	n = 0
	while n <= len(dirs_raw)-1:
		dirpath = await convert_to_path(dirs_raw[n])
		await total_appender(dirpath)
		n += 1
		await pbar(n, len(dirs_raw))
	print(f"Saving file list...")
	await save_files()


# read config file
async def main() -> None:
	global printout
	sclear()
	parser = ArgumentParser(description="FFlist Argument Parser", add_help=True)
	folder_group = parser.add_mutually_exclusive_group()
	folder_group.add_argument('-dir','--directory', type=str, help="User Defined Folder")
	folder_group.add_argument('-r','--read', type=str, help="User Defined Folders From File [EX: dirs.txt]")
	folder_group.add_argument('-full','--full', action="store_true", help="All System Files")
	parser.add_argument('-print','--print', action="store_true", help="Print Output")
	args = parser.parse_args()

	if args.print:
		printout = True
	else:
		printout = False

	if args.directory:
		if args.directory != None:
			try:
				asyncio.gather(init(args.directory, False))
			except Exception as e:
				raise e
	if args.read:
		read_tasks = []
		if args.read != None:
			dirs = readfilelines(args.read)
			for _dir in dirs:
				read_tasks.append(asyncio.create_task(init(_dir, False)))
			runs = await asyncio.gather(*read_tasks, return_exceptions=True)
	if args.full:
		plt = get_os_name()
		sysdir = ""
		match plt:
			case "Windows":
				sysdir = "C:/"
			case "Linux":
				sysdir = "/home/"
			case "Darwin":
				sysdir = "/home/"
		try:
			asyncio.gather(init(sysdir, True))
		except Exception as e:
			raise e


if __name__ == "__main__":
	asyncio.run(main())
