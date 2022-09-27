import serial.tools.list_ports


def return_com_port(mfr_name: str, debug: bool = None) -> str:
    """
    :param debug: boolean to show names of all ports and their information
    :param mfr_name: The name of the device you're looking for
    :return:
    """
    ports = list(serial.tools.list_ports.comports())
    if debug:
        for port in ports:
            print("total: {}".format(port))
            print("mfr name: {}".format(port.manufacturer))
            print("com name: {}".format(port.name))

    res = [p.name for p in ports if (str.lower(p.manufacturer) == str.lower(mfr_name))]
    if len(res) == 0:
        print("No port found for mfr name {}".format(mfr_name))
        return ""
    return str(res[0])


def test_return_com_port():
    com_port_test = return_com_port(mfr_name="")
    assert com_port_test == ""
    com_port_test2 = return_com_port(mfr_name="FTDI")
    assert "COM" in com_port_test2


if __name__ == '__main__':
    com_port = return_com_port(mfr_name="")
    print("result: {}".format(com_port))
    com_port = return_com_port(mfr_name="FTDI")
    print("result: {}".format(com_port))
