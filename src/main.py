import os, logging, shutil
from pathlib import Path

from textnode import TextNode, TextType
from htmlnode import HTMLNode, LeafNode, ParentNode
from markdown_blocks import markdown_to_html_node
from copystatic import copy_files_recursive



"""Sets the basic logging handler to /var/log"""
logging.basicConfig(
    encoding="utf-8",
    level="DEBUG",
    format="%(levelname)s - %(asctime)s | %(message)s",
    filename="/var/log/static_site_bootdev.log",
    filemode="w",
    datefmt="%m/%d/%Y %I:%M:%S %P"
)

"""Sets the logging behavior to the terminal"""
to_console = logging.StreamHandler()
to_console_formatter = logging.Formatter("%(levelname)s - %(asctime)s | %(message)s", "%m/%d/%Y %I:%M:%S %P")
to_console.setFormatter(to_console_formatter)
to_console.setLevel(logging.DEBUG)
logging.getLogger("").addHandler(to_console)

working_dir = Path(__file__)
source_dir = working_dir.parent.parent.joinpath("static")
target_dir = working_dir.parent.parent.joinpath("public")

content_dir = working_dir.parent.parent.joinpath("content")
template_dir = working_dir.parent.parent

def cleanup():
    logging.info("Starting to cleanup project")
    # 1. Delete all contents of destination directory.
    if target_dir.exists():
        shutil.rmtree(target_dir)
        logging.debug(f"Removing {target_dir}.")
    # 2. Copy all files and subdirectories & nest files
    if not target_dir.exists():
        shutil.copytree(source_dir, target_dir)
    ##    shutil.copytree(content_dir, target_dir)
    #    print(os.listdir(source_dir))
        logging.debug(f"Copy from source to target location.")
    # 3. Add logging.
    if target_dir.exists():
        shutil.rmtree(target_dir)

    print("Copying static files to public directory...")
    copy_files_recursive(source_dir, target_dir)
    #copy_files_recursive(content_dir, target_dir)

    target_dir.joinpath("blog","glorfindel").mkdir(parents=True,exist_ok=True)
    target_dir.joinpath("blog","tom").mkdir(parents=True,exist_ok=True)
    target_dir.joinpath("blog","majesty").mkdir(parents=True,exist_ok=True)
    target_dir.joinpath("contact").mkdir(parents=True,exist_ok=True)



def extract_title(markdown):
    for line in markdown.split("\n"):
        if line.startswith("# "):
            return line[2:].strip()
    raise ValueError("There is no 'h1' header.")


def generate_page(from_path, template_path, dest_path):
    print(f"DEBUGGING: {type(from_path)}")
    print(f"DEBUGGING: {from_path.resolve()}")
    from_file = from_path.joinpath("index.md")
    template_file = template_path.joinpath("template.html")
    dest_file = dest_path.joinpath("index.html")
    print(f"from:{from_file.resolve()}")
    print(type(dest_path))
    print(dest_path.resolve())
    print(dest_path)
    logging.info(f"Generating page from {from_file} to {dest_file} using {template_file}")
    if from_file.is_file():
        with open(from_file, mode="r") as f:   
            logging.debug(f"Reading {from_file}.") 
            from_file_content = f.read()

        with open(template_file, mode="r") as f:
            logging.debug(f"Reading {template_file}.")
            template_file_content = f.read()
    
        logging.info("Trying to create html from markdown.")
        create_html = markdown_to_html_node(from_file_content)
        logging.info("Creating htmlish")
        htmlish = create_html.to_html()
        logging.info("Getting htmlish title")
        htmlish_title = extract_title(from_file_content)

        updated_content = template_file_content.replace("{{ Title }}", htmlish_title).replace("{{ Content }}", htmlish)
        os.makedirs(os.path.dirname(dest_file), exist_ok=True)
        with open(dest_file, mode="w") as f:
            logging.info(f"Reading {dest_file}")
            f.write(updated_content)

def generate_pages_recursively(dir_path_content, template_path, dest_dir_path):
    logging.info("Looking through pages.")
    try:
        print(f"dir-path_attempt{os.chdir(dir_path_content)}")
    except:
        logging.error(f"ERROR 1: {Path(dir_path_content).resolve()}")
        logging.error(f"ERROR 2: {Path(dir_path_content).resolve()}")
        logging.error(f"ERROR 3: {dest_dir_path}")
        #if dir_path_content == "contact":
        #chatch = Path(dir_path_content).parent.parent.parent.parent
        #print(chatch)
        #print(logging.error(f"ERROR3 : {chatch.resolve()}"))
        
    try:
        directory_items = os.listdir(dir_path_content)
        logging.error(f"ERROR 4: {dir_path_content}")
        item_count = len(directory_items)
    except:
        item_count = 0
    
    if item_count<= 0:
        #directory_items = os.listdir(Path(dir_path_content).resolve().parent.parent)
        return
    print(f"DIR_ITEMS: {directory_items}")
    
    for item in directory_items:
        #print(f"chacha: {item}")
        #print(f"choochoo: {type(Path(item).resolve())}")
        #print(Path(item).is_file())
        #print(type(item))
        #if Path(item).is_file() or item.endswith(".md"):
        if item.endswith(".md"):
            logging.info(f"Generating {item}.")
            generate_page(Path(item).parent, template_path, dest_dir_path)
            """Something not working right here"""
        elif Path(item).is_file() == False:
            #print(f"NOTFILE: {os.listdir(item)}")
            print(f"CHECK: {Path(item).is_file()}")
            for dir in os.listdir(item):
                generate_page(Path(item).joinpath(dir), template_path, dest_dir_path.joinpath(item,dir))


        #for item in directory_items:
        #    if Path(item).is_file() == False:
        #        new_dest = dest_dir_path.joinpath(item)
        #        print(f"new_dest: {new_dest}")
        #        print(f"item: {Path(item).resolve()}")
        #        generate_pages_recursively(item, template_path, new_dest)

    for item in directory_items:
        if not Path(item).is_file():
            new_dest = dest_dir_path.joinpath(item)
            print(f"Ayo: {new_dest}")
            generate_pages_recursively(item, template_path, new_dest)


def main():
    logging.info("Starting main function.")
    cleanup()
    generate_pages_recursively(content_dir, template_dir, target_dir)
    print("MANUALLY")
    generate_page(content_dir.joinpath("contact"), template_dir, target_dir.joinpath("contact"))

if __name__ == "__main__":
    main()
