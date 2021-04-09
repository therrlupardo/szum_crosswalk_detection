import sys
import json
import csv
from types import SimpleNamespace


def has_crosswalk(_image):
    labels = _image.labels
    for label in labels:
        if label.category == "lane" and label.attributes.laneType == "crosswalk":
            return True
    return False


def simplify_images(_images):
    return list(map(lambda i: {"name": i.name, "has_crosswalks": has_crosswalk(i)}, _images))


def simplify_images_from_file(_file_name):
    with open(_file_name) as images_file:
        images = json.load(images_file, object_hook=lambda d: SimpleNamespace(**d))
        return simplify_images(images)


def get_simplified_images():
    result = []
    for arg in sys.argv[1:]:
        result += simplify_images_from_file(arg)
    return result


def save_result_as_json(_simplified_images):
    result_json_file = 'results/simplified.json'
    with open(result_json_file, 'w') as outfile:
        json.dump(_simplified_images, outfile)
        print('Saved results as JSON file: ' + result_json_file)


def save_results_as_csv(_simplified_images):
    result_csv_file = 'results/simplified.csv'
    with open(result_csv_file, 'w') as csv_output_file:
        writer = csv.writer(csv_output_file)
        writer.writerow(['Name', 'Has crosswalk'])
        for image in _simplified_images:
            writer.writerow([image['name'], image['has_crosswalks']])
        print('Saved results as CSV file: ' + result_csv_file)


if __name__ == "__main__":
    simplified_images = get_simplified_images()
    save_result_as_json(simplified_images)
    save_results_as_csv(simplified_images)
    print('Result file contains ' + str(len(simplified_images)) + ' elements')
