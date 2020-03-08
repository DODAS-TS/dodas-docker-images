VERSION?=latest
DOCBIN?=mkdocs
OWNER?=dodasts

PREFIX:= build/
IMAGES:= centos7_grid \
				htcondor/htcondor

.PHONY: init build push publish-doc

all: env build

help:
	@echo "Available commands:\n"
	@echo "- publish-doc			: "

publish-doc:
	cp README.md docs/README.md
	$(DOCBIN) gh-deploy

build/%: DARGS?=

build/%:
	echo $(PREFIX)
	IMG=$(strip $(subst $(PREFIX), ,$@))
	echo "docker build $(DARGS) --rm --force-rm -t $(OWNER)/$(notdir docker/$@):${VERSION} ./docker/$(strip $(subst $(PREFIX), ,$@))"
	docker build $(DARGS) --rm --force-rm -t $(OWNER)/$(notdir docker/$@):${VERSION} ./docker/$(strip $(subst $(PREFIX), ,$@))

build-all:
	$(foreach I,$(IMAGES),make build/$(I) )

push/%: DARGS?=

push/%:
	docker push $(DARGS) $(OWNER)/$(notdir docker/$@):$(VERSION)

push-all:
	$(foreach I,$(IMAGES),make push/$(I) )