from f5_version_num_gt_eq import execute_version_check, VersionInfo


def test_execute_version_check_12_1_3():
    assert execute_version_check("12.1.3", "13.1.0") is False


def test_execute_version_check_13_1_0():
    assert execute_version_check("13.1.0", "13.1.0") is True


def test_execute_version_check_13_1_0_0():
    assert execute_version_check("13.1.0.0", "13.1.0") is True


def test_execute_version_check_14_0_0():
    assert execute_version_check("14.0.0", "13.1.0") is True


def test_execute_version_check_13_1_1_1():
    assert execute_version_check("13.1.1.1", "13.1.0") is True


def test_execute_version_check_11_6_2():
    assert execute_version_check("11.6.2", "13.1.0") is False


def test_execute_version_check_11_6_2():
    #TODO I might not need this. Need to check my input tomorrow.
    assert execute_version_check("11.6.2-1hf2.4", "13.1.0") is False