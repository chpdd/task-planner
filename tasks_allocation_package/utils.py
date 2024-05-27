from datetime import date, timedelta, datetime


def read_class_instances(file_name: str, class_init, *pos_attr_names: []) -> []:
    result = []
    with open(file_name, 'r', encoding="UTF-8") as input_file:
        lines = input_file.readlines()
        for line in lines:
            if line.count(",") == 0:
                continue
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


def date_to_normal_str(arg_date: date):
    day_ = arg_date.day
    month_ = arg_date.month
    year_ = arg_date.year
    return f"{day_ if day_ > 9 else '0' + str(day_)}.{month_ if month_ > 9 else '0' + str(month_)}.{arg_date.year}"
