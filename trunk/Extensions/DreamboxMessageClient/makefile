dreamUpload=$(shell pwd)/../common/dreamUpload

run:
	python run.py

install:
	${dreamUpload} -c /usr/lib/enigma2/python/Plugins/Extensions/DMC DMC.py DMCSetup.py __init__.py plugin.py
	cd Wrapper_; ${dreamUpload} -c /usr/lib/enigma2/python/Plugins/Extensions/DMC/Wrapper Config.py __init__.py Message.py; cd ..
