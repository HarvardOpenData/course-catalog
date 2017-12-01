import csv
import json

from course import Course

def dump_csv(courses):
    # dumps a list of courses to CSV
    with open('course_catalog_dump.csv', 'w') as csvfile:
        fieldnames = Course.CSV_FIELDS
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()

        for course in courses:
            writer.writerow(course.to_dict_for_csv())


def dump_json(courses):
    # dumps a list of courses to JSON
    course_dicts = [c.to_dict() for c in courses]

    with open('course_catalog_dump.json', 'w') as outfile:
        json.dump(course_dicts, outfile)
