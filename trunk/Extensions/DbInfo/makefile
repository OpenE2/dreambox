dreamUpload=$(shell pwd)/../common/dreamUpload

run: DbUserConf.py
	python run.py

install: DbUserConf.py
	${dreamUpload} -c /usr/lib/enigma2/python/Plugins/Extensions/DbInfo DbInfo.py DbStation.py DbUserConf.py plugin.py __init__.py

DbUserConf.py:
	@test -e DbUserConf.py || ( echo "DbUserConf.py missing!\\nRun\\n> cp DbUserConf.py.example DbUserConf.py\\nand adapt DbUserConf.py to your needs."; exit 1 )
