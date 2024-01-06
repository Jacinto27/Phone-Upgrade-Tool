# test_my_project.py

# Import mainmodule
from Analysis import phonecomparisor as pc

strict_conditions = ['announcement_date', 'resolution', 'battery', 'ram(GB)', 'storage(GB)', 'system',
                     'recording quality']


def test_check_record_q_higher():
    # Assuming check_record_q compares recording qualities of two phones
    user_phone = {'video_720p': True, 'video_1080p': True, 'video_4K': False}
    compared_phone = {'video_720p': True, 'video_1080p': True, 'video_4K': True}

    # Expect False if compared_phone has higher recording quality
    assert pc.optimized_suggestion(user_phone, strict_conditions)


def test_check_record_q_equal_or_lower():
    user_phone = {'video_720p': True, 'video_1080p': True, 'video_4K': True}
    compared_phone = {'video_720p': True, 'video_1080p': True, 'video_4K': False}

    # Expect True if compared_phone has equal or lower recording quality
    assert pc.check_record_q(user_phone, compared_phone)


def test_compare_os_versions_different_systems():
    user_phone = {'system': 'Android', 'version': 10}
    compared_phone = {'system': 'iOS', 'version': 14}

    # Expect True if the systems are different
    assert pc.compare_os_versions(user_phone, compared_phone)


def test_compare_os_versions_same_system_higher_version():
    user_phone = {'system': 'Android', 'version': 10}
    compared_phone = {'system': 'Android', 'version': 11}

    # Expect False if the systems are the same and the compared phone has a higher version
    assert not pc.compare_os_versions(user_phone, compared_phone)


def test_compare_os_versions_same_system_lower_or_equal_version():
    user_phone = {'system': 'Android', 'version': 10}
    compared_phone = {'system': 'Android', 'version': 9}

    # Expect True if the systems are the same and the compared phone has a lower or equal version
    assert pc.compare_os_versions(user_phone, compared_phone)
