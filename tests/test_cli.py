from shiftguard import main


def test_main_prints_the_demo_conflicts(capsys) -> None:
    main()

    output = capsys.readouterr().out

    assert "ShiftGuard found 3 conflict(s):" in output
    assert "Harbour Foods shift - Friday conflicts with Team bus to Saint John" in output
    assert "Harbour Foods shift - Saturday conflicts with Fundy Invitational" in output
