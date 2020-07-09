VERSION?=latest
DOCBIN?=mkdocs
OWNER?=dodasts

PREFIX:= build/
IMAGES:= centos7_grid \
				cachingondemand/xrootd-escape-http \
				cachingondemand/xcache-escape-http \
				cachingondemand/xrootd-escape-xrd \
				cachingondemand/xcache-escape-xrd \
				htcondor/htcondor \
				htcondor/cms \
				htcondor/ams \
				htcondor/fermi \
				jupyter/pyspark-notebook \
				spark

.PHONY: init build push publish-doc

all: build-all 

help:
	@echo "Available commands:\n"
	@echo "- publish-doc			: "

publish-doc:
	cp README.md docs/README.md
	$(DOCBIN) gh-deploy

build/%: DARGS?=

build/%:
	./scripts/travis-build.sh $(OWNER)/$(notdir docker/$@):${VERSION} docker/$(strip $(subst $(PREFIX), ,$@))


build-all: $(foreach I,$(IMAGES),build/$(I) )

push/%: DARGS?=

push/%:
	./scripts/travis-publish.sh  $(OWNER)/$(notdir docker/$@) $(OWNER)/$(notdir docker/$@):$(VERSION) docker/$(strip $(subst $(PREFIX), ,$@))

push-all:  $(foreach I,$(IMAGES),push/$(I) )
