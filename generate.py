from src.operations.configure_logging import configure_logging
from src.operations.copy_downloads import copy_downloads
from src.operations.copy_static import copy_static
from src.operations.generate_pages import generate_pages
from src.operations.parse_args import parse_args
from src.operations.parse_data import parse_data
from src.operations.process_assets import process_assets
from src.operations.process_core_assets import process_core_assets
from src.operations.scaffold_dist import scaffold_dist


def main() -> None:
    configure_logging()
    args = parse_args()
    data = parse_data(args.data)
    scaffold_dist()
    copy_static()
    process_assets(process_images=not args.no_image_processing)
    copy_downloads()
    process_core_assets(process_images=not args.no_image_processing)
    generate_pages(data)


if __name__ == "__main__":
    main()
