.PHONY: build test-upload upload

build:
	@/bin/sh -c 'rm -rf dist/* >> /dev/null && python -m build; twine check dist/*'

test-upload:
	@/bin/sh -c 'twine upload -r testpypi dist/*'

upload:
	@/bin/sh -c 'twine upload dist/*'