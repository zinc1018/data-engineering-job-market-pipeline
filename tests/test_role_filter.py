from src.utils.role_filter import is_target_role


def test_is_target_role_includes_engineering_and_data_roles():
    assert is_target_role("Data Engineer")
    assert is_target_role("AI Analytics Engineer (Business Analytics)")
    assert is_target_role("Software Engineer, Infrastructure (8+ YOE)")
    assert is_target_role("Engineering Manager, AI Product")


def test_is_target_role_excludes_business_roles():
    assert not is_target_role("Account Executive, Commercial")
    assert not is_target_role("Product Manager, AI")
    assert not is_target_role("Technical Account Manager")
    assert not is_target_role("Sales Manager, Strategic Accounts")


def test_is_target_role_requires_positive_signal():
    assert not is_target_role("Manager, Renewals Management")
    assert not is_target_role(None)
