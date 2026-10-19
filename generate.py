from src.operations.copy_static import copy_static
from src.operations.generate_pages import generate_pages
from src.operations.parse_data import parse_data
from src.operations.scaffold_dist import scaffold_dist


def main() -> None:
    data = parse_data()
    scaffold_dist()
    copy_static()
    generate_pages(data)


if __name__ == "__main__":
    main()
