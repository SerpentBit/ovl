import typing


def team_number_to_ip(team_number: typing.Union[str, int]):
    """
    Turns a team number into the static ip of the roborio
    TEAM -> 10.TE.AM.2
    :param team_number: string or int of the team number
    """

    team_number = str(team_number)
    first_numbers = team_number[:-2]
    second_numbers = team_number[-2:]
    if first_numbers == "":
        first_numbers = 0
    team_number = "{}.{}".format(first_numbers, second_numbers)
    return "10.{team_number}.2".format(team_number=team_number)
