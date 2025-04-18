import os
import json

BASE_DIR = "E:/Design Generation/Final Output/Final JSON/JSON Output"

####################### RENAME FILES #######################

# def clean_filenames(folder_path):
#     for filename in os.listdir(folder_path):
#         if filename.endswith(".png.json"):
#             old_path = os.path.join(folder_path, filename)
#             new_filename = filename.replace(".png.json", ".json")
#             new_path = os.path.join(folder_path, new_filename)
#             os.rename(old_path, new_path)
#             print(f"Renamed: {filename} → {new_filename}")

# clean_filenames(BASE_DIR)

#############################################################

ORIGINAL_DIRS = [
    "E:/Design Generation/Crello Explore/train/metadata_jsons",
    "E:/Design Generation/Crello Explore/test/metadata_jsons",
    "E:/Design Generation/Crello Explore/validation/metadata_jsons"
]

####################### EXTRACTING DIMENSION #######################

# def update_canvas_dimensions(base_dir, reference_dirs):
#     updated_files = []
#     not_found_files = []
#     missing_keys_files = []

#     for filename in os.listdir(base_dir):
#         if not filename.endswith('.json'):
#             continue

#         base_path = os.path.join(base_dir, filename)
#         found = False

#         for ref_dir in reference_dirs:
#             ref_path = os.path.join(ref_dir, filename)
#             if os.path.exists(ref_path):
#                 found = True
#                 try:
#                     with open(ref_path, 'r', encoding='utf-8') as f:
#                         ref_data = json.load(f)

#                     canvas_width = ref_data["poster"].get('canvas_width')
#                     canvas_height = ref_data["poster"].get('canvas_height')

#                     if canvas_width is not None and canvas_height is not None:
#                         with open(base_path, 'r', encoding='utf-8') as f:
#                             base_data = json.load(f)

#                         base_data['canvas_width'] = canvas_width
#                         base_data['canvas_height'] = canvas_height

#                         with open(base_path, 'w', encoding='utf-8') as f:
#                             json.dump(base_data, f, indent=4)

#                         updated_files.append(filename)
#                     else:
#                         missing_keys_files.append(filename)
#                 except Exception as e:
#                     print(f"Error updating '{filename}' from '{ref_dir}': {e}")
#                 break  # Found in one folder is enough

#         if not found:
#             not_found_files.append(filename)

#     print(f"\n✅ Updated Files:{len(updated_files)}")
#     # for f in updated_files:
#     #     print(f"  - {f}")

#     print(f"\n❌ Not Found in Any Reference Folder:{len(not_found_files)}")
#     # for f in not_found_files:
#     #     print(f"  - {f}")

#     print(f"\n⚠️ Found but Missing 'canvas_width' or 'canvas_height':{len(missing_keys_files)}")
#     # for f in missing_keys_files:
#     #     print(f"  - {f}")

# update_canvas_dimensions(BASE_DIR, ORIGINAL_DIRS)

####################################################################

from gen_ai_func import get_llm_res
####################### FIND LAYER TYPE #######################

import os
import json

def process_json_layers(directory, get_llm_res):
    for filename in os.listdir(directory):
        if filename.endswith(".json"):
            file_path = os.path.join(directory, filename)
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)

                updated = False
                layers = data.get("layers", [])
                if isinstance(layers, list):
                    for layer in layers:
                        if isinstance(layer, dict) and "label" in layer:
                            label = layer["label"]
                            layer_type = get_llm_res(label)
                            layer["layer_type"] = layer_type
                            updated = True

                if updated:
                    with open(file_path, 'w', encoding='utf-8') as f:
                        json.dump(data, f, indent=4)
                    print(f"✅ Updated: {filename}")
                else:
                    print(f"⚠️ No update needed: {filename}")
            except Exception as e:
                print(f"❌ Failed to process {filename}: {e}")

process_json_layers(BASE_DIR, get_llm_res)

###############################################################
