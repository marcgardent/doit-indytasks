
import re

def replace_in_file(file, regex_source, regex_dest):     
    
    print(f"replace in '{file}' /{regex_source}/ by /{regex_dest}/ ...")
    content_new = ""
    
    with open (file, 'r', encoding='utf-8' ) as f:
        content_new = re.sub(regex_source, regex_dest, f.read(), flags = re.M)
    
    with open (file, 'w', encoding='utf-8' ) as f:
            f.write(content_new)