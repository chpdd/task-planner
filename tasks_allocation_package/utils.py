import datetime as dt


def str_to_bool(string):
    return True if string == "True" else False


def str_to_date(string):
    return dt.datetime.strptime(string, "%d.%m.%Y").date()


def read_class_instances(file_name: str, class_init, pos_args_names: []) -> []:
    result = []
    names_int_args = ("interest", "work_hours", "importance")
    names_date_args = ("deadline")
    with open(file_name, 'r', encoding="UTF-8") as input_file:
        lines = input_file.readlines()
    for line in lines:
        if line.count(",") == 0:
            continue
        args_list = line.strip().split(",")
        kwargs = dict()
        args = []
        for i in range(len(args_list)):
            arg_str = args_list[i].strip()
            if i < len(pos_args_names):
                if pos_args_names[i] == "date":
                    arg_str = str_to_date(arg_str)
                    # print(arg_str)
                args.append(arg_str)
            else:
                for symb in "=:":
                    if symb in arg_str:
                        keyword, arg = arg_str.split(symb)
                        arg = arg.strip()
                        keyword = keyword.strip()
                        if keyword in names_date_args:
                            arg = str_to_date(arg)
                        elif keyword in names_int_args:
                            arg = int(arg)
                        kwargs[keyword] = arg
        result.append(class_init(*args, **kwargs))
    return result


def print_instances(input_list: [], *attrs):
    for instance_ in input_list:
        # print(attrs)
        print(to_str_instance(instance_, *attrs))


def to_str_instance(instance, *attrs):
    return ", ".join([f"{attr}={getattr(instance, attr, "None")}" for attr in attrs])


def get_hours_from_timedelta(td_obj: dt.timedelta) -> int:
    return td_obj.seconds // 3600


def get_instance_by_attr(instance_list, attr_name, attr_value):
    for instance_ in instance_list:
        if getattr(instance_, attr_name) == attr_value:
            return instance_
    return None


def date_to_normal_str(arg_date: dt.date):
    day = arg_date.day
    month = arg_date.month
    year = arg_date.year
    return f"{day if day > 9 else '0' + str(day)}.{month if month > 9 else '0' + str(month)}.{year}"
