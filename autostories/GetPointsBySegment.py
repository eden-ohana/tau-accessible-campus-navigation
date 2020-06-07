import pprint

from autostories import Building
from autostories.ExampleInput import *
from autostories import OSMParser
from autostories.Section import sort_by_distance


def dist_from_segment(coordinates_1, coordinates_2, coordinates_3):  # x3,y3 is the point
    x1 = coordinates_1[0]
    y1 = coordinates_1[1]
    x2 = coordinates_2[0]
    y2 = coordinates_2[1]
    x3 = coordinates_3[0]
    y3 = coordinates_3[1]

    px = x2 - x1  # coordinates
    py = y2 - y1

    norm = px * px + py * py

    u = ((x3 - x1) * px + (y3 - y1) * py) / float(norm)

    if u > 1:
        u = 1
    elif u < 0:
        u = 0

    x = x1 + u * px
    y = y1 + u * py

    dx = x - x3
    dy = y - y3

    # Note: If the actual distance does not matter,
    # if you only want to compare what this function
    # returns to other results of this function, you
    # can just return the squared distance instead
    # (i.e. remove the sqrt) to gain a little performance

    dist = (dx * dx + dy * dy) ** .5

    return dist


def get_points_between_two_points_by_segment_distance(nodes_info: list, point1: Point, point2: Point,
                                                      dis: float = 0.0005):
    """
    Args:
        point1: Point type
        point2: Point type
        dis: dis to include in
    """
    result = []
    point1_x_y = point1.get_x_y()
    point2_x_y = point2.get_x_y()
    for node_dict in nodes_info:
        node_start_point_x_y = node_dict["start_point"].get_x_y()
        if dist_from_segment(point1_x_y, point2_x_y, node_start_point_x_y) < dis:
            if len(node_dict.keys()) > 2 or ("name" not in node_dict.keys() and len(node_dict.keys()) > 1):
                result.append(node_dict)  # node_dict["start_point"])
    return result


def example_on_entrance_to_gilman():
    first = 0
    second = 1
    nodes_info = OSMParser.create_nodes_info("part_map_entrance_to_gilman.osm")
    points_list = Building.create_points_list(entrance_to_gilman)

    point1_x_y = points_list[first].get_x_y()
    point2_x_y = points_list[second].get_x_y()
    result = get_points_between_two_points_by_segment_distance(nodes_info, points_list[first], points_list[second])
    print(len(result))
    sort_by_distance(result, points_list[first])
    print(points_list[first].to_string())
    print(points_list[second].to_string())

    for node in result:
        pprint.pprint(node)


if __name__ == '__main__':
    first = 0
    second = 1
    nodes_info = OSMParser.create_nodes_info("part_map_entrance_to_gilman.osm")
    points_list = Building.create_points_list(entrance_to_gilman)

    point1_x_y = points_list[first].get_x_y()
    point2_x_y = points_list[second].get_x_y()
    result = get_points_between_two_points_by_segment_distance(nodes_info, points_list[first], points_list[second],
                                                               0.0005)
    print(len(result))
    sort_by_distance(result, points_list[first])
    print(points_list[first].to_string())
    print(points_list[second].to_string())

    for node in result:
        pprint.pprint(node)
        print(node["start_point"].id)
