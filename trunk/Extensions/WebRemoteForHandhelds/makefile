common=$(shell pwd)/../common

package:
	@${common}/package clean
	@${common}/package put simple_remote.html /usr/lib/enigma2/python/Plugins/Extensions/WebInterface/web-data
	@${common}/package build

install:
	${common}/dreamUpload -c /usr/lib/enigma2/python/Plugins/Extensions/WebInterface/web-data simple_remote.html

remote_release:
	ssh ahso bin/dreambox/create_WebRemoteForHandhelds_release

clean:
	rm -fR build 2>/dev/null || true
