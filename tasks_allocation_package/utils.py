from datetime import date, timedelta, datetime


def read_class_instances(file_name: str, class_init, *pos_attr_names: []) -> []:
    result = []
    with open(file_name, 'r') as input_file:
        lines = input_file.readlines()
        for line in lines:
            attrs = line.strip().split(",")
            kw_attrs = dict()
            pos_attrs = []
            for i in range(len(attrs)):
                attr_str = attrs[i].strip()
                if i < len(pos_attr_names):
                    pos_attrs.append(attr_str)
                elif ":" in attr_str:
                    key, val = attr_str.split(":")
                    kw_attrs[key.strip()] = val.strip()
                elif "=" in attr_str:
                    key, val = attr_str.split("=")
                    kw_attrs[key.strip()] = val.strip()
            result.append(class_init(*pos_attrs, **kw_attrs))
    return result


def print_instances(input_list: [], *attrs):
    for instance_ in input_list:
        # print(attrs)
        print(to_str_instance(instance_, *attrs))


def to_str_instance(instance_, *attrs):
    # for attr in attrs:
    #     result = getattr(instance_, attr, "No attr")
    return ", ".join([f"{attr}={getattr(instance_, attr, "None")}" for attr in attrs])

def get_hours_from_timedelta(td_obj: timedelta) -> int:
    return td_obj.seconds // 3600


def get_instance_by_attr(instance_list, attr_name, attr_value):
    for instance_ in instance_list:
        if getattr(instance_, attr_name) == attr_value:
            return instance_
    return None
