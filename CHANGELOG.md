# Changelog

Every noteable change is logged here.

## v0.6.0 (2022-10-06)

### Chore

* change nightly to all (a36f90913f23)
* add separate generate step (3f4e51b32e55)
* publish generated data if nightly fails (72817ed76d51)
* do not run in privileged mode (ffafd36e793e)
* run cleanup (c42009dd99cd)
* add headnote step (d187ebd2e5b7)
* add headnote extractor (7e0a55eebe92)
* upgrade requirements.txt (1079364e31dd)
* increase max worker count (b0e44350d875)
* adjust resource data generator (18fd2b04adcf)
* add Jenkinsfile (b252ce9856ac)
* upgrade requirements.txt (264f637af385)

## v0.5.0

### Feature

* add objectc as valid code input (54e80a28e3f2)
* split into separate step (ed6f29a62053)
* add separate horizontals step (c40bebcd2905)

## v0.4.2

## v0.4.1

### Feature

* extend JavaScript detector (6513ac1f8efb)

## v0.4.0

### Feature

* extend bash detector (5d35a8579102)
* run more code extractor to increase code detection (c104662ec326)
* add bash code detector (9c6cf611c8b8)

### Fix

* run final step if no invalid number ends (ffc93f959bf1)

### Documentation

* adjust module path (da324f653968)
* Happy New Year! (e02730a03f29)

## v0.3.2

## v0.3.1

### Fix

* remove magic parameter (6159a59afa34)

## v0.3.0

### Feature

* convert codero detection to non horizontal ptn indexes (01af6acfaae8)
* extend loc detector (2b762f1bb604)
* add loc line decider (8fea1c21981a)
* add code detector without caption to general strategy (445431ebbfe4)
* add code inside text extractor (b3465180d9c1)

### Fix

* adjust index and remove invalids (d0d8fa9591e4)
* adjust horizontal non horizontal line numbering (92a735e64719)
* distinguish code from list (86bb980c7542)

### Documentation

* add module documentation (830d110dec52)
* add module documentation (9b23306085f1)

## v0.2.2

### Fix

* skip code out of navigator range (f1f7ab5249f6)

## v0.2.1

### Fix

* skip false positive parsing (5b3a24a089ab)

## v0.2.0

### Feature

* insert code bounding to best result (4d101a0cb1e6)

## v0.1.1

### Feature

* add result step to select best code parsing (9e17b3593742)

## v0.1.0

### Feature

* add text step to cli (a609df5c5088)
* add text step (7e716cf146cf)
* add cli and feature package (ef1bb23c1de6)
* add specialized rcode parser (38b133d0b0c2)
* add decider to select best strategy (12060631c419)
* add text based code parser (ccf09da50b7c)
* add strategy to detect linting with caption below (b845e9edb596)
* add code detection validator (8ebe3cb62c74)
* add strategy to detect listing between lines (b8d59a76adf4)

### Fix

* skip very short codes without any caption (4b98f6bb2b5c)

## v0.0.0 Initial release
