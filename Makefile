.PHONY: clean format

format:
	yapf -i $(shell git ls-tree --full-tree -r --name-only HEAD | grep ".py")

clean:
	rm -rf *~ .*~ __pycache__
