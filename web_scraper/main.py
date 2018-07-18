from icrawler.builtin import GoogleImageCrawler
import pathlib
import argparse

def main():
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('-s', '--search', default='bananas', type=str, help='search term')
    parser.add_argument('-n', '--num_images', default=10, type=int, help='num images to save')
    parser.add_argument('-f', '--folder', default='bananas', type=str, help='save directory')
    args = parser.parse_args()

    search_term = args.search
    folder = args.folder
    max_num = args.num_images
    root_dir = f"./scrap_data/{folder}"

    print(search_term, folder, max_num, root_dir)

    pathlib.Path(root_dir).mkdir(parents=True, exist_ok=True)

    google_crawler = GoogleImageCrawler(storage={'root_dir': root_dir})
    google_crawler.crawl(keyword=search_term, max_num=max_num)

if __name__ == '__main__':
    main()
