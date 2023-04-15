@echo off
FOR /f %%p in ('where python') do SET PYTHONPATH=%%p
python ".\run_attendance.py" "%~1"
pause