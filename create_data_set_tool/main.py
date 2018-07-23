import os
from pathlib import Path
import shutil

subsets_config = [
    'test',
    'train',
    'valid',
]

targed_dir = '../dataset/'

def iterate_kinds(path):
    if path.is_dir():
        for data_kind_dir in path.iterdir():
            if data_kind_dir.is_dir():
                yield(data_kind_dir)
    else:
        raise Exception('there are no web scrapped data yet, run a web scrapper to obtain a data')

def iterate_images(path):
    for data_kind_dir in iterate_kinds(path):
        for sample_image in data_kind_dir.iterdir():
            yield(data_kind_dir, sample_image)

def main():
    root_dataset_path = Path(targed_dir)
    root_dataset_path.mkdir(parents=True, exist_ok=True)

    raw_scrapped_data = Path('../web_scraper/scrap_data')

    images = [data_obj for data_obj in iterate_images(raw_scrapped_data)]
    images_per_kind = []

    for data_kind in iterate_kinds(raw_scrapped_data):
        kind_name = data_kind.name
        images_of_a_kind = list(filter(lambda x: x[0].name == kind_name, images))
        len_of_a_kind = len(images_of_a_kind)
        images_per_kind.append(
            (kind_name, len_of_a_kind, images_of_a_kind)
        )

    num_of_subsets = len(subsets_config)

    for kind, size, images in images_per_kind:
        num_of_images_per_subset = int(size/num_of_subsets)
        rest_of_them = size % num_of_subsets

        moved_images = 0
        while moved_images < ((num_of_images_per_subset * num_of_subsets) + rest_of_them):
            subset_index = min(num_of_subsets - 1, int(moved_images/num_of_images_per_subset))

            dest_path = Path(f"{str(root_dataset_path)}/{subsets_config[subset_index]}/{kind}")
            if not dest_path.exists():
                dest_path.mkdir(parents=True, exist_ok=True)

            img_to_copy = images[moved_images][1]

            print(f"copying {img_to_copy} to {dest_path}")
            shutil.copy(str(img_to_copy), str(dest_path))
            moved_images += 1




if __name__ == '__main__':
    main()
