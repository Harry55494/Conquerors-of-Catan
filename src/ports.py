"""
Ports Function

© 2023 HARRISON PHILLINGHAM, mailto:harrison@phillingham.com. For the full licence, please see LICENCE.txt (https://github.com/Harry55494/conquerors-of-catan/blob/master/LICENCE)
"""


def get_port_combinations(interface, player):
    """
    Gets all the combinations of resources that can be traded at the ports
    :param interface: The interface object
    :param player: The player object
    :return: The list of combinations
    """
    port_resources = []
    for port in interface.get_ports_list():
        if interface.get_ports_list()[port] is not None:
            if interface.get_ports_list()[port]["player"] is not None:
                if interface.get_ports_list()[port]["player"].number == player.number:
                    # Get the resource that the port trades for
                    resource = interface.get_ports_list()[port]["resource"]
                    # If the port is a 3:1 port, add all resources to the list
                    if resource == "any":
                        for card in player.resources:
                            if player.resources.count(card) >= 3:
                                port_resources.append(card)
                    else:
                        for card in player.resources:
                            if card == resource and player.resources.count(card) >= 2:
                                port_resources.append(card)
    return port_resources
